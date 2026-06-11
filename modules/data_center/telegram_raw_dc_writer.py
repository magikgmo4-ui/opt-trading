"""
telegram_raw_dc_writer.py — route collector raw messages to data_center.

Produces:
    telegram_raw.v1 — per-channel raw message views
    Writes to: data/data_center/views/telegram_raw/by_channel/{CHANNEL}/latest.json
               data/data_center/views/telegram_raw/latest.json

Usage:
    python -m modules.data_center.telegram_raw_dc_writer
"""

from __future__ import annotations

import json
import tempfile
from datetime import datetime, timezone
from pathlib import Path

_PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
_VIEWS_DIR = _PROJECT_ROOT / "data" / "data_center" / "views"
_RAW_DIR = _PROJECT_ROOT / "modules" / "collector_telegram" / "outputs" / "raw"


def _atomic_write(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", dir=path.parent, delete=False, encoding="utf-8", suffix=".tmp") as fh:
        json.dump(payload, fh, indent=2, default=str)
        fh.write("\n")
        tmp = Path(fh.name)
    tmp.replace(path)


def produce_telegram_raw_views() -> dict:
    """Route collector raw messages to data_center views."""
    if not _RAW_DIR.exists():
        return {"error": "collector raw dir not found"}

    now = datetime.now(timezone.utc).isoformat()
    total_msgs = 0
    channels = []

    for jsonl_file in sorted(_RAW_DIR.glob("*.jsonl")):
        channel = jsonl_file.stem
        messages = []
        for line in jsonl_file.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
                messages.append({
                    "message_id": msg.get("message_id", ""),
                    "raw_text": (msg.get("raw_text", "") or "")[:200],
                    "timestamp": msg.get("timestamp_utc", ""),
                })
            except json.JSONDecodeError:
                continue

        if not messages:
            continue

        ch_dir = _VIEWS_DIR / "telegram_raw" / "by_channel" / channel
        ch_dir.mkdir(parents=True, exist_ok=True)
        payload = {
            "input_class": "telegram_raw.v1",
            "provider_id": "collector_telegram",
            "channel": channel,
            "produced_at": now,
            "total_messages": len(messages),
            "messages": messages[-20:],  # Last 20
        }
        _atomic_write(ch_dir / "latest.json", payload)
        total_msgs += len(messages)
        channels.append(channel)

    # Global latest
    global_payload = {
        "input_class": "telegram_raw.v1",
        "provider_id": "collector_telegram",
        "produced_at": now,
        "total_channels": len(channels),
        "total_messages": total_msgs,
        "channels": channels,
    }
    _atomic_write(_VIEWS_DIR / "telegram_raw" / "latest.json", global_payload)

    from modules.data_center.runtime_registry import update_producer_last_write
    update_producer_last_write(
        producer_id="collector_telegram",
        contract_class="telegram_raw.v1",
        output_path=str(_VIEWS_DIR / "telegram_raw" / "latest.json"),
        status="ok",
        evidence={"channels": len(channels), "messages": total_msgs},
    )

    return global_payload


if __name__ == "__main__":
    result = produce_telegram_raw_views()
    if "error" in result:
        print("ERROR:", result["error"])
    else:
        print(f"telegram_raw.v1: {result['total_channels']} channels, {result['total_messages']} messages")
