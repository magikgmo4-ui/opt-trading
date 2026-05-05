---
doc_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01_V2_SPEC
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_MVP_V2_ORCHESTRATOR_ANALYZER_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 01_V2_SPEC — MVP v2 Orchestrator + Analyzer

## Nouveaux roles

| Role | Task Type | Description |
|:-----|:----------|:------------|
| **Analyzer** | `ANALYZE_INVENTORY` | Lit la sortie Observer, classifie les chantiers par domaine/statut, extrait des patterns, produit une synthèse structurée |
| **Orchestrator** | `ORCHESTRATOR_CHAIN` | Chaîne des sous-tâches séquentielles, transmet les sorties intermédiaires, ne fait aucun git write |

## Chaîne MVP v2

```
┌─────────────────┐     ┌─────────────────────┐     ┌──────────────┐
│ READ_INVENTORY  │ ──► │ ANALYZE_INVENTORY   │ ──► │ DOC_DRAFT    │
│ (Observer)      │     │ (Analyzer)          │     │ (Documenter) │
└─────────────────┘     └─────────────────────┘     └──────────────┘
        │                        │                         │
        ▼                        ▼                         ▼
  observer_output       analyze_output              final_draft
  (drafts/)             (drafts/)                   (drafts/)
                                                        │
                                              ┌─────────▼──────────┐
                                              │ Gatekeeper (HITL)  │
                                              │ validation humaine │
                                              └────────────────────┘
```

## ANALYZE_INVENTORY spec

L'Analyzer prend en entrée la sortie brute de l'Observer et produit :

```markdown
# ANALYZE_INVENTORY — Analyse structurelle

## 13_ESTABLISHED
- Nombre total de chantiers : N
- Domaines identifiés : AI Team, Trading, Réseau, Registry, UI, Infra, Gouvernance, Divers
- Chantiers avec closeout : X (statut = CLOS)
- Chantiers sans closeout : Y (statut = ACTIVE)
- Fichiers par chantier : min/M, max/X, moyenne/Y

## 14_HYPOTHESIS
- Patterns de nommage
- Relations parent/enfant probables
- Domaines sur-représentés / sous-représentés

## 15_REMAINING_GAP
- Chantiers non classifiables
- Absences détectées

## 16_TODO
- Recommandations de consolidation
- Prochains GO suggérés

## VERDICT_DRAFT_ONLY
```

## ORCHESTRATOR_CHAIN spec

L'Orchestrator est un meta-task. Il charge un `chain` de sous-tâches et les exécute séquentiellement. Chaque sous-tâche produit un fichier intermédiaire dans `drafts/`. Si une sous-tâche échoue (exit != 0), la chaîne s'arrête.

```json
{
  "task_type": "ORCHESTRATOR_CHAIN",
  "chain": [
    {"task_packet": "tasks/read_inventory.json", "output_tag": "observer"},
    {"task_packet": "tasks/analyze_inventory.json", "output_tag": "analyzer"},
    {"task_packet": "tasks/observer_doc_draft.json", "output_tag": "doc"}
  ]
}
```

## Contrat Strict Workers

Tous les task types respectent le même contrat :
- no_secrets, no_env_files, no_git_write_ops
- no_runtime_write_by_default
- output_status: DRAFT_ONLY
- requires_external_validation
- only_verified_models
- denied_inputs / denied_commands

## Fichiers produits

Tous les fichiers de sortie sont dans `modules/ai_team_mvp/drafts/` :
- `.observer_output_last.txt` — sortie brute Observer
- `analyze_inventory_01_<ts>.md` — analyse structurée
- `documenter_draft_synthesis_01_<ts>.md` — brouillon final
