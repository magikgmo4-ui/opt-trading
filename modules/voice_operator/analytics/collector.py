"""
Voice Operator Analytics — Event Collector
GO_VOICE_OPERATOR_USAGE_ANALYTICS_01

Captures voice events to voice_events.jsonl.
Lightweight, append-only, local — no external telemetry.
"""
from __future__ import annotations
import json
from pathlib import Path
from datetime import datetime, timezone

REPO_ROOT = Path(__file__).resolve().parents[3]
EVENTS_PATH = REPO_ROOT / "data" / "logs" / "voice_events.jsonl"


def _ensure_dir():
    EVENTS_PATH.parent.mkdir(parents=True, exist_ok=True)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def log_command(command: str, intent: str, endpoint: str) -> None:
    """Log a voice command event."""
    _ensure_dir()
    event = {
        "ts": _now(),
        "event": "voice_command",
        "command": command,
        "intent": intent,
        "endpoint": endpoint,
    }
    _append(event)


def log_response(intent: str, latency_ms: int, ok: bool, source: str = "") -> None:
    """Log a voice response event."""
    _ensure_dir()
    event = {
        "ts": _now(),
        "event": "voice_response",
        "intent": intent,
        "latency_ms": latency_ms,
        "ok": ok,
        "source": source,
    }
    _append(event)


def log_error(intent: str, error: str) -> None:
    """Log a voice error event."""
    _ensure_dir()
    event = {
        "ts": _now(),
        "event": "voice_error",
        "intent": intent,
        "error": str(error)[:200],
    }
    _append(event)


def log_tts(intent: str) -> None:
    """Log a TTS playback event."""
    _ensure_dir()
    event = {
        "ts": _now(),
        "event": "tts_play",
        "intent": intent,
    }
    _append(event)


def log_profile(profile: str) -> None:
    """Log a profile switch event."""
    _ensure_dir()
    event = {
        "ts": _now(),
        "event": "profile_switch",
        "profile": profile,
    }
    _append(event)


def _append(event: dict) -> None:
    try:
        with open(EVENTS_PATH, "a", encoding="utf-8") as f:
            f.write(json.dumps(event, default=str, ensure_ascii=False) + "\n")
    except Exception:
        pass  # analytics failure must never break voice
