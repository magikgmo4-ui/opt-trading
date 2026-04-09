# GO_OT_TRAE_RULES_V1_01 — DÉCISION CANONIQUE (GEL PRÉ-V1 RULES)

Date (America/Montreal) : 2026-04-09

## 1. Objet
Acter, de manière strictement doc-only, si le bloc “Rules Trae V1” doit être gelé en pré‑V1 de façon opposable, sans ouvrir les couches Agents/Skills/MCP, et sans toucher au runtime ni au code.

## 2. Éléments établis (preuves)
- Le socle pré‑V1 est déjà matérialisé dans le repo sous `docs/ot/trae/` (dont `01_RULES_V1.txt`).
- Le kanban canonique indique : `Rules Trae V1` = `ÉTABLI / MATÉRIALISÉ (PRE-V1)` avec suite `revue + gel pré-V1`.
- La décision de cadrage “CONTRADICTOIRE” fixe : repo-first, helpers non opposables, grandfathering legacy, et interdit la normalisation implicite.

## 3. Constat (ce qui manque)
- Le kanban ne distingue pas explicitement “pré‑V1 matérialisé” de “pré‑V1 gelé/opposable” pour `Rules Trae V1`.
- Sans gel explicite, le contenu de `01_RULES_V1.txt` reste exposé à des retouches opportunistes et la suite “revue + gel” reste indéfinie.

## 4. Décision canonique
- Le gel pré‑V1 **opposable** est acté pour `Rules Trae V1` sur la base du fichier `docs/ot/trae/01_RULES_V1.txt`.
- Portée du gel : uniquement `Rules` (ce document). Aucune ouverture implicite de `Agents`, `Skills` ou `MCP`.
- Le gel est doc-only : aucune modification de runtime, de scripts ou de modules n’est autorisée dans ce cadre.

## 5. Artefacts doc-only requis
- Décision : `docs/ot/trae/OT_TRAE_RULES_PRE_V1_GEL_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_RULES_V1_01_CLOSING.txt`
- Alignement kanban :
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`

## 6. Conséquences
- Le bloc `Rules Trae V1` devient “pré‑V1 gelé/opposable” (doc-only).
- Toute évolution ultérieure de `01_RULES_V1.txt` doit passer par une mission explicite, avec preuves et mise à jour kanban si un statut/suite change.

## 7. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01` (décider explicitement si ouverture de la couche Agents V1, sans inventer de nouveau GO).
