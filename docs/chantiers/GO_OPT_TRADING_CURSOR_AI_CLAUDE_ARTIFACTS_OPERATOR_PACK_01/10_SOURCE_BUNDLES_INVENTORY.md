---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_OPERATOR_PACK_01_10_SOURCE_INVENTORY
doc_type: chantier/source_inventory
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/chantiers/GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01/
  - docs/chantiers/GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01/
  - bundles/README.md
  - bundles/CURSOR_AI_BUNDLES_REPRISE.md
---

# 10_SOURCE_BUNDLES_INVENTORY

Inventaire des artefacts Claude / IDE / cowork deja presents dans le repo et utilises comme sources pour ce pack.

## 1. IDE Bundle — `GO_LIVE_ARTIFACTS_CLAUDE_COWORK_IDE_BUNDLE_01`

| Fichier source | Contenu | Utilisation dans ce pack |
| --- | --- | --- |
| `00_BUNDLE_MANIFEST.md` | Manifeste du bundle IDE, invariants Claude | Source pour README, invariants |
| `01_IDE_HANDOFF.md` | Instructions handoff pour Trae / Claude / OpenCode | Source pour PROMPT_TEMPLATES (handoff) |

- **Statut** : MERGE (PR #201), branche supprimee
- **Machine** : cursor-ai
- **Type** : Bundle IDE documentaire

## 2. Claude cowork parent — `GO_OPT_TRADING_CLAUDE_COWORK_PARENT_LIVE_ARTIFACTS_01`

| Fichier source | Contenu | Utilisation dans ce pack |
| --- | --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Cadrage initial, architecture Live Artifacts, invariants | Source pour la philosophie read-only, role Cockpit vs Canon |
| `01_FULL_RESPONSE_CAPTURE.md` | Capture complete de reponse, prompt Attention Center, dashboard multi-sources | Source pour PROMPT_TEMPLATES, scoring P0/P1/P2 |
| `02_REMAINING_GAP.md` | Gaps securite, connecteurs, scoring, multi-machines | Source pour NO_COMMIT_RULES, regles read-only |

- **Statut** : MERGE (PR #201), branche supprimee
- **Machine** : cursor-ai
- **Note** : Matiere Claude cowork integree, non transformee en pack operateur avant ce GO

## 3. Bundles method — `bundles/`

| Fichier source | Contenu | Utilisation dans ce pack |
| --- | --- | --- |
| `README.md` | Index des bundles, conventions | Source pour les conventions de bundle |
| `CURSOR_AI_BUNDLES_REPRISE.md` | Reprise operateur cursor-ai, methode de creation de bundle | Source pour REPRISE_TEMPLATE, methode de creation |

- **Statut** : ACTIVE
- **Machine** : cursor-ai
- **Note** : Bundle method documentee, application partielle

## 4. Parent operational plan — `GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01`

| Fichier source | Contenu | Utilisation dans ce pack |
| --- | --- | --- |
| `80_NEXT_GO_SEQUENCE.md` | Sequence GO recommandee | Ce GO est la position 1 dans la sequence |
| `40_BUNDLES_OPERATIONAL_PLAN.md` | Plan Bundles | Lien Bundles / Claude artifacts |
| `50_CLAUDE_ARTIFACTS_OPERATOR_PLAN.md` | Plan candidat pour ce pack | Spec de depart de ce GO |

- **Statut** : MERGE (PR #205)
- **Machine** : cursor-ai

## Etat global des sources

| Source | Statut | Packagé avant ce GO |
| --- | --- | --- |
| IDE Bundle | MERGE | Non — documente mais non packagé |
| Claude cowork parent | MERGE | Non — matiere integree, non structuree |
| Bundles method | ACTIVE | Partiel — methode documentee, templates manquants |
| Parent operational plan | MERGE | N/A — plan, pas source |
