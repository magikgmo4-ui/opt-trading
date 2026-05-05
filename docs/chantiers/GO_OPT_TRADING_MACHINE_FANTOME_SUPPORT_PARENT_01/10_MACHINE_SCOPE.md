---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_MACHINE_SCOPE
doc_type: machine_scope
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: machine_scope
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - machine_scope
  - ai_team
  - strict_workers
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
point_de_reprise: "7_CANONICAL_STATE"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 10_MACHINE_SCOPE

## Perimetre machine

```text id="machine_fantome_scope"
Machine : fantome
Role : AI Team / Strict Workers / workspace support agents
Type : parent machine / support (pas runtime trading)
Statut : ouvert doc-only
```

## Assignation

```text id="machine_fantome_assignment"
AI_TEAM + STRICT_WORKERS = fantome
fantome = AI Team / Strict Workers / workspace support agents
```

La machine `fantome` heberge tout ce qui concerne :
- l'architecture et la gestion de l'AI Team (agents specialises) ;
- les Strict Workers (workers autonomes a perimetre etroit) ;
- le workspace support pour les agents ;
- les audits et evaluations de configuration agent.

Important : `fantome` est un parent **support / AI-workspace**, pas un runtime trading.
Il ne gere pas de webhooks, pas de desk, pas d'execution temps reel.

## Frontiere avec les autres machines

| Machine | Frontiere | Interaction |
|---------|-----------|-------------|
| cursor-ai | Aucun partage direct | Pas de runtime commun |
| student | Machine distincte (Local Ollama) | Pas de melange |
| admin-trading | Ne pas activer maintenant | Pas de runtime admin-trading ici |
| db-layer | Garder disponible | Pas d'ingestion pour le moment |

## Rattachement aux parents existants

```text id="machine_fantome_existing_parents"
Parents actifs :
- GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (KEEP_ACTIVE)

Parents a auditer :
- go/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 (a verifier avant promotion)

Sauvegardes :
- save/fantome-YYYY-MM-DD
```

## Invariants machine

- Ne pas recreer AI_TEAM (deja KEEP_ACTIVE).
- Ne pas promouvoir STRICT_WORKERS sans audit complet.
- Ne pas modifier les parents existants.
- Ne pas creer de runtime trading sur cette machine.
- Chaque branche modifie son propre dossier `docs/chantiers/<GO_ID>/`.
- Pas de modification des index globaux sauf inbox atomique.

## Prochain GO

`GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01`
Objectif : reconcilier AI_TEAM et STRICT_WORKERS avec le parent machine fantome.
