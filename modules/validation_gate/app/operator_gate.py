from __future__ import annotations
import json
import logging
import time
from pathlib import Path
from typing import Optional

log = logging.getLogger("validation_gate.operator")


class OperatorGate:
    """File-based operator approval polling for V1."""

    def __init__(self, approval_dir: Path):
        self.approval_dir = approval_dir

    def _approval_path(self, request_id: str) -> Path:
        return self.approval_dir / f"{request_id}.json"

    def write_approval(self, request_id: str, verdict: str) -> None:
        """Write approval file (test helper and CLI use)."""
        self.approval_dir.mkdir(parents=True, exist_ok=True)
        self._approval_path(request_id).write_text(json.dumps({"verdict": verdict.upper()}))

    def poll(
        self,
        request_id: str,
        timeout_s: float,
        poll_interval_s: float = 2.0,
    ) -> Optional[bool]:
        """Poll for approval. Returns True (APPROVE), False (REJECT), None (timeout)."""
        self.approval_dir.mkdir(parents=True, exist_ok=True)
        path = self._approval_path(request_id)
        deadline = time.monotonic() + timeout_s

        while time.monotonic() < deadline:
            if path.exists():
                try:
                    data = json.loads(path.read_text())
                    verdict = data.get("verdict", "").upper()
                    path.unlink(missing_ok=True)
                    if verdict == "APPROVE":
                        log.info("operator APPROVE request_id=%s", request_id)
                        return True
                    if verdict == "REJECT":
                        log.info("operator REJECT request_id=%s", request_id)
                        return False
                    log.warning("unknown verdict=%r request_id=%s", verdict, request_id)
                except Exception as exc:
                    log.warning("approval file parse error: %s", exc)
            time.sleep(poll_interval_s)

        log.info("operator approval timeout request_id=%s timeout_s=%s", request_id, timeout_s)
        return None
