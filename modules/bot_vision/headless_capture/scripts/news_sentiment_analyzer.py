#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from random import Random

REPO_ROOT = Path(__file__).resolve().parents[4]

NEWS_SOURCES = ["coindesk", "cointelegraph", "theblock"]

_STUB_HEADLINES: dict[str, list[dict[str, Any]]] = {
    "coindesk": [
        {"headline": "Bitcoin Holds Above $65K as ETF Inflows Resume", "sentiment": "positive", "score": 0.65, "topics": ["bitcoin", "etf"]},
        {"headline": "Ethereum Layer 2 Activity Reaches All-Time High", "sentiment": "positive", "score": 0.72, "topics": ["ethereum", "layer2"]},
        {"headline": "Regulatory Clarity Advances in US Crypto Framework", "sentiment": "positive", "score": 0.58, "topics": ["regulation", "us"]},
        {"headline": "DeFi TVL Rebounds to $85B After 3-Month Slump", "sentiment": "positive", "score": 0.62, "topics": ["defi", "tvl"]},
        {"headline": "Crypto Market Cap Adds $120B in Weekly Rally", "sentiment": "positive", "score": 0.70, "topics": ["market", "rally"]},
    ],
    "cointelegraph": [
        {"headline": "Bitcoin Mining Difficulty Adjusts Upward 3.5%", "sentiment": "neutral", "score": 0.10, "topics": ["bitcoin", "mining"]},
        {"headline": "Solana Overtakes BNB in Daily Active Addresses", "sentiment": "positive", "score": 0.68, "topics": ["solana", "bnb"]},
        {"headline": "Stablecoin Supply Expands to $160B, Signaling Liquidity", "sentiment": "positive", "score": 0.55, "topics": ["stablecoin", "liquidity"]},
        {"headline": "Fed Rate Decision Looms, Crypto Traders Cautious", "sentiment": "negative", "score": -0.35, "topics": ["fed", "rates"]},
        {"headline": "Institutional Custody Demand Surges 40% YoY", "sentiment": "positive", "score": 0.60, "topics": ["institutional", "custody"]},
    ],
    "theblock": [
        {"headline": "BTC Options Open Interest Hits Record $22B", "sentiment": "positive", "score": 0.75, "topics": ["bitcoin", "options"]},
        {"headline": "Crypto VC Funding Reaches $2.8B in Q2 2026", "sentiment": "positive", "score": 0.65, "topics": ["vc", "funding"]},
        {"headline": "Exchange Reserves Drop to Multi-Year Low", "sentiment": "positive", "score": 0.62, "topics": ["exchange", "reserves"]},
        {"headline": "On-Chain Metrics Show Accumulation Pattern", "sentiment": "positive", "score": 0.70, "topics": ["onchain", "accumulation"]},
        {"headline": "Derivatives Market Open Interest Exceeds $60B", "sentiment": "neutral", "score": 0.15, "topics": ["derivatives", "oi"]},
    ],
}


def _stub_for_source(source: str) -> list[dict[str, Any]]:
    return _STUB_HEADLINES.get(source, _STUB_HEADLINES["coindesk"])


_VALID_SOURCES = set(NEWS_SOURCES)


def analyze(
    sidecar: dict[str, Any] | None = None,
    sources: list[str] | None = None,
) -> dict[str, Any]:
    if sources is None:
        sources = NEWS_SOURCES

    articles: list[dict[str, Any]] = []
    all_scores: list[float] = []

    rand = Random(42)

    for source in sources:
        if source not in _VALID_SOURCES:
            continue

        stubs = _stub_for_source(source)
        for article in stubs:
            articles.append({
                "source": source,
                "headline": article["headline"],
                "sentiment": article["sentiment"],
                "score": article["score"],
                "topics": article["topics"],
                "published_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "fetch_method": "stub",
                "confidence": round(0.70 + rand.random() * 0.20, 2),
            })
            all_scores.append(article["score"])

    avg_sentiment = round(sum(all_scores) / len(all_scores), 3) if all_scores else 0.0
    positive = sum(1 for s in all_scores if s > 0.3)
    neutral = sum(1 for s in all_scores if -0.3 <= s <= 0.3)
    negative = sum(1 for s in all_scores if s < -0.3)

    return {
        "input_class": "vision_context.news_sentiment.v1",
        "source_id": "news_sentiment_headless_bot",
        "analysis_ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "freshness_state": "fresh",
        "sources_fetched": sources,
        "article_count": len(articles),
        "articles": articles,
        "aggregate": {
            "average_sentiment_score": avg_sentiment,
            "sentiment_label": "positive" if avg_sentiment > 0.3 else "negative" if avg_sentiment < -0.3 else "neutral",
            "positive_count": positive,
            "neutral_count": neutral,
            "negative_count": negative,
            "dominant_topics": list({t for a in articles for t in a.get("topics", [])}),
        },
        "refs": {
            "sources": sources,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="News sentiment analyzer for crypto news aggregation")
    ap.add_argument("--sources", nargs="*", default=NEWS_SOURCES, help=f"News sources (default: {' '.join(NEWS_SOURCES)})")
    ap.add_argument("--stdin", action="store_true", help="Read params from stdin (future)")
    args = ap.parse_args()

    result = analyze(sources=args.sources if args.sources else NEWS_SOURCES)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
