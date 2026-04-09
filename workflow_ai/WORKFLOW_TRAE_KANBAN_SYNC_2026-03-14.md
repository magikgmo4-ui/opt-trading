# Workflow — Sync Trae↔Kanban (OT)

Date (America/Montreal) : 2026-03-14

## 1. Objet
Décrire la procédure minimale et opposable de synchronisation entre :
- la progression réelle d’un chantier (décisions + clôture),
- le kanban OT (source of truth + synthèse),
- et le point de reprise de session.

Ce document ne remplace pas la doctrine gated : `workflow_ai/WORKFLOW.md`.

## 2. Règle de priorité (résolution des contradictions)
Si conflit, appliquer l’ordre suivant :
1) état réel prouvé (git + artefacts présents),
2) dernière clôture pertinente,
3) workflow (`workflow_ai/WORKFLOW.md`),
4) starter pack,
5) kanban.

## 3. Artefacts canoniques à synchroniser
- Kanban (source of truth) : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
- Synthèse opérationnelle : `docs/ot/kanban/opt_trading_kanban_operational_summary_2026-03-14.md`
- Clôtures : `docs/ot/closings/`
- Décisions Trae : `docs/ot/trae/OT_TRAE_*_DECISION_*.md`
- Reprise de session : `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md`

## 4. Quand déclencher la sync
Déclencher une sync si et seulement si au moins un des éléments suivants change :
- statut d’une brique (ex. “MATÉRIALISÉ” → “GELÉ (PRE‑V1, OPPOSABLE)”),
- preuve/justification canonique (décision ou clôture),
- suite / point de reprise,
- interdiction explicite (ne pas rouvrir / hors-scope),
- ordre des briques (si et seulement si acté).

## 5. Checklist de sync (doc-only)
1) Relire la dernière clôture pertinente sous `docs/ot/closings/`.
2) Vérifier que la décision associée existe (si changement “opposable” ou règle).
3) Mettre à jour le kanban source of truth (ligne(s) concernée(s) uniquement).
4) Mettre à jour la synthèse opérationnelle (mêmes lignes, même suite).
5) Mettre à jour la reprise de session si le point actif ou une interdiction de réouverture change.
6) Vérifier que la doc de référence pointe vers les bons fichiers (`docs/ot/README.md`, `docs/ot/trae/README.md` si nécessaire).

## 6. Interdits (dans la sync)
- Ne pas “inventer” un nouveau GO pour conclure une sync.
- Ne pas dégrader un statut opposable sans décision/clôture.
- Ne pas patcher code/runtime dans une sync.

## 7. Missions longues / multi-étapes
Modèle canonique : `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`.
