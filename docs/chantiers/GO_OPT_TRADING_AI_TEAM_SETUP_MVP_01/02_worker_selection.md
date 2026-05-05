---
doc_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01_WORKER_SELECTION
doc_type: spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_AI_TEAM_SETUP_MVP_01
status: open
lifecycle_stage: spec
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CANON_01/01_architecture_cible.md
---

# 02_WORKER_SELECTION — Selection des 3 workers MVP

## Workers retenus

Les 3 workers selectionnes pour le MVP sont les 3 roles les plus proches du read-only, sans risque d'ecriture, alignes sur le contrat Strict Workers :

| Role | Tache MVP | Justification |
|:-----|:----------|:--------------|
| **Observer** | READ_INVENTORY : lister les chantiers actifs, leur etat, leurs GO | Role exclusivement read-only. Premier worker a qualifier car sans risque. |
| **Documenter** | Produire un rapport structure (DRAFT_ONLY) a partir de la sortie Observer | Read-only + output draft. Ne modifie rien, produit une synthese. |
| **Gatekeeper** | Verifier que la sortie Documenter respecte le contrat Strict Workers | Validation HITL, pas d'ecriture automatique. Derniere barriere avant suite. |

## Workers differes

| Role | Raison du report |
|:-----|:-----------------|
| Orchestrator / Supervisor | Necessite un graphe de taches + handoffs. Deferre au MVP suivant. |
| Analyzer / Reasoner | Necessite PATCH_DRAFT (write draft). Deferre apres validation read-only. |

## Sequence d'execution MVP

```
Observer (READ_INVENTORY) → Documenter (DRAFT synthese) → Gatekeeper (validation HITL)
```

Chaque etape produit une sortie DRAFT_ONLY. Aucune ecriture Git. Le Gatekeeper est l'operateur humain qui valide la sortie finale.

## Mapping des workers vers le contrat Strict Workers

| Worker | tasks.index.json entry | Type autorise | Modele VERIFIED |
|:-------|:-----------------------|:--------------|:----------------|
| Observer | `observer_read_inventory_01` | READ_INVENTORY | opencode-go/deepseek-v4-pro |
| Documenter | `documenter_draft_synthesis_01` | DOC_DRAFT | opencode-go/deepseek-v4-pro |
| Gatekeeper | `gatekeeper_validate_output_01` | GATEKEEPER_VALIDATE | opencode-go/deepseek-v4-pro |

## Selection des modeles

Pour le MVP, un seul modele VERIFIED est requis (le modele courant) :
- `opencode-go/deepseek-v4-pro` : modele actif sur fantome, deja verifie

Les 6 modeles pending (MiMo-V2, DeepSeek V4, etc.) sont differes.
