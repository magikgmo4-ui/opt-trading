"""Tests for telegram_command_center formatters."""
from modules.telegram_command_center.app.formatters import (
    alert, decision_required, info, snapshot, ops_result, error,
    routes_summary, help_text, route_test_result,
)


class TestAlert:
    def test_format(self):
        msg = alert("Test", "healthcheck", "FAIL", "service down", "run /health")
        assert "🔴" in msg
        assert "ALERT" in msg
        assert "healthcheck" in msg
        assert "FAIL" in msg
        assert "/health" in msg

    def test_plain_text(self):
        msg = alert("X", "source", "WARN", "impact", "action")
        assert "<b>" not in msg
        assert "<code>" not in msg


class TestDecisionRequired:
    def test_basic(self):
        msg = decision_required("BTCUSDT", "LONG", 66250, 65800, 67200)
        assert "DECISION REQUIRED" in msg
        assert "BTCUSDT" in msg
        assert "LONG" in msg
        assert "66250" in msg
        assert "APPROVE" in msg
        assert "REJECT" in msg

    def test_multi_tp(self):
        msg = decision_required("ETHUSDT", "SHORT", 3500, 3600, [3400, 3300])
        assert "3400" in msg
        assert "3300" in msg
        assert "/" in msg.split("TP:")[1]

    def test_with_confidence(self):
        msg = decision_required("SOLUSDT", "LONG", 140, 135, 150, confidence="HIGH")
        assert "HIGH" in msg

    def test_plain_text(self):
        msg = decision_required("X", "LONG", 1, 2, 3)
        assert "<b>" not in msg
        assert "<code>" not in msg


class TestNoRawHtml:
    def test_help_text_has_no_raw_html(self):
        msg = help_text([("/help", "show help")])
        assert "<" not in msg

    def test_route_test_has_no_raw_html(self):
        msg = route_test_result("ops", True, 10)
        assert "<" not in msg


class TestInfo:
    def test_basic(self):
        msg = info("STATUS", ["line1", "line2"], action="none")
        assert "STATUS" in msg
        assert "line1" in msg
        assert "line2" in msg
        assert "none" in msg

    def test_empty_details(self):
        msg = info("EMPTY", [])
        assert "EMPTY" in msg


class TestOpsResult:
    def test_ok(self):
        msg = ops_result("/health", "PASS", "all checks passed")
        assert "OPS RESULT" in msg
        assert "/health" in msg
        assert "PASS" in msg

    def test_error(self):
        msg = ops_result("/analyze", "ERROR", "timeout")
        assert "ERROR" in msg

    def test_minimal(self):
        msg = ops_result("/test", "OK")
        assert "OK" in msg


class TestError:
    def test_format(self):
        msg = error("/test", "something broke")
        assert "Command error" in msg
        assert "/test" in msg
        assert "something broke" in msg


class TestRoutesSummary:
    def test_format(self):
        channels = {"alerts": "critical", "pipeline": "trading"}
        msg = routes_summary(channels)
        assert "Telegram routes" in msg
        assert "alerts" in msg
        assert "pipeline" in msg


class TestHelpText:
    def test_format(self):
        cmds = [("/help", "show help"), ("/status", "system status")]
        msg = help_text(cmds)
        assert "Available commands" in msg
        assert "/help" in msg
        assert "/status" in msg


class TestRouteTestResult:
    def test_ok(self):
        msg = route_test_result("alerts", True, 123.4)
        assert "✅" in msg
        assert "OK" in msg
        assert "123" in msg

    def test_fail(self):
        msg = route_test_result("pipeline", False, 0)
        assert "❌" in msg
        assert "FAIL" in msg
