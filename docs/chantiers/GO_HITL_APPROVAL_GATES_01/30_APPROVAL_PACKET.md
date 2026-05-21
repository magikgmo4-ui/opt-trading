---
doc_id: GO_HITL_APPROVAL_GATES_01_APPROVAL
doc_type: hitl_packet
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 30_APPROVAL_PACKET.md

## Objectif

Packet de décision (approbation ou rejet) émis par un approver humain ou AI manager.

## Schéma

```yaml
approval_id: uuid                        # généré par l'approver
proposal_id: uuid                        # référence au proposal
approver_id: string                      # identifiant de l'approver
approver_role: string                    # human | team_ai_manager | safety_gate
decision: "approved" | "rejected" | "escalated"
decision_ts: ISO8601                     # timestamp de la décision
conditions:
  - dry_run_executed: boolean
  - dual_confirm_required: boolean
  - manual_review_notes: string | null
signature:
  method: "manual_confirm" | "telegram_btn" | "cms_approve" | "emergency_override"
  proof: string                          # hash ou reference de la preuve
rejection_reason: string | null          # si decision = rejected
escalation_target: string | null         # si decision = escalated
```

## Règles

- L'approbation est caduque après 24h (expiration)
- Un approver ne peut pas approuver ses propres proposals
- Niveau L6+ nécessite approbation humaine obligatoire (AI manager ne suffit pas)
- La signature inclut la méthode de preuve (bouton Telegram, CMS, override d'urgence)
