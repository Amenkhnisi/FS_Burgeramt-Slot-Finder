from typing import List, Dict
import os
import hashlib
from typing import Dict, List
import httpx
from cachetools import TTLCache

OPENAI_API_KEY = os.environ.get(
    "OPENAI_API_KEY")
OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
MAX_CHARS = int(os.environ.get("SUMMARIZER_MAX_CHARS", "6000"))
CACHE_TTL = int(os.environ.get("SUMMARIZER_CACHE_TTL_SECONDS", "3600"))


# In-memory TTL cache: key -> result
cache = TTLCache(maxsize=1024, ttl=CACHE_TTL)

SYSTEM_PROMPT = (
    "You are a helpful assistant specialized in simplifying German bureaucratic text "
    "for non-native speakers. Output a short simplified German version (clear, plain language), "
    "a short bullet list of actions the user must take, and an optional short English translation if requested. "
    "Keep it concise and actionable; aim for CEFR level A2-B1 unless another level is requested."
)


async def _call_openai_chat(messages: List[Dict], model: str = OPENAI_MODEL, timeout: int = 30) -> str:
    """
    Call OpenAI Chat Completions using httpx async client.
    Returns assistant text or raises detailed error.
    """
    if not OPENAI_API_KEY or not OPENAI_API_KEY.startswith("sk-"):
        raise RuntimeError("OPENAI_API_KEY is missing or invalid.")

    url = "https://api.openai.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 800,
    }

    async with httpx.AsyncClient(timeout=timeout) as client:
        try:
            response = await client.post(url, json=payload, headers=headers)
            print(f"OpenAI response status: {response.status_code}")
            print(f"OpenAI response body: {response.text}")
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except httpx.HTTPStatusError as e:
            raise RuntimeError(
                f"OpenAI API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise RuntimeError(f"Unexpected error calling OpenAI: {str(e)}")


def _hash_input(text: str, translate: bool, level: str) -> str:
    key = f"{level}|{translate}|{text}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()


def _chunk_text(text: str, max_chars: int = MAX_CHARS) -> List[str]:
    """Naive chunker on paragraphs ~ keep chunks under max_chars."""
    if len(text) <= max_chars:
        return [text]
    # split by paragraphs
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks = []
    current = ""
    for p in paras:
        if len(current) + len(p) + 2 <= max_chars:
            current = (current + "\n\n" + p).strip() if current else p
        else:
            if current:
                chunks.append(current)
            # if single paragraph too long, slice it
            if len(p) > max_chars:
                for i in range(0, len(p), max_chars):
                    chunks.append(p[i:i+max_chars])
                current = ""
            else:
                current = p
    if current:
        chunks.append(current)
    return chunks


async def summarize_text(text: str, translate_to_en: bool = False, level: str = "A2") -> Dict:
    """
    Summarize/simplify given German bureaucratic text:
      - returns simplified German,
      - bullet points of actions,
      - optional English translation.
    Caching applied by hashed input.
    """
    key = _hash_input(text, translate_to_en, level)
    if key in cache:
        return cache[key]

    # chunk text and summarize each chunk
    chunks = _chunk_text(text)
    summaries = []
    for chunk in chunks:
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": (
                 f"Please simplify the following German bureaucratic text to CEFR level {level}. "
                 f"Return JSON with fields: simplified_de (short paragraph), actions (bullet list), "
                 f"translate_en (optional short translation) if requested.\n\nText:\n{chunk}"
             )}
        ]
        if translate_to_en:
            messages[1]["content"] += "\n\nAlso provide an English translation in translate_en."
        assistant_text = await _call_openai_chat(messages)
        summaries.append(assistant_text)

    # Merge summaries (we assume assistant provided simplified text and action bullets)
    merged = "\n\n".join(summaries)
    # Basic postprocessing: try to parse assistant output or return raw.
    result = {"simplified_de": merged}
    if translate_to_en:
        # try to ask a short follow-up translation consolidation if needed
        # For simplicity we ask model to combine translations if multiple chunks
        messages = [
            {"role": "system", "content": "You are an assistant that combines short English translations into a single compact paragraph."},
            {"role": "user", "content": "Combine the following translations into a single concise English translation:\n\n" +
                "\n\n".join(summaries)}
        ]
        try:
            combined_en = await _call_openai_chat(messages)
            result["simplified_en"] = combined_en
        except Exception:
            # fallback: no translation combined
            result["simplified_en"] = None
    # cache result
    cache[key] = result
    return result
