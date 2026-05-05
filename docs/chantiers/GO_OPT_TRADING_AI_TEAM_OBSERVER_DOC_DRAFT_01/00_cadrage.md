---
doc_id: GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01_CADRAGE
doc_type: cadrage
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01
status: open
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01/01_mvp_spec.md
  - modules/ai_team_mvp/runner.py
---

# GO_OPT_TRADING_AI_TEAM_OBSERVER_DOC_DRAFT_01 — 00_cadrage

## 1_MASTER_TARGET

Produire un premier DOC_DRAFT controle a partir d'une sortie Observer READ_INVENTORY, sans ecriture runtime et sans automatisation de merge, en respectant le contrat Strict Workers.

## 3_INITIAL_NEED

Le runner MVP est valide en read-only (PASS, 6/6 smoke). L'etape suivante logique est de transformer une sortie Observer en brouillon documentaire controle : le worker Documenter produit un rapport structure a partir des donnees de l'Observer, sans ecrire hors du dossier `drafts/` autorise.

## 4_MASTER_PROJECT_PLAN

1. Definir le format DOC_DRAFT minimal (required_sections Strict Workers).
2. Prendre la sortie Observer READ_INVENTORY comme input.
3. Etendre le runner pour supporter DOC_DRAFT (nouveau task type).
4. Creer un task packet `observer_doc_draft.json`.
5. Executer le runner en mode DOC_DRAFT, sortie dans `drafts/`.
6. Valider le resultat : contrat, 0 denied, 0 git write.
7. Documenter les limites et le next GO.

## 7_CANONICAL_STATE

- Parent : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (OPEN)
- GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01 = PASS
- Runner MVP read-only fonctionnel (32 chantiers, 6/6 smoke)
- Type : doc-only + runner avec write limite a drafts/

## 11_KEY_DECISIONS

- Le DOC_DRAFT est genere dans `modules/ai_team_mvp/drafts/` uniquement.
- Aucune ecriture hors de ce dossier.
- Le format DOC_DRAFT reprend les required_sections Strict Workers.
- L'input vient d'une sortie Observer (pas de read supplementaire hors perimetre).
- validated_prompt_factory peut etre utilise pour standardiser le format.
- ClickUp differe.

## 12_INVARIANTS

- Doc-only, write limite a drafts/.
- Ne pas ouvrir ClickUp.
- Ne pas toucher au runtime trading.
- Ne pas faire de git write ops depuis le runner.
- Ne pas ecrire de secrets, .env, cles, tokens.
- Ne pas toucher aux untracked legacy dirs.

## 16_TODO

1. Rediger `01_doc_draft_spec.md`.
2. Creer `02_observer_output_sample.md`.
3. Creer `modules/ai_team_mvp/tasks/observer_doc_draft.json`.
4. Etendre `modules/ai_team_mvp/runner.py` pour DOC_DRAFT.
5. Creer `modules/ai_team_mvp/drafts/README.md`.
6. Executer et valider.
7. Rediger `03_validation.md`.
8. Rediger `90_CLOSEOUT.md`.

## 17_RESUME_POINT

Reprendre depuis `01_doc_draft_spec.md`, etendre le runner, executer DOC_DRAFT, valider.
