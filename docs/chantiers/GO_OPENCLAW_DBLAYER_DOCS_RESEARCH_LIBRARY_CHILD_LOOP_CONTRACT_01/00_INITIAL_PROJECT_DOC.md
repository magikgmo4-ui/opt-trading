---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01_INIT
doc_type: initial_project_doc
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
status: open
created_at: 2026-05-30
---

# 00_INITIAL_PROJECT_DOC — Child Loop Contract

## 1_MASTER_TARGET

Formaliser la boucle ChatGPT ↔ OpenClaw ↔ IDE en 4 formats contractuels + 1 gate
humain, de sorte que chaque segment de la boucle ait un schéma d'entrée/sortie
défini, reproductible et vérifiable.

## 2_PARENT

```
GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
GAP 3 : boucle ChatGPT ↔ OpenClaw ↔ IDE pas encore contractuelle
```

Parent : open — ne pas fermer.

## 3_BOUCLE_CIBLE

```
ChatGPT (gouvernance)
  │
  │ FORMAT 1 — job spec
  ▼
OpenClaw (orchestrateur)
  │
  │ FORMAT 2 — instruction structurée
  ▼
IDE / agent / job (exécution)
  │
  │ FORMAT 3 — résultat structuré
  ▼
OpenClaw (orchestrateur)
  │
  │ FORMAT 4 — synthèse + gate humain
  ▼
ChatGPT (gouvernance)
  │
  │ FORMAT 5 — validation humaine (APPROVE / REJECT / RESTART)
  ▼
[relance ou clôture]
```

## 4_SCOPE

Ce child se limite à :

- Définir les 5 formats contractuels (schémas + templates)
- Documenter les règles de validation à chaque segment
- Identifier les champs obligatoires vs optionnels
- Poser les modes d'échec par segment
- 0 runtime modifié — doc-only

## 5_DELIVERABLES

| Fichier | Contenu |
| --- | --- |
| `docs/openclaw/loop_contract/INDEX.md` | Vue d'ensemble boucle + liens |
| `docs/openclaw/loop_contract/01_chatgpt_to_openclaw.md` | FORMAT 1 — job spec ChatGPT → OpenClaw |
| `docs/openclaw/loop_contract/02_openclaw_to_ide.md` | FORMAT 2 — instruction OpenClaw → IDE |
| `docs/openclaw/loop_contract/03_ide_to_openclaw.md` | FORMAT 3 — résultat IDE → OpenClaw |
| `docs/openclaw/loop_contract/04_openclaw_to_chatgpt.md` | FORMAT 4 — synthèse OpenClaw → ChatGPT |
| `docs/openclaw/loop_contract/05_human_gate.md` | FORMAT 5 — gate humain validation |

## 6_INVARIANTS

- Doc-only — 0 ligne de code modifiée
- Pas de nouveau parent OpenClaw
- Index globaux non touchés
- Parent non fermé
- PR gated obligatoire

## 7_ACCEPTANCE_CRITERIA

```
5 fichiers loop_contract/ produits avec schéma + template + modes d'échec
INDEX.md boucle navigable
20_ACCEPTANCE_REPORT.md rédigé et validé opérateur
```

## 17_RESUME_POINT

```
Branch: go/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_LOOP_CONTRACT_01
Étape courante: docs/openclaw/loop_contract/ à créer
```
