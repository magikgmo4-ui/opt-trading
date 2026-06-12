from __future__ import annotations

import re
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from typing import Any


def fetch_yahoo_rss(query: str = "SpaceX OR SPCX OR Starlink", timeout: int = 12) -> dict[str, Any]:
    now = datetime.now(timezone.utc).isoformat()
    url = "https://news.search.yahoo.com/rss?p=" + urllib.parse.quote(query)
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "opt-trading-spacex-monitor/0.2"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            xml_text = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        return {"ok": False, "provider": "yahoo_rss", "produced_at": now, "query": query, "error": str(e)}
    try:
        root = ET.fromstring(xml_text)
    except ET.ParseError as e:
        return {"ok": False, "provider": "yahoo_rss", "produced_at": now, "query": query, "error": f"parse:{e}"}
    items = []
    for item in root.findall(".//item")[:30]:
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        desc = re.sub("<[^>]+>", "", item.findtext("description") or "").strip()
        items.append({"title": title, "link": link, "published_at": pub, "summary": desc[:280]})
    return {"ok": True, "provider": "yahoo_rss", "produced_at": now, "query": query, "articles": items, "count": len(items)}
