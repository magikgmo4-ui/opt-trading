#!/bin/bash
set -e
cd /opt/trading
source venv/bin/activate
python3 -c '
from modules.ipo_tracking.collectors.rss_news import collect_yahoo_rss
from modules.ipo_tracking.storage import persist_event
from modules.ipo_tracking.config import load_config

cfg = load_config()
news = collect_yahoo_rss("SPCX OR SpaceX OR Starlink")
persist_event(news, cfg)
s = news.get("sentiment", {})
articles_count = len(news.get("articles", []))
polarity = s.get("polarity", "?")
bull = s.get("bullish_count", 0)
bear = s.get("bearish_count", 0)
print("RSS: " + str(articles_count) + " headlines | sentiment: " + polarity + " | bull=" + str(bull) + " bear=" + str(bear))
'
