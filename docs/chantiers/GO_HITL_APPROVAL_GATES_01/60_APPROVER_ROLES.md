---
doc_id: GO_HITL_APPROVAL_GATES_01_ROLES
doc_type: hitl_policy
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 60_APPROVER_ROLES.md

## Rôles approvers

| Role | Niveau max | Domaine | Méthode signature |
|---|---|---|---|
| `human` | L8 (tous) | Tous les domaines | Telegram btn, CMS approve, manual confirm |
| `team_ai_manager` | L5 | Automation, drafts, lecture | Auto-approve si règles respectées |
| `safety_gate` | L4 | Tous (lecture seule jusqu'à L4) | Vérification automatique des préconditions |

## Règles d'escalade

- L6+ → passe de `team_ai_manager` → `human` (escalade automatique)
- L8 → passe de `human` → `second_human` (dual confirm obligatoire)
- Tout rejet peut être escaladé à un rôle supérieur
- L'approbation automatique par `team_ai_manager` est limitée aux actions L0-L5
