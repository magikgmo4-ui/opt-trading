from __future__ import annotations
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any
from ..io import utc_now

def collect_yahoo_rss(query: str = "SpaceX OR SPCX OR Starlink", *, timeout: int = 15) -> dict[str, Any]:
    out = {"source": "yahoo_news_rss", "query": query, "collected_at": utc_now(), "ok": False, "articles": [], "error": None}

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
            return out
    except Exception as exc:
        out["error"] = str(exc)

    return out
