---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01_GAPS_DECISION
doc_type: gaps_and_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_REPRISE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 50_GAPS_AND_NEXT_DECISION - Gaps and Next Decision

## Gaps classés

### Consumer schema gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-CS-01 | Desk Pro n'a pas de schema d'entrée formalisé pour `signal_event` | MEDIUM | OPEN |
| G-CS-02 | Desk Pro n'a pas de schema d'entrée formalisé pour `visual_context` | LOW | OPEN (consommé indirectement) |
| G-CS-03 | Les modules utilisent des sample configs, pas des inputs live | MEDIUM | DOCUMENTED |
| G-CS-04 | Pas de reader `events.jsonl` dans le pipeline Desk Pro | MEDIUM | OPEN |

### Freshness gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-FR-01 | `desk/state/latest.json` stale depuis 2026-03-03 | HIGH | OPEN |
| G-FR-02 | `desk/inputs/tv_inputs_latest.json` stale depuis 2026-03-03 | HIGH | OPEN |
| G-FR-03 | `/shared/desk_pro/latest/` stale depuis 2026-04-04 | MEDIUM | OPEN |
| G-FR-04 | `desk/inputs/coinglass_latest.json` manquant | LOW | OPEN |
| G-FR-05 | `desk/snapshots/latest.json` est FRAIS | — | OK |

### Missing adapter gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-MA-01 | Pas d'adapter `signal_event` V0→V1 pour Desk Pro | MEDIUM | OPEN |
| G-MA-02 | Pas d'adapter `visual_context` sidecar → Desk Pro | LOW | OPEN (non bloquant) |
| G-MA-03 | Pas de reader `events.jsonl` dans le pipeline | MEDIUM | OPEN |
| G-MA-04 | Normalisation symbol `BTCUSDT` vs `BTCUSDT.P` non résolue | MEDIUM | OPEN |

### Runtime availability gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-RA-01 | Desk Pro n'est pas automatisé (manuel uniquement) | MEDIUM | DOCUMENTED |
| G-RA-02 | Pas de service systemd pour Desk Pro | LOW | DOCUMENTED (design choice) |
| G-RA-03 | Dernier run 2026-05-04 (acceptable) | LOW | OK |

### Stale artifact gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-SA-01 | `desk_state` stale — relancer `desk_state.py` | HIGH | OPEN |
| G-SA-02 | `tv_inputs` stale — relancer `extract_tv_inputs.py` | HIGH | OPEN |
| G-SA-03 | shared export stale — relancer dashboard export | MEDIUM | OPEN |

### Integration/smoke gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-IS-01 | Pas de smoke test signal_event → Desk Pro | MEDIUM | FUTURE GO |
| G-IS-02 | Pas de smoke test visual_context → Desk Pro | LOW | FUTURE GO |
| G-IS-03 | Pas de smoke test end-to-end webhook → capture → Desk Pro | MEDIUM | FUTURE GO |

### Upstream gaps (non bloquants pour Desk Pro)

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-UP-01 | Playwright absent — headless capture failed | HIGH | UPSTREAM (pas bloquant si ShareX suffit) |
| G-UP-02 | headless_capture en quarantaine | MEDIUM | UPSTREAM |

## Décision

### Verdict: PASS

Desk Pro peut être décrit comme consumer final de `signal_event + visual_context + desk_snapshot`. Les contrats V1 sont compatibles. Les gaps sont des lacunes d'intégration/fraîchesse, pas des blocages contractuels.

### Raisonnement

1. **desk_snapshot est déjà consommé**: `desk/snapshots/latest.json` est FRAIS et fonctionnel
2. **visual_context est consommé indirectement**: les PNG de `desk/snapshots/` sont utilisés par `desk_analyze` (OpenAI vision)
3. **signal_event nécessite un adapter**: le mapping V0→V1 est documenté, l'adapter est une couche d'intégration
4. **Les contrats V1 sont définis**: `signal_event` V1, `visual_context` V1, `desk_snapshot` sont documentés et compatibles
5. **Les gaps de fraîchesse sont relançables**: `desk_state`, `tv_inputs`, shared export peuvent être relancés sans modification runtime
6. **Le pipeline fonctionne**: 11/11 modules OK dans le dernier run (2026-05-04)

### Prochain GO recommandé

Option A (recommandée): **Smoke global producer/consumer**
```
GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
```
But: valider end-to-end que les contrats V1 sont consumables par Desk Pro via un smoke test read-only.

Option B: **Setup Playwright**
```
GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PLAYWRIGHT_SETUP_01
```
But: restaurer le pipeline headless pour capturer les 4 symboles (pas seulement le fallback ShareX).

Option C: **Adapter/schema**
```
GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_SCHEMA_ADAPTER_01
```
But: formaliser le schema d'entrée Desk Pro et créer les adapters signal_event → pipeline.

### Si FAIL/BLOCKED

Non applicable — le verdict est PASS.
