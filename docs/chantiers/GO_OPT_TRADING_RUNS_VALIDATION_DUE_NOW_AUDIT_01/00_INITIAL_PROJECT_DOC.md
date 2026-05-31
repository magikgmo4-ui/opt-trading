---
doc_id: GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01
status: active
source_kind: canonical
created_at: 2026-05-30
updated_at: 2026-05-30
GO_ID: GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: null
MASTER_TARGET_ID: null
MASTER_PROJECT_PLAN_ID: null
PARENT_GO_ID: GO_OPT_TRADING_RUNS_VALIDATION_BACKLOG_CANONICALIZE_01
NEXT_ATTACH_TARGET: null
6_FINAL_TARGET: auditer et preparer le traitement des lignes DUE_NOW du ledger canonical runs validation backlog
BUNDLE_TARGET: docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01/10_DUE_NOW_AUDIT_REPORT.md
TRANSPORT_MODE: none
CLOSE_GATE_MASTER_TARGET: not_applicable
topic_keys:
  - runs
  - validation
  - due_now
  - strict_workers
  - openclaw
  - github_actions
  - operator_packet
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
links:
  - docs/index/RUNS_VALIDATION_BACKLOG_01.md
  - docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01/10_DUE_NOW_AUDIT_REPORT.md
  - docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01/20_OPERATOR_RUNTIME_PACKET.md
  - docs/index/inbox/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01.md
---

# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Transformer les lignes `DUE_NOW` du registre `docs/index/RUNS_VALIDATION_BACKLOG_01.md` en actions de verification clairement executables, sans inventer de preuve runtime et sans fermer de parent.

## 3_INITIAL_NEED

L'utilisateur a valide le prochain mouvement logique : ouvrir le ledger, traiter les lignes `DUE_NOW` dans l'ordre, puis passer aux blockers CI et au gate Fleet Health planifie.

Ordre valide :

```text
1. PHASE_01_STRICT_WORKER_READONLY_SMOKE
2. PHASE_5_DBLAYER_TO_FANTOME_OPENCLAW_REMOTE_EXEC
3. GitHub Actions BLOCKED_BY_CI_SCOPE / BLOCKED_BY_PRECHECK
4. Fleet Health Phase 1 le 2026-05-30 09:00
```

## 4_MASTER_PROJECT_PLAN

1. Lire le ledger mergé sur `sot/mainline`.
2. Requalifier la première ligne DUE_NOW : strict-worker-readonly-smoke.
3. Requalifier la deuxième ligne DUE_NOW : OpenClaw db-layer -> fantome.
4. Relever les blockers CI disponibles via GitHub Actions.
5. Produire un packet opérateur reproductible pour les runs qui exigent accès runtime/machine.
6. Ne pas modifier les index globaux.
7. Ne pas relancer les workflows CI ni exécuter de runtime depuis le connecteur GitHub.

## 6_FINAL_TARGET

Livrer :

- un rapport d'audit DUE_NOW ;
- un packet opérateur avec commandes exactes ;
- une entrée inbox locale ;
- aucun closeout.

## 12_INVARIANTS

- Ne pas convertir `PRECHECK_PASS` en `PASS_FULL` sans sortie modèle réelle.
- Ne pas convertir `PARTIAL_PASS` en `PASS_FULL` sans run OpenClaw applicatif réel.
- Ne pas relancer GitHub Actions.
- Ne pas écrire sur machines runtime depuis ce chantier.
- Ne pas modifier les index globaux.

## 17_RESUME_POINT

```text
CANONICAL_LEDGER = docs/index/RUNS_VALIDATION_BACKLOG_01.md
DUE_NOW_1 = strict-worker-readonly-smoke requires real worker model output
DUE_NOW_2 = db-layer -> fantome requires real OpenClaw app runtime after clearance
CI_NEXT = inspect/repair no-lock-overlap, file-scope, Validate Job Packets
FLEET_NEXT = wait/verify 2026-05-30 09:00 Fleet Health Phase 1
```
