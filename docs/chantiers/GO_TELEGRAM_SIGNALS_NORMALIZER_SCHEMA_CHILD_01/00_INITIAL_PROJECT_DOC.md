---
doc_id: GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01
go_structural_role: GO_CHILD_ATTACHED_TO_PARENT
parent_go_id: GO_OPT_TRADING_TELEGRAM_SCREENER_PARENT_OPEN_01
pf_id: PF_TELEGRAM_SCREENER
status: open
lifecycle_stage: implementation
surface: modules/telegram_screener
source_kind: canonical
created_at: 2026-06-03
updated_at: 2026-06-03
upstream:
  - GO_TELEGRAM_SIGNALS_PARSERS_FIXTURES_CHILD_01
links:
  - docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/10_CURRENT_PARSER_OUTPUT_AUDIT.md
  - docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/20_SIGNAL_CANDIDATE_SCHEMA.md
  - docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/30_SCREENER_SIGNAL_SCHEMA.md
  - docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/40_NORMALIZER_PLAN.md
  - docs/chantiers/GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01/50_VALIDATION_PLAN.md
---

# GO_TELEGRAM_SIGNALS_NORMALIZER_SCHEMA_CHILD_01

## Objectif

Normaliser les sorties des parseurs Telegram (trade, news, alpha, coinglass) en un modele commun `SignalCandidate`, puis les convertir en `ScreenerSignal` pour le pipeline existant.

## 1_MASTER_TARGET

```text
parseur outputs (dict / ScreenerSignal) -> SignalCandidate -> normalizer -> ScreenerSignal -> pipeline
```

## 4_MASTER_PROJECT_PLAN

1. Auditer les sorties actuelles de chaque parseur (trade, news, alpha, coinglass).
2. Definir le schema `SignalCandidate` comme modele intermediaire universel.
3. Verifier l'alignement de `ScreenerSignal` existant comme cible de normalisation.
4. Implementer le normalizer : `SignalCandidate` -> `ScreenerSignal`.
5. Ajouter des tests de normalisation sans dependance reseau ni fixture live.

## 12_INVARIANTS

- Aucun appel reseau.
- Aucune modification des parseurs existants (trade, news, alpha, coinglass).
- Aucune modification des fixtures existantes.
- `coinglass_parser.py` conserve son retour dict (retrocompatibilite).
- Les types existants (`ScreenerSignal`, `Direction`, `SignalType`, `Confidence`) ne sont pas modifies.

## 17_RESUME_POINT

```text
parseurs audites -> SignalCandidate defini -> normalizer implemente -> tests valides -> ScreenerSignal unifie
```
