from __future__ import annotations

from pathlib import Path

from modules.telegram_ingestion.parser.message_schema import RawMessage
from modules.telegram_ingestion.parser.telethon_client import TelethonInboundClient


class CollectorTelegramClient:
    def __init__(self, session_path: Path, api_id: int, api_hash: str):
        self._client = TelethonInboundClient(str(session_path), api_id, api_hash)

    def start(self) -> None:
        self._client.start()

    def fetch_messages(self, source_ref: str, limit: int) -> list[RawMessage]:
        return self._client.get_messages(source_ref, limit=limit)
