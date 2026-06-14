from __future__ import annotations
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any
from ..io import utc_now

def collect_yahoo_rss(query: str = "SpaceX OR SPCX OR Starlink", *, timeout: int = 15) -> dict[str, Any]:
    out = {"source": "yahoo_news_rss", "query": query, "collected_at": utc_now(), "ok": False, "articles": [], "error": None,
           "sentiment": {"polarity": "neutral", "bullish_count": 0, "bearish_count": 0, "neutral_count": 0},
           "clusters": []}

    BULLISH = ["surge","soar","jump","rally","record","breakout","bullish","upgrade","outperform","buy","beat","exceed","raised","growth","momentum","partnership","contract win","profit","positive","strong buy","accumulate","expansion","launch success","subscriber growth","revenue beat"]
    BEARISH = ["plunge","tumble","crash","drop","decline","bearish","sell-off","downgrade","underperform","sell","miss","below","cut","lowered","risk","concern","warning","caution","overvalued","bubble","dilution","lockup","fine","penalty","delay","failure","loss","negative","weak","slowdown","headwind","probe","lawsuit","investigation"]

    def _fetch(url, user_agent="Mozilla/5.0 opt-trading spacex_super_desk"):
        req = urllib.request.Request(url, headers={"User-Agent": user_agent})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()

    def _parse_rss(xml_bytes):
        root = ET.fromstring(xml_bytes)
        items = []
        for item in root.findall(".//item")[:40]:
            title = (item.findtext("title") or "").strip()
            desc = re.sub("<[^>]+>", " ", item.findtext("description") or "").strip()
            items.append({"title": title, "link": item.findtext("link"), "published_at": item.findtext("pubDate"), "summary": desc[:400]})
        return items

    # Try Google News RSS (more reliable than Yahoo)
    try:
        gn_url = "https://news.google.com/rss/search?q=" + urllib.parse.quote(query) + "&hl=en-US&ceid=US:en"
        out["url"] = gn_url
        xml_bytes = _fetch(gn_url)
        articles = _parse_rss(xml_bytes)
        if articles:
            out.update({"ok": True, "articles": articles})
            _compute_sentiment(out, articles)
            return out
    except Exception as exc:
        out["google_error"] = str(exc)

    # Fallback: Yahoo RSS
    try:
        yh_url = "https://news.search.yahoo.com/rss?p=" + urllib.parse.quote(query)
        out["url"] = yh_url
        xml_bytes = _fetch(yh_url)
        articles = _parse_rss(xml_bytes)
        if articles:
            out.update({"ok": True, "articles": articles})
            _compute_sentiment(out, articles)
            return out
    except Exception as exc:
        out["error"] = str(exc)

    return out


def _compute_sentiment(out: dict, articles: list) -> None:
    """Inline keyword-based sentiment classification. No LLM required."""
    bullish_keywords = out["_bull_kw"] if "_bull_kw" in out else []
    bearish_keywords = out["_bear_kw"] if "_bear_kw" in out else []
    # Re-read from closure
    BULLISH = ["surge","soar","jump","rally","record","breakout","bullish","upgrade","outperform","buy","beat","exceed","raised","growth","momentum","partnership","contract win","profit","positive","strong buy","accumulate","expansion","launch success","subscriber growth","revenue beat"]
    BEARISH = ["plunge","tumble","crash","drop","decline","bearish","sell-off","downgrade","underperform","sell","miss","below","cut","lowered","risk","concern","warning","caution","overvalued","bubble","dilution","lockup","fine","penalty","delay","failure","loss","negative","weak","slowdown","headwind","probe","lawsuit","investigation"]

    bull = bear = neut = 0
    clusters = []
    seen = set()
    for a in articles:
        title = a.get("title", "").lower()
        words = set(re.findall(r"\w+", title))
        # Dedup: skip similar titles
        key = " ".join(sorted(words)[:5])
        if key in seen:
            continue
        seen.add(key)

        b_hits = sum(1 for kw in BULLISH if kw in title)
        r_hits = sum(1 for kw in BEARISH if kw in title)

        if b_hits > r_hits:
            bull += 1
            pol = "bullish"
        elif r_hits > b_hits:
            bear += 1
            pol = "bearish"
        else:
            neut += 1
            pol = "neutral"

        clusters.append({"title": a["title"][:100], "polarity": pol})

    # Overall polarity
    if bull > bear and bull > neut:
        overall = "bullish"
    elif bear > bull and bear > neut:
        overall = "bearish"
    else:
        overall = "mixed" if bull > 0 or bear > 0 else "neutral"

    out["sentiment"] = {
        "polarity": overall,
        "bullish_count": bull,
        "bearish_count": bear,
        "neutral_count": neut,
    }
    out["clusters"] = clusters[:20]
