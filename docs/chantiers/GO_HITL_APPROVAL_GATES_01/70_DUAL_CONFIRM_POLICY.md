---
doc_id: GO_HITL_APPROVAL_GATES_01_DUAL_CONFIRM
doc_type: hitl_policy
go_id: GO_HITL_APPROVAL_GATES_01
status: draft
---

# 70_DUAL_CONFIRM_POLICY.md

## Principe

Certaines actions nécessitent deux approbations indépendantes avant exécution (dual confirm).

## Actions concernées

Toute action avec `action_level >= 6` ou appartenant à ces catégories :

- Écriture sur production (write_gated sur surfaces critiques)
- Modification de permissions/ACL
- Déploiement de nouveaux workers
- Opérations financières ou trading
- Modification de la machine_runtime_map

## Processus

1. Approver 1 examine et approuve le proposal → `status: approved_pending_second`
2. Approver 2 (rôle différent) examine et confirme → `status: dual_confirmed`
3. L'exécution n'est autorisée qu'après dual confirm
4. Si Approver 2 rejette → `status: rejected` (retour à l'émetteur)

## Délais

- Dual confirm doit être complété dans les 2h suivant la première approbation
- Passé ce délai, le proposal expire et doit être resoumis
