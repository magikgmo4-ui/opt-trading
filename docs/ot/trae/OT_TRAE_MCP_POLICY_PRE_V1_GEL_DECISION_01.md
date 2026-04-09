# GO_OT_TRAE_MCP_POLICY_V1_01 — DÉCISION CANONIQUE (GEL PRÉ-V1 MCP POLICY)

Date (America/Montreal) : 2026-04-09

## 1. Objet
Acter, de manière strictement doc-only, si le bloc “MCP Policy V1” doit être gelé en pré‑V1 de façon opposable, sans toucher au runtime, au code, ni dériver vers un chantier non borné.

## 2. Éléments établis (preuves)
- Le socle pré‑V1 est déjà matérialisé dans le repo sous `docs/ot/trae/` (dont `05_RUNTIME_MCP_POLICY_V1.txt`).
- Le kanban canonique indique : `MCP Policy V1` = `ÉTABLI / MATÉRIALISÉ (PRE-V1)` avec suite `revue + gel pré-V1`.
- `05_RUNTIME_MCP_POLICY_V1.txt` explicite déjà les distinctions obligatoires “ÉTABLI vs À CONFIRMER”, la doctrine “runtime réel d’abord”, et la politique MCP comme couche d’outillage (pas de gouvernance).

## 3. Constat (ce qui manque)
- Le kanban ne distingue pas explicitement “pré‑V1 matérialisé” de “pré‑V1 gelé/opposable” pour `MCP Policy V1`.
- Le document contient des points explicitement “À CONFIRMER avant gel final” (mapping rôle ↔ agent runtime, sous-dossier Windows, etc.). Le gel pré‑V1 doc-only doit conserver ces statuts et ne pas les convertir en “ÉTABLI”.

## 4. Décision canonique
- Le gel pré‑V1 **opposable** est acté pour `MCP Policy V1` sur la base du fichier `docs/ot/trae/05_RUNTIME_MCP_POLICY_V1.txt`.
- Portée du gel : uniquement `MCP Policy` (ce document). Aucune exécution MCP n’est autorisée dans ce cadre.
- Le gel est doc-only : aucune modification de runtime, de scripts ou de modules n’est autorisée dans ce cadre.

## 5. Artefacts doc-only requis
- Décision : `docs/ot/trae/OT_TRAE_MCP_POLICY_PRE_V1_GEL_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_MCP_POLICY_V1_01_CLOSING.txt`
- Alignement kanban :
  - `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
  - `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`

## 6. Conséquences
- Le bloc `MCP Policy V1` devient “pré‑V1 gelé/opposable” (doc-only).
- Toute évolution ultérieure de `05_RUNTIME_MCP_POLICY_V1.txt` doit passer par une mission explicite, avec preuves et mise à jour kanban si un statut/suite change.

## 7. Point de reprise
- Suite recommandée : `GO_OT_NEXT_MISSION_SELECTION_01` (sélectionner la suite sans inventer de nouveau GO).
