# GO_OT_TRAE_SKILLS_V1_01 — DÉCISION CANONIQUE (GEL PRÉ-V1 SKILLS)

Date (America/Montreal) : 2026-04-09

## 1. Objet
Acter, de manière strictement doc-only, si le bloc “Skills Trae V1” doit être gelé en pré‑V1 de façon opposable, sans ouvrir la couche MCP, et sans toucher au runtime ni au code.

## 2. Éléments établis (preuves)
- Le socle pré‑V1 est déjà matérialisé dans le repo sous `docs/ot/trae/` (dont `04_SKILLS_V1.txt`).
- Le kanban canonique indique : `Skills Trae V1` = `ÉTABLI / MATÉRIALISÉ (PRE-V1)` avec suite `revue + gel pré-V1`.
- `04_SKILLS_V1.txt` définit déjà un noyau minimal de skills V1 bornés (opérations fréquentes, répétables, et sorties stables), et liste explicitement des skills hors noyau V1.

## 3. Constat (ce qui manque)
- Le kanban ne distingue pas explicitement “pré‑V1 matérialisé” de “pré‑V1 gelé/opposable” pour `Skills Trae V1`.
- Le noyau minimal étant déjà défini et borné, l’étape “revue + gel” peut être actée sans dépendre du runtime, ni ouvrir la couche MCP.

## 4. Décision canonique
- Le gel pré‑V1 **opposable** est acté pour `Skills Trae V1` sur la base du fichier `docs/ot/trae/04_SKILLS_V1.txt`.
- Portée du gel : uniquement `Skills` (ce document). Aucune ouverture implicite de `MCP`.
- Le gel est doc-only : aucune modification de runtime, de scripts ou de modules n’est autorisée dans ce cadre.

## 5. Artefacts doc-only requis
- Décision : `docs/ot/trae/OT_TRAE_SKILLS_PRE_V1_GEL_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_SKILLS_V1_01_CLOSING.txt`
- Alignement kanban :
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`

## 6. Conséquences
- Le bloc `Skills Trae V1` devient “pré‑V1 gelé/opposable” (doc-only).
- Toute évolution ultérieure de `04_SKILLS_V1.txt` doit passer par une mission explicite, avec preuves et mise à jour kanban si un statut/suite change.

## 7. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01` (décider explicitement si l’étape suivante est la couche MCP V1, sans inventer de nouveau GO).
