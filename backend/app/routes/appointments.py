from fastapi import APIRouter, Header, HTTPException, Request
from app.services.scraper import scrape_appointments_playwright_sync
from slowapi import Limiter
from slowapi.util import get_remote_address
from datetime import datetime, timedelta

import os


router = APIRouter(prefix="/appointments", tags=["Appointments"])


# --- API Security ---
# Replace with env variable for production
limiter = Limiter(key_func=get_remote_address)

# --- Cache ---
CACHE = {"slots": [], "updated": datetime.min}
CACHE_TTL = timedelta(minutes=10)  # Cache duration

# --- Helper Functions ---
API_KEY = os.environ.get("API_KEY")


def get_cached_slots():
    now = datetime.now()
    if now - CACHE["updated"] > CACHE_TTL:
        CACHE["slots"] = scrape_appointments_playwright_sync()
        CACHE["updated"] = now
    return CACHE["slots"]


@router.get("")
@limiter.limit("5/minute")  # Rate limiting: 5 requests per minute per IP
def fetch_appointments(request: Request, city: str = "Berlin", service: str = "Anmeldung", x_api_key: str = Header(...)):

    # API Key validation
    if x_api_key != API_KEY:
        raise HTTPException(status_code=403, detail="Forbidden")

        # Only Berlin + Anmeldung supported currently
    if city.lower() != "berlin" or service.lower() != "anmeldung":
        return {"error": "Only Berlin + Anmeldung supported currently."}

    slots = get_cached_slots()
    return {"city": city, "service": service, "slots": slots}
