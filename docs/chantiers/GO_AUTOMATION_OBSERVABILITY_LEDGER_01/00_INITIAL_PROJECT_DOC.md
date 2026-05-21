---
doc_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01_INITIAL
doc_type: initial_project_doc
go_id: GO_AUTOMATION_OBSERVABILITY_LEDGER_01
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-21
links:
  - deploy/systemd/opt-trading-runtime-health.service
  - deploy/systemd/opt-trading-fleet-orchestrator.service
  - config/machine_runtime_map.yml
  - data/runtime_health/
---

# GO_AUTOMATION_OBSERVABILITY_LEDGER_01

## Objectif

Créer le ledger global des actions automatisées : schéma, stockage, writer, events, replay/audit, affichage cockpit (GAP_06 du parent).

## Périmètre

- Schema du ledger (event_id, actor, action, surface, timestamp, status, payload)
- Stockage (fichier JSON ou DB légère)
- Writer unique (une seule source d'écriture)
- 3 events sample minimum
- Replay/audit validé
- Vue lecture LocalCMS prévue

## Preuve concrète pour l'ouverture

- `deploy/systemd/*` : runtime-health et fleet-orchestrator produisent des données de santé sans ledger centralisé
- `data/runtime_health/` : répertoire de données runtime existe, peut servir de base au ledger
- `config/machine_runtime_map.yml` : machines et services identifiés, peuvent alimenter le ledger

## Livrables

- Schema de l'event ledger
- Writer implémenté
- 3 events sample
- Replay/audit fonctionnel
- Vue lecture LocalCMS documentée
