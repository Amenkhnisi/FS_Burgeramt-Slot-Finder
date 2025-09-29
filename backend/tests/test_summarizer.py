import pytest
import asyncio
from unittest.mock import AsyncMock
from app.services.summarizer import (
    _chunk_text, _hash_input, summarize_text, SYSTEM_PROMPT, cache
)


long_text = "longpara" * 50
expected = [long_text[i:i+100] for i in range(0, len(long_text), 100)]


@pytest.mark.parametrize("text,max_chars,expected_chunks", [
    ("short text", 100, ["short text"]),
    ("para1\n\npara2", 10, ["para1", "para2"]),
    (long_text, 100, expected)
])
def test_chunk_text(text, max_chars, expected_chunks):
    chunks = _chunk_text(text, max_chars)
    assert isinstance(chunks, list)
    assert chunks == expected_chunks


def test_hash_input_consistency():
    text = "Einbürgerung Antrag"
    h1 = _hash_input(text, True, "A2")
    h2 = _hash_input(text, True, "A2")
    assert h1 == h2
    assert isinstance(h1, str)
    assert len(h1) == 64  # SHA-256 hex length


@pytest.mark.asyncio
async def test_summarize_text_basic(monkeypatch):
    dummy_response = '{"simplified_de": "Vereinfachter Text", "actions": ["Formular ausfüllen"], "translate_en": "Simplified text"}'

    async_mock = AsyncMock(return_value=dummy_response)

    monkeypatch.setattr(
        "app.services.summarizer._call_openai_chat", async_mock)

    result = await summarize_text("Dies ist ein Testtext.", translate_to_en=True, level="A2")
    assert "simplified_de" in result
    assert "simplified_en" in result
    assert isinstance(result["simplified_de"], str)
    assert isinstance(result["simplified_en"], str)


@pytest.mark.asyncio
async def test_summarize_text_cache(monkeypatch):
    cache.clear()  # Ensure clean state

    dummy_response = '{"simplified_de": "Cached Text", "actions": ["Do something"], "translate_en": "Cached translation"}'
    async_mock = AsyncMock(return_value=dummy_response)

    monkeypatch.setattr(
        "app.services.summarizer._call_openai_chat", async_mock)

    result1 = await summarize_text("Testtext", translate_to_en=True, level="A2")
    result2 = await summarize_text("Testtext", translate_to_en=True, level="A2")
    assert async_mock.call_count == 2

    assert result1 == result2
    assert len(cache) == 1  # Ensure caching occurred
