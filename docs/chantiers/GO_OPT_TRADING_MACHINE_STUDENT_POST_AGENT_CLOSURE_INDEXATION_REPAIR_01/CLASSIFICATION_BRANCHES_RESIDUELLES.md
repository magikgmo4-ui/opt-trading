# Classification des branches Student résiduelles

## Contexte

Student/Ollama = FULLY_CLOSED. Toutes les branches listées ci-dessous sont des branches distantes résiduelles. Aucune suppression n'est exécutée dans ce GO. Ce document produit une classification pour décision future.

## Légende

| Verdict | Signification |
| --- | --- |
| `KEEP_ARCHIVE` | Conserver comme archive historique. Branch de snapshot, backup, ou reference. |
| `DELETE_AFTER_VALIDATION` | Supprimer après validation explicite. Branch dont le contenu est merged et qui peut être nettoyée. |
| `UNKNOWN_REVIEW_REQUIRED` | Nécessite revue avant décision. Branche dont le statut de merge est incertain. |

---

## Classification

### Branches snapshot — KEEP_ARCHIVE

| Branche | Verdict | Justification |
| --- | --- | --- |
| `save/student-2026-04-01` | `KEEP_ARCHIVE` | Snapshot machine student ; conserve comme reference et rollback potentiel ; déjà classé KEEP_REFERENCE dans BRANCH_STATE |

### Branches historiques — KEEP_ARCHIVE

| Branche | Verdict | Justification |
| --- | --- | --- |
| `feat/student-mimo-bitget-live-equity` | `KEEP_ARCHIVE` | Branche historique student/mimo ; 23 ahead / 1480 behind ; conservée comme reference de la phase pré-Ollama |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | `KEEP_ARCHIVE` | DEFERRED per doc-ops decision ; jamais ouvert formellement ; 2 ahead / 683 behind ; conserve comme reference de l'intention machine parent |

### Branches merged — DELETE_AFTER_VALIDATION

Ces branches correspondent à des PR mergées ou dont le contenu est absorbé dans sot/mainline. La suppression est sécurisée après validation.

| Branche | Verdict | Justification | Ahead | Behind | Référence |
| --- | --- | --- | --- | --- | --- |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | `DELETE_AFTER_VALIDATION` | Parent Student/Ollama — closeout PASS | 12 | 886 | `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_CANONICAL_INDEX_AGGREGATION_01` | `DELETE_AFTER_VALIDATION` | Sub-parent Student/Ollama | 1 | 695 | Branche résiduelle, contenu absorbé |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01` | `DELETE_AFTER_VALIDATION` | PR #251 merged | 0 | 449 | `git log` — PR merged |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_SELECTIVE_PROPAGATION_01` | `DELETE_AFTER_VALIDATION` | Sub-parent Student/Ollama | 1 | 695 | Branche résiduelle, contenu absorbé |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_CLOSEOUT_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_GATEWAY_SESSION_FIX_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_APPLY_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_AUTHORIZATION_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_DRYRUN_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_SOURCE_PROOF_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_LOCAL_OLLAMA_BINDING_SMOKE_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01_RETRY` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_03` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_NETWORK_DIAG_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_DISK_FIX_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01` | `DELETE_AFTER_VALIDATION` | Lab child — closeout PASS | — | — | `docs/chantiers/...OLLAMA_E2E_SMOKE_01/90_CLOSEOUT.md` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_ROUTING_AUDIT_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_DRYRUN_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_SCOPE_VALIDATION_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01` | `DELETE_AFTER_VALIDATION` | Lab child — closed | — | — | Dossier chantier présent sur mainline |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01` | `DELETE_AFTER_VALIDATION` | Lab child — closeout PASS | — | — | `docs/chantiers/...WORKSPACE_SLIM_01/90_CLOSEOUT.md` |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — CLOSED | 0 | 43 | CHECKPOINT indique "Fermer le GO après merge" |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — CLOSED | 0 | 51 | FIRST_CONSUMER_PASS |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — CLOSED | 0 | 69 | CHECKPOINT indique "Fermer le GO après merge" |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — FULL_PASS | 0 | 71 | Chaîne Student/Ollama complète |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — CLOSED | 0 | 829 | Politique documentée |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01` | `DELETE_AFTER_VALIDATION` | Agent standardization — CLOSED | 0 | 75 | Enforcement scripts produits |

### Branches nécessitant revue — UNKNOWN_REVIEW_REQUIRED

| Branche | Verdict | Justification |
| --- | --- | --- |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_REALIGN_01` | `UNKNOWN_REVIEW_REQUIRED` | Dossier chantier présent sur mainline mais branche non trouvée dans git remote ; peut avoir été déjà supprimée |

---

## Synthèse

| Verdict | Nombre |
| --- | --- |
| `KEEP_ARCHIVE` | 3 |
| `DELETE_AFTER_VALIDATION` | 30 |
| `UNKNOWN_REVIEW_REQUIRED` | 1 |
| **Total** | **34** |

## Contrainte

Aucune suppression n'est exécutée dans ce GO. La classification ci-dessus est un livrable pour décision ultérieure.

## RISKS

- À qualifier.
