from __future__ import annotations

import json
import sys
from pathlib import Path

from modules.telegram_ingestion.parser.message_schema import RawMessage


MODULE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = MODULE_DIR / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from collector_telegram.normalize import parse_message  # noqa: E402


def test_real_collector_message_samples_parse_as_expected():
    fixture_path = MODULE_DIR / "tests" / "fixtures" / "collector_message_samples.json"
    samples = json.loads(fixture_path.read_text(encoding="utf-8"))

    for sample in samples:
        parsed = parse_message(
            RawMessage(
                message_id=sample["message_id"],
                channel=sample["channel"],
                raw_text=sample["raw_text"],
            )
        )
        assert parsed["message_type"] == sample["message_type"], sample["channel"]
        assert parsed["parser_status"] == sample["parser_status"], sample["channel"]
        assert parsed["parsed"] == sample["parsed"], sample["channel"]
