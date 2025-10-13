from fastapi import FastAPI, Request,  Depends, HTTPException
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from app.routes.appointments import router as appt_router
from app.routes import users, telegram, summarize
from app.routes.oauth import oauth, routes as oauthv2
from app.routes.auth import auth
from app.services.telegram_bot import process_updates
from pathlib import Path
from dotenv import load_dotenv
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response
from datetime import datetime, timezone
import time
import os


PROJECT_ROOT = Path(os.getcwd())
ENV_PATH = PROJECT_ROOT / "../.env"

""" if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found at {ENV_PATH}") """

# Load all env variables and override any existing ones
load_dotenv(dotenv_path=ENV_PATH, override=True)
API = os.environ.get('API_VERSION', 'api/v1')

# Basic Auth for docs
security = HTTPBasic()


def verify_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = os.environ.get("DOCS_USERNAME")
    correct_password = os.environ.get("DOCS_PASSWORD")
    if credentials.username != correct_username or credentials.password != correct_password:
        raise HTTPException(status_code=401, detail="Unauthorized")


app = FastAPI(title="Bürgeramt Slot Finder",
              redirect_slashes=False, docs_url=None, redoc_url=None)

##  monitoring metrics ##

REQUEST_COUNT = Counter("request_count", "Total number of requests")
REQUEST_LATENCY = Histogram(
    "request_latency_seconds", "Request latency in seconds")
ACTIVE_USERS = Gauge("active_users", "Number of active users")
ERROR_COUNT = Counter("error_count", "Total number of errors")

# Simulated active users (for demo purposes)
ACTIVE_USERS.set(5)


# Allow frontend origin
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",  # if you use CRA
    "https://fs-burgeramt-slot-finder.vercel.app",  # Vercel frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 👈 only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],         # 👈 allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],         # 👈 allow all headers (including x-api-key)
)


# Secure Swagger docs endpoint
@app.get("/docs", include_in_schema=False)
def custom_swagger_ui(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_swagger_ui_html(openapi_url=app.openapi_url, title="Secure Docs")


# Secure Swagger redoc endpoint
@app.get("/redoc", include_in_schema=False)
def custom_redoc_ui(credentials: HTTPBasicCredentials = Depends(verify_credentials)):
    return get_redoc_html(openapi_url=app.openapi_url, title="Secure Redoc")


# Rate limiter
limiter = Limiter(key_func=lambda request: request.client.host)
app.state.limiter = limiter


# Handle rate limit errors
@app.exception_handler(RateLimitExceeded)
async def rate_limit_handler(request: Request, exc: RateLimitExceeded):
    return JSONResponse(
        status_code=429,
        content={"error": "Too many requests, please try later."}
    )


# API routes


app.include_router(
    appt_router, prefix=f"/{API}")
app.include_router(
    users.router, prefix=f"/{API}")
app.include_router(
    auth.router,    prefix=f"/{API}")
app.include_router(
    oauth.router,  prefix=f"/{API}")
app.include_router(
    oauthv2.router, prefix=f"/{API}")
app.include_router(
    telegram.router, prefix=f"/{API}")
app.include_router(
    summarize.router, prefix=f"/{API}")

# Track metrics middleware


@app.middleware("http")
async def track_metrics(request: Request, call_next):
    REQUEST_COUNT.inc()
    start_time = time.time()
    try:
        response = await call_next(request)
    except Exception:
        ERROR_COUNT.inc()
        raise
    duration = time.time() - start_time
    REQUEST_LATENCY.observe(duration)
    return response

# Metrics Endpoint


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)


# API status
start_time = datetime.now(timezone.utc)


@app.get("/health", tags=["Health"])
def health_check():
    uptime = datetime.now(timezone.utc) - start_time
    return {
        "status": "online",
        "uptime": str(uptime).split('.')[0],  # Format as HH:MM:SS
        "version": "v1.0.0",
        "last_checked": datetime.now(timezone.utc).isoformat() + "Z"
    }


@app.get("/")
def homepage():
    return {
        "message": "Welcome to the FS Burgeramt Slot Finder API — your smart gateway to real-time appointment availability across Berlin's Bürgerämter. Secure, fast, and built for automation."
    }
