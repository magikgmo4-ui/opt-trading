# GO_OT_TRAE_SKILLS_V1_OPEN_01 — DÉCISION CANONIQUE (OUVERTURE SKILLS V1)

Date (America/Montreal) : 2026-04-11

## 1. Objet
Ouvrir explicitement la trajectoire Trae V1 par la couche **Skills V1** uniquement, après clôture de `GO_OT_TRAE_AGENTS_V1_OPEN_01`, en restant strictement doc-only (sans runtime, sans code) et sans ouvrir automatiquement MCP.

## 2. Contexte établi
- La couche Agents V1 est ouverte explicitement (doc-only) :
  - décision : `docs/ot/trae/OT_TRAE_AGENTS_V1_OPEN_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_AGENTS_V1_OPEN_01_CLOSING.txt`
- Le socle Skills V1 est déjà matérialisé dans le repo : `docs/ot/trae/04_SKILLS_V1.txt`
- Un gel pré‑V1 opposable (doc-only) existe déjà pour Skills :
  - décision : `docs/ot/trae/OT_TRAE_SKILLS_PRE_V1_GEL_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_SKILLS_V1_01_CLOSING.txt`
- L’ordre canonique V1 est : Rules -> Agents -> Skills -> MCP.

## 3. Décision canonique (ouverture Skills V1)
- La couche **Skills V1** est désormais considérée **ouverte explicitement** pour `opt-trading` (doc-only).
- Le socle normatif Skills V1 opposable est : `docs/ot/trae/04_SKILLS_V1.txt`.
- Cette ouverture Skills V1 ne constitue pas une ouverture MCP : elle prépare uniquement la couche suivante, qui reste à sélectionner explicitement.

## 4. Bornes opposables
- **Borne 1 (scope Skills uniquement)** : l’ouverture de Skills V1 n’implique aucune ouverture automatique de `MCP Policy`.
- **Borne 2 (doc-only)** : l’ouverture de Skills V1 est une bascule documentaire ; elle n’autorise ni n’exige aucun patch runtime ou code.
- **Borne 3 (opposabilité)** : toute mission Trae ultérieure est tenue de respecter `04_SKILLS_V1.txt` (skills bornés, inputs/outputs fixes, hors-scope explicite, non-invention).

## 5. Artefacts canoniques minimaux
- Socle Skills V1 : `docs/ot/trae/04_SKILLS_V1.txt`
- Décision d’ouverture : `docs/ot/trae/OT_TRAE_SKILLS_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_SKILLS_V1_OPEN_01_CLOSING.txt`
- Références opposables (pré‑requis / cohérence) :
  - `docs/ot/trae/OT_TRAE_AGENTS_V1_OPEN_DECISION_01.md`
  - `docs/ot/trae/OT_TRAE_SKILLS_PRE_V1_GEL_DECISION_01.md`

## 6. Conséquences (synchronisation)
- Le kanban, la synthèse, la reprise de session et la matrice des GO actifs doivent refléter :
  - Skills V1 = ouvert explicitement (Skills uniquement)
  - point de reprise suivant = `GO_OT_TRAE_MCP_POLICY_V1_OPEN_01` (sans lancement automatique)

## 7. Point de reprise
- `GO_OT_TRAE_MCP_POLICY_V1_OPEN_01`

## RISKS

- À qualifier.
