from __future__ import annotations
from typing import Any
from .io import utc_now, read_json, REPO_ROOT


def render_command_center() -> str:
    snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
    enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})

    indicators = enriched.get("indicators", {})
    smart_money = enriched.get("smart_money", {})
    consensus = enriched.get("consensus", {})
    scores = snap.get("scores", {})

    price = indicators.get("close") or snap.get("price", 135)
    volume = indicators.get("volume")
    gap_pct = indicators.get("ipo_gap_pct") or 0
    rel_vol = indicators.get("relative_volume")
    vwap = indicators.get("vwap")
    rsi = indicators.get("rsi_14")
    atr = indicators.get("atr_14")
    bb_lower = indicators.get("bb_lower")
    bb_middle = indicators.get("bb_middle")
    ipo_price = snap.get("ipo_price", 135)

    is_open = price is not None and price != 135 and price != ipo_price
    market_state = "OPEN" if is_open else "PRE_MARKET"

    staleness = len(consensus.get("stale_sources", []))
    disagreement = consensus.get("source_disagreement_score", 0) or 0
    sources_ok = 5 - staleness

    from .ipo_analogs import compute_analog_score
    analog = compute_analog_score({
        "gap_pct": gap_pct, "relative_volume": rel_vol or 1,
        "fvg_bullish": smart_money.get("fvg_bullish", False),
        "bos": smart_money.get("bos", False),
    })
    top_analogs = analog.get("top3", [])[:3]
    analog_top = top_analogs[0]["symbol"] if top_analogs else "NONE"
    analog_consensus = analog.get("analog_consensus", {})

    from .edge_engine import compute_setup_probabilities
    edge = compute_setup_probabilities(indicators, smart_money, consensus, scores, enriched, analog)
    edge_score = int(edge.get("edge_score", 0) * 100)
    best_setup = edge.get("best_setup", {})
    classification = edge.get("classification", "NO_TRADE")
    probs = edge.get("setup_probabilities", {})

    from .sector_intelligence import compute_sector_health
    sector_changes = {"RKLB": 2.5, "ASTS": 1.8, "RDW": -0.5, "LUNR": -1.2, "TSLA": 1.2, "NVDA": 3.1, "QQQ": 0.5, "SPY": 0.3}
    sector = compute_sector_health({t: 100.0 for t in sector_changes}, sector_changes)
    sector_regime = sector.get("regime", "NEUTRAL")

    # Compute realistic open score
    open_score = 50
    if gap_pct and gap_pct > 10: open_score += 20
    elif gap_pct and gap_pct > 5: open_score += 15
    elif gap_pct and gap_pct > 2: open_score += 10
    elif gap_pct and abs(gap_pct) < 2: open_score += 0
    if rel_vol and rel_vol > 2: open_score += 15
    elif rel_vol and rel_vol > 1.2: open_score += 8
    if smart_money.get("fvg_bullish"): open_score += 8
    if smart_money.get("bos"): open_score += 7
    if sector_regime == "RISK_ON": open_score += 5
    open_score = min(100, max(0, open_score))

    # WHY_NOT_TRADE
    risks = []
    if disagreement > 20:
        risks.append("High disagreement ({:.0f}%)".format(disagreement))
    if staleness > 0:
        risks.append(f"{staleness} stale sources")
    if rel_vol is not None and rel_vol < 0.5:
        risks.append("Weak volume")
    if edge_score < 60:
        risks.append("Low edge")
    if sector_regime == "RISK_OFF":
        risks.append("Sector risk off")
    if price and ipo_price and abs(price - ipo_price) / max(1, ipo_price) > 0.5:
        risks.append("Extreme gap")
    if not risks:
        risks.append("None")

    # Consensus label
    if disagreement < 5:
        consensus_label = "STRONG"
    elif disagreement < 15:
        consensus_label = "MODERATE"
    else:
        consensus_label = "WEAK"

    # Entry/Stop/TP estimation
    entry = price
    if atr and entry:
        stop = round(entry - atr * 1.5, 2)
        tp1 = round(entry + atr * 2.0, 2)
        tp2 = round(entry + atr * 3.5, 2)
    else:
        stop = round(entry * 0.98, 2) if entry else None
        tp1 = round(entry * 1.02, 2) if entry else None
        tp2 = round(entry * 1.04, 2) if entry else None

    W = 48
    L = []
    L.append("=" * W)
    L.append("")
    L.append(f"  SPCX COMMAND CENTER")
    L.append("")

    # Bloc 1 — Decision (always first)
    L.append(f"  ACTION          {classification + ' SETUP' if classification != 'NO_TRADE' else 'NO TRADE'}")
    L.append(f"  CONFIDENCE      {classification}")
    edge_bar = "\u2588" * (edge_score // 5) + "\u2591" * (20 - edge_score // 5)
    L.append(f"  EDGE SCORE      {edge_score}  [{edge_bar}]")
    L.append("")

    # Bloc 2 — Market
    L.append(f"  PRICE           {price:.2f}" if price else f"  PRICE           N/A")
    L.append(f"  VOLUME          {_fmt_vol(volume):>10}" if volume else f"  VOLUME          N/A")
    L.append(f"  GAP             {gap_pct:+.1f}%" if gap_pct is not None else f"  GAP             N/A")
    L.append(f"  VWAP            {vwap:.2f}" if vwap else f"  VWAP            N/A")
    L.append("")

    # Bloc 3 — Why
    L.append(f"  OPEN_SCORE      {open_score}")
    L.append(f"  Sector          {sector_regime}")
    L.append(f"  Consensus       {consensus_label}")
    L.append(f"  Analog          {analog_top}-LIKE")
    L.append("")

    # Bloc 4 — Top Setup
    best_prob = best_setup.get("probability", 0)
    L.append(f"  TOP_SETUP")
    L.append(f"  {best_setup.get('id', 'NONE')}")
    L.append(f"  Probability     {int(best_prob*100)}%")
    if classification != "NO_TRADE":
        L.append(f"  Entry           {entry:.2f}" if entry else "  Entry           N/A")
        L.append(f"  Stop            {stop:.2f}" if stop else "  Stop            N/A")
        L.append(f"  TP1             {tp1:.2f}" if tp1 else "  TP1             N/A")
        L.append(f"  TP2             {tp2:.2f}" if tp2 else "  TP2             N/A")
    L.append("")

    # Bloc 5 — Analogs
    L.append(f"  IPO_ANALOGS")
    for i, a in enumerate(top_analogs):
        L.append(f"  {i+1}. {a['symbol']:<5s} {int(analog.get('probabilities', {}).get(a['symbol'], 0)):>3d}%")
    L.append("")

    # Bloc 6 — Sector
    L.append(f"  SECTOR           {sector_regime}")

    # Bloc 7 — Why Not Trade
    L.append("")
    L.append(f"  WHY_NOT_TRADE")
    for r in risks:
        L.append(f"  {r}")
    L.append("")

    # Bloc 8 — Pipeline health
    L.append(f"  PIPELINE         {'HEALTHY' if staleness == 0 else 'DEGRADED'}")
    L.append(f"  Sources          {sources_ok}/5")
    L.append(f"  Disagreement     {disagreement:.1f}%")
    L.append("")
    L.append("=" * W)

    return "\n".join(L)


def command_center_json() -> dict[str, Any]:
    snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
    enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
    indicators = enriched.get("indicators", {})
    smart_money = enriched.get("smart_money", {})
    consensus = enriched.get("consensus", {})
    price = indicators.get("close") or snap.get("price", 135)
    gap_pct = indicators.get("ipo_gap_pct") or 0
    is_open = price is not None and price != 135

    from .ipo_analogs import compute_analog_score
    analog = compute_analog_score({"gap_pct": gap_pct, "relative_volume": indicators.get("relative_volume") or 1, "fvg_bullish": smart_money.get("fvg_bullish", False), "bos": smart_money.get("bos", False)})
    from .edge_engine import compute_setup_probabilities
    edge = compute_setup_probabilities(indicators, smart_money, consensus, snap.get("scores", {}), enriched, analog)
    from .sector_intelligence import compute_sector_health
    sector = compute_sector_health({"RKLB": 100.0}, {"RKLB": 2.5})

    staleness = len(consensus.get("stale_sources", []))
    risks = []
    if consensus.get("source_disagreement_score", 0) > 20: risks.append("high_disagreement")
    if staleness > 0: risks.append("stale")
    if edge.get("edge_score", 0) < 0.5: risks.append("low_edge")

    return {
        "generated_at": utc_now(),
        "market_state": "OPEN" if is_open else "PRE_MARKET",
        "action": "NO_TRADE" if edge.get("classification") == "NO_TRADE" else f"{edge.get('classification')}_SETUP",
        "confidence": edge.get("classification"),
        "edge_score": round(edge.get("edge_score", 0) * 100),
        "price": price,
        "volume": indicators.get("volume"),
        "gap_pct": gap_pct,
        "vwap": indicators.get("vwap"),
        "rsi": indicators.get("rsi_14"),
        "top_setup": edge.get("best_setup", {}).get("id"),
        "top_setup_prob_pct": round(edge.get("best_setup", {}).get("probability", 0) * 100),
        "ipo_analogs": [{"symbol": a["symbol"], "pct": int(analog.get("probabilities", {}).get(a["symbol"], 0))} for a in analog.get("top3", [])[:3]],
        "sector_regime": sector.get("regime"),
        "pipeline_healthy": staleness == 0,
        "sources_ok": 5 - staleness,
        "disagreement": consensus.get("source_disagreement_score", 0),
        "risks": risks,
    }


def _fmt_vol(v: float | None) -> str:
    if v is None: return "N/A"
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.0f}K"
    return f"{v:.0f}"


def _compute_open_score(gap_pct: float, rel_vol: float | None, smc: dict, edge: float) -> int:
    score = 50
    if gap_pct and gap_pct > 5: score += 15
    elif gap_pct and gap_pct > 2: score += 10
    if rel_vol and rel_vol > 1.5: score += 10
    elif rel_vol and rel_vol > 1.0: score += 5
    if smc.get("fvg_bullish"): score += 5
    if smc.get("bos"): score += 10
    score += int(edge * 10)
    return min(100, max(0, score))
