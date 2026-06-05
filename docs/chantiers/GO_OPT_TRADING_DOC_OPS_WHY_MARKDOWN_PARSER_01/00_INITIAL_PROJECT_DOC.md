---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01_INITIAL_PROJECT_DOC
repo: opt-trading
status: active
branch: go/GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01
scope: doc_ops
parent_context: SYSTEM_WHY_LAYER_01
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Cadrer le parser markdown WHY reel pour lire les blocs WHY, detecter les sections critiques manquantes et preparer le scoring automatique.

## 3_INITIAL_NEED

Apres merge du WHY layer et de la runtime risk map, le prochain socle est un parser documentaire non destructif capable d'extraire les sections WHY dans les documents du repo.

## 4_MASTER_PROJECT_PLAN

- Definir les sections markdown a reconnaitre.
- Definir les surfaces documentaires cibles.
- Definir le modele de sortie attendu.
- Definir les erreurs et gaps detectables.
- Preparer le futur scoring automatique sans l'implementer.

## 6_FINAL_TARGET

Produire une specification claire du parser WHY markdown avant toute implementation.

## 7_CANONICAL_STATE

Le repo possede maintenant:
- `SYSTEM_WHY_LAYER_01.md`,
- une checklist WHY,
- une enforcement policy WHY,
- une classification runtime R0-R5,
- une cartographie runtime WHY.

Il manque:
- une lecture structuree automatique des blocs WHY.

## 12_INVARIANTS

- Doc-only pour ce cadrage initial.
- Aucun runtime.
- Aucun CI actif.
- Aucun scoring automatique actif.
- Aucun lint bloquant.
- Aucun APPLY automatique.

## 16_TODO

- Creer la specification du parser.
- Creer le schema de sortie.
- Creer la liste des sections detectees.
- Creer les regles de gap detection.
- Creer le point de reprise vers implementation future.

## 17_RESUME_POINT

Reprendre sur `go/GO_OPT_TRADING_DOC_OPS_WHY_MARKDOWN_PARSER_01` pour specifier un parser WHY markdown non destructif.

## RISKS

- À qualifier.
