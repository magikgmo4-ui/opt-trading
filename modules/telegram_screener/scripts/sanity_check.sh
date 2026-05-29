#!/usr/bin/env bash
set -euo pipefail
MOD="${0%/*}/.."
MOD="$(cd "$MOD" && pwd -P)"

[ -d "$MOD/service" ] || { echo "FAIL: service missing"; exit 2; }
[ -f "$MOD/service/signal_context_reader.py" ] || { echo "FAIL: signal_context_reader missing"; exit 2; }
[ -d "$MOD/parser" ] || { echo "FAIL: parser missing"; exit 2; }
[ -f "$MOD/parser/trade_parser.py" ] || { echo "FAIL: trade_parser missing"; exit 2; }
[ -f "$MOD/parser/news_parser.py" ] || { echo "FAIL: news_parser missing"; exit 2; }
[ -f "$MOD/parser/alpha_parser.py" ] || { echo "FAIL: alpha_parser missing"; exit 2; }
[ -f "$MOD/parser/signal_normalizer.py" ] || { echo "FAIL: signal_normalizer missing"; exit 2; }
[ -f "$MOD/parser/signal_schema.py" ] || { echo "FAIL: signal_schema missing"; exit 2; }
[ -d "$MOD/signal" ] || { echo "FAIL: signal missing"; exit 2; }
[ -f "$MOD/signal/signal_schema.py" ] || { echo "FAIL: signal_schema missing"; exit 2; }
[ -f "$MOD/signal/signal_producer.py" ] || { echo "FAIL: signal_producer missing"; exit 2; }
[ -f "$MOD/signal/desk_pro_adapter.py" ] || { echo "FAIL: desk_pro_adapter missing"; exit 2; }
[ -d "$MOD/registry" ] || { echo "FAIL: registry missing"; exit 2; }
[ -f "$MOD/registry/models.py" ] || { echo "FAIL: registry models missing"; exit 2; }
[ -f "$MOD/registry/loader.py" ] || { echo "FAIL: registry loader missing"; exit 2; }
[ -f "$MOD/registry/channels.yaml" ] || { echo "FAIL: registry channels.yaml missing"; exit 2; }
[ -d "$MOD/router" ] || { echo "FAIL: router missing"; exit 2; }
[ -f "$MOD/router/__init__.py" ] || { echo "FAIL: router __init__ missing"; exit 2; }
[ -d "$MOD/pipeline" ] || { echo "FAIL: pipeline missing"; exit 2; }
[ -f "$MOD/pipeline/__init__.py" ] || { echo "FAIL: pipeline __init__ missing"; exit 2; }
[ -x "$MOD/scripts/cmd.sh" ] || { echo "FAIL: cmd.sh not executable"; exit 2; }
[ -x "$MOD/scripts/menu.sh" ] || { echo "FAIL: menu.sh not executable"; exit 2; }
echo "PASS: telegram_screener sanity OK"
