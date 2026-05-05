---
doc_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01_LOCAL_OLLAMA_LINK
doc_type: link
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01
status: open
lifecycle_stage: link
topic_keys:
  - opt-trading
  - machine_parent
  - student
  - local_ollama
  - link
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
point_de_reprise: "Lien etabli"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01 — 40_LOCAL_OLLAMA_LINK

## Lien vers le parent Local Ollama existant

Le parent `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` est la racine de la famille Local Ollama.
Il est rattache a la machine `student` via l'arbitrage `OLLAMA = student`.

```text id="local_ollama_link"
Machine : student
Famille rattachee : GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
Branche : go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01
Dossier : docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/
```

## Contenu du parent Local Ollama

Le parent Local Ollama contient les documents suivants (inventaire de branche) :

| Fichier | Description |
|---------|-------------|
| `00_START.md` | Cadrage initial du parent |
| `00_PARENT_CADRAGE.md` | Cadrage parent detaille |
| `01_SYNTHESE_OLLAMA_LOCAL.md` | Synthese Ollama local |
| `02_MACHINE_QUALIFICATION_PLAN.md` | Plan de qualification machine |
| `03_SECURITY_BASELINE.md` | Baseline securite |
| `04_INTEGRATION_MAP.md` | Carte d'integration |
| `05_INFRA_RANKING_AND_USAGE.md` | Classement et usage infra |
| `06_COMMIT_TRANSFER_INVENTORY.md` | Inventaire transfert commit |
| `06_DECISION_LAB_STUDENT_OPENCLAW_ORCHESTRATION.md` | Decision orchestration lab |
| `07_LAB_USAGE_SCOPE.md` | Perimetre d'usage du lab |
| `10_LOCAL_OLLAMA_PARENT_STATE.md` | Etat du parent Local Ollama |
| `20_STUDENT_RUNTIME_MAPPING.md` | Mapping runtime student |
| `30_OPENCLAW_LAB_DEFERRED_BOUNDARY.md` | Frontiere differee OpenClaw Lab |
| `40_INDEX_CANONICALIZATION_GAPS.md` | Gaps d'indexation canonique |
| `90_CLOSEOUT.md` | Closeout du parent |
| `90_PARENT_CHECKPOINT.md` | Checkpoint du parent |

## Statut

Le parent Local Ollama est `branch-only` (non agrege dans les index globaux).
Le GO enfant `GO_OPT_TRADING_STUDENT_LOCAL_OLLAMA_PARENT_RECONCILIATION_01` devra :
1. Lire le contenu du parent Local Ollama.
2. Etablir la continuite documentaire entre le parent famille et le parent machine.
3. Preparer l'agregation des index.

## Verdict

Lien etabli. Le parent Local Ollama est reference, non modifie.
