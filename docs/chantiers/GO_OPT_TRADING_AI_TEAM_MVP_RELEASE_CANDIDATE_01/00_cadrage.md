---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/90_PARENT_CLOSEOUT.md
  - modules/ai_team_mvp/runner.py
  - modules/ai_team_mvp/registry/
---

# GO_OPT_TRADING_AI_TEAM_MVP_RELEASE_CANDIDATE_01 — 00_cadrage

## 1_MASTER_TARGET

Figer une release candidate locale du MVP AI Team : documenter les 5 task types, les commandes d'usage safe, la matrice des smokes cumules, les limites de securite et les interdits permanents.

## 3_INITIAL_NEED

Le MVP AI Team est complet cote task types (5/5), les smokes sont PASS (35/35 cumules), les registres sont a jour. Il manque un document unique de release candidate qui permette la reprise, l'usage et l'extension sans relire l'ensemble des chantiers.

## 4_MASTER_PROJECT_PLAN

1. Documenter les 5 task types et leurs commandes.
2. Consolider la matrice des smokes cumules (5 task types × criteres).
3. Definir les limites de securite et les interdits permanents.
4. Lister les next GO candidates.
5. Clore.

## 7_CANONICAL_STATE

- Runner : 5 task types (READ_INVENTORY, DOC_DRAFT, ANALYZE_INVENTORY, PATCH_DRAFT, ORCHESTRATOR_CHAIN)
- Smokes : 35/35 criteres PASS cumules
- Registres : 5 workers, 5 tasks, 4 outputs, 5 smoke traces
- Contrat : Strict Workers respecte partout
- PATCH_DRAFT : proposal-only, jamais applique automatiquement
- Type : doc-only

## 11_KEY_DECISIONS

- La release candidate est locale (PASS_LOCAL).
- Push GitHub reste a confirmer (PUSH_PENDING_AUTH).
- Aucun patch n'est applique automatiquement.
- ClickUp differe.
- Stash reseau_ssh conserve.

## 12_INVARIANTS

- Doc-only.
- Aucun git write depuis le runner.
- Aucune application automatique de patch.
- Aucun secret.

## 16_TODO

1. Rediger `01_release_candidate.md`.
2. Rediger `02_smoke_matrix_cumulative.md`.
3. Rediger `03_usage_safe_commands.md`.
4. Rediger `90_CLOSEOUT.md`.
