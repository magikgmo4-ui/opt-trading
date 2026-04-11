# GO_OT_TRAE_RULES_V1_OPEN_01 — DÉCISION CANONIQUE (OUVERTURE RULES V1)

Date (America/Montreal) : 2026-04-11

## 1. Objet
Ouvrir explicitement la trajectoire Trae V1 par la couche **Rules V1** uniquement, après clôture de `GO_OT_TRAE_STARTERPACK_GATING_PROOF_01`, en restant strictement doc-only (sans runtime, sans code) et sans ouvrir automatiquement Agents/Skills/MCP.

## 2. Contexte établi
- Le statut global Trae pré‑V1 est acté : `PRE_V1_COHERENT_AVEC_DELTAS_FINAUX`.
- La réserve sur l’adoption systématique du gating GO/STOP est bornée doc-only (preuve non consolidée, borne documentée).
- L’ordre canonique V1 est : Rules -> Agents -> Skills -> MCP.

## 3. Décision canonique (ouverture Rules V1)
- La couche **Rules V1** est désormais considérée **ouverte explicitement** pour `opt-trading`.
- Le socle normatif Rules V1 opposable est : `docs/ot/trae/01_RULES_V1.txt`.

## 4. Bornes opposables
- **Borne 1 (scope Rules uniquement)** : l’ouverture de Rules V1 n’implique aucune ouverture automatique des couches `Agents`, `Skills` ou `MCP Policy`.
- **Borne 2 (doc-only)** : l’ouverture de Rules V1 est une bascule de gouvernance documentaire ; elle n’autorise ni n’exige aucun patch runtime ou code.
- **Borne 3 (opposabilité)** : toute mission Trae ultérieure est tenue de respecter `01_RULES_V1.txt` (sources de vérité, non-invention, certitudes, contradictions, preuve avant conclusion, point de reprise).

## 5. Artefacts canoniques minimaux
- Socle Rules V1 : `docs/ot/trae/01_RULES_V1.txt`
- Décision d’ouverture : `docs/ot/trae/OT_TRAE_RULES_V1_OPEN_DECISION_01.md`
- Closing : `docs/ot/closings/OT_TRAE_RULES_V1_OPEN_01_CLOSING.txt`

## 6. Conséquences (synchronisation)
- Le kanban doit refléter l’ouverture Rules V1 et déplacer le point actif vers l’ouverture explicite de la couche suivante (Agents), sans lancement automatique.

## 7. Point de reprise
- `GO_OT_TRAE_AGENTS_V1_OPEN_01`
