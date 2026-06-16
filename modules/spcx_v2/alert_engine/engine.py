"""
SPCX TV Alert Automation Engine
GO_SPACEX_TV_ALERT_AUTOMATION_ENGINE_01

Reads enriched SPCX data → decides alert placement → dispatches via TV orchestrator.
Tracks alert analytics: fire count, direction, win rate, SMC context.
"""
from __future__ import annotations
import json, os, time
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from dataclasses import dataclass, field

REPO_ROOT = Path(__file__).resolve().parents[3]

# ── Alert Types ──────────────────────────────────────────
ALERT_TEMPLATES = {
    "SPCX_HEARTBEAT_1M": {
        "condition": "greater_than", "price": 1,
        "frequency": "on_bar_close",
        "description": "1m heartbeat — confirms TV webhook is alive",
    },
    "SPCX_VWAP_RECLAIM": {
        "condition": "crossing", "price": 0,
        "frequency": "on_bar_close",
        "description": "Price reclaims VWAP from below",
    },
    "SPCX_ORB_BREAK_UP": {
        "condition": "greater_than", "price": None,  # dynamic: ORB high
        "frequency": "on_bar_close",
        "description": "Break above opening range high",
    },
    "SPCX_ORB_BREAK_DOWN": {
        "condition": "less_than", "price": None,  # dynamic: ORB low
        "frequency": "on_bar_close",
        "description": "Break below opening range low",
    },
    "SPCX_FVG_BULLISH_ZONE": {
        "condition": "crossing", "price": None,  # dynamic: FVG top
        "frequency": "on_bar_close",
        "description": "Price enters bullish FVG zone",
    },
    "SPCX_FVG_BEARISH_ZONE": {
        "condition": "crossing", "price": None,  # dynamic: FVG bottom
        "frequency": "on_bar_close",
        "description": "Price enters bearish FVG zone",
    },
    "SPCX_BOS_LEVEL": {
        "condition": "greater_than", "price": None,  # dynamic: BOS level
        "frequency": "on_bar_close",
        "description": "Break of structure confirmed",
    },
    "SPCX_VOLUME_SPIKE": {
        "condition": "greater_than", "price": 0,
        "frequency": "on_bar_close",
        "description": "Volume spike > 2x average",
    },
}


@dataclass
class AlertState:
    alert_id: str
    alert_type: str
    symbol: str = "BATS:SPCX"
    price_level: float | None = None
    active: bool = True
    created_at: str = ""
    last_fired_at: str = ""
    fire_count: int = 0
    fire_directions: list[str] = field(default_factory=list)  # "UP", "DOWN", "NEUTRAL"
    smc_context: dict[str, Any] = field(default_factory=dict)


@dataclass
class AlertPlacementDecision:
    alert_type: str
    action: str  # "create", "update", "delete", "keep"
    price_level: float | None = None
    reason: str = ""


class AlertAutomationEngine:
    """Reads enriched data, decides alert placement, dispatches to TV orchestrator."""

    def __init__(self, webhook_url: str = "https://spacex-tv.magikgmo4.uk/tv/spacex"):
        self.webhook_url = webhook_url
        self.registry_path = REPO_ROOT / "data" / "ipo" / "spacex" / "alert_registry.json"
        self.analytics_path = REPO_ROOT / "data" / "ipo" / "spacex" / "alert_analytics.jsonl"
        self.registry = self._load_registry()

    def _load_registry(self) -> dict[str, AlertState]:
        if self.registry_path.exists():
            data = json.loads(self.registry_path.read_text())
            return {k: AlertState(**v) for k, v in data.items()}
        return {}

    def _save_registry(self):
        data = {k: vars(v) for k, v in self.registry.items()}
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        self.registry_path.write_text(json.dumps(data, indent=2, default=str))

    def evaluate(self, enriched: dict) -> list[AlertPlacementDecision]:
        """Read enriched data, return alert placement decisions."""
        decisions = []
        smc = enriched.get("smart_money", {})
        indicators = enriched.get("indicators", {})
        consensus = enriched.get("consensus", {})
        scores = enriched.get("scores", {})
        price = consensus.get("consensus_price")

        # Always: heartbeat
        if "SPCX_HEARTBEAT_1M" not in self.registry:
            decisions.append(AlertPlacementDecision(
                "SPCX_HEARTBEAT_1M", "create",
                reason="No heartbeat alert registered"
            ))

        # VWAP reclaim/reject
        vwap_dist = indicators.get("vwap_distance_pct")
        if vwap_dist is not None and abs(vwap_dist) < 0.5:
            if vwap_dist > 0 and "SPCX_VWAP_RECLAIM" not in self.registry:
                decisions.append(AlertPlacementDecision(
                    "SPCX_VWAP_RECLAIM", "create", price_level=price,
                    reason=f"Price near VWAP (+{vwap_dist:.2f}%)"
                ))

        # SMC-based alerts
        if smc.get("fvg_bullish"):
            if "SPCX_FVG_BULLISH_ZONE" not in self.registry and price:
                decisions.append(AlertPlacementDecision(
                    "SPCX_FVG_BULLISH_ZONE", "create", price_level=price,
                    reason="Bullish FVG detected"
                ))

        if smc.get("fvg_bearish"):
            if "SPCX_FVG_BEARISH_ZONE" not in self.registry and price:
                decisions.append(AlertPlacementDecision(
                    "SPCX_FVG_BEARISH_ZONE", "create", price_level=price,
                    reason="Bearish FVG detected"
                ))

        if smc.get("bos"):
            if "SPCX_BOS_LEVEL" not in self.registry and price:
                decisions.append(AlertPlacementDecision(
                    "SPCX_BOS_LEVEL", "create", price_level=price,
                    reason="Break of Structure detected"
                ))

        # Volume spike
        rel_vol = indicators.get("relative_volume", 0)
        if rel_vol and rel_vol > 2.0 and "SPCX_VOLUME_SPIKE" not in self.registry:
            decisions.append(AlertPlacementDecision(
                "SPCX_VOLUME_SPIKE", "create", price_level=price,
                reason=f"Volume spike {rel_vol:.1f}x average"
            ))

        # Cleanup: remove alerts for structures that no longer exist
        if not smc.get("bos") and "SPCX_BOS_LEVEL" in self.registry:
            decisions.append(AlertPlacementDecision(
                "SPCX_BOS_LEVEL", "delete",
                reason="BOS no longer active"
            ))

        return decisions

    def record_fire(self, webhook_event: dict):
        """Record an alert fire from webhook."""
        alert_name = webhook_event.get("alert_name", "")
        alert_type = webhook_event.get("event", webhook_event.get("signal", ""))
        price = webhook_event.get("price", webhook_event.get("close"))
        received_at = webhook_event.get("received_at", "")

        if alert_name in self.registry:
            st = self.registry[alert_name]
        else:
            st = AlertState(alert_id=alert_name, alert_type=alert_type)
            self.registry[alert_name] = st

        st.last_fired_at = received_at
        st.fire_count += 1

        # Track direction
        if price:
            try:
                p = float(price)
                if st.price_level:
                    st.fire_directions.append("UP" if p > st.price_level else "DOWN")
                else:
                    st.fire_directions.append("NEUTRAL")
            except (ValueError, TypeError):
                st.fire_directions.append("NEUTRAL")

        # Persist analytics
        self.analytics_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.analytics_path, "a") as f:
            f.write(json.dumps({
                "ts": received_at,
                "alert_name": alert_name,
                "alert_type": alert_type,
                "price": price,
                "fire_count": st.fire_count,
                "smc_context": st.smc_context,
            }, default=str) + "\n")

        self._save_registry()

    def dispatch(self, decisions: list[AlertPlacementDecision], dry_run: bool = True) -> list[dict]:
        """Dispatch decisions to TV orchestrator. Returns job results."""
        results = []
        for d in decisions:
            if d.action == "keep":
                continue

            template = ALERT_TEMPLATES.get(d.alert_type, {})
            price = d.price_level if d.price_level is not None else template.get("price", 1)

            if d.action == "create":
                job = {
                    "schema": "tv_job_v1",
                    "id": f"auto_alert_{d.alert_type}_{int(time.time())}",
                    "type": "alert.create",
                    "params": {
                        "symbol": "BATS:SPCX",
                        "condition": template.get("condition", "crossing"),
                        "price": price,
                        "frequency": template.get("frequency", "on_bar_close"),
                        "name": d.alert_type,
                        "webhook_url": self.webhook_url,
                        "message": json.dumps(self._webhook_payload(d.alert_type)),
                    },
                    "gate": "approved",
                    "status": "pending",
                    "notes": f"Auto-generated by AlertAutomationEngine: {d.reason}",
                }
                results.append({"decision": d, "job": job})

                if not dry_run and d.alert_type not in self.registry:
                    self.registry[d.alert_type] = AlertState(
                        alert_id=d.alert_type, alert_type=d.alert_type,
                        price_level=d.price_level, created_at=datetime.now(timezone.utc).isoformat()
                    )

            elif d.action == "delete":
                job = {
                    "schema": "tv_job_v1",
                    "id": f"auto_alert_del_{d.alert_type}_{int(time.time())}",
                    "type": "alert.delete",
                    "params": {"alert_id": d.alert_type},
                    "gate": "approved",
                    "status": "pending",
                    "notes": f"Auto-generated by AlertAutomationEngine: {d.reason}",
                }
                results.append({"decision": d, "job": job})
                if not dry_run:
                    self.registry.pop(d.alert_type, None)

        if not dry_run:
            self._save_registry()

        # Actually dispatch via TV runner (if not dry_run)
        if not dry_run and results:
            try:
                from modules.tradingview_orchestrator.app.tv_runner import run_job
                for r in results:
                    if "job" in r:
                        run_result = run_job(r["job"], gate_approved=True, dry_run=False)
                        r["result"] = run_result
            except ImportError:
                r["result"] = {"error": "tv_runner not available (cursor-ai unreachable?)"}

        return results

    def _webhook_payload(self, alert_type: str) -> dict:
        return {
            "key": "__TV_WEBHOOK_KEY__",
            "schema": "spacex_tv_event_v1",
            "source": "tradingview",
            "alert_name": f"{{{{alert_name}}}}",
            "event": alert_type,
            "symbol": "{{ticker}}",
            "exchange": "{{exchange}}",
            "interval": "{{interval}}",
            "price": "{{close}}",
            "open": "{{open}}",
            "high": "{{high}}",
            "low": "{{low}}",
            "close": "{{close}}",
            "volume": "{{volume}}",
            "time": "{{time}}",
            "mode": "monitor_only",
        }

    def get_analytics(self) -> dict:
        """Return alert analytics summary."""
        total_fires = sum(a.fire_count for a in self.registry.values())
        by_type = {}
        for name, state in self.registry.items():
            ups = sum(1 for d in state.fire_directions if d == "UP")
            downs = sum(1 for d in state.fire_directions if d == "DOWN")
            by_type[name] = {
                "fire_count": state.fire_count,
                "last_fired": state.last_fired_at,
                "up_count": ups,
                "down_count": downs,
                "active": state.active,
                "price_level": state.price_level,
            }
        return {
            "total_alerts": len(self.registry),
            "total_fires": total_fires,
            "by_type": by_type,
            "registry_path": str(self.registry_path),
            "analytics_path": str(self.analytics_path),
        }
