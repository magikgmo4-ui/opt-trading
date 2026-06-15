---
doc_id: GO_DESKPRO_VOICE_OPERATOR_01_LOT_C_ENGINE
doc_type: implementation_report
repo: opt-trading
go_id: GO_DESKPRO_VOICE_OPERATOR_01
status: completed
created_at: 2026-06-15
lot: C
---

# 30_LOT_C_VOICE_ENGINE

## Architecture

```text
User phrase
    │
    ▼
intent_router.route("Setup BTC")
    │
    ├── keyword matching → RoutedIntent {intent, endpoint, params}
    │
    ▼
read_api_client.call(endpoint, params)
    │
    ├── HTTP GET → /read/setup?symbol=BTC
    │
    ▼
Response {one_line, ...}
    │
    ▼
CLI display (console) or JSON output
```

## Intent Router

`modules/voice_operator/engine/intent_router.py` — 25+ intents, keyword-based routing.

| Intent | Keywords | Endpoint |
|--------|----------|----------|
| system_status | "etat systeme", "health", "sante" | `/read/system` |
| spcx_summary | "resume spcx", "spcx", "spacex" | `/read/spacex` |
| alerts | "alertes telegram", "alerts" | `/read/alerts` |
| alerts_critical | "alertes critiques", "urgences" | `/read/alerts?limit=50` |
| setups_all | "setups actifs", "liste setups" | `/read/setups` |
| setup_detail | "setup btc", "setup gold", "setup spcx" | `/read/setup?symbol=X` |
| score_detail | "score btc", "score gold", "score spcx" | `/read/score?symbol=X` |
| market | "rapport marche", "marche" | `/read/market` |
| report | "rapport quotidien", "daily" | `/read/report` |

Word-boundary matching ensures "rapport" doesn't match "or" as gold.

## CLI

```bash
# Single command
python -m modules.voice_operator.cli.voice_operator_cli "Etat systeme"
python -m modules.voice_operator.cli.voice_operator_cli "Setup BTC"
python -m modules.voice_operator.cli.voice_operator_cli "Rapport marche"

# JSON output
python -m modules.voice_operator.cli.voice_operator_cli --json "Score SPCX"

# Interactive mode
python -m modules.voice_operator.cli.voice_operator_cli --interactive

# List intents
python -m modules.voice_operator.cli.voice_operator_cli --help-intents
```

## Supported Symbols

| Symbol | Keywords |
|--------|----------|
| BTC | btc, bitcoin |
| ETH | eth, ethereum |
| XAUUSD | gold, xau, xauusd |
| SPCX | spcx, spacex |
| SOL | sol, solana |
| NVDA | nvda |
| RKLB | rklb |
| DXY | dxy |
| SPY | spy |
| VIX | vix |

## Fichiers crees

```text
modules/voice_operator/engine/
  __init__.py
  intent_router.py    (178 lignes, 25+ intents)
  read_api_client.py  (33 lignes, HTTP client)

modules/voice_operator/cli/
  __init__.py
  voice_operator_cli.py (164 lignes, CLI + interactive mode)
```

## Mode

- **Pas de micro** — text-mode only
- **Pas de TTS** — console output
- **Pas de OpenAI Realtime** — keyword matching, zero cost
- **Monitor-only** — affiche "MONITOR-ONLY" dans la sortie
- **Validation humaine obligatoire**

## Next: Lot D — OpenAI Realtime

Connect to OpenAI Realtime API for voice input/output.
