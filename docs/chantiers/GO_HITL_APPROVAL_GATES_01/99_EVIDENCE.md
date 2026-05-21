---
doc_id: GO_HITL_APPROVAL_GATES_01_EVIDENCE
doc_type: evidence
go_id: GO_HITL_APPROVAL_GATES_01
status: passed_with_evidence
---

# 99_EVIDENCE

## Preuve concrète de validation

### 1. Proposal packet
- `20_PROPOSAL_PACKET.md` — schéma complet (proposal_id, actor, surface, action, level, justification, risk, dry_run, rollback)
- Règles : L5+ dry-run obligatoire, L5+ dual confirm auto

### 2. Approval packet
- `30_APPROVAL_PACKET.md` — schéma complet (approver, decision, signature, conditions, escalation)
- Règles : caducité 24h, L6+ humain obligatoire, pas d'auto-approbation

### 3. Execution packet
- `40_EXECUTION_PACKET.md` — schéma complet (dry_run/live/rollback, commands, pre_checks)
- Règles : dry-run avant live, rollback command associée

### 4. Verification packet
- `50_VERIFICATION_PACKET.md` — schéma complet (checks, expected vs actual, overall_status, rollback_needed)
- Règles : vérification 5 min post-execution, rollback auto si FAIL

### 5. Approver roles
- `60_APPROVER_ROLES.md` — 3 rôles : human (L8), team_ai_manager (L5), safety_gate (L4)
- Escalade automatique L6+ → human, L8 → dual confirm

### 6. Dual confirm policy
- `70_DUAL_CONFIRM_POLICY.md` — actions L6+, écriture prod, permissions, déploiement, trading
- Délai 2h entre première et deuxième approbation

### 7. Write-gated scenario test

```bash
$ python3 scripts/ai/tests/hitl_scenarios.py
```

**Scenario 1 — L5 write-gated pipeline :**
- Proposal (L5, repo, PATCH_CONFIG) → team_ai_manager approve → dry-run → verify → live → final verify
- Toutes les étapes PASS

**Scenario 2 — L6 dual confirm :**
- Proposal (L6, Airtable, WRITE_RECORDS) → team_ai_manager auto-blocked → escalated → human_1 approve → human_2 confirm
- Dual confirm enforced

## Conclusion

Tous les critères de succès sont remplis (proposal→approve→execute→verify, dual confirm L6+). Statut : PASS_WITH_EVIDENCE.
