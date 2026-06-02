---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01_MATRIX
doc_type: activation_matrix
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01
status: active
produced_at: 2026-06-01
sources:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/10_NON_TRADING_JOBS_REGISTER.md
  - docs/registry/JOBS_REGISTRY.md
---

# 10_ACTIVATION_MATRIX — Priorisation jobs récurrents

## Méthode de scoring

```
P  = Priorité opérationnelle (1=critique → 5=optionnel)
U  = Utilité systémique (1=faible → 5=haute)
R  = Prêt à activer (1=bloqué → 5=script+packet validé)
Vecteur = dispatcher | script_direct | gha | manual | shell
Verdict = NOW | NEXT | LATER | MANUAL_ONLY | BLOCKED | ALREADY_ACTIVE
```

Règle de sélection Lot 1 (`NOW`) :
- P ≤ 2 ET U ≥ 4 ET R ≥ 4
- Script Python existant (`scripts/ai/workers/`) OU packet job existant
- Phase 01–03 PASS prouvé

---

## LOT 0 — Déjà actifs (GHA en production)

Ces jobs tournent déjà. Aucune action requise.

| job_id | vecteur | cadence | P | U | R | verdut |
|---|---|---|---|---|---|---|
| `gha_gated_pr` | gha | PR | 1 | 5 | 5 | ALREADY_ACTIVE |
| `gha_registry_validation` | gha | PR (paths) | 1 | 5 | 5 | ALREADY_ACTIVE |
| `gha_openclaw_mcp_policy` | gha | PR (paths) | 2 | 4 | 5 | ALREADY_ACTIVE |
| `gha_strict_workers_schedule` | gha | lun 08:00 | 1 | 5 | 5 | ALREADY_ACTIVE |
| `gha_strict_workers_smoke` | gha | PR (paths) | 1 | 5 | 5 | ALREADY_ACTIVE |
| `gha_strict_workers_validate` | gha | PR (paths) | 1 | 5 | 5 | ALREADY_ACTIVE |
| `gha_openclaw_skill_policy` | gha | manual | 3 | 3 | 4 | ALREADY_ACTIVE |

---

## LOT 1 — NOW : Activation immédiate recommandée (15 jobs)

Scripts confirmés, phase PASS, read-only ou local-write uniquement.
Tous peuvent être lancés via `python3 scripts/ai/workers/<script>.py`
ou `OperatorBridge.send(action="dispatch", parameters={"packet_id": ...})`.

| # | job_id | script / packet | cadence | P | U | R | vecteur | phase_pass |
|---|---|---|---|---|---|---|---|---|
| 1 | `automation-health-status` | `health_status.py` | 15 min | 1 | 5 | 5 | script_direct | phase_01 |
| 2 | `ledger-heartbeat` | `ledger_writer.py` | 15 min | 1 | 5 | 5 | script_direct | phase_01 |
| 3 | `stuck-job-detector` | `stuck_job_detector.py` | 15 min | 1 | 4 | 5 | script_direct | phase_03 |
| 4 | `ledger-replay-check` | `ledger_replay.py` | 1 h | 1 | 5 | 5 | script_direct | phase_01 |
| 5 | `ledger-schema-validation` | `ledger_schema_validation.py` | 1 h | 1 | 5 | 5 | script_direct | phase_03 |
| 6 | `ledger-blocked-events-digest` | `ledger_blocked_events_digest.py` | 1 h | 2 | 4 | 5 | script_direct | phase_03 |
| 7 | `localcms-automation-status-sync` | `localcms_automation_status_sync.py` | 30 min | 1 | 4 | 5 | script_direct | phase_01 |
| 8 | `strict-worker-readonly-smoke` | `GO_STRICT_WORKERS_READONLY_SMOKE_01.json` | 6 h | 1 | 5 | 5 | dispatcher | phase_01 |
| 9 | `strict-worker-log-archive` | `strict_worker_log_archive.py` | daily | 2 | 3 | 5 | script_direct | phase_02 |
| 10 | `strict-worker-denied-command-scan` | `strict_worker_denied_command_scan.py` | after run | 2 | 4 | 5 | script_direct | phase_02 |
| 11 | `permission-drift-check` | `permission_drift_check.py` | daily | 2 | 4 | 5 | script_direct | phase_03 |
| 12 | `repo-doc-frontmatter-lint` | `repo_doc_frontmatter_lint.py` | daily | 2 | 3 | 5 | script_direct | phase_02 |
| 13 | `repo-doc-link-check` | `repo_doc_link_check.py` | daily | 2 | 3 | 5 | script_direct | phase_02 |
| 14 | `ledger-rotation-check` | `ledger_rotation_check.py` | daily | 2 | 3 | 5 | script_direct | phase_03 |
| 15 | `repo-pr-audit` | `gh pr list` (shell) | 1 h | 2 | 4 | 4 | shell | phase_01 |

### Notes Lot 1

- `#8 strict-worker-readonly-smoke` : dispatcher déterministe opérationnel.
  Commande : `OperatorBridge.send(BridgeRequest(action="dispatch", parameters={"packet_id": "GO_STRICT_WORKERS_READONLY_SMOKE_01", "dry_run": True}))`
- `#15 repo-pr-audit` : `gh pr list --state open --json number,title,state` — dépend de `gh` auth.
  Aucun Python script dédié requis — opérateur ou cron shell direct.

---

## LOT 2 — NEXT : Semaine suivante (20 jobs)

Prêts mais demandent un setup mineur (script existe, token manquant,
ou cadence "after run" nécessite un trigger défini).

| # | job_id | script / outil | cadence | P | U | R | vecteur | blocage mineur |
|---|---|---|---|---|---|---|---|---|
| 1 | `kill-switch-state-check` | state reader (à écrire, 30 lignes) | 5 min | 1 | 5 | 3 | script_direct | script minimal manquant |
| 2 | `anti-leak-scan` | secret scanner (trufflehog / grep) | 6 h | 1 | 5 | 3 | script_direct | outil à configurer |
| 3 | `ledger-trace-id-audit` | `ledger_trace_id_audit.py` | daily | 2 | 3 | 5 | script_direct | aucun |
| 4 | `strict-worker-output-schema-check` | `strict_worker_output_schema_check.py` | after run | 2 | 4 | 5 | script_direct | trigger à définir |
| 5 | `strict-worker-failure-report` | reporter (after failure) | on failure | 2 | 4 | 3 | script_direct | script à écrire |
| 6 | `oauth-scope-audit` | `oauth_scope_audit.py` | daily | 2 | 4 | 5 | script_direct | tokens OAuth requis |
| 7 | `strict-worker-model-registry-check` | `_validate_job.py` (models) | daily | 2 | 4 | 5 | script_direct | aucun |
| 8 | `strict-worker-task-index-check` | `_validate_job.py` (tasks.index) | daily | 2 | 4 | 5 | script_direct | aucun |
| 9 | `repo-branch-audit` | `gh branch` shell | daily | 2 | 3 | 4 | shell | gh auth |
| 10 | `repo-go-index-audit` | index audit runner | daily | 2 | 4 | 3 | script_direct | runner à écrire |
| 11 | `repo-closeout-eligibility-check` | closeout audit | daily | 2 | 3 | 3 | script_direct | runner à écrire |
| 12 | `repo-orphan-files-audit` | orphan audit | daily | 2 | 3 | 3 | script_direct | runner à écrire |
| 13 | `env-file-presence-check` | env audit | daily | 2 | 3 | 4 | shell | aucun |
| 14 | `gitignore-secrets-policy-check` | policy check | daily | 2 | 3 | 4 | shell | aucun |
| 15 | `capability-matrix-validate` | matrix validator | nightly | 2 | 3 | 3 | script_direct | matrix à formaliser |
| 16 | `hitl-scenarios-smoke` | dry-run | nightly | 2 | 3 | 3 | script_direct | HITL infra partielle |
| 17 | `ai-team-handoff-dry-run` | dry-run | nightly | 2 | 3 | 3 | script_direct | role registry à valider |
| 18 | `task-router-dry-run` | dry-run router | nightly | 2 | 3 | 3 | script_direct | router à implémenter |
| 19 | `repo-changelog-digest` | digest runner | daily | 3 | 3 | 3 | script_direct | runner à écrire |
| 20 | `localcms-workers-state-sync` | sync runner | 30 min | 3 | 3 | 3 | script_direct | cockpit infra |

---

## LOT 3 — LATER : Phase 04–06 (HITL / cockpit / AI team)

Dépendent d'une infrastructure HITL ou LocalCMS cockpit non encore
complètement déployée. Activer après Lot 2 validé.

| job_id | catégorie | P | U | R | blocage principal |
|---|---|---|---|---|---|
| `proposal-packet-create` | hitl | 2 | 4 | 2 | HITL infra incomplète |
| `approval-packet-validate` | hitl | 2 | 4 | 2 | HITL infra incomplète |
| `execution-packet-preflight` | hitl | 2 | 4 | 2 | HITL infra incomplète |
| `approval-expiry-check` | hitl | 2 | 4 | 2 | HITL infra incomplète |
| `pending-approvals-digest` | hitl | 2 | 3 | 2 | HITL infra incomplète |
| `capability-drift-check` | ai-team | 3 | 3 | 2 | mapping app/job incomplet |
| `ai-team-role-registry-check` | ai-team | 3 | 3 | 2 | role registry absent |
| `memory-broker-dry-run` | ai-team | 3 | 3 | 2 | shared memory non déployé |
| `localcms-static-cockpit-build` | cockpit | 3 | 3 | 2 | build infra localcms |
| `localcms-workers-state-sync` | cockpit | 3 | 3 | 2 | cockpit infra |
| `localcms-jobs-queue-sync` | cockpit | 3 | 3 | 2 | cockpit infra |
| `localcms-approvals-sync` | cockpit | 3 | 3 | 2 | cockpit infra |
| `localcms-ledger-view-refresh` | cockpit | 3 | 3 | 2 | cockpit infra |
| `localcms-safe-buttons-check` | cockpit | 3 | 3 | 2 | cockpit UI |
| `localcms-kill-switch-widget-check` | cockpit | 3 | 3 | 2 | cockpit UI |
| `scheduler-config-validate` | scheduler | 2 | 4 | 3 | config à produire |
| `scheduler-unit-lint` | scheduler | 2 | 3 | 3 | units à écrire |
| `scheduler-user-timers-list` | scheduler | 2 | 3 | 3 | timers à installer |
| `scheduler-dry-run-next-fire` | scheduler | 2 | 3 | 3 | timers à installer |
| `scheduler-dead-letter-check` | scheduler | 2 | 4 | 3 | dead-letter queue |
| `ci-nightly-validation` | scheduler | 2 | 4 | 3 | CI à câbler |
| `ci-status-ingest` | scheduler | 2 | 3 | 3 | ingest runner à écrire |
| `deny-by-default-check` | security | 2 | 4 | 3 | policy gates à formaliser |
| `external-token-presence-check` | security | 2 | 3 | 3 | env vars à inventorier |

---

## MANUAL_ONLY — Ne jamais scheduler

Jobs qui doivent rester déclenchés par opérateur uniquement.

| job_id | raison | script |
|---|---|---|
| `kill-switch-fullstop-test` | déclenche arrêt système — risque HIGH | `kill_switch_fullstop_test.py` |
| `repo-release-note-draft` | HITL obligatoire — validation humaine | draft generator |
| `repo-pr-review-preflight` | par définition : avant chaque PR | preflight runner |
| `dual-confirm-required-check` | on demand uniquement | dual confirm checker |
| `repo-parent-coverage-board-refresh` | HITL requis | board refresh |
| `repo-repo-memory-bricks-candidate-scan` | draft docs + HITL | scan runner |
| `verification-packet-create` | after action uniquement | verification generator |
| `airtable-canary-write` | dual confirm requis | write-gated bridge |
| `clickup-canary-task-create` | dual confirm requis | write-gated bridge |
| All `*-canary-proposal` jobs | HITL obligatoire | proposal runners |

---

## BLOCKED — Apps externes (Phase 07–08)

Bloqués jusqu'à preuve d'un bridge contract live (OAuth prouvé, token présent, readback PASS).

| catégorie | jobs bloqués | count | débloqueur |
|---|---|---|---|
| Airtable | `airtable-read-health`, `airtable-contract-check`, canary × 5 | 7 | OAuth Airtable validé en live |
| ClickUp | `clickup-read-health`, `clickup-contract-check`, canary × 5 | 7 | token ClickUp validé en live |
| Botpress | `botpress-read-health`, `botpress-contract-check`, canary × 4 | 6 | credentials Botpress validés |
| KG Repo | `kg-repo-read-index`, `kg-repo-drift-check`, × 4 | 6 | KG reader opérationnel |
| Google Sheets | `sheets-read-health`, canary × 4 | 5 | OAuth Sheets validé |
| Telegram non-trading | notification × 4 | 4 | TELEGRAM_BOT_TOKEN présent + policy |
| Gmail / Calendar / Drive | read + write × 6 | 6 | OAuth Google validé en live |
| **Total bloqué** | | **41** | bridges externes |

---

## Résumé chiffré

| lot | count | verdict | vecteur principal |
|---|---|---|---|
| Lot 0 | 7 | ALREADY_ACTIVE | gha |
| **Lot 1** | **15** | **NOW** | script_direct + dispatcher |
| Lot 2 | 20 | NEXT | script_direct + shell |
| Lot 3 | 23 | LATER | infra HITL / cockpit |
| MANUAL_ONLY | 10 | MANUAL_ONLY | opérateur |
| BLOCKED | 41 | BLOCKED | bridges externes |
| **Total couvert** | **116** | | |

> 116 = 114 non-trading + les 7 GHA (7 déjà comptés dans Lot 0).
> Quelques jobs du Lot 3 peuvent se chevaucher entre phases ; le compte
> est indicatif ± 2.

---

## Activation Lot 1 — Commandes de référence

```bash
# Lot 1, jobs script_direct — lancer manuellement pour valider avant cron
python3 scripts/ai/workers/health_status.py
python3 scripts/ai/workers/ledger_writer.py --heartbeat
python3 scripts/ai/workers/stuck_job_detector.py
python3 scripts/ai/workers/ledger_replay.py
python3 scripts/ai/workers/ledger_schema_validation.py
python3 scripts/ai/workers/ledger_blocked_events_digest.py
python3 scripts/ai/workers/localcms_automation_status_sync.py
python3 scripts/ai/workers/strict_worker_log_archive.py
python3 scripts/ai/workers/strict_worker_denied_command_scan.py
python3 scripts/ai/workers/permission_drift_check.py
python3 scripts/ai/workers/repo_doc_frontmatter_lint.py
python3 scripts/ai/workers/repo_doc_link_check.py
python3 scripts/ai/workers/ledger_rotation_check.py

# Lot 1, job dispatcher (#8)
python3 - <<'EOF'
import sys; sys.path.insert(0, "modules/openclaw_operator_bridge")
from app.schema import BridgeRequest
from app.bridge import OperatorBridge
resp = OperatorBridge().send(BridgeRequest(
    action="dispatch",
    instruction="smoke readonly",
    parameters={"packet_id": "GO_STRICT_WORKERS_READONLY_SMOKE_01", "dry_run": True}
))
print(resp.status, resp.content)
EOF

# Lot 1, repo-pr-audit (shell)
gh pr list --state open --json number,title,headRefName,updatedAt | python3 -m json.tool
```

---

## Prochaine étape recommandée

```
Chantier suivant : GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_LOT1_SMOKE_01
Objectif : valider les 15 jobs Lot 1 en run réel (non dry-run)
           et produire un rapport d'activation pour chaque job.
Gate : tous les scripts Lot 1 lancés sans erreur → activation cron.
```
