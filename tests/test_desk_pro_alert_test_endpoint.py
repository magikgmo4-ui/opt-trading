"""Tests for POST /desk/alert/test — smoke alert dispatch endpoint."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from modules.desk_pro.api.routes import desk_alert_test, _dispatch_alert


class TestDeskAlertTestEndpoint(unittest.TestCase):

    def test_returns_ok_true(self):
        result = desk_alert_test()
        self.assertTrue(result["ok"])

    def test_returns_alert_with_status_test(self):
        result = desk_alert_test()
        self.assertEqual(result["alert"]["status"], "test")

    def test_returns_alert_with_ts(self):
        result = desk_alert_test()
        self.assertIn("ts", result["alert"])
        self.assertTrue(result["alert"]["ts"].endswith("Z"))

    def test_dispatch_list_present(self):
        result = desk_alert_test()
        self.assertIsInstance(result["dispatch"], list)

    def test_dispatch_has_telegram_and_webhook(self):
        result = desk_alert_test()
        destinations = {d["destination"] for d in result["dispatch"]}
        self.assertIn("telegram", destinations)
        self.assertIn("webhook", destinations)

    def test_no_env_vars_all_skipped(self):
        with patch.dict("os.environ", {}, clear=True):
            result = desk_alert_test()
        for d in result["dispatch"]:
            self.assertEqual(d["status"], "skipped", f"{d['destination']} should be skipped without env vars")

    def test_dispatch_status_delivered_on_sent_true(self):
        sent_dispatch = [
            {"destination": "telegram", "sent": True, "reason": "telegram"},
            {"destination": "webhook", "sent": True, "reason": "webhook status=200"},
        ]
        with patch("modules.desk_pro.api.routes._dispatch_alert", return_value=sent_dispatch):
            result = desk_alert_test()
        for d in result["dispatch"]:
            self.assertEqual(d["status"], "delivered")

    def test_dispatch_status_failed_on_sent_false_with_reason(self):
        failed_dispatch = [
            {"destination": "telegram", "sent": False, "reason": "connection refused"},
            {"destination": "webhook", "sent": False, "reason": "timeout"},
        ]
        with patch("modules.desk_pro.api.routes._dispatch_alert", return_value=failed_dispatch):
            result = desk_alert_test()
        for d in result["dispatch"]:
            self.assertEqual(d["status"], "failed")

    def test_dispatch_status_skipped_on_not_configured(self):
        skipped_dispatch = [
            {"destination": "telegram", "sent": False, "reason": "not configured"},
            {"destination": "webhook", "sent": False, "reason": "not configured"},
        ]
        with patch("modules.desk_pro.api.routes._dispatch_alert", return_value=skipped_dispatch):
            result = desk_alert_test()
        for d in result["dispatch"]:
            self.assertEqual(d["status"], "skipped")

    def test_no_secret_in_alert_payload(self):
        result = desk_alert_test()
        alert_str = str(result["alert"])
        self.assertNotIn("token", alert_str.lower())
        self.assertNotIn("bot", alert_str.lower())


class TestDispatchAlertNoSideEffects(unittest.TestCase):

    def test_dispatch_without_env_returns_not_configured(self):
        with patch.dict("os.environ", {}, clear=True):
            results = _dispatch_alert({"status": "test"})
        self.assertEqual(len(results), 2)
        for r in results:
            self.assertFalse(r["sent"])
            self.assertEqual(r["reason"], "not configured")

    def test_dispatch_with_telegram_env_calls_send(self):
        fake_resp = MagicMock()
        fake_resp.read.return_value = b'{"ok": true}'
        fake_resp.__enter__ = lambda s: s
        fake_resp.__exit__ = MagicMock(return_value=False)
        env = {"TELEGRAM_BOT_TOKEN": "tok123", "TELEGRAM_CHAT_ID": "chat456"}
        with patch.dict("os.environ", env), \
             patch("urllib.request.urlopen", return_value=fake_resp):
            results = _dispatch_alert({"status": "test"})
        tg = next(r for r in results if r["destination"] == "telegram")
        self.assertTrue(tg["sent"])

    def test_dispatch_with_webhook_env_calls_send(self):
        fake_resp = MagicMock()
        fake_resp.status = 200
        fake_resp.__enter__ = lambda s: s
        fake_resp.__exit__ = MagicMock(return_value=False)
        env = {"ALERT_WEBHOOK_URL": "http://localhost:9999/hook"}
        with patch.dict("os.environ", env), \
             patch("urllib.request.urlopen", return_value=fake_resp):
            results = _dispatch_alert({"status": "test"})
        wh = next(r for r in results if r["destination"] == "webhook")
        self.assertTrue(wh["sent"])

    def test_dispatch_telegram_exception_returns_failed_not_raises(self):
        env = {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "chat"}
        with patch.dict("os.environ", env), \
             patch("urllib.request.urlopen", side_effect=OSError("connection refused")):
            results = _dispatch_alert({"status": "test"})
        tg = next(r for r in results if r["destination"] == "telegram")
        self.assertFalse(tg["sent"])
        self.assertIn("connection refused", tg["reason"])

    def test_dispatch_does_not_modify_alert_state(self):
        import modules.desk_pro.api.routes as r_mod
        before = dict(r_mod._alert_state)
        with patch.dict("os.environ", {}, clear=True):
            _dispatch_alert({"status": "test"})
        self.assertEqual(r_mod._alert_state, before)
