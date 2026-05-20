---
doc_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01_VALIDATION_FLOW
doc_type: methodology
repo: opt-trading
go_id: GO_STRATEGY_REGISTRY_TELEGRAM_LATENCY_01
status: active
source_kind: canonical
updated_at: 2026-05-19
---

# 30_VALIDATION_FLOW

## Step 1 — Collecte telemetry (dry-run OK)

- exécuter des runs dry-run qui déclenchent des notifications (dispatcher, alerts)
- la telemetry `telegram_send.jsonl` est écrite localement (pas de secrets)

## Step 2 — Backtest offline

```powershell
python scripts\telegram\latency_backtest.py
```

Lire:

- `ok_rate`
- `p95_ms` / `p99_ms`
- breakdown par `strategy_id` si tags présents

## Step 3 — Registry update

- mettre à jour `95_STRATEGY_REGISTRY.md`
  - colonne `telegram_latency`
  - champs par stratégie (status + evidence ref)

## Gate (règle simple V1)

- `PASS`: `ok_rate >= 0.99` et `p95_ms` sous seuil (défini par produit)
- sinon `DEGRADED` ou `BLOCKED`
