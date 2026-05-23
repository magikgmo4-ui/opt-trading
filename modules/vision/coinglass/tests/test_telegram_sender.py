import json
import unittest
from pathlib import Path

from modules.vision.coinglass.telegram_sender import send_vision_summary

FIXTURE_VALID = Path("tests/fixtures/vision/coinglass/vision_coinglass_v1_valid.json")
FIXTURE_LOW = Path("tests/fixtures/vision/coinglass/vision_coinglass_v1_low_conf.json")


def _write_tmp(tmp_path: Path, payload: dict) -> Path:
    p = tmp_path / "latest.json"
    p.write_text(json.dumps(payload), encoding="utf-8")
    return p


def _valid_payload() -> dict:
    return {
        "contract_version": "v1",
        "input_class": "vision_context.coinglass.v1",
        "source_id": "coinglass_headless_bot",
        "screenshot_ts": "2026-05-23T06:00:00Z",
        "symbol": "BTCUSDT",
        "timeframe": "1H",
        "board": "liquidations",
        "page": "liquidation_heatmap",
        "freshness_state": "fresh",
        "detections": [
            {"detected_metric_type": "liquidations_long", "extracted_value": 48_500_000.0,
             "unit": "USD", "confidence": 0.82, "evidence_ref": "ref.png", "notes": ""},
        ],
        "warnings": [],
        "refs": {"raw_screenshot": "r.png", "normalized": "n.json",
                 "latest": "latest.json", "events": "events.jsonl"},
    }


class TestSendVisionSummary(unittest.TestCase):

    # TC-SEND-01: données valides → send_fn appelé avec message non vide
    def test_valid_data_calls_send_fn(self):
        import tempfile
        received = []

        def _mock_send(msg: str) -> None:
            received.append(msg)

        with tempfile.TemporaryDirectory() as td:
            p = _write_tmp(Path(td), _valid_payload())
            result = send_vision_summary(path=p, send_fn=_mock_send)

        self.assertTrue(result)
        self.assertEqual(len(received), 1)
        self.assertGreater(len(received[0]), 10)

    # TC-SEND-02: message contient les valeurs extraites
    def test_message_contains_extracted_values(self):
        import tempfile
        received = []

        def _mock_send(msg: str) -> None:
            received.append(msg)

        with tempfile.TemporaryDirectory() as td:
            p = _write_tmp(Path(td), _valid_payload())
            send_vision_summary(path=p, send_fn=_mock_send)

        msg = received[0]
        self.assertIn("BTCUSDT", msg)
        self.assertIn("$48.50M", msg)

    # TC-SEND-03: fichier absent → retourne False, send_fn jamais appelé
    def test_absent_file_returns_false_no_send(self):
        import tempfile
        calls = []

        def _mock_send(msg: str) -> None:
            calls.append(msg)

        with tempfile.TemporaryDirectory() as td:
            result = send_vision_summary(path=Path(td) / "missing.json", send_fn=_mock_send)

        self.assertFalse(result)
        self.assertEqual(calls, [])

    # TC-SEND-04: input_class incorrect → retourne False, pas d'envoi
    def test_wrong_input_class_returns_false(self):
        import tempfile
        calls = []

        def _mock_send(msg: str) -> None:
            calls.append(msg)

        payload = _valid_payload()
        payload["input_class"] = "market_metrics.v1"
        with tempfile.TemporaryDirectory() as td:
            p = _write_tmp(Path(td), payload)
            result = send_vision_summary(path=p, send_fn=_mock_send)

        self.assertFalse(result)
        self.assertEqual(calls, [])

    # TC-SEND-05: send_fn lève exception → retourne False, pas de propagation
    def test_send_fn_exception_returns_false(self):
        import tempfile

        def _boom(msg: str) -> None:
            raise ConnectionError("network down")

        with tempfile.TemporaryDirectory() as td:
            p = _write_tmp(Path(td), _valid_payload())
            result = send_vision_summary(path=p, send_fn=_boom)

        self.assertFalse(result)

    # TC-SEND-06: fixture valide → send_fn appelé
    def test_valid_fixture_sends(self):
        if not FIXTURE_VALID.exists():
            self.skipTest("fixture not present")
        received = []
        result = send_vision_summary(path=FIXTURE_VALID, send_fn=received.append)
        self.assertTrue(result)
        self.assertEqual(len(received), 1)

    # TC-SEND-07: fixture low_conf (null values) → pas de valeur inventée
    def test_low_conf_fixture_no_invented_values(self):
        if not FIXTURE_LOW.exists():
            self.skipTest("fixture not present")
        received = []
        send_vision_summary(path=FIXTURE_LOW, send_fn=received.append)
        if received:
            msg = received[0]
            # null values → N/A, no dollar amounts fabricated
            self.assertNotIn("$48", msg)
            self.assertNotIn("$21", msg)

    # TC-SEND-08: send_fn reçoit exactement 1 appel (pas de double envoi)
    def test_exactly_one_send_call(self):
        import tempfile
        calls = []

        with tempfile.TemporaryDirectory() as td:
            p = _write_tmp(Path(td), _valid_payload())
            send_vision_summary(path=p, send_fn=calls.append)

        self.assertEqual(len(calls), 1)


if __name__ == "__main__":
    unittest.main()
