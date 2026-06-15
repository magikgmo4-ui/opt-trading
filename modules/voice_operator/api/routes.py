"""
Voice Operator API — Read-Only Abstraction Layer
GO_DESKPRO_VOICE_OPERATOR_01 — Lot B

Exposes 8 canonical /read/* endpoints that aggregate data from
existing services (DeskPro, Perf, LocalCMS, Memory) without
modifying them.

Endpoints:
  GET /read/system    — full system health
  GET /read/market    — market overview
  GET /read/spacex    — SPCX summary
  GET /read/alerts    — recent alerts
  GET /read/setups    — active setups
  GET /read/setup     — setup detail (query: symbol)
  GET /read/score     — scores detail (query: symbol)
  GET /read/report    — daily report summary

Invariants:
  - Read-only, no side effects
  - No trading logic, no score computation
  - DeskPro remains source of truth
  - Monitor-only
"""
from __future__ import annotations
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
from datetime import datetime, timezone

from .readers import deskpro_reader, perf_reader, localcms_reader, memory_reader

app = FastAPI(
    title="Voice Operator API",
    description="Read-only abstraction for Opt-Trading voice interface",
    version="0.1.0",
)


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _safe_float(v: any, default: float = 0.0) -> float:
    try:
        return float(v) if v is not None else default
    except (ValueError, TypeError):
        return default


def _safe_int(v: any, default: int = 0) -> int:
    try:
        return int(v) if v is not None else default
    except (ValueError, TypeError):
        return default


# ── /read/system ────────────────────────────────────────────────────────
@app.get("/read/system")
def read_system():
    """Full system health — all services, timers, critical alerts."""
    desk_status = deskpro_reader.read_status()
    perf_summary = perf_reader.read_summary()

    services = []
    services_running = 0

    # DeskPro
    if desk_status.get("ok"):
        services_running += 1
    services.append({
        "name": "deskpro",
        "ok": desk_status.get("ok", False),
        "details": desk_status.get("status", {}),
    })

    # Perf
    if perf_summary.get("ok") or "total_trades" in perf_summary:
        services_running += 1
    services.append({
        "name": "perf_app",
        "ok": perf_summary.get("ok") or "total_trades" in perf_summary,
        "details": {
            "total_trades": perf_summary.get("total_trades", 0),
            "winrate": perf_summary.get("winrate", 0),
        },
    })

    # LocalCMS
    cms_health = localcms_reader.read_menu_state()
    if cms_health.get("ok", True):
        services_running += 1
    services.append({
        "name": "localcms",
        "ok": cms_health.get("ok", True),
    })

    # Memory
    mem = memory_reader.read_status()
    services.append({
        "name": "memory_bricks",
        "ok": mem.get("ok", False),
        "status": mem.get("status", "unknown"),
    })

    # Webhook
    services.append({
        "name": "webhook_server",
        "ok": True,  # assumed if desk_status works
    })
    services_running += 1

    critical = 0
    alerts_data = deskpro_reader.read_alerts(limit=5)
    if alerts_data.get("alerts"):
        critical = sum(1 for a in alerts_data["alerts"] if a.get("severity") == "critical")

    pipeline_state = "healthy"
    if desk_status.get("status", {}).get("health") == "degraded":
        pipeline_state = "degraded"
    elif critical > 0:
        pipeline_state = "warning"

    one_line = f"Systeme operationnel. {services_running} services actifs"
    if critical > 0:
        one_line += f", {critical} alertes critiques"
    if pipeline_state == "degraded":
        one_line += ", pipeline degrade"

    return {
        "status": "ok" if services_running >= 4 else "degraded",
        "services_running": services_running,
        "services": services,
        "critical_alerts": critical,
        "pipeline_state": pipeline_state,
        "timers_active": 2,  # orderflow + EOD backtest
        "stale_sources": [],
        "one_line": one_line,
        "generated_at": _now(),
    }


# ── /read/spacex ────────────────────────────────────────────────────────
@app.get("/read/spacex")
def read_spacex():
    """SPCX summary — price, VWAP, scores, top setup."""
    cc = deskpro_reader.read_command_center()
    snap = deskpro_reader.read_snapshot()

    price = _safe_float(cc.get("price"))
    vwap = cc.get("vwap")
    vwap_state = "NO_DATA"
    vwap_score = 0

    # Extract VWAP analysis from snapshot
    vwap_data = snap.get("vwap_analysis", {})
    if vwap_data:
        vwap_state = vwap_data.get("vwap_state", "NO_DATA")
        vwap_score = _safe_int(vwap_data.get("vwap_score"))

    # Trend from scores
    scores = snap.get("scores", {})
    momentum = _safe_float(scores.get("momentum"))
    gap_ipo = _safe_float(cc.get("gap_pct") or snap.get("gap_vs_ipo_pct"))
    trend = "neutral"
    if momentum and momentum > 0.7:
        trend = "bullish"
    elif gap_ipo and gap_ipo < 0:
        trend = "bearish"

    confidence = _safe_float(cc.get("confidence"))
    ow_score = None
    of_score = None
    sq_tier = "unknown"

    sq = snap.get("source_quality", {})
    if sq:
        sq_tier = sq.get("overall_tier", "unknown")
    of_data = snap.get("orderflow_score", {})
    if isinstance(of_data, dict):
        of_score = of_data.get("score")
    ow_data = snap.get("ownership_score", {})
    if isinstance(ow_data, dict):
        ow_score = ow_data.get("score")

    pipeline_state = snap.get("pipeline_state", "unknown")

    summary = f"SPCX a {price:.1f}"
    if vwap and vwap > 0:
        summary += f", VWAP {vwap:.1f}, etat {vwap_state}"
    summary += f". Score VWAP {vwap_score}/100"
    if cc.get("top_setup"):
        summary += f". Setup {cc['top_setup']}"
    if gap_ipo:
        summary += f". Gap IPO {gap_ipo:+.1f}%"

    return {
        "symbol": "SPCX",
        "price": price,
        "vwap": vwap,
        "vwap_state": vwap_state,
        "vwap_score": vwap_score,
        "gap_ipo_pct": round(gap_ipo, 2) if gap_ipo else None,
        "trend": trend,
        "trade_ready": _safe_int(scores.get("trade_ready", 0) * 100 if scores.get("trade_ready") and scores["trade_ready"] <= 1 else scores.get("trade_ready", 0)),
        "top_setup": cc.get("top_setup"),
        "setup_grade": cc.get("grade", "reject"),
        "confidence": confidence,
        "orderflow_score": of_score,
        "ownership_pressure_score": ow_score,
        "pipeline_state": pipeline_state,
        "source_quality": sq_tier,
        "summary": summary,
        "generated_at": _now(),
    }


# ── /read/alerts ────────────────────────────────────────────────────────
@app.get("/read/alerts")
def read_alerts(limit: int = Query(10, ge=1, le=50)):
    """Recent alerts from all sources."""
    items = []

    # DeskPro alerts
    desk_alerts = deskpro_reader.read_alerts(limit=limit)
    for a in (desk_alerts.get("alerts") or [])[:limit]:
        items.append({
            "ts": a.get("ts", a.get("timestamp", "")),
            "source": "deskpro",
            "severity": a.get("severity", a.get("level", "info")),
            "message": a.get("message", a.get("title", "")),
        })

    # Telegram signals as alerts
    sigs = localcms_reader.read_signals_summary()
    for s in (sigs.get("signals") or [])[:3]:
        items.append({
            "ts": s.get("ts", ""),
            "source": "telegram",
            "severity": "info",
            "message": f"{s.get('pair','')} {s.get('direction','')} via {s.get('channel','')}",
        })

    critical = sum(1 for i in items if i["severity"] == "critical")
    one_line = f"{len(items)} alertes"
    if critical:
        one_line = f"{critical} alertes critiques sur {len(items)}"

    return {
        "total": len(items),
        "critical": critical,
        "items": items,
        "one_line": one_line,
        "generated_at": _now(),
    }


# ── /read/setups ────────────────────────────────────────────────────────
@app.get("/read/setups")
def read_setups():
    """Active setups from all sources."""
    items = []
    a_plus = 0
    a_grade = 0

    # SPCX V2 setups from command center
    cc = deskpro_reader.read_command_center()
    top_setup = cc.get("top_setup")
    if top_setup and top_setup != "NONE":
        grade = cc.get("grade", "B")
        items.append({
            "symbol": "SPCX",
            "setup_type": top_setup,
            "direction": "LONG" if cc.get("action") and "buy" in str(cc.get("action", "")).lower() else "SHORT",
            "grade": grade,
            "trade_ready": _safe_int(cc.get("trade_ready") or cc.get("edge_score", 0)),
            "confidence": _safe_float(cc.get("confidence")),
            "entry_zone": cc.get("entry_zone"),
            "invalidation": cc.get("invalidation"),
            "target_1": cc.get("tp1"),
            "source": "spcx_v2",
        })
        if grade == "A+":
            a_plus += 1
        elif grade == "A":
            a_grade += 1

    # Open trades from perf as active setups
    open_trades = perf_reader.read_open_trades()
    for t in (open_trades.get("open") or [])[:5]:
        items.append({
            "symbol": t.get("symbol", "???"),
            "setup_type": t.get("engine", "unknown"),
            "direction": t.get("side", "LONG"),
            "grade": "ACTIVE",
            "trade_ready": 0,
            "confidence": 0,
            "entry_zone": str(t.get("entry", "")),
            "invalidation": f"SL {t.get('stop', '?')}",
            "target_1": None,
            "source": "tv_webhook",
        })

    active = len(items)
    one_line = f"{active} setups actifs"
    if a_plus:
        one_line += f", dont {a_plus} A+"

    return {
        "active": active,
        "a_plus": a_plus,
        "a_grade": a_grade,
        "items": items,
        "one_line": one_line,
        "generated_at": _now(),
    }


# ── /read/setup ─────────────────────────────────────────────────────────
@app.get("/read/setup")
def read_setup(symbol: str = Query("SPCX", min_length=1, max_length=20)):
    """Setup detail for a specific symbol."""
    # For SPCX, use command center
    if symbol.upper() == "SPCX":
        cc = deskpro_reader.read_command_center()
        return {
            "symbol": "SPCX",
            "setup_type": cc.get("top_setup", "NONE"),
            "direction": "LONG" if cc.get("action") and "buy" in str(cc.get("action", "")).lower() else "SHORT",
            "grade": cc.get("grade", "reject"),
            "trade_ready": _safe_int(cc.get("trade_ready") or cc.get("edge_score", 0)),
            "confidence": _safe_float(cc.get("confidence")),
            "entry_zone": cc.get("entry_zone"),
            "invalidation": cc.get("invalidation"),
            "target_1": cc.get("tp1"),
            "target_2": cc.get("tp2"),
            "source": "spcx_v2",
            "generated_at": _now(),
        }

    # For other symbols, check open trades
    open_trades = perf_reader.read_open_trades()
    for t in (open_trades.get("open") or []):
        if t.get("symbol", "").upper().startswith(symbol.upper()):
            return {
                "symbol": t.get("symbol", symbol),
                "setup_type": t.get("engine", "unknown"),
                "direction": t.get("side", "LONG"),
                "grade": "ACTIVE",
                "trade_ready": 0,
                "confidence": 0,
                "entry_zone": str(t.get("entry", "")),
                "invalidation": f"SL {t.get('stop', '?')}",
                "target_1": None,
                "source": "tv_webhook",
                "generated_at": _now(),
            }

    return {
        "symbol": symbol.upper(),
        "setup_type": "NONE",
        "direction": "neutral",
        "grade": "reject",
        "trade_ready": 0,
        "confidence": 0,
        "source": "none",
        "one_line": f"Aucun setup actif pour {symbol.upper()}",
        "generated_at": _now(),
    }


# ── /read/score ─────────────────────────────────────────────────────────
@app.get("/read/score")
def read_score(symbol: str = Query("SPCX", min_length=1, max_length=20)):
    """Score detail for a specific symbol."""
    if symbol.upper() == "SPCX":
        snap = deskpro_reader.read_snapshot()
        scores = snap.get("scores", {})
        vwap_data = snap.get("vwap_analysis", {})
        of_data = snap.get("orderflow_score", {})
        ow_data = snap.get("ownership_score", {})

        tr = _safe_int(scores.get("trade_ready", 0))
        if isinstance(scores.get("trade_ready"), float) and scores["trade_ready"] <= 1:
            tr = int(scores["trade_ready"] * 100)

        momentum = _safe_float(scores.get("momentum"))
        risk = _safe_float(scores.get("risk"))
        sm = _safe_int(scores.get("smart_money", 0))
        liq = _safe_int(scores.get("liquidity", 0))
        vwap_s = _safe_int(vwap_data.get("vwap_score")) if vwap_data else None
        of_s = of_data.get("score") if isinstance(of_data, dict) else None
        ow_s = ow_data.get("score") if isinstance(ow_data, dict) else None

        # Build voice-friendly one-liner
        parts = [f"SPCX trade_ready {tr}/100"]
        if vwap_s:
            parts.append(f"VWAP {vwap_s}")
        if of_s:
            parts.append(f"orderflow {of_s:.0f}")
        if risk:
            parts.append(f"risque {risk:.0f}%")
        one_line = ". ".join(parts)

        return {
            "symbol": "SPCX",
            "trade_ready": tr,
            "momentum": round(momentum, 3) if momentum else None,
            "risk": round(risk, 3) if risk else None,
            "smart_money": sm,
            "liquidity": liq,
            "vwap_score": vwap_s,
            "orderflow_score": round(of_s, 1) if of_s else None,
            "ownership_pressure_score": round(ow_s, 1) if ow_s else None,
            "probability": _safe_float(scores.get("probability", 0.5)),
            "one_line": one_line,
            "generated_at": _now(),
        }

    return {
        "symbol": symbol.upper(),
        "trade_ready": 0,
        "one_line": f"Scores non disponibles pour {symbol.upper()}",
        "generated_at": _now(),
    }


# ── /read/market ────────────────────────────────────────────────────────
@app.get("/read/market")
def read_market():
    """Market overview — all tracked symbols."""
    cc = deskpro_reader.read_command_center()
    snap = deskpro_reader.read_snapshot()

    symbols = []

    # SPCX
    spcx = {
        "symbol": "SPCX",
        "price": _safe_float(cc.get("price")),
        "vwap": cc.get("vwap"),
        "gap_ipo_pct": _safe_float(cc.get("gap_pct") or snap.get("gap_vs_ipo_pct")),
        "trade_ready": _safe_int(cc.get("trade_ready") or cc.get("edge_score", 0)),
        "trend": "bullish" if _safe_float(cc.get("gap_pct", 0)) > 1 else "bearish" if _safe_float(cc.get("gap_pct", 0)) < -1 else "neutral",
        "source_quality": snap.get("source_quality", {}).get("overall_tier", "unknown"),
    }
    symbols.append(spcx)

    one_line = f"SPCX a {spcx['price']:.1f}"
    if spcx.get("gap_ipo_pct"):
        one_line += f", gap IPO {spcx['gap_ipo_pct']:+.1f}%"
    one_line += f". Qualite source: {spcx['source_quality']}"

    return {
        "generated_at": _now(),
        "symbols": symbols,
        "top_setups": [],
        "active_alerts": [],
        "one_line": one_line,
    }


# ── /read/report ────────────────────────────────────────────────────────
@app.get("/read/report")
def read_report():
    """Daily report summary — voice-friendly."""
    cc = deskpro_reader.read_command_center()
    perf_s = perf_reader.read_summary()
    alerts = deskpro_reader.read_alerts(limit=3)
    snap = deskpro_reader.read_snapshot()

    scores = snap.get("scores", {})
    vwap = snap.get("vwap_analysis", {})

    summary_parts = [
        f"SPCX a {_safe_float(cc.get('price')):.1f}",
        f"VWAP {vwap.get('vwap_state', 'NO_DATA').lower()}",
        f"score VWAP {vwap.get('vwap_score', 0)}/100",
        f"trade_ready {_safe_int(scores.get('trade_ready', 0) * 100 if isinstance(scores.get('trade_ready'), float) and scores['trade_ready'] <= 1 else scores.get('trade_ready', 0))}/100",
    ]
    if cc.get("top_setup") and cc.get("top_setup") != "NONE":
        summary_parts.append(f"setup {cc['top_setup']} grade {cc.get('grade', '?')}")

    perf_one_line = ""
    if perf_s.get("total_trades"):
        perf_one_line = f"Perf: {perf_s.get('total_trades', 0)} trades, winrate {perf_s.get('winrate', 0)}%"

    alert_count = len(alerts.get("alerts", []))
    alert_one_line = ""
    if alert_count > 0:
        alert_one_line = f"{alert_count} alertes actives"

    one_line = ". ".join(summary_parts)
    if perf_one_line:
        one_line += ". " + perf_one_line
    if alert_one_line:
        one_line += ". " + alert_one_line

    return {
        "generated_at": _now(),
        "symbols": [{
            "symbol": "SPCX",
            "price": _safe_float(cc.get("price")),
            "trade_ready": _safe_int(scores.get("trade_ready", 0) * 100 if isinstance(scores.get("trade_ready"), float) and scores["trade_ready"] <= 1 else scores.get("trade_ready", 0)),
            "top_setup": cc.get("top_setup"),
            "grade": cc.get("grade", "reject"),
        }],
        "top_setups": [],
        "active_alerts": alerts.get("alerts", [])[:3],
        "one_line": one_line,
    }


# ── Health check ────────────────────────────────────────────────────────
@app.get("/health")
def health():
    return {"ok": True, "module": "voice_operator", "version": "0.1.0"}
