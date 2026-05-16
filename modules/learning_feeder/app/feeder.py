from __future__ import annotations
import json
import logging
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[3]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from .schema import FeedRequest, FeedResult
from .composer import compose_feedback

try:
    from modules.openclaw_operator_bridge.app.bridge import OperatorBridge
    from modules.openclaw_operator_bridge.app.schema import BridgeRequest
    _BRIDGE_AVAILABLE = True
except ImportError:
    _BRIDGE_AVAILABLE = False

log = logging.getLogger("learning_feeder")

_DEFAULT_BRICKS_DIR = PROJECT_ROOT / "data" / "learning_bricks"


class LearningFeeder:
    """
    Sends trade feedback to OpenClaw (bridge) and stores it as a learning brick.
    V1: dry_run skips bridge + brick write; live uses file-based brick store.
    """

    def __init__(self, bridge=None, bricks_dir: Path | None = None):
        self._bridge = bridge          # injectable for tests
        self.bricks_dir = bricks_dir or _DEFAULT_BRICKS_DIR

    def _get_bridge(self):
        if self._bridge is not None:
            return self._bridge
        if _BRIDGE_AVAILABLE:
            return OperatorBridge()
        return None

    def _store_brick(self, req: FeedRequest, summary: str) -> str:
        """Write learning brick to local JSON store. Returns brick_id."""
        try:
            date_str = datetime.now(timezone.utc).strftime("%Y%m%d")
            brick_dir = self.bricks_dir / date_str
            brick_dir.mkdir(parents=True, exist_ok=True)
            brick_id = f"lf_{req.signal_id}_{req.request_id[:8]}"
            brick = {
                "brick_id": brick_id,
                "signal_id": req.signal_id,
                "request_id": req.request_id,
                "ticker": req.trade_record.ticker,
                "action": req.trade_record.action,
                "outcome": req.trade_record.outcome,
                "net_pnl": req.trade_record.net_pnl,
                "confidence": req.proposition.confidence,
                "summary": summary,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
            path = brick_dir / f"{brick_id}.json"
            path.write_text(json.dumps(brick, indent=2, ensure_ascii=False))
            log.info("brick stored brick_id=%s path=%s", brick_id, path)
            return brick_id
        except Exception as exc:
            log.error("brick store failed: %s", exc)
            return ""

    def feed(self, req: FeedRequest) -> FeedResult:
        if not req.request_id:
            req.request_id = str(uuid.uuid4())

        t0 = time.monotonic()
        summary = compose_feedback(req.proposition, req.trade_record)

        # --- dry_run: skip bridge + brick store ---
        if req.dry_run:
            return FeedResult(
                request_id=req.request_id,
                signal_id=req.signal_id,
                bridge_status="dry_run",
                brick_stored=False,
                brick_id="",
                summary=summary,
                duration_ms=int((time.monotonic() - t0) * 1000),
                dry_run=True,
                meta={"dry_run": True},
            )

        # --- live: send to bridge ---
        bridge_status = "error"
        bridge_meta: dict = {}
        bridge = self._get_bridge()

        if bridge is not None:
            br = BridgeRequest(
                action="evaluate",
                instruction=summary,
                context=f"learning_feeder signal_id={req.signal_id} outcome={req.trade_record.outcome}",
                request_id=req.request_id,
                timeout_s=req.bridge_timeout_s,
            )
            resp = bridge.send(br)
            bridge_status = resp.status
            bridge_meta = {"bridge_response": resp.status, "bridge_error": resp.error}
        else:
            bridge_meta = {"error": "bridge_unavailable"}

        # --- store brick ---
        brick_id = ""
        brick_stored = False
        if req.store_brick:
            brick_id = self._store_brick(req, summary)
            brick_stored = brick_id != ""

        log.info(
            "learning_feeder signal_id=%s outcome=%s bridge=%s brick=%s",
            req.signal_id, req.trade_record.outcome, bridge_status, brick_id,
        )

        return FeedResult(
            request_id=req.request_id,
            signal_id=req.signal_id,
            bridge_status=bridge_status,
            brick_stored=brick_stored,
            brick_id=brick_id,
            summary=summary,
            duration_ms=int((time.monotonic() - t0) * 1000),
            dry_run=False,
            meta=bridge_meta,
        )
