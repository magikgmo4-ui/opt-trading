"""Mock tests — no live gateway required."""
import json
import sys
import types
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent.parent))

from app.schema import BridgeRequest, ALLOWED_ACTIONS, ActionNotAllowed
from app.bridge import OperatorBridge


MOCK_OK_RESPONSE = {
    "runId": "test-run-id",
    "status": "ok",
    "summary": "completed",
    "result": {
        "payloads": [{"text": "mock response content", "mediaUrl": None}],
        "meta": {"durationMs": 123},
    },
}


def _make_proc(stdout: str, returncode: int = 0) -> MagicMock:
    proc = MagicMock()
    proc.stdout = stdout
    proc.returncode = returncode
    return proc


class TestBridgeRequest(unittest.TestCase):
    def test_allowed_actions_accepted(self):
        for action in ALLOWED_ACTIONS:
            req = BridgeRequest(action=action, instruction="test")
            req.validate()  # must not raise

    def test_forbidden_action_raises(self):
        req = BridgeRequest(action="execute", instruction="trade now")
        with self.assertRaises(ActionNotAllowed):
            req.validate()

    def test_empty_instruction_raises(self):
        req = BridgeRequest(action="ask", instruction="   ")
        with self.assertRaises(ValueError):
            req.validate()

    def test_request_id_auto_generated(self):
        bridge = OperatorBridge()
        req = BridgeRequest(action="ask", instruction="hello")
        with patch("app.client.subprocess.run") as mock_run:
            mock_run.return_value = _make_proc(json.dumps(MOCK_OK_RESPONSE))
            resp = bridge.send(req)
        self.assertTrue(len(resp.request_id) > 0)


class TestBridgeMock(unittest.TestCase):
    def _send(self, action: str, instruction: str, stdout: str) -> object:
        bridge = OperatorBridge()
        req = BridgeRequest(action=action, instruction=instruction)
        with patch("app.client.subprocess.run") as mock_run:
            with patch("app.client.shutil.which", return_value="/usr/bin/openclaw"):
                mock_run.return_value = _make_proc(stdout)
                return bridge.send(req)

    def test_ok_response_parsed(self):
        resp = self._send("ask", "what is 2+2", json.dumps(MOCK_OK_RESPONSE))
        self.assertEqual(resp.status, "ok")
        self.assertEqual(resp.content, "mock response content")
        self.assertEqual(resp.duration_ms, 123)

    def test_blocked_action_returns_error(self):
        bridge = OperatorBridge()
        req = BridgeRequest(action="execute", instruction="buy BTC")
        resp = bridge.send(req)
        self.assertEqual(resp.status, "error")
        self.assertIn("whitelist", resp.error)

    def test_builder_error_status(self):
        error_payload = {"status": "error", "summary": "failed", "result": {"payloads": [], "meta": {"durationMs": 0}}}
        resp = self._send("evaluate", "check signal", json.dumps(error_payload))
        self.assertEqual(resp.status, "error")

    def test_empty_stdout_returns_error(self):
        resp = self._send("ask", "hello", "")
        self.assertEqual(resp.status, "error")

    def test_non_json_stdout_returns_error(self):
        resp = self._send("review", "check trade", "not json at all")
        self.assertEqual(resp.status, "error")

    def test_response_to_dict(self):
        resp = self._send("build", "propose trade", json.dumps(MOCK_OK_RESPONSE))
        d = resp.to_dict()
        self.assertIn("request_id", d)
        self.assertIn("status", d)
        self.assertIn("result", d)
        self.assertEqual(d["result"]["content"], "mock response content")


if __name__ == "__main__":
    unittest.main()
