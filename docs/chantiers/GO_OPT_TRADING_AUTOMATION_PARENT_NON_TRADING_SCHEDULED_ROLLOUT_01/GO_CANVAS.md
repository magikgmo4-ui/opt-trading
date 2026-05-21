---
doc_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
doc_type: go_canvas
go_id: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
status: active
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01 (CLOSED)
---


# GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01


## 7_CANONICAL_STATE

NON_TRADING_AUTOMATION_ONLY
= repo jobs + docs jobs + governance jobs + worker jobs + scheduler jobs + app bridges + cockpit + ledger

Base disponible : PR #678 mergée avec les briques G01-G12, scripts workers, tests, ledger, HITL, contrats bridges, cockpit et scheduler.
Les apps externes ont des contrats `PASS_WITH_EVIDENCE`, avec reads/writes/gates/rollback definis.


### A. Jobs repo / Git / docs

| Job                                  | Role                                            | Mode               | Scheduler         |
| ------------------------------------ | ----------------------------------------------- | ------------------ | ----------------- |
| `repo-status-check`                  | verifier branche, proprete, ahead/behind        | read-only          | 15 min            |
| `repo-diff-check`                    | `git diff --check`, whitespace, conflit simple  | read-only          | 30 min            |
| `repo-branch-audit`                  | lister branches GO, merged, orphan, ahead       | read-only          | daily             |
| `repo-pr-audit`                      | lister PR ouvertes, merged, blocked             | read-only          | hourly            |
| `repo-go-index-audit`                | verifier dossiers `docs/chantiers/<GO>` + inbox | read-only          | daily             |
| `repo-doc-frontmatter-lint`          | verifier frontmatter canonique                  | read-only / report | daily             |
| `repo-doc-link-check`                | verifier liens internes docs                    | read-only / report | daily             |
| `repo-closeout-eligibility-check`    | detecter GO closables selon evidence            | read-only          | daily             |
| `repo-parent-coverage-board-refresh` | mettre a jour board parent propose              | draft only         | manual/HITL       |
| `repo-memory-bricks-candidate-scan`  | extraire `19_TO_REMEMBER` candidats             | read-only / draft  | daily             |
| `repo-changelog-digest`              | synthese commits/PR du jour                     | read-only / report | daily             |
| `repo-orphan-files-audit`            | fichiers non suivis / hors scope                | read-only          | daily             |
| `repo-scope-guard`                   | verifier qu un GO ne touche pas hors scope      | read-only          | pre-commit/manual |
| `repo-pr-review-preflight`           | checks avant review/merge                       | read-only          | manual            |
| `repo-release-note-draft`            | generer release note draft                      | draft only         | manual/HITL       |


### B. Jobs strict workers

| Job                                  | Role                               | Mode                | Scheduler  |
| ------------------------------------ | ---------------------------------- | ------------------- | ---------- |
| `strict-worker-model-registry-check` | valider `models.registry.json`     | read-only           | daily      |
| `strict-worker-task-index-check`     | valider `tasks.index.json`         | read-only           | daily      |
| `strict-worker-job-packet-validate`  | valider packets avant run          | read-only           | on demand  |
| `strict-worker-readonly-smoke`       | smoke runner read-only             | read-only + reports | 6 h        |
| `strict-worker-output-schema-check`  | verifier output JSON/MD attendu    | read-only           | after run  |
| `strict-worker-denied-command-scan`  | verifier no git write / no secrets | read-only           | after run  |
| `strict-worker-log-archive`          | archiver logs de jobs              | local write logs    | daily      |
| `strict-worker-failure-report`       | rapport si job FAIL/BLOCKED        | report              | on failure |


### C. Jobs ledger / observabilite

| Job                            | Role                            | Mode                | Scheduler |
| ------------------------------ | ------------------------------- | ------------------- | --------- |
| `ledger-heartbeat`             | ecrire heartbeat automation     | local write ledger  | 15 min    |
| `ledger-replay-check`          | relire ledger et verifier ordre | read-only           | hourly    |
| `ledger-blocked-events-digest` | synthese des BLOCKED/FAIL       | read-only / report  | hourly    |
| `ledger-rotation-check`        | surveiller taille + archive     | local write archive | daily     |
| `ledger-schema-validation`     | valider JSONL events            | read-only           | hourly    |
| `ledger-trace-id-audit`        | verifier trace_id presents      | read-only           | daily     |
| `automation-health-status`     | generer `health_status.json`    | local write report  | 15 min    |
| `automation-health-digest`     | resume sante systeme            | report              | hourly    |
| `kill-switch-state-check`      | lire `kill_switch.state`        | read-only           | 5 min     |
| `stuck-job-detector`           | detecter jobs running > seuil   | read-only/report    | 15 min    |


### D. Jobs securite / secrets / permissions

| Job                              | Role                                              | Mode             | Scheduler    |
| -------------------------------- | ------------------------------------------------- | ---------------- | ------------ |
| `anti-leak-scan`                 | scanner secrets dans outputs                      | read-only        | 6 h          |
| `env-file-presence-check`        | verifier `.env*` non trackes                      | read-only        | daily        |
| `gitignore-secrets-policy-check` | verifier patterns secrets                         | read-only        | daily        |
| `oauth-scope-audit`              | comparer scopes requis vs utilises                | read-only/report | daily        |
| `external-token-presence-check`  | verifier variables requises sans afficher secrets | read-only        | manual/daily |
| `permission-drift-check`         | detecter permission/scope drift                   | read-only/report | daily        |
| `kill-switch-fullstop-test`      | test controle etat kill switch                    | dry-run          | manual       |
| `deny-by-default-check`          | confirmer qu un write sans approval bloque        | dry-run          | daily        |


### E. Jobs HITL / approvals

| Job                           | Role                                 | Mode               | Scheduler    |
| ----------------------------- | ------------------------------------ | ------------------ | ------------ |
| `proposal-packet-create`      | creer proposition d action           | draft              | on demand    |
| `approval-packet-validate`    | valider approbation humaine          | read-only          | on demand    |
| `execution-packet-preflight`  | verifier action avant execution      | read-only          | on demand    |
| `verification-packet-create`  | preuve apres action                  | report             | after action |
| `approval-expiry-check`       | expirer demandes trop vieilles       | local write status | hourly       |
| `dual-confirm-required-check` | exiger 2 approvals actions sensibles | read-only          | on demand    |
| `hitl-scenarios-smoke`        | scenarios HITL                       | dry-run            | nightly      |
| `pending-approvals-digest`    | lister approvals en attente          | report             | hourly       |


### F. Jobs capability matrix / AI team

| Job                           | Role                                        | Mode             | Scheduler |
| ----------------------------- | ------------------------------------------- | ---------------- | --------- |
| `capability-matrix-validate`  | valider actor x surface x gate              | read-only        | nightly   |
| `capability-drift-check`      | detecter app/job non mappe                 | read-only/report | daily     |
| `ai-team-handoff-dry-run`     | scenario manager/specialiste                | dry-run          | nightly   |
| `ai-team-role-registry-check` | verifier roles et modeles                   | read-only        | daily     |
| `handoff-packet-schema-check` | valider packet handoff                      | read-only        | on demand |
| `memory-broker-dry-run`       | tester memoire partagee sans write critique | dry-run/local    | nightly   |
| `task-router-dry-run`         | router taches vers specialistes             | dry-run          | nightly   |
| `handoff-timeout-check`       | detecter handoff expire                     | read-only/report | hourly    |


### G. Jobs LocalCMS / cockpit

| Job                                 | Role                                  | Mode                  | Scheduler |
| ----------------------------------- | ------------------------------------- | --------------------- | --------- |
| `localcms-static-cockpit-build`     | generer/servir cockpit statique       | local write build     | on change |
| `localcms-automation-status-sync`   | afficher health/ledger/jobs           | write-gated/local     | 30 min    |
| `localcms-workers-state-sync`       | afficher etat workers                 | write-gated/local     | 30 min    |
| `localcms-jobs-queue-sync`          | afficher jobs pending/running/blocked | write-gated/local     | 30 min    |
| `localcms-approvals-sync`           | afficher approvals                    | write-gated/local     | 15 min    |
| `localcms-ledger-view-refresh`      | afficher ledger filtre                | read/local write view | 15 min    |
| `localcms-safe-buttons-check`       | verifier boutons dangereux desactives | read-only             | daily     |
| `localcms-kill-switch-widget-check` | verifier kill switch + dual confirm   | read-only             | daily     |


### H. Jobs apps externes

## Airtable

| Job                              | Role                            | Mode           | Scheduler         |
| -------------------------------- | ------------------------------- | -------------- | ----------------- |
| `airtable-read-health`           | lire base/table/vue autorisee   | read-only      | hourly            |
| `airtable-contract-check`        | verifier contrat app bridge     | read-only      | daily             |
| `airtable-canary-proposal`       | preparer record test            | draft          | manual            |
| `airtable-canary-write`          | creer/update record test        | write-gated    | manual puis daily |
| `airtable-readback-verify`       | verifier record cree            | read-only      | after write       |
| `airtable-snapshot-before-write` | snapshot avant write            | local/app read | before write      |
| `airtable-rollback-verify`       | confirmer compensation possible | read-only      | after write       |

## ClickUp

| Job                            | Role                                | Mode        | Scheduler         |
| ------------------------------ | ----------------------------------- | ----------- | ----------------- |
| `clickup-read-health`          | lire workspace/list/tasks           | read-only   | hourly            |
| `clickup-contract-check`       | verifier contrat app bridge         | read-only   | daily             |
| `clickup-canary-proposal`      | preparer tache test                 | draft       | manual            |
| `clickup-canary-task-create`   | creer tache canary                  | write-gated | manual puis daily |
| `clickup-task-readback-verify` | relire tache creee                  | read-only   | after write       |
| `clickup-task-update-canary`   | update champ/commentaire test       | write-gated | manual            |
| `clickup-compensation-note`    | noter etat precedent / compensation | write-gated | after write       |

## Botpress

| Job                               | Role                                   | Mode        | Scheduler   |
| --------------------------------- | -------------------------------------- | ----------- | ----------- |
| `botpress-read-health`            | lire bot/logs/conversations autorisees | read-only   | hourly      |
| `botpress-contract-check`         | verifier contrat app bridge            | read-only   | daily       |
| `botpress-dev-message-proposal`   | preparer message dev                   | draft       | manual      |
| `botpress-dev-message-send`       | envoyer message test dev               | write-gated | manual      |
| `botpress-variable-update-canary` | update variable controlee              | write-gated | manual      |
| `botpress-readback-verify`        | verifier message/variable              | read-only   | after write |

## KG Repo / Repo KG

| Job                         | Role                        | Mode             | Scheduler    |
| --------------------------- | --------------------------- | ---------------- | ------------ |
| `kg-repo-read-index`        | lire graphe/index KG        | read-only        | hourly/daily |
| `kg-repo-drift-check`       | detecter docs non indexes   | read-only        | daily        |
| `kg-repo-node-proposal`     | proposer node/edge/doc      | draft            | daily        |
| `kg-repo-pr-gated-sync`     | appliquer via PR            | PR-gated         | manual       |
| `kg-repo-readback-verify`   | verifier node/edge ajoute   | read-only        | after PR     |
| `kg-repo-orphan-node-audit` | nodes sans source canonique | read-only/report | daily        |

## Google Sheets

| Job                             | Role                  | Mode            | Scheduler    |
| ------------------------------- | --------------------- | --------------- | ------------ |
| `sheets-read-health`            | lire plage dediee     | read-only       | hourly       |
| `sheets-report-export-proposal` | preparer update plage | draft           | manual       |
| `sheets-canary-cell-write`      | ecrire cellule test   | write-gated     | manual       |
| `sheets-readback-verify`        | relire cellule/plage  | read-only       | after write  |
| `sheets-snapshot-before-write`  | snapshot plage        | read-only/local | before write |

## Telegram non-trading

| Job                             | Role                             | Mode               | Scheduler    |
| ------------------------------- | -------------------------------- | ------------------ | ------------ |
| `telegram-notification-health`  | tester notification non critique | write notification | manual/daily |
| `telegram-automation-digest`    | envoyer resume sante automation  | notification only  | daily        |
| `telegram-blocked-events-alert` | alerte BLOCKED/FAIL              | notification only  | on failure   |
| `telegram-approval-reminder`    | rappel approvals                 | notification only  | hourly       |

## Gmail / Calendar / Drive

| Job                               | Role                           | Mode              | Scheduler |
| --------------------------------- | ------------------------------ | ----------------- | --------- |
| `gmail-read-report-inbox`         | lire messages/labels autorises | read-only         | daily     |
| `gmail-draft-report`              | creer brouillon rapport        | write-gated/draft | manual    |
| `calendar-read-automation-events` | lire evenements automation     | read-only         | daily     |
| `calendar-create-review-event`    | creer evenement review         | write-gated       | manual    |
| `drive-read-folder-health`        | verifier dossier partage       | read-only         | daily     |
| `drive-upload-report-canary`      | upload rapport test            | write-gated       | manual    |


### I. Jobs scheduler / CI

| Job                            | Role                                | Mode              | Scheduler |
| ------------------------------ | ----------------------------------- | ----------------- | --------- |
| `scheduler-config-validate`    | valider config schedule             | read-only         | on change |
| `scheduler-unit-lint`          | verifier `.service/.timer`          | read-only         | on change |
| `scheduler-user-timers-list`   | lister timers actifs                | read-only         | hourly    |
| `scheduler-dry-run-next-fire`  | calculer prochaines executions      | read-only         | daily     |
| `scheduler-dead-letter-check`  | lire dead-letter queue              | read-only         | hourly    |
| `scheduler-retry-policy-check` | verifier retry/backoff              | read-only         | daily     |
| `ci-nightly-validation`        | lancer suite validation non-trading | CI/local          | nightly   |
| `ci-status-ingest`             | resumer CI vers ledger/cockpit      | write-gated/local | hourly    |


## Priorisation pour utilisation reelle

### Phase 01 — immediat

```
repo-status-check
repo-diff-check
repo-pr-audit
automation-health-status
ledger-heartbeat
ledger-replay-check
anti-leak-scan
strict-worker-readonly-smoke
capability-matrix-validate
ai-team-handoff-dry-run
bridge-contract-validation
hitl-scenarios-smoke
localcms-automation-status-sync
```

### Phase 02 — apps externes canary

```
clickup-canary-task-create
airtable-canary-write
botpress-dev-message-send
kg-repo-node-proposal / pr-gated-sync
localcms-status-sync
telegram-automation-digest
```

### Phase 03 — scheduler reel

```
scheduler-user-timers-list
automation-health-status.timer
automation-ledger-heartbeat.timer
automation-nightly-validation.timer
external-apps-canary.timer
```


## 16_TODO — prochain livrable

Creer le registre canonique :

```text
docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/10_NON_TRADING_JOBS_REGISTER.md
```

avec colonnes :

```text
job_id
category
surface
script_or_tool
mode
allowed_writes
gate
scheduler
frequency
evidence_required
status
```
