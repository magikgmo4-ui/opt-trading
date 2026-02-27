from __future__ import annotations
from datetime import datetime, timezone
from modules.desk_pro.models import DeskForm, Snapshot, ScoreResult, ScoreReason

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _sr_summary(form: DeskForm):
    out = {"W_S": [], "W_R": [], "D_S": [], "D_R": []}
    for x in form.sr:
        out[f"{x.tf}_{x.kind}"].append(float(x.level))
    for k in out:
        out[k] = sorted(out[k])
    return out

def compute_probability(form: DeskForm, snap: Snapshot) -> ScoreResult:
    # Step-2: simple explainable scoring stub (will be calibrated later).
    score = 0.0
    reasons: list[ScoreReason] = []

    if form.bias == "bull":
        score += 0.15; reasons.append(ScoreReason(code="BIAS_BULL", weight=0.15, detail="Form bias bull"))
    elif form.bias == "bear":
        score -= 0.15; reasons.append(ScoreReason(code="BIAS_BEAR", weight=-0.15, detail="Form bias bear"))

    if form.vol_regime == "high":
        score -= 0.05; reasons.append(ScoreReason(code="VOL_HIGH", weight=-0.05, detail="High volatility regime"))
    elif form.vol_regime == "low":
        score += 0.03; reasons.append(ScoreReason(code="VOL_LOW", weight=0.03, detail="Low volatility regime"))

    def flow(code_in: str, code_out: str, v):
        nonlocal score
        if v == "in":
            score += 0.10; reasons.append(ScoreReason(code=code_in, weight=0.10, detail="Flow IN"))
        elif v == "out":
            score -= 0.10; reasons.append(ScoreReason(code=code_out, weight=-0.10, detail="Flow OUT"))

    flow("ETF_IN", "ETF_OUT", form.etf_flow_bias)
    flow("ONCHAIN_IN", "ONCHAIN_OUT", form.onchain_flow_bias)
    flow("FUTURES_IN", "FUTURES_OUT", form.futures_flow_bias)

    if form.funding_bias == "pos":
        score -= 0.04; reasons.append(ScoreReason(code="FUNDING_POS", weight=-0.04, detail="Funding positive (crowded longs)"))
    elif form.funding_bias == "neg":
        score += 0.04; reasons.append(ScoreReason(code="FUNDING_NEG", weight=0.04, detail="Funding negative (crowded shorts)"))

    if form.fear_greed is not None:
        if form.fear_greed <= 25:
            score += 0.06; reasons.append(ScoreReason(code="FEAR", weight=0.06, detail=f"Fear&Greed={form.fear_greed}"))
        elif form.fear_greed >= 75:
            score -= 0.06; reasons.append(ScoreReason(code="GREED", weight=-0.06, detail=f"Fear&Greed={form.fear_greed}"))

    if form.dxy_trend == "up":
        score -= 0.04; reasons.append(ScoreReason(code="DXY_UP", weight=-0.04, detail="DXY up = headwind"))
    elif form.dxy_trend == "down":
        score += 0.04; reasons.append(ScoreReason(code="DXY_DOWN", weight=0.04, detail="DXY down = tailwind"))

    if form.corr_xau_btc is not None and form.corr_xau_btc >= 0.6 and form.vol_regime == "high":
        score -= 0.02; reasons.append(ScoreReason(code="CORR_HIGH_VOL", weight=-0.02, detail="High XAU/BTC corr under high vol"))

    prob = 0.5 + max(-0.45, min(0.45, score))

    return ScoreResult(
        ts_iso=now_iso(),
        symbol=form.symbol,
        probability=prob,
        score=score,
        reasons=reasons,
        sr_summary=_sr_summary(form),
    )
