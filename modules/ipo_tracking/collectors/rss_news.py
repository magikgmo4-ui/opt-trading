from __future__ import annotations
import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from typing import Any
from ..io import utc_now

def collect_yahoo_rss(query: str = "SpaceX OR SPCX OR Starlink", *, timeout: int = 15) -> dict[str, Any]:
    url = "https://news.search.yahoo.com/rss?p=" + urllib.parse.quote(query)
    out = {"source": "yahoo_news_rss", "query": query, "collected_at": utc_now(), "url": url, "ok": False, "articles": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 opt-trading spacex_super_desk"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml = resp.read()
        root = ET.fromstring(xml)
        items = []
        for item in root.findall(".//item")[:40]:
            title = (item.findtext("title") or "").strip()
            desc = re.sub("<[^>]+>", " ", item.findtext("description") or "").strip()
            items.append({"title": title, "link": item.findtext("link"), "published_at": item.findtext("pubDate"), "summary": desc[:400]})
        out.update({"ok": True, "articles": items})
    except Exception as exc:
        out["error"] = str(exc)
    return out
