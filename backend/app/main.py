from fastapi import FastAPI, Request
from starlette.responses import JSONResponse
from slowapi.errors import RateLimitExceeded
from slowapi import Limiter
from fastapi.middleware.cors import CORSMiddleware
from app.routes.appointments import router as appt_router
from app.routes import users, telegram
from app.routes.oauth import oauth, routes as oauthv2
from app.routes.auth import auth
from app.services.telegram_bot import process_updates
from pathlib import Path
from dotenv import load_dotenv
import os


PROJECT_ROOT = Path(os.getcwd())
ENV_PATH = PROJECT_ROOT / "../.env"

""" if not ENV_PATH.exists():
    raise FileNotFoundError(f".env file not found at {ENV_PATH}") """

# Load all env variables and override any existing ones
load_dotenv(dotenv_path=ENV_PATH, override=True)
API = os.environ.get('API_VERSION', 'api/v1')


app = FastAPI(title="Bürgeramt Slot Finder", redirect_slashes=False)


# Allow frontend origin
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
    "http://localhost:3000",  # if you use CRA
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # 👈 only allow your frontend
    allow_credentials=True,
    allow_methods=["*"],         # 👈 allow GET, POST, OPTIONS, etc.
    allow_headers=["*"],         # 👈 allow all headers (including x-api-key)
)

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


@app.get("/")
def health_check():
    return {"status": "ok"}
