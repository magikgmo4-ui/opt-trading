#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from random import Random
from typing import Any
from urllib.error import URLError
from urllib.request import Request, urlopen

REPO_ROOT = Path(__file__).resolve().parents[4]

NEWS_SOURCES = ["coindesk", "cointelegraph", "theblock"]
FEED_URLS = {
    "coindesk": "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "cointelegraph": "https://cointelegraph.com/rss",
    "theblock": "https://www.theblock.co/rss.xml",
}

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

_VALID_SOURCES = set(NEWS_SOURCES)
_POSITIVE_KEYWORDS = {
    "resume", "surge", "record", "rebound", "clarity", "approval", "adoption", "growth",
    "inflow", "high", "accumulation", "bullish", "expands", "overtakes", "rally",
}
_NEGATIVE_KEYWORDS = {
    "slump", "cautious", "decline", "drops", "selloff", "outflow", "hack", "lawsuit",
    "bearish", "crash", "delay", "ban", "risk", "pressure",
}


def _utc_now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def _stub_for_source(source: str) -> list[dict[str, Any]]:
    return _STUB_HEADLINES.get(source, _STUB_HEADLINES["coindesk"])


def _infer_topics(headline: str) -> list[str]:
    text = headline.lower()
    topic_map = {
        "bitcoin": ["bitcoin", "btc", "etf", "mining", "options"],
        "ethereum": ["ethereum", "eth", "layer 2", "layer2"],
        "regulation": ["regulation", "sec", "framework", "lawsuit", "ban"],
        "defi": ["defi", "tvl", "yield"],
        "liquidity": ["liquidity", "stablecoin", "reserve", "reserves"],
        "macro": ["fed", "rates", "inflation", "macro"],
        "derivatives": ["derivatives", "options", "open interest", "oi", "funding"],
        "institutional": ["institutional", "custody", "etf", "inflows"],
    }
    topics = [topic for topic, keywords in topic_map.items() if any(keyword in text for keyword in keywords)]
    return topics or ["general"]


def _score_headline(headline: str) -> float:
    text = headline.lower()
    score = 0.0
    for keyword in _POSITIVE_KEYWORDS:
        if keyword in text:
            score += 0.18
    for keyword in _NEGATIVE_KEYWORDS:
        if keyword in text:
            score -= 0.18
    return round(max(min(score, 0.9), -0.9), 2)


def _sentiment_label(score: float) -> str:
    if score > 0.3:
        return "positive"
    if score < -0.3:
        return "negative"
    return "neutral"


def _fetch_feed_xml(source: str, timeout_seconds: int = 5) -> str | None:
    url = FEED_URLS.get(source)
    if not url:
        return None
    req = Request(url, headers={"User-Agent": "opt-trading-bot-vision/1.0"})
    try:
        with urlopen(req, timeout=timeout_seconds) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except (URLError, TimeoutError, ValueError):
        return None


def _extract_feed_articles(source: str, xml_text: str, limit: int = 5) -> list[dict[str, Any]]:
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError:
        return []

    items = root.findall(".//item")
    entries = root.findall(".//{http://www.w3.org/2005/Atom}entry")
    nodes = items if items else entries
    articles: list[dict[str, Any]] = []

    for node in nodes[:limit]:
        title_node = node.find("title") or node.find("{http://www.w3.org/2005/Atom}title")
        if title_node is None or not (title_node.text or "").strip():
            continue
        headline = (title_node.text or "").strip()
        published_node = (
            node.find("pubDate")
            or node.find("published")
            or node.find("updated")
            or node.find("{http://www.w3.org/2005/Atom}published")
            or node.find("{http://www.w3.org/2005/Atom}updated")
        )
        score = _score_headline(headline)
        articles.append({
            "source": source,
            "headline": headline,
            "sentiment": _sentiment_label(score),
            "score": score,
            "topics": _infer_topics(headline),
            "published_at": (published_node.text or _utc_now_iso()).strip() if published_node is not None else _utc_now_iso(),
            "fetch_method": "rss",
            "confidence": 0.82,
        })
    return articles


def _fetch_live_articles(source: str, limit: int = 5) -> list[dict[str, Any]]:
    xml_text = _fetch_feed_xml(source)
    if not xml_text:
        return []
    return _extract_feed_articles(source, xml_text, limit=limit)


def analyze(
    sidecar: dict[str, Any] | None = None,
    sources: list[str] | None = None,
    prefer_live: bool = True,
    max_articles_per_source: int = 5,
) -> dict[str, Any]:
    if sources is None:
        sources = NEWS_SOURCES

    articles: list[dict[str, Any]] = []
    all_scores: list[float] = []
    live_hits = 0
    valid_sources = [source for source in sources if source in _VALID_SOURCES]
    rand = Random(42)

    for source in sources:
        if source not in _VALID_SOURCES:
            continue

        source_articles = _fetch_live_articles(source, limit=max_articles_per_source) if prefer_live else []
        if source_articles:
            live_hits += 1
            articles.extend(source_articles)
            all_scores.extend(float(article["score"]) for article in source_articles)
            continue

        for article in _stub_for_source(source)[:max_articles_per_source]:
            articles.append({
                "source": source,
                "headline": article["headline"],
                "sentiment": article["sentiment"],
                "score": article["score"],
                "topics": article["topics"],
                "published_at": _utc_now_iso(),
                "fetch_method": "stub",
                "confidence": round(0.70 + rand.random() * 0.20, 2),
            })
            all_scores.append(article["score"])

    avg_sentiment = round(sum(all_scores) / len(all_scores), 3) if all_scores else 0.0
    positive = sum(1 for s in all_scores if s > 0.3)
    neutral = sum(1 for s in all_scores if -0.3 <= s <= 0.3)
    negative = sum(1 for s in all_scores if s < -0.3)
    if live_hits == len(valid_sources) and live_hits > 0:
        fetch_mode = "live"
    elif live_hits > 0:
        fetch_mode = "mixed"
    else:
        fetch_mode = "stub"

    return {
        "input_class": "vision_context.news_sentiment.v1",
        "source_id": "news_sentiment_headless_bot",
        "analysis_ts": _utc_now_iso(),
        "freshness_state": "fresh",
        "sources_fetched": sources,
        "article_count": len(articles),
        "articles": articles,
        "aggregate": {
            "average_sentiment_score": avg_sentiment,
            "sentiment_label": _sentiment_label(avg_sentiment),
            "positive_count": positive,
            "neutral_count": neutral,
            "negative_count": negative,
            "dominant_topics": list({t for a in articles for t in a.get("topics", [])}),
        },
        "refs": {
            "capture_source": str((sidecar or {}).get("source", "news_sentiment_headless")),
            "image_ref": str((sidecar or {}).get("png_path") or (sidecar or {}).get("output_png") or ""),
            "sources": sources,
            "feed_urls": {source: FEED_URLS[source] for source in sources if source in FEED_URLS},
            "fetch_mode": fetch_mode,
        },
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="News sentiment analyzer for crypto news aggregation")
    ap.add_argument("--sources", nargs="*", default=NEWS_SOURCES, help=f"News sources (default: {' '.join(NEWS_SOURCES)})")
    ap.add_argument("--stdin", action="store_true", help="Read params from stdin (future)")
    ap.add_argument("--stub-only", action="store_true", help="Disable network fetch and use stub headlines only")
    args = ap.parse_args()

    result = analyze(sources=args.sources if args.sources else NEWS_SOURCES, prefer_live=not args.stub_only)
    json.dump(result, sys.stdout, indent=2, ensure_ascii=False)
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
