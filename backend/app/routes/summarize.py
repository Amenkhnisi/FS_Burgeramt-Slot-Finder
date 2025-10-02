from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.utils.auth_utils import get_current_user
from app.services.summarizer import summarize_text
from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.responses import JSONResponse


security = HTTPBearer()

router = APIRouter(tags=["Summarizer"])
limiter = Limiter(key_func=get_remote_address)


class SummarizeRequest(BaseModel):
    text: str
    translate_to_en: bool = False
    level: str = "A2"


class SummarizeResponse(BaseModel):
    simplified_de: str
    simplified_en: str | None = None


@router.post("/summarize", response_model=SummarizeResponse)
@limiter.limit("10/minute")  # adjust for your needs
async def summarize_endpoint(req: SummarizeRequest, request: Request, user=Depends(get_current_user)):
    """
    Simplify German bureaucratic text for authenticated users.
    Rate-limited to avoid runaway cost.
    """
    if not req.text or len(req.text.strip()) == 0:
        raise HTTPException(status_code=400, detail="Text is required")

    # Validate length
    if len(req.text) > 1000:
        return JSONResponse(
            status_code=422,
            content={"error": "Text too long. Maximum 1000 characters",
                     "code": "TEXT_TOO_LONG"}
        )

    if len(req.text) < 400:
        return JSONResponse(
            status_code=422,
            content={"error": "Text too short. Minimum 400 characters.",
                     "code": "TEXT_TOO_SHORT"}
        )

    try:
        result = await summarize_text(req.text, translate_to_en=req.translate_to_en, level=req.level)
        return {
            "simplified_de": result.get("simplified_de"),
            "simplified_en": result.get("simplified_en")
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e), "code": "INTERNAL_ERROR"}
        )
