---
doc_id: GO_HITL_APPROVAL_GATES_01_PROPOSAL
doc_type: hitl_packet
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 20_PROPOSAL_PACKET.md

## Objectif

Packet de proposition d'action à soumettre au circuit HITL. Représente la demande initiale avant toute exécution.

## Schéma

```yaml
proposal_id: uuid                        # généré par l'émetteur
proposal_version: "1.0"
actor_id: string                         # émetteur (strict_worker, specialist, manager)
surface_id: string                       # surface cible (repo, Telegram, Airtable, etc.)
action_id: string                        # action demandée
action_level: int                        # niveau de risque L0-L8
justification: string                    # pourquoi cette action est nécessaire
risk_assessment: string                  # évaluation du risque (none/low/medium/high/critical)
dry_run_first: boolean                   # dry-run obligatoire avant exécution réelle
rollback_plan: string | null             # plan de rollback si échec
dependencies: list[string]              # actions prérequises
proposal_ts: ISO8601                     # timestamp de création
status: "pending"                        # pending | approved | rejected | cancelled
```

## Règles

- Un proposal ne peut pas être modifié après soumission
- Le niveau L5+ nécessite automatiquement dual confirm
- Un proposal sans `dry_run_first: true` pour L4+ est rejeté automatiquement
- L'`action_level` doit correspondre à la permission matrix (`skill_policy.yaml`)
