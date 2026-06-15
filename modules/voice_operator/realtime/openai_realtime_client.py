"""
OpenAI Realtime Client — STT + TTS wrapper
GO_DESKPRO_VOICE_OPERATOR_01 — Lot D

Handles:
  - Speech-to-Text (Whisper API)
  - Text-to-Speech (OpenAI TTS API)
  - Model selection, cost tracking

Dependencies: requests (stdlib fallback: urllib)
API key: OPENAI_API_KEY env var
"""
from __future__ import annotations
import json
import os
import io
import urllib.request
from typing import Optional

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE = "https://api.openai.com/v1"

# Cost tracking (per 1M tokens / per 1M chars for TTS)
COST_TRACKER: dict[str, float] = {"stt_calls": 0, "tts_calls": 0, "estimated_cost_usd": 0.0}


def _api_headers() -> dict:
    return {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": "application/json",
    }


def _post(path: str, payload: dict, timeout: int = 30) -> dict:
    """POST to OpenAI API with error handling."""
    url = f"{OPENAI_BASE}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_api_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        body = e.read().decode() if e.fp else ""
        return {"ok": False, "error": f"HTTP {e.code}: {body[:200]}"}
    except Exception as e:
        return {"ok": False, "error": str(e)}


def _post_bytes(path: str, payload: dict, timeout: int = 30) -> bytes | None:
    """POST and return raw bytes (for TTS)."""
    url = f"{OPENAI_BASE}{path}"
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=_api_headers(), method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.read()
    except Exception:
        return None


def speech_to_text(audio_bytes: bytes, language: str = "fr") -> Optional[str]:
    """Transcribe audio to text using OpenAI Whisper API.

    Args:
        audio_bytes: Raw audio data (WAV, MP3, etc.)
        language: ISO language code (fr, en)

    Returns:
        Transcribed text or None on failure.
    """
    if not OPENAI_API_KEY:
        return None

    # Whisper expects multipart form data, not JSON
    # Use a simple approach: write temp file and use urllib with multipart
    import tempfile
    import uuid

    boundary = f"----WhisperBoundary{uuid.uuid4().hex[:8]}"

    # Build multipart body manually
    body_parts = []
    body_parts.append(f'--{boundary}'.encode())
    body_parts.append(b'Content-Disposition: form-data; name="model"')
    body_parts.append(b"")
    body_parts.append(b"whisper-1")
    body_parts.append(f'--{boundary}'.encode())
    if language:
        body_parts.append(b'Content-Disposition: form-data; name="language"')
        body_parts.append(b"")
        body_parts.append(language.encode())
        body_parts.append(f'--{boundary}'.encode())
    body_parts.append(b'Content-Disposition: form-data; name="file"; filename="audio.wav"')
    body_parts.append(b"Content-Type: audio/wav")
    body_parts.append(b"")
    body_parts.append(audio_bytes)
    body_parts.append(f'--{boundary}--'.encode())

    body = b"\r\n".join(body_parts)

    url = f"{OPENAI_BASE}/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {OPENAI_API_KEY}",
        "Content-Type": f"multipart/form-data; boundary={boundary}",
    }
    req = urllib.request.Request(url, data=body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
            COST_TRACKER["stt_calls"] += 1
            COST_TRACKER["estimated_cost_usd"] += 0.006 / 60  # ~$0.006/min Whisper
            return result.get("text", "").strip()
    except Exception:
        return None


def text_to_speech(text: str, voice: str = "alloy", speed: float = 1.0) -> bytes | None:
    """Convert text to speech using OpenAI TTS API.

    Args:
        text: Text to speak (max 4096 chars)
        voice: alloy, echo, fable, nova, onyx, shimmer
        speed: 0.25 to 4.0

    Returns:
        MP3 audio bytes or None on failure.
    """
    if not OPENAI_API_KEY or not text:
        return None

    payload = {
        "model": "tts-1",
        "voice": voice,
        "input": text[:4096],
        "speed": max(0.25, min(4.0, speed)),
        "response_format": "mp3",
    }
    result = _post_bytes("/audio/speech", payload, timeout=30)
    if result:
        COST_TRACKER["tts_calls"] += 1
        COST_TRACKER["estimated_cost_usd"] += len(text) * 0.015 / 1000  # $15/1M chars
    return result


def is_available() -> bool:
    """Check if OpenAI API key is configured."""
    return bool(OPENAI_API_KEY)


def get_cost_summary() -> dict:
    """Return cost tracking summary."""
    return dict(COST_TRACKER)
