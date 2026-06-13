"""
SPCX News Sentiment Analyzer
GO_SPACEX_MACRO_SENTIMENT_AND_DERIVATIVES_DATA_01

Dedup, polarity classification, analyst tracking, catalyst decay, sector halo.
No LLM required — keyword-based classification.
"""
from __future__ import annotations
import json, re, os
from pathlib import Path
from datetime import datetime, timezone
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[3]

BULLISH_KEYWORDS = [
    "surge", "soar", "jump", "rally", "record", "breakout", "bullish",
    "upgrade", "outperform", "buy", "overweight", "strong buy",
    "beat", "exceed", "raise target", "raised", "growth", "momentum",
    "buyback", "accumulate", "demand", "expansion", "partnership",
    "contract win", "approval", "breakthrough", "launch success",
    "subscriber growth", "revenue beat", "profit", "positive",
]

BEARISH_KEYWORDS = [
    "plunge", "tumble", "crash", "drop", "decline", "bearish", "sell-off",
    "downgrade", "underperform", "sell", "underweight", "strong sell",
    "miss", "below", "cut target", "lowered", "risk", "concern",
    "warning", "caution", "overvalued", "bubble", "dilution",
    "lockup expiry", "insider sell", "probe", "investigation",
    "lawsuit", "fine", "penalty", "delay", "failure",
    "loss", "negative", "weak", "slowdown", "headwind",
]

REASON_TAGS = {
    "IPO_DEMAND": ["ipo", "debut", "listing", "first day", "open", "priced", "subscription"],
    "VALUATION": ["valuation", "trillion", "billion", "market cap", "overvalued", "undervalued", "worth"],
    "STARLINK": ["starlink", "satellite", "broadband", "subscriber", "internet"],
    "REGULATORY": ["sec", "regulation", "regulatory", "filing", "compliance", "approval", "license"],
    "CONTRACT": ["contract", "nasa", "dod", "defense", "military", "space force", "award"],
    "ANALYST": ["analyst", "upgrade", "downgrade", "target", "rating", "initiate", "coverage"],
    "RETAIL_HYPE": ["reddit", "wallstreetbets", "meme", "retail", "social media", "viral"],
    "TECHNICAL": ["vwap", "resistance", "support", "breakout", "volume", "volatility", "range"],
    "COMPETITOR": ["rklb", "rocket lab", "blue origin", "virgin galactic", "astra", "competitor"],
    "MACRO": ["fed", "interest rate", "inflation", "gdp", "recession", "yield", "treasury"],
}


def dedup_headlines(articles: list[dict]) -> tuple[list[dict], int]:
    """Group similar headlines by word overlap. Returns deduped list + cluster count."""
    if not articles:
        return [], 0

    clusters = []
    used = set()

    for i, a1 in enumerate(articles):
        if i in used:
            continue
        t1 = set(re.findall(r"\w+", a1.get("title", "").lower()))
        if len(t1) < 3:
            used.add(i)
            continue

        cluster = [a1]
        for j, a2 in enumerate(articles):
            if j <= i or j in used:
                continue
            t2 = set(re.findall(r"\w+", a2.get("title", "").lower()))
            if len(t2) < 3:
                continue
            overlap = len(t1 & t2) / min(len(t1), len(t2))
            if overlap > 0.5:
                cluster.append(a2)
                used.add(j)

        used.add(i)
        canonical = max(cluster, key=lambda a: len(a.get("title", "")))
        clusters.append({
            "canonical_title": canonical.get("title", ""),
            "duplicate_count": len(cluster),
            "sources": list(set(a.get("link", "")[:60] for a in cluster)),
            "first_seen": min((a.get("published_at", "") for a in cluster), default=""),
        })

    return clusters, len(clusters)


def classify_sentiment(title: str) -> dict[str, Any]:
    """Keyword-based sentiment polarity."""
    text = title.lower()
    bullish_hits = sum(1 for kw in BULLISH_KEYWORDS if kw in text)
    bearish_hits = sum(1 for kw in BEARISH_KEYWORDS if kw in text)

    if bullish_hits > bearish_hits:
        polarity = "bullish"
        confidence = min(0.9, 0.5 + bullish_hits * 0.1)
    elif bearish_hits > bullish_hits:
        polarity = "bearish"
        confidence = min(0.9, 0.5 + bearish_hits * 0.1)
    else:
        polarity = "neutral"
        confidence = 0.3

    # Reason tags
    tags = []
    for tag, keywords in REASON_TAGS.items():
        if any(kw in text for kw in keywords):
            tags.append(tag)

    return {
        "polarity": polarity,
        "confidence": round(confidence, 2),
        "bullish_keywords": bullish_hits,
        "bearish_keywords": bearish_hits,
        "reason_tags": tags[:3],
    }


def compute_catalyst_decay(filing_date: str | None = None) -> float:
    """Decay catalyst score based on age. IPO day = 1.0, decays over days."""
    if not filing_date:
        return 0.5
    try:
        dt = datetime.fromisoformat(filing_date.replace("Z", "+00:00"))
        age_hours = (datetime.now(timezone.utc) - dt).total_seconds() / 3600
        if age_hours < 2:
            return 1.0
        elif age_hours < 6:
            return 0.8
        elif age_hours < 24:
            return 0.6
        elif age_hours < 72:
            return 0.4
        else:
            return 0.2
    except (ValueError, TypeError):
        return 0.5


def analyze_spcx_news(articles: list[dict], sec_filing_date: str | None = None) -> dict[str, Any]:
    """Full SPCX news sentiment analysis."""
    clusters, cluster_count = dedup_headlines(articles)

    sentiments = []
    bullish_count = 0
    bearish_count = 0
    neutral_count = 0

    for cl in clusters:
        s = classify_sentiment(cl["canonical_title"])
        s["title"] = cl["canonical_title"][:120]
        s["duplicate_count"] = cl["duplicate_count"]
        sentiments.append(s)
        if s["polarity"] == "bullish":
            bullish_count += 1
        elif s["polarity"] == "bearish":
            bearish_count += 1
        else:
            neutral_count += 1

    # Overall sentiment
    if bullish_count > bearish_count and bullish_count > neutral_count:
        overall_polarity = "bullish"
    elif bearish_count > bullish_count and bearish_count > neutral_count:
        overall_polarity = "bearish"
    else:
        overall_polarity = "mixed"

    catalyst_decay = compute_catalyst_decay(sec_filing_date)

    return {
        "schema": "spacex_news_sentiment_v1",
        "symbol": "SPCX",
        "analyzed_at": datetime.now(timezone.utc).isoformat(),
        "headline_count": len(articles),
        "cluster_count": cluster_count,
        "dedup_ratio": round(cluster_count / max(1, len(articles)), 2),
        "sentiment": {
            "overall_polarity": overall_polarity,
            "bullish_count": bullish_count,
            "bearish_count": bearish_count,
            "neutral_count": neutral_count,
            "clusters": sentiments,
        },
        "catalyst": {
            "ipo_day": True,
            "filing_date": sec_filing_date,
            "catalyst_decay": catalyst_decay,
            "catalyst_score_adjusted": round(1.0 * catalyst_decay, 2),
        },
        "analysts": {
            "coverage_count": 0,
            "rating_consensus": "unknown",
            "price_target_mean": None,
            "note": "Analyst coverage not yet available for IPO day-1",
        },
    }


def analyze_sector_halo() -> dict[str, Any]:
    """Extract sector halo from existing DOM captures of comparables."""
    vision_dir = REPO_ROOT / "data" / "vision_inbox"
    if not vision_dir.exists():
        return {"available": False, "error": "vision_inbox not found"}

    comparables = {}
    targets = {
        "RKLB": "rklb", "ASTS": "asts", "LUNR": "lunr",
        "RDW": "rdw", "TSLA": "tsla", "QQQ": "qqq", "ARKX": "arkx",
    }

    for sym, pattern in targets.items():
        for f in sorted(vision_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True):
            if pattern in f.name.lower() and f.suffix == ".json":
                try:
                    data = json.loads(f.read_text())
                    dom = data.get("dom_extracted", {})
                    if dom and isinstance(dom, dict):
                        comparables[sym] = {
                            "close": dom.get("close"),
                            "open": dom.get("open"),
                            "high": dom.get("high"),
                            "low": dom.get("low"),
                            "volume": dom.get("volume"),
                            "captured_at": str(datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)),
                        }
                except Exception:
                    pass
                break

    return {
        "available": len(comparables) > 0,
        "comparable_count": len(comparables),
        "comparables": comparables,
    }
