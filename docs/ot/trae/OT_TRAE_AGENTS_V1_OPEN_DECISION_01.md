# GO_OT_TRAE_AGENTS_V1_OPEN_01 — DÉCISION CANONIQUE (OUVERTURE AGENTS V1)

Date (America/Montreal) : 2026-04-11

## 1. Objet
Ouvrir explicitement la trajectoire Trae V1 par la couche **Agents V1** uniquement, après clôture de `GO_OT_TRAE_RULES_V1_OPEN_01`, en restant strictement doc-only (sans runtime, sans code) et sans ouvrir automatiquement Skills/MCP.

## 2. Contexte établi
- La couche Rules V1 est ouverte explicitement (doc-only) :
  - décision : `docs/ot/trae/OT_TRAE_RULES_V1_OPEN_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_RULES_V1_OPEN_01_CLOSING.txt`
- Le socle Agents V1 est déjà matérialisé dans le repo : `docs/ot/trae/02_AGENTS_V1.txt`
- Un gel pré‑V1 opposable (doc-only) existe déjà pour Agents :
  - décision : `docs/ot/trae/OT_TRAE_AGENTS_PRE_V1_GEL_DECISION_01.md`
  - closing : `docs/ot/closings/OT_TRAE_AGENTS_V1_01_CLOSING.txt`
- L’ordre canonique V1 est : Rules -> Agents -> Skills -> MCP.

## 3. Décision canonique (ouverture Agents V1)
- La couche **Agents V1** est désormais considérée **ouverte explicitement** pour `opt-trading` (doc-only).
- Le socle normatif Agents V1 opposable est : `docs/ot/trae/02_AGENTS_V1.txt`.
- Cette ouverture Agents V1 **ne remplace pas** le gel pré‑V1 Agents existant ; elle le rend simplement opposable comme couche suivante ouverte (après Rules).

## 4. Bornes opposables
- **Borne 1 (scope Agents uniquement)** : l’ouverture de Agents V1 n’implique aucune ouverture automatique de `Skills` ni de `MCP Policy`.
- **Borne 2 (doc-only)** : l’ouverture de Agents V1 est une bascule documentaire ; elle n’autorise ni n’exige aucun patch runtime ou code.
- **Borne 3 (opposabilité)** : toute mission Trae ultérieure est tenue de respecter `02_AGENTS_V1.txt` (obligations minimales des rôles, sorties attendues, non-invention, scope, preuve, point de reprise).

## 5. Artefacts canoniques minimaux
- Socle Agents V1 : `docs/ot/trae/02_AGENTS_V1.txt`
- Décision d’ouverture : `docs/ot/trae/OT_TRAE_AGENTS_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_AGENTS_V1_OPEN_01_CLOSING.txt`
- Références opposables (pré‑requis / cohérence) :
  - `docs/ot/trae/OT_TRAE_RULES_V1_OPEN_DECISION_01.md`
  - `docs/ot/trae/OT_TRAE_AGENTS_PRE_V1_GEL_DECISION_01.md`

## 6. Conséquences (synchronisation)
- Le kanban, la synthèse, la reprise de session et la matrice des GO actifs doivent refléter :
  - Agents V1 = ouvert explicitement (Agents uniquement)
  - point de reprise suivant = `GO_OT_TRAE_SKILLS_V1_OPEN_01` (sans lancement automatique)

## 7. Point de reprise
- `GO_OT_TRAE_SKILLS_V1_OPEN_01`
