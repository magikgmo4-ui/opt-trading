import os
import requests
import html
import json
from datetime import datetime, timezone
from pathlib import Path
from time import perf_counter
from typing import Any


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _default_log_path() -> Path:
    project_root = Path(__file__).resolve().parents[1]
    return project_root / "data" / "telemetry" / "telegram_send.jsonl"


def _append_jsonl(path: Path, record: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, default=str) + "\n")


def _extract_telegram_refs(response: requests.Response) -> tuple[str | None, str | None]:
    try:
        payload = response.json()
    except ValueError:
        return None, None

    result = payload.get("result") if isinstance(payload, dict) else None
    if not isinstance(result, dict):
        return None, None

    message_id = result.get("message_id")
    chat = result.get("chat")
    chat_id = chat.get("id") if isinstance(chat, dict) else None
    return (
        str(chat_id) if chat_id not in (None, "") else None,
        str(message_id) if message_id not in (None, "") else None,
    )


def send_telegram_with_metrics(
    message: str,
    *,
    source: str | None = None,
    tags: dict[str, Any] | None = None,
    escape: bool = True,
    parse_mode: str | None = "HTML",
    disable_web_page_preview: bool = True,
    timeout_s: float = 10.0,
) -> dict[str, Any]:
    token = os.getenv("TELEGRAM_BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not token or not chat_id:
        return {
            "ok": False,
            "error": "Telegram env vars not set",
            "timestamp": _utc_now_iso(),
            "source": source or "",
            "tags": tags or {},
        }

    text = html.escape(message) if escape else message
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "disable_web_page_preview": disable_web_page_preview,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode

    start = perf_counter()
    status_code = None
    err = None
    telegram_chat_id = None
    telegram_message_id = None
    try:
        r = requests.post(url, json=payload, timeout=timeout_s)
        status_code = r.status_code
        r.raise_for_status()
        telegram_chat_id, telegram_message_id = _extract_telegram_refs(r)
        ok = True
    except requests.RequestException as exc:
        ok = False
        err = str(exc)

    duration_ms = int((perf_counter() - start) * 1000)
    record = {
        "timestamp": _utc_now_iso(),
        "source": source or "",
        "tags": tags or {},
        "ok": ok,
        "duration_ms": duration_ms,
        "status_code": status_code,
        "timeout_s": timeout_s,
        "message_len": len(text),
        "error": err,
        "telegram_chat_id": telegram_chat_id,
        "telegram_message_id": telegram_message_id,
    }

    log_path = os.getenv("TELEGRAM_LATENCY_LOG_PATH")
    if log_path:
        _append_jsonl(Path(log_path), record)
    else:
        _append_jsonl(_default_log_path(), record)

    return record


def send_telegram(message: str, *, source: str | None = None, tags: dict[str, Any] | None = None):
    r = send_telegram_with_metrics(message, source=source, tags=tags, escape=True, parse_mode="HTML")
    if not r.get("ok"):
        raise RuntimeError(r.get("error") or "Telegram send failed")


def send_telegram_html(message: str, *, source: str | None = None, tags: dict[str, Any] | None = None):
    r = send_telegram_with_metrics(message, source=source, tags=tags, escape=False, parse_mode="HTML")
    if not r.get("ok"):
        raise RuntimeError(r.get("error") or "Telegram send failed")
