"""Tests for telegram_command_center command dispatch."""
import json
from pathlib import Path

from modules.telegram_command_center.app.commands import (
    dispatch, COMMANDS, register, cmd_help, cmd_routes, cmd_test_routes,
)


class TestDispatch:
    def test_unknown_command(self):
        resp, ch, action = dispatch("/nonexistent")
        assert "Unknown command" in resp
        assert ch is None
        assert action is None

    def test_empty_text(self):
        resp, ch, action = dispatch("")
        assert resp == ""
        assert ch is None
        assert action is None

    def test_non_command(self):
        resp, ch, action = dispatch("hello world")
        assert resp == ""
        assert ch is None
        assert action is None

    def test_help(self):
        resp, ch, action = dispatch("/help")
        assert "Command Center" in resp
        assert ch is None
        assert action is None

    def test_help_with_arg(self):
        resp, ch, _ = dispatch("/help status")
        assert "/status" in resp

    def test_help_unknown_arg(self):
        resp, ch, _ = dispatch("/help unknowncmd")
        assert "Unknown command" in resp

    def test_routes(self):
        resp, ch, _ = dispatch("/routes")
        assert "Telegram routes" in resp
        assert ch == "ops"

    def test_status(self):
        resp, ch, _ = dispatch("/status")
        assert ch == "pipeline"

    def test_health(self):
        resp, ch, _ = dispatch("/health")
        assert ch == "ops"

    def test_approvals(self):
        resp, ch, _ = dispatch("/approvals")
        assert ch == "pipeline"
        # Should handle missing queue file gracefully
        assert resp

    def test_perf(self):
        resp, ch, _ = dispatch("/perf")
        assert ch == "pipeline"

    def test_signals(self):
        resp, ch, _ = dispatch("/signals")
        assert ch == "pipeline"

    def test_analyze(self):
        resp, ch, _ = dispatch("/analyze")
        assert ch == "ops"

    def test_analyze_uses_latest_headless_context(self, monkeypatch, tmp_path):
        latest_dir = tmp_path / "data" / "deskpro" / "vision" / "latest"
        latest_dir.mkdir(parents=True)
        (latest_dir / "summary.json").write_text(json.dumps({
            "run_id": "run-1",
            "source_screenshot": "/tmp/screen_btc.png",
        }), encoding="utf-8")
        (latest_dir / "analysis.txt").write_text("line1\nline2\n", encoding="utf-8")
        published = tmp_path / "data" / "deskpro" / "inputs" / "vision_analysis"
        published.mkdir(parents=True)
        (published / "latest.json").write_text(json.dumps({"signals": [{"type": "support_level"}]}), encoding="utf-8")

        monkeypatch.setattr("modules.telegram_command_center.app.commands.REPO_ROOT", tmp_path)

        resp, ch, _ = dispatch("/analyze")
        assert ch == "ops"
        assert "Latest headless run: run-1" in resp
        assert "Published signals: 1" in resp

    def test_case_insensitive(self):
        resp, ch, _ = dispatch("/HELP")
        assert "Command Center" in resp

    def test_with_extra_args(self):
        resp, ch, _ = dispatch("/help --verbose")
        assert resp  # Should not crash

    def test_start_alias(self):
        resp, ch, _ = dispatch("/start")
        assert "Command Center" in resp
        assert ch is None

    def test_commands_alias(self):
        resp, ch, _ = dispatch("/commands")
        assert "Command Center" in resp
        assert ch is None

    def test_test_route_alias(self):
        resp, ch, _ = dispatch("/test_route")
        assert ch == "ops"
        assert "Route test" in resp or "Error" in resp

    def test_healthcheck_alias(self):
        resp, ch, _ = dispatch("/healthcheck")
        assert ch == "ops"

    def test_bot_mention_suffix(self):
        resp, ch, _ = dispatch("/help@ghost_admin_trading_bot")
        assert "Command Center" in resp
        assert ch is None

    def test_legacy_help_guidance(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_CHAT_ID", "-1001")
        monkeypatch.setattr("shared.telegram_channels.get_chat_id", lambda channel: "-1001" if channel == "default" else "")
        resp, ch, _ = dispatch("/help", chat_id="-1001")
        assert "legacy" in resp
        assert "OT_PIPELINE_GATES" in resp

    def test_wrong_group_guidance(self, monkeypatch):
        monkeypatch.setenv("TELEGRAM_CHAT_ID_PUSH", "-2002")
        resp, ch, action = dispatch("/status", chat_id="-2002")
        assert "OT_OPS_TOOLS" in resp
        assert ch is None
        assert action is None

    def test_detect_context_uses_channel_fallback(self, monkeypatch):
        monkeypatch.setattr("shared.telegram_channels.get_chat_id", lambda channel: {
            "ops": "-3003",
            "default": "-1000",
        }.get(channel, ""))
        resp, ch, _ = dispatch("/routes@ghost_admin_trading_bot", chat_id="-3003")
        assert ch == "ops"
        assert "Telegram routes" in resp

    def test_snapshot_returns_action(self):
        resp, ch, action = dispatch("/snapshot")
        assert "OT_PUSH_MARKET_DATA" in resp
        assert ch is None
        assert action is not None
        assert action["kind"] == "send_photo_channel"

    def test_test_screenshot_alias(self):
        resp, ch, action = dispatch("/test_screenshot")
        assert action is not None
        assert action["channel"] == "push"


class TestRegistry:
    def test_commands_registered(self):
        assert "/help" in COMMANDS
        assert "/status" in COMMANDS
        assert "/health" in COMMANDS
        assert "/approvals" in COMMANDS
        assert "/perf" in COMMANDS
        assert "/signals" in COMMANDS
        assert "/analyze" in COMMANDS
        assert "/routes" in COMMANDS
        assert "/test_routes" in COMMANDS
        assert "/snapshot" in COMMANDS

    def test_register_duplicate(self):
        # Registering the same command again should overwrite (no crash)
        register("/test_dup", "desc", cmd_help, channel="ops")
        assert "/test_dup" in COMMANDS
        desc, ch, _ = COMMANDS["/test_dup"]
        assert ch == "ops"


class TestCmdRoutes:
    def test_format(self):
        resp, ch, _ = cmd_routes()
        assert "alerts" in resp
        assert "pipeline" in resp
        assert "push" in resp
        assert "ops" in resp
        assert ch == "ops"


class TestCmdHelp:
    def test_with_args(self):
        resp, ch, _ = cmd_help("routes")
        assert "/routes" in resp

    def test_with_channel_unknown(self):
        resp, ch, _ = cmd_help("unknowncmd")
        assert "Unknown" in resp
