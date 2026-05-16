from __future__ import annotations
import logging
import time
import uuid
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .schema import GateRequest, GateDecision
from .risk_check import check_risk
from .operator_gate import OperatorGate

try:
    from modules.notification_dispatcher.app.dispatcher import NotificationDispatcher
    from modules.notification_dispatcher.app.events import PipelineEvent
    _DISPATCHER_AVAILABLE = True
except ImportError:
    _DISPATCHER_AVAILABLE = False

log = logging.getLogger("validation_gate")

_DEFAULT_APPROVAL_DIR = PROJECT_ROOT / "data" / "gate_approvals"

_DRY_APPROVE_THRESHOLD = 0.7


class ValidationGate:
    def __init__(
        self,
        approval_dir: Path | None = None,
        dispatcher=None,
    ):
        self.approval_dir = approval_dir or _DEFAULT_APPROVAL_DIR
        self.operator_gate = OperatorGate(self.approval_dir)
        if dispatcher is not None:
            self.dispatcher = dispatcher
        elif _DISPATCHER_AVAILABLE:
            self.dispatcher = NotificationDispatcher()
        else:
            self.dispatcher = None

    def _send_approval_notification(self, req: GateRequest) -> dict:
        if self.dispatcher is None:
            return {"ok": False, "error": "no_dispatcher"}
        prop = req.proposition
        ticker = req.ticker or prop.engines_context.get("ticker", prop.signal_id)
        event = PipelineEvent(
            event_type="approval_required",
            signal_id=prop.signal_id,
            request_id=req.request_id,
            payload={
                "ticker": ticker,
                "action": prop.action,
                "entry": prop.entry,
                "sl": prop.sl,
                "tp": prop.tp,
                "confidence": prop.confidence,
            },
        )
        return self.dispatcher.dispatch(event, dry_run=req.dry_run)

    def gate(self, req: GateRequest) -> GateDecision:
        if not req.request_id:
            req.request_id = str(uuid.uuid4())

        t0 = time.monotonic()
        risk_status, risk_reason = check_risk(req.proposition)

        if risk_status == "BLOCK":
            return GateDecision(
                request_id=req.request_id,
                signal_id=req.proposition.signal_id,
                verdict="REJECTED",
                reason=risk_reason,
                risk_status=risk_status,
                risk_reason=risk_reason,
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=req.dry_run,
            )

        # Risk is ALLOW or CAUTION — need operator gate or auto-decision
        if not req.require_operator:
            verdict = "APPROVED" if risk_status == "ALLOW" else "NEEDS_REVIEW"
            return GateDecision(
                request_id=req.request_id,
                signal_id=req.proposition.signal_id,
                verdict=verdict,
                reason=f"auto_{verdict.lower()}",
                risk_status=risk_status,
                risk_reason=risk_reason,
                operator_approved=None,
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=req.dry_run,
            )

        # Send operator approval notification
        notif_result = self._send_approval_notification(req)
        log.info(
            "approval_required sent request_id=%s dry_run=%s notif_ok=%s",
            req.request_id, req.dry_run, notif_result.get("ok"),
        )

        if req.dry_run:
            # Simulate operator: approve if confidence >= threshold
            simulated = req.proposition.confidence >= _DRY_APPROVE_THRESHOLD
            verdict = "APPROVED" if simulated else "HOLD"
            return GateDecision(
                request_id=req.request_id,
                signal_id=req.proposition.signal_id,
                verdict=verdict,
                reason="dry_run_simulated_operator",
                risk_status=risk_status,
                risk_reason=risk_reason,
                operator_approved=simulated,
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=True,
                meta={"notif": notif_result},
            )

        # Live: poll approval file
        approved = self.operator_gate.poll(
            req.request_id, req.timeout_s, req.poll_interval_s
        )

        if approved is None:
            verdict, reason, op_approved = "HOLD", "operator_timeout", None
        elif approved:
            verdict, reason, op_approved = "APPROVED", "operator_approved", True
        else:
            verdict, reason, op_approved = "REJECTED", "operator_rejected", False

        return GateDecision(
            request_id=req.request_id,
            signal_id=req.proposition.signal_id,
            verdict=verdict,
            reason=reason,
            risk_status=risk_status,
            risk_reason=risk_reason,
            operator_approved=op_approved,
            duration_ms=int((time.monotonic() - t0) * 1000),
            dry_run=False,
            meta={"notif": notif_result},
        )
