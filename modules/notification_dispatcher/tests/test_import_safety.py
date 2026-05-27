"""
Import safety tests for notification_dispatcher.

Verifies:
- events.py has no external deps — importable without requests
- __init__.py lazy import — PipelineEvent accessible without requests
- NotificationDispatcher degrades to None (not raises) when requests absent
- No network call triggered on package import
- Downstream modules (validation_gate, trade_executor, result_tracker) import cleanly
"""
import sys
import subprocess
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def _run(code: str) -> tuple[str, str]:
    result = subprocess.run(
        [sys.executable, "-c", code],
        capture_output=True,
        text=True,
        cwd=str(REPO_ROOT),
    )
    return result.stdout.strip(), result.stderr.strip()


_PREAMBLE = f"""
import sys
sys.path.insert(0, r'{REPO_ROOT}')
sys.modules["requests"] = None
"""


class TestEventsImportSafety(unittest.TestCase):
    def test_events_importable_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.notification_dispatcher.app.events import PipelineEvent, EventType
e = PipelineEvent(event_type="pipeline_info", payload={"message": "ok"})
assert e.event_type == "pipeline_info"
print("PASS")
""")
        self.assertIn("PASS", out, f"events import failed\nstderr: {err}")

    def test_package_import_pipeline_event_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.notification_dispatcher.app import PipelineEvent
assert PipelineEvent is not None
e = PipelineEvent(event_type="signal_received")
assert e.event_type == "signal_received"
print("PASS")
""")
        self.assertIn("PASS", out, f"package PipelineEvent import failed\nstderr: {err}")

    def test_notificationdispatcher_none_when_requests_absent(self):
        out, err = _run(_PREAMBLE + """
from modules.notification_dispatcher.app import NotificationDispatcher
assert NotificationDispatcher is None, f"Expected None, got {NotificationDispatcher}"
print("PASS")
""")
        self.assertIn("PASS", out, f"NotificationDispatcher should degrade to None\nstderr: {err}")

    def test_import_does_not_trigger_network_call(self):
        out, err = _run(_PREAMBLE + """
import socket
_orig = socket.socket.connect
def _no_connect(self, *a, **kw):
    raise AssertionError("network call on import: " + str(a))
socket.socket.connect = _no_connect
try:
    from modules.notification_dispatcher.app import PipelineEvent, NotificationDispatcher
    print("PASS")
finally:
    socket.socket.connect = _orig
""")
        self.assertIn("PASS", out, f"import triggered network call\nstderr: {err}")

    def test_all_event_types_accessible_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.notification_dispatcher.app.events import ALL_EVENT_TYPES
assert len(ALL_EVENT_TYPES) == 7
print("PASS")
""")
        self.assertIn("PASS", out, f"ALL_EVENT_TYPES not accessible\nstderr: {err}")


class TestDownstreamImportSafety(unittest.TestCase):
    def test_validation_gate_imports_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.validation_gate.app.gate import ValidationGate
print("PASS")
""")
        self.assertIn("PASS", out, f"validation_gate import failed\nstderr: {err}")

    def test_trade_executor_imports_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.trade_executor.app.executor import TradeExecutor
print("PASS")
""")
        self.assertIn("PASS", out, f"trade_executor import failed\nstderr: {err}")

    def test_result_tracker_imports_without_requests(self):
        out, err = _run(_PREAMBLE + """
from modules.result_tracker.app.tracker import ResultTracker
print("PASS")
""")
        self.assertIn("PASS", out, f"result_tracker import failed\nstderr: {err}")

    def test_pipeline_event_fallback_in_validation_gate(self):
        out, err = _run(_PREAMBLE + """
from modules.validation_gate.app.gate import ValidationGate
# When requests absent, _DISPATCHER_AVAILABLE is False
# ValidationGate must instantiate without error
import tempfile, pathlib
gate = ValidationGate(approval_dir=pathlib.Path(tempfile.mkdtemp()))
assert gate.dispatcher is None
print("PASS")
""")
        self.assertIn("PASS", out, f"ValidationGate fallback broken\nstderr: {err}")


if __name__ == "__main__":
    unittest.main()
