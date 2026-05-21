---
doc_id: GO_HITL_APPROVAL_GATES_01_EXECUTION
doc_type: hitl_packet
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 40_EXECUTION_PACKET.md

## Objectif

Packet d'exécution d'une action approuvée, incluant dry-run et rollback.

## Schéma

```yaml
execution_id: uuid                       # généré au moment de l'exécution
approval_id: uuid                        # référence à l'approval
proposal_id: uuid                        # référence au proposal
actor_id: string                         # exécutant
surface_id: string                       # surface cible
action_id: string                        # action exécutée
mode: "dry_run" | "live" | "rollback"
commands:
  - type: string                         # shell | api | patch | bridge_write
    target: string                       # cible de la commande
    payload: string                      # contenu de la commande
    rollback_command: string | null      # commande de rollback associée
environment: string                      # production | staging | dry-run
pre_checks:
  - check: string                        # vérification pré-exécution
    status: "PASS" | "FAIL"
    detail: string
execution_ts: ISO8601
status: "pending" | "running" | "success" | "failed" | "rolled_back"
result: string | null                    # résultat brut
error_log: list[string]                 # logs d'erreur
```

## Règles

- Toute exécution live doit d'abord passer par un dry-run réussi
- Si `mode: rollback`, la commande de rollback est exécutée
- L'exécution sans approval valide est interdite
- Le résultat est conservé pour la verification packet
