---
doc_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/02_decisions.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_BUNDLES_REUSE_AUDIT_01/
---

# GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01 — 00_cadrage

## 1_MASTER_TARGET

Implementer le premier MVP de l'AI Team avec 3 workers qualifies, sur 1 tache reelle doc-only, sans write runtime, avec smoke validation, en reutilisant les 4 artefacts REUSE_FOR_MVP.

## 3_INITIAL_NEED

L'architecture canonique est posee (PASS), les bundles sont inventories (PASS). Il faut maintenant materialiser le MVP minimal sans reinventer de socle : un runner Python read-only, un task packet Strict Workers, un smoke READ_INVENTORY, et la preuve que le contrat d'integration fonctionne.

## 4_MASTER_PROJECT_PLAN

1. Selectionner 3 workers initiaux : Observer, Documenter, Gatekeeper.
2. Definir la tache READ_INVENTORY doc-only sur docs/chantiers/ + GO_INDEX.
3. Creer `tasks/read_inventory.json` compatible Strict Workers.
4. Creer le runner Python minimal (`modules/ai_team_mvp/runner.py`).
5. Respecter le contrat Strict Workers : denied_inputs, denied_commands, no_git_write, DRAFT_ONLY.
6. Executer le smoke READ_INVENTORY.
7. Documenter le bundle reuse map.
8. Rediger le closeout.

## 5_GO_PLAN

Workstream :
- W1 : spec MVP + selection workers
- W2 : task packet + runner
- W3 : smoke execution
- W4 : bundle reuse map
- W5 : closeout

## 7_CANONICAL_STATE

- Parent : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (OPEN)
- Architecture Canon : PASS
- Doc Audit : PASS
- Bundles Reuse Audit : PASS
- Type : doc-only + runner minimal read-only, aucun runtime modifie

## 11_KEY_DECISIONS

- MVP demarre avec 3 workers sur 1 tache READ_INVENTORY doc-only.
- Pas de Docker, pas de sandbox dans ce MVP.
- Runner Python minimal, stdlib only.
- Sortie DRAFT_ONLY, jamais de git write.
- Strict Workers est la couche de securite obligatoire.
- validated_prompt_factory sert a standardiser les prompts/packets.
- ClickUp differe.

## 12_INVARIANTS

- Doc-only + runner read-only.
- Ne pas ouvrir ClickUp.
- Ne pas toucher au runtime trading.
- Ne pas faire de git write ops depuis le runner.
- Ne pas ecrire de secrets, .env, cles, tokens.
- Ne pas toucher aux untracked legacy dirs.
- Reutiliser les bundles existants avant de creer du neuf.

## 16_TODO

1. Rediger `01_mvp_spec.md`.
2. Rediger `02_worker_selection.md`.
3. Rediger `03_smoke_plan.md`.
4. Rediger `04_bundle_reuse_map.md`.
5. Creer `modules/ai_team_mvp/runner.py`.
6. Creer `modules/ai_team_mvp/tasks/read_inventory.json`.
7. Executer smoke READ_INVENTORY.
8. Rediger `90_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre depuis `01_mvp_spec.md`, verifier le runner et le smoke, puis closeout.
