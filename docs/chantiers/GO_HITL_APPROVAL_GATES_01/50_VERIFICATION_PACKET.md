---
doc_id: GO_HITL_APPROVAL_GATES_01_VERIFICATION
doc_type: hitl_packet
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 50_VERIFICATION_PACKET.md

## Objectif

Packet de vérification post-exécution. Confirme que l'action a eu l'effet attendu.

## Schéma

```yaml
verification_id: uuid                    # généré par le vérificateur
execution_id: uuid                       # référence à l'execution
approval_id: uuid                        # référence à l'approval
proposal_id: uuid                        # référence au proposal
verifier_id: string                      # entité qui vérifie
verification_ts: ISO8601
checks:
  - check_name: string                   # nom de la vérification
    expected: string                     # résultat attendu
    actual: string                       # résultat réel
    status: "PASS" | "FAIL" | "WARN"
    evidence: string                     # preuve (log, screenshot, hash)
overall_status: "PASS" | "FAIL" | "PARTIAL"
post_conditions:
  - condition: string
    status: boolean
rollback_needed: boolean                 # true si verification FAIL
rollback_executed: boolean               # true si rollback fait
audit_log: string                        # chemin vers le log d'audit
```

## Règles

- La vérification est obligatoire dans les 5 minutes suivant l'exécution
- Si `overall_status = FAIL` et `rollback_needed = true`, le rollback est automatique
- Le résultat est envoyé au ledger (G06) pour traçabilité
