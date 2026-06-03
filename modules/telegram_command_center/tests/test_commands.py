"""Tests for telegram_command_center command dispatch."""
from modules.telegram_command_center.app.commands import (
    dispatch, COMMANDS, register, cmd_help, cmd_routes, cmd_test_routes,
)


class TestDispatch:
    def test_unknown_command(self):
        resp, ch = dispatch("/nonexistent")
        assert "Unknown command" in resp
        assert ch is None

    def test_empty_text(self):
        resp, ch = dispatch("")
        assert resp == ""
        assert ch is None

    def test_non_command(self):
        resp, ch = dispatch("hello world")
        assert resp == ""
        assert ch is None

    def test_help(self):
        resp, ch = dispatch("/help")
        assert "Command Center" in resp
        assert ch is None

    def test_help_with_arg(self):
        resp, ch = dispatch("/help status")
        assert "/status" in resp

    def test_help_unknown_arg(self):
        resp, ch = dispatch("/help unknowncmd")
        assert "Unknown command" in resp

    def test_routes(self):
        resp, ch = dispatch("/routes")
        assert "Telegram routes" in resp
        assert ch == "ops"

    def test_status(self):
        resp, ch = dispatch("/status")
        assert ch == "pipeline"

    def test_health(self):
        resp, ch = dispatch("/health")
        assert ch == "ops"

    def test_approvals(self):
        resp, ch = dispatch("/approvals")
        assert ch == "pipeline"
        # Should handle missing queue file gracefully
        assert resp

    def test_perf(self):
        resp, ch = dispatch("/perf")
        assert ch == "pipeline"

    def test_signals(self):
        resp, ch = dispatch("/signals")
        assert ch == "pipeline"

    def test_analyze(self):
        resp, ch = dispatch("/analyze")
        assert ch == "ops"

    def test_case_insensitive(self):
        resp, ch = dispatch("/HELP")
        assert "Command Center" in resp

    def test_with_extra_args(self):
        resp, ch = dispatch("/help --verbose")
        assert resp  # Should not crash


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

    def test_register_duplicate(self):
        # Registering the same command again should overwrite (no crash)
        register("/test_dup", "desc", cmd_help, channel="ops")
        assert "/test_dup" in COMMANDS
        desc, ch, _ = COMMANDS["/test_dup"]
        assert ch == "ops"


class TestCmdRoutes:
    def test_format(self):
        resp, ch = cmd_routes()
        assert "alerts" in resp
        assert "pipeline" in resp
        assert "push" in resp
        assert "ops" in resp
        assert ch == "ops"


class TestCmdHelp:
    def test_with_args(self):
        resp, ch = cmd_help("routes")
        assert "/routes" in resp

    def test_with_channel_unknown(self):
        resp, ch = cmd_help("unknowncmd")
        assert "Unknown" in resp
