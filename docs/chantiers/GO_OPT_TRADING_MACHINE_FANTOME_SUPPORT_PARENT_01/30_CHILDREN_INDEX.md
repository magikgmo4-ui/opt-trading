---
doc_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01_CHILDREN_INDEX
doc_type: children_index
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01
status: open
lifecycle_stage: children_index
topic_keys:
  - opt-trading
  - machine_parent
  - fantome
  - children_index
  - ai_team
  - strict_workers
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
point_de_reprise: "Children cadres"
updated_at: 2026-05-05
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/00_START.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/10_MACHINE_SCOPE.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01/20_EXISTING_BRANCHES_INVENTORY.md
---

# GO_OPT_TRADING_MACHINE_FANTOME_SUPPORT_PARENT_01 — 30_CHILDREN_INDEX

## GO enfants proposes

### GO_CHILD_01 — Reconciliation AI Team + Strict Workers (IMMEDIAT)

```yaml
go_id: GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01
statut: a_ouvrir
priorite: P1
branche_proposee: go/GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01
objectif: |
  Reconciller :
  - GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01 (KEEP_ACTIVE)
  - GO_OPT_TRADING_STRICT_WORKERS_PARENT_01 (a auditer)
  avec le parent machine fantome.
dependance: aucun (GO courant)
```

### GO_CHILD_02 — Audit Strict Workers

```yaml
go_id: GO_OPT_TRADING_FANTOME_STRICT_WORKERS_AUDIT_01
statut: a_ouvrir_apres_reconciliation
priorite: P2
branche_proposee: go/GO_OPT_TRADING_FANTOME_STRICT_WORKERS_AUDIT_01
objectif: |
  Auditer completement le parent Strict Workers avant promotion :
  - verifier le contenu documentaire ;
  - valider les smoke reports ;
  - controler les modeles et configurations ;
  - decider de la promotion ou correction.
dependance: GO_CHILD_01 (reconciliation)
```

### GO_CHILD_03a — Reprise implementation Strict Workers

```yaml
go_id: GO_OPT_TRADING_FANTOME_STRICT_WORKERS_IMPL_REPRISE_01
statut: candidat
priorite: P3
branche_proposee: go/GO_OPT_TRADING_FANTOME_STRICT_WORKERS_IMPL_REPRISE_01
objectif: |
  Reprendre l'implementation des Strict Workers apres audit reussi.
  Repartir de l'etat etabli dans le parent Strict Workers.
dependance: GO_CHILD_02 (audit)
```

### GO_CHILD_03b — AI Team worker runtime review

```yaml
go_id: GO_OPT_TRADING_FANTOME_AI_TEAM_WORKER_RUNTIME_REVIEW_01
statut: candidat_alternatif
priorite: P3
branche_proposee: go/GO_OPT_TRADING_FANTOME_AI_TEAM_WORKER_RUNTIME_REVIEW_01
objectif: |
  Reviser le runtime worker de l'AI Team.
  Alternative a GO_CHILD_03a si l'audit Strict Workers n'est pas prioritaire.
dependance: GO_CHILD_01 (reconciliation)
```

## Ordre recommande

```text id="fantome_go_order"
1. GO_OPT_TRADING_FANTOME_AI_TEAM_STRICT_WORKERS_RECONCILIATION_01 (P1, immediat)
2. GO_OPT_TRADING_FANTOME_STRICT_WORKERS_AUDIT_01 (P2, apres reconciliation)
3. GO_OPT_TRADING_FANTOME_STRICT_WORKERS_IMPL_REPRISE_01 (P3, candidat)
   OU
   GO_OPT_TRADING_FANTOME_AI_TEAM_WORKER_RUNTIME_REVIEW_01 (P3, candidat alternatif)
```

La decision entre GO_CHILD_03a et GO_CHILD_03b dependra de ce que la reconciliation etablit.

## Verdict

Children cadres. Le GO_CHILD_01 (reconciliation) est le prochain GO immediat.
Aucun child n'est ouvert dans ce parent.
