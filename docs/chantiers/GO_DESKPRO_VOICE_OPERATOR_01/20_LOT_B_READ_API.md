---
doc_id: GO_DESKPRO_VOICE_OPERATOR_01_LOT_B_API
doc_type: implementation_report
repo: opt-trading
go_id: GO_DESKPRO_VOICE_OPERATOR_01
status: completed
created_at: 2026-06-15
lot: B
---

# 20_LOT_B_READ_API

## Architecture

```text
Voice Operator (/read/*)
    │
    ├── deskpro_reader → GET /desk/spacex/command-center
    │                  → GET /desk/status
    │                  → GET /desk/alerts
    │                  → GET /desk/spacex/snapshot
    │
    ├── perf_reader    → GET /perf/summary
    │                  → GET /perf/open
    │                  → GET /perf/trades
    │
    ├── localcms_reader → GET /cms/signals/summary
    │                   → GET /cms/signals
    │                   → GET /cms/spacex/json
    │                   → GET /cms/menu/state
    │
    └── memory_reader   → placeholder (Lot C/D)
```

## 8 Endpoints

| Endpoint | Source | Vocal intent | Payload keys |
|----------|--------|-------------|--------------|
| `GET /read/system` | DeskPro + Perf + LocalCMS | "Etat systeme" | status, services_running, critical_alerts, pipeline_state, one_line |
| `GET /read/spacex` | DeskPro command-center + snapshot | "Resume SPCX" | price, vwap, vwap_state, vwap_score, trend, trade_ready, top_setup, summary |
| `GET /read/alerts?limit=N` | DeskPro alerts + Telegram signals | "Alertes Telegram" | total, critical, items[], one_line |
| `GET /read/setups` | DeskPro + Perf open trades | "Setups actifs" | active, a_plus, a_grade, items[], one_line |
| `GET /read/setup?symbol=X` | DeskPro (SPCX) or Perf (others) | "Setup BTC" | symbol, setup_type, direction, grade, entry_zone, invalidation |
| `GET /read/score?symbol=X` | Snapshot scores | "Score BTC" | trade_ready, momentum, risk, vwap_score, orderflow_score, one_line |
| `GET /read/market` | DeskPro command-center | "Rapport marche" | symbols[], one_line |
| `GET /read/report` | DeskPro + Perf + Alerts | "Rapport quotidien" | symbols[], top_setups[], active_alerts[], one_line |

## Payload examples

### /read/system

```json
{
  "status": "ok",
  "services_running": 5,
  "critical_alerts": 0,
  "pipeline_state": "healthy",
  "timers_active": 2,
  "one_line": "Systeme operationnel. 5 services actifs"
}
```

### /read/spacex

```json
{
  "symbol": "SPCX",
  "price": 160.95,
  "vwap": 164.70,
  "vwap_state": "BEARISH",
  "vwap_score": 50,
  "gap_ipo_pct": 19.22,
  "trend": "bullish",
  "trade_ready": 0,
  "top_setup": null,
  "setup_grade": "reject",
  "confidence": 0,
  "orderflow_score": 70.5,
  "ownership_pressure_score": 36.8,
  "pipeline_state": "degraded",
  "source_quality": "direct",
  "summary": "SPCX a 161.0, VWAP 164.7, etat BEARISH. Score VWAP 50/100. Gap IPO +19.2%"
}
```

### /read/setups

```json
{
  "active": 1,
  "a_plus": 0,
  "a_grade": 0,
  "items": [
    {
      "symbol": "SPCX",
      "setup_type": "VWAP_HOLD_LONG",
      "direction": "LONG",
      "grade": "B",
      "trade_ready": 60,
      "source": "spcx_v2"
    }
  ],
  "one_line": "1 setups actifs"
}
```

## Invariants respectes

- **Aucun service existant modifie** — les 4 readers sont des wrappers HTTP
- **Read-only** — tous les endpoints sont GET, aucun POST/PUT/DELETE
- **Aucun calcul de score** — les scores viennent de DeskPro/snapshot
- **Aucune logique trading** — pas de Signal, pas d'ordre
- **DeskPro reste source de verite** — les readers lisent, ne produisent pas

## Fichiers crees

```text
modules/voice_operator/
  __init__.py
  api/
    __init__.py
    routes.py              (286 lignes, 8 endpoints)
    schemas.py             (108 lignes, 9 dataclasses)
    readers/
      __init__.py
      deskpro_reader.py    (55 lignes, 5 fonctions)
      perf_reader.py       (35 lignes, 3 fonctions)
      localcms_reader.py   (35 lignes, 4 fonctions)
      memory_reader.py     (26 lignes, 2 fonctions)
  docs/
```

## Run

```bash
cd /opt/trading
source venv/bin/activate
python -m uvicorn modules.voice_operator.api.routes:app --host 0.0.0.0 --port 8020
```

Then: `curl http://127.0.0.1:8020/read/system`
