# GO_OT_TRAE_AGENTS_V1_01 — DÉCISION CANONIQUE (GEL PRÉ-V1 AGENTS)

Date (America/Montreal) : 2026-04-09

## 1. Objet
Acter, de manière strictement doc-only, si le bloc “Agents Trae V1” doit être gelé en pré‑V1 de façon opposable, sans ouvrir les couches Skills/MCP, et sans toucher au runtime ni au code.

## 2. Éléments établis (preuves)
- Le socle pré‑V1 est déjà matérialisé dans le repo sous `docs/ot/trae/` (dont `02_AGENTS_V1.txt`).
- Le kanban canonique indiquait au départ : `Agents Trae V1` = `ÉTABLI / MATÉRIALISÉ (PRE-V1)` avec suite `revue + gel pré-V1`.
- Les règles communes de non-invention, scope strict, preuve et point de reprise sont déjà gelées côté Rules (pré‑V1 opposable) et applicables à ce chantier.

## 3. Constat (ce qui manque)
- Le statut “gel pré‑V1 opposable” doit être appuyé par une décision et une clôture doc-only explicites (traçabilité opposable).
- `09_GEL_PRE_V1_RECAP_V0` liste encore des points à confirmer avant un gel V1 final (notamment le mapping runtime exact rôle ↔ agent). Ce point est hors périmètre du gel Agents doc-only : il relève de la couche runtime/policy, pas de la définition minimale des rôles.

## 4. Décision canonique
- Le gel pré‑V1 **opposable** est acté pour `Agents Trae V1` sur la base du fichier `docs/ot/trae/02_AGENTS_V1.txt`.
- Portée du gel : uniquement `Agents` (ce document). Aucune ouverture implicite de `Skills` ou `MCP`.
- Le gel est doc-only : aucune modification de runtime, de scripts ou de modules n’est autorisée dans ce cadre.

## 5. Artefacts doc-only requis
- Décision : `docs/ot/trae/OT_TRAE_AGENTS_PRE_V1_GEL_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_AGENTS_V1_01_CLOSING.txt`
- Alignement kanban :
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`

## 6. Conséquences
- Le bloc `Agents Trae V1` devient “pré‑V1 gelé/opposable” (doc-only).
- Toute évolution ultérieure de `02_AGENTS_V1.txt` doit passer par une mission explicite, avec preuves et mise à jour kanban si un statut/suite change.

## 7. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01` (décider explicitement si ouverture de la couche Skills V1, sans inventer de nouveau GO).

## RISKS

- À qualifier.
