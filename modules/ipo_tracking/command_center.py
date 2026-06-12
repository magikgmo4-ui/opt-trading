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
    signals = snap.get("signals", [])

    price = indicators.get("close") or snap.get("price", 135)
    volume = indicators.get("volume")
    rel_vol = indicators.get("relative_volume")
    gap_pct = indicators.get("ipo_gap_pct") or 0
    vwap = indicators.get("vwap")
    rsi = indicators.get("rsi_14")

    is_open = price is not None and price != 135
    market_state = "OPEN" if is_open else "PRE_MARKET"

    # Pipeline health
    raw = read_json(REPO_ROOT / "data/ipo/spacex/raw/events.jsonl", [])
    if isinstance(raw, dict):
        raw = []
    sources_ok = len(set(e.get("source", "") for e in raw if e.get("ok")))
    sources_total = 5
    staleness = len(consensus.get("stale_sources", []))
    disagreement = consensus.get("source_disagreement_score", 0) or 0
    pipeline_healthy = staleness == 0 and sources_ok >= 3

    # Analog
    from .ipo_analogs import compute_analog_score
    analog = compute_analog_score({
        "gap_pct": gap_pct, "relative_volume": rel_vol or 1,
        "fvg_bullish": smart_money.get("fvg_bullish", False),
        "bos": smart_money.get("bos", False),
    })
    top_analogs = analog.get("top3", [])[:3]

    # Edge
    from .edge_engine import compute_setup_probabilities
    edge = compute_setup_probabilities(indicators, smart_money, consensus, scores, enriched, analog)
    edge_score = edge.get("edge_score", 0)
    best_setup = edge.get("best_setup", {})
    best_setup_name = best_setup.get("id", "NONE")
    best_setup_prob = best_setup.get("probability", 0)
    classification = edge.get("classification", "NO_TRADE")

    # Sector
    from .sector_intelligence import compute_sector_health
    sector_changes = {"RKLB": 2.5, "ASTS": 1.8, "RDW": -0.5, "LUNR": -1.2, "PL": 0.3,
                      "TSLA": 1.2, "NVDA": 3.1, "ARKX": 0.8, "UFO": 0.5, "QQQ": 0.5, "SPY": 0.3}
    sector_prices = {t: 100.0 for t in sector_changes}
    sector = compute_sector_health(sector_prices, sector_changes)
    sector_regime = sector.get("regime", "NEUTRAL")

    # Risk: why NOT trade
    risks = []
    if disagreement > 20:
        risks.append(f"High disagreement ({disagreement}%)")
    if staleness > 0:
        risks.append(f"{staleness} stale sources")
    if rel_vol and rel_vol < 0.5:
        risks.append("Weak volume")
    if edge_score < 50:
        risks.append(f"Low EDGE_SCORE ({int(edge_score*100)})")
    if sector_regime == "RISK_OFF":
        risks.append("Sector RISK_OFF")
    if not risks:
        risks.append("None")

    # Open score
    open_score = _compute_open_score(gap_pct, rel_vol, smart_money, edge_score)

    # Sector summary
    sector_summary = [f"RKLB  {'Strong' if sector_changes.get('RKLB',0)>1 else 'Neutral'}",
                      f"ASTS  {'Strong' if sector_changes.get('ASTS',0)>1 else 'Neutral'}",
                      f"RDW   {'Strong' if sector_changes.get('RDW',0)>1 else 'Neutral'}"]

    width = 52

    lines = []
    lines.append("=" * width)
    lines.append("")
    lines.append(f"  SPCX COMMAND CENTER")
    lines.append("")
    lines.append("-" * width)
    lines.append("")
    lines.append(f"  Pipeline      {'HEALTHY' if pipeline_healthy else 'DEGRADED':>12}")
    lines.append(f"  Market        {market_state:>12}")
    lines.append("")
    lines.append(f"  Price         {price:>12.2f}" if price else f"  Price         {'N/A':>12}")
    lines.append(f"  Volume        {_fmt_vol(volume):>12}" if volume else f"  Volume        {'N/A':>12}")
    lines.append(f"  Gap           {gap_pct:>+11.1f}%" if gap_pct else f"  Gap           {'N/A':>12}")
    lines.append(f"  VWAP          {vwap:>12.2f}" if vwap else f"  VWAP          {'N/A':>12}")
    lines.append(f"  RSI           {rsi:>12.1f}" if rsi else f"  RSI           {'N/A':>12}")
    lines.append("")
    lines.append(f"  OPEN_SCORE    {open_score:>12}")
    lines.append(f"  EDGE_SCORE    {int(edge_score*100):>12}")
    lines.append("")
    lines.append(f"  TOP_SETUP")
    lines.append(f"  {best_setup_name}")
    lines.append(f"  {int(best_setup_prob*100)}%")
    lines.append(f"  Confidence: {classification}")
    lines.append("")
    lines.append(f"  IPO ANALOGS")
    for i, a in enumerate(top_analogs):
        lines.append(f"  {i+1}. {a['symbol']:<5s} {int(analog.get('probabilities', {}).get(a['symbol'], 0)):>3d}%")
    lines.append("")
    lines.append(f"  SECTOR")
    lines.append(f"  {sector_regime}")
    for ss in sector_summary:
        lines.append(f"  {ss}")
    lines.append("")
    lines.append(f"  WHY NOT TRADE")
    for r in risks:
        lines.append(f"  {r}")
    lines.append("")
    lines.append(f"  ACTION")
    if classification == "NO_TRADE":
        lines.append(f"  NO TRADE")
    else:
        lines.append(f"  {classification} SETUP")
    lines.append("")
    lines.append("=" * width)

    return "\n".join(lines)


def command_center_json() -> dict[str, Any]:
    snap = read_json(REPO_ROOT / "data/ipo/spacex/scored/latest_snapshot.json", {})
    enriched = read_json(REPO_ROOT / "data/ipo/spacex/enriched/latest.json", {})
    indicators = enriched.get("indicators", {})
    smart_money = enriched.get("smart_money", {})
    consensus = enriched.get("consensus", {})
    scores = snap.get("scores", {})
    price = indicators.get("close") or snap.get("price", 135)
    gap_pct = indicators.get("ipo_gap_pct") or 0
    rel_vol = indicators.get("relative_volume")
    is_open = price is not None and price != 135

    from .ipo_analogs import compute_analog_score
    analog = compute_analog_score({"gap_pct": gap_pct, "relative_volume": rel_vol or 1, "fvg_bullish": smart_money.get("fvg_bullish", False), "bos": smart_money.get("bos", False)})
    from .edge_engine import compute_setup_probabilities
    edge = compute_setup_probabilities(indicators, smart_money, consensus, scores, enriched, analog)
    from .sector_intelligence import compute_sector_health
    sector_changes = {"RKLB": 2.5, "ASTS": 1.8, "RDW": -0.5, "TSLA": 1.2, "NVDA": 3.1, "QQQ": 0.5, "SPY": 0.3}
    sector = compute_sector_health({t: 100.0 for t in sector_changes}, sector_changes)

    staleness = len(consensus.get("stale_sources", []))
    disagreement = consensus.get("source_disagreement_score", 0) or 0

    risks = []
    if disagreement > 20: risks.append("high_disagreement")
    if staleness > 0: risks.append("stale_sources")
    if edge.get("edge_score", 0) < 0.5: risks.append("low_edge")
    if sector.get("regime") == "RISK_OFF": risks.append("sector_risk_off")

    return {
        "generated_at": utc_now(),
        "market_state": "OPEN" if is_open else "PRE_MARKET",
        "pipeline_healthy": staleness == 0,
        "price": price,
        "volume": indicators.get("volume"),
        "gap_pct": gap_pct,
        "vwap": indicators.get("vwap"),
        "rsi": indicators.get("rsi_14"),
        "open_score": _compute_open_score(gap_pct, rel_vol, smart_money, edge.get("edge_score", 0)),
        "edge_score": round(edge.get("edge_score", 0) * 100),
        "top_setup": edge.get("best_setup", {}).get("id"),
        "top_setup_prob_pct": round(edge.get("best_setup", {}).get("probability", 0) * 100),
        "classification": edge.get("classification"),
        "ipo_analogs": [{"symbol": a["symbol"], "probability_pct": int(analog.get("probabilities", {}).get(a["symbol"], 0))} for a in analog.get("top3", [])[:3]],
        "sector_regime": sector.get("regime"),
        "risks": risks,
        "action": "NO_TRADE" if edge.get("classification") == "NO_TRADE" else f"{edge.get('classification')}_SETUP",
    }


def _compute_open_score(gap_pct: float, rel_vol: float | None, smc: dict, edge: float) -> int:
    score = 50
    if gap_pct and gap_pct > 5: score += 15
    if gap_pct and gap_pct > 2: score += 10
    if rel_vol and rel_vol > 1.5: score += 10
    if rel_vol and rel_vol > 1.0: score += 5
    if smc.get("fvg_bullish"): score += 5
    if smc.get("bos"): score += 10
    score += int(edge * 10)
    return min(100, max(0, score))


def _fmt_vol(v: float | None) -> str:
    if v is None: return "N/A"
    if v >= 1_000_000: return f"{v/1_000_000:.1f}M"
    if v >= 1_000: return f"{v/1_000:.0f}K"
    return str(int(v))
