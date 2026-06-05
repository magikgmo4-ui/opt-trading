---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01_FIXTURES
doc_type: fixtures_and_contracts
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 20_FIXTURES_AND_CONTRACTS - Fixtures and Contracts

## Fixtures créées

Chemin: `tests/fixtures/admin_trading_contract_smoke/`

### signal_event_v0_minimal.json

Payload V0 minimal (webhook) — champs requis seulement.

```json
{
  "engine": "USDTM_LONG",
  "signal": "BUY",
  "symbol": "BTCUSDT",
  "tf": "H1",
  "_ts": "2026-05-06T02:20:00+00:00"
}
```

### signal_event_v0_complete.json

Payload V0 complet — tous les champs.

```json
{
  "key": null,
  "engine": "USDTM_LONG",
  "signal": "BUY",
  "symbol": "BTCUSDT",
  "tf": "H1",
  "price": 68000.0,
  "tp": 69000.0,
  "sl": 67500.0,
  "reason": "breakout",
  "_ts": "2026-05-06T02:20:00+00:00",
  "_ip": "127.0.0.1",
  "qty": 0.01,
  "risk_usd": 50.0,
  "risk_real_usd": 50.0
}
```

### visual_context_v1_minimal.json

Visual context V1 conforme au contrat.

```json
{
  "source": "sharex",
  "capture_id": "screen_tradingview_BTCUSDT.P_H1_2026-05-06_02-20-15",
  "symbol": "BTCUSDT.P",
  "timeframe": "H1",
  "captured_at": "2026-05-06T02:20:15+00:00",
  "image_ref": "/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-06_02-20-15.png",
  "metadata_ref": null,
  "payload_hash": null,
  "chart_source": "tradingview",
  "status": "ready",
  "errors": [],
  "signal_event_ref": null,
  "desk_snapshot_ref": "BTCUSDT.P_H1_20260506_022015.png"
}
```

### desk_snapshot_minimal.json

Desk snapshot conforme au format `desk/snapshots/latest.json`.

```json
{
  "symbol": "BTCUSDT.P",
  "tf": "H1",
  "snapshot_ts": "2026-05-06T02:20:15",
  "path": "/opt/trading/desk/snapshots/BTCUSDT.P/BTCUSDT.P_H1_20260506_022015.png",
  "ingested_at": "2026-05-06T02:25:35-04:00",
  "source": "sharex",
  "host": "admin-trading"
}
```

## Pas de secrets

Toutes les fixtures sont synthétiques. Aucun token, API key, ou payload réel n'est inclus.

## Contrats vérifiés

| Contrat | Champ clé | Fixture | Adapter |
| --- | --- | --- | --- |
| signal_event V1 | `direction`, `timeframe`, `timestamp`, `status` | V0 fixtures | `normalize_signal_event_v1` |
| visual_context V1 | `symbol`, `timeframe`, `captured_at`, `status` | visual_context fixture | — |
| desk_snapshot | `symbol`, `tf`, `snapshot_ts`, `path` | desk_snapshot fixture | — |
| Desk Pro synthesis | ensemble | toutes | test `TestDeskProSynthesisSmoke` |

## RISKS

- À qualifier.
