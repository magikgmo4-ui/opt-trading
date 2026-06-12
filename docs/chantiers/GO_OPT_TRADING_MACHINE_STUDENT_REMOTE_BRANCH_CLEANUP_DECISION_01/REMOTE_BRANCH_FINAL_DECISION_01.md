# Décision finale — branches remote Student résiduelles

## Contexte

Student/Ollama = FULLY_CLOSED. Indexation réparée. Il reste 34 branches remote résiduelles. Ce GO produit la décision finale de classification.

## Méthode de revue

Chaque branche a été vérifiée :
- statut Git réel (`git branch -r`, `merge-base --is-ancestor`, `rev-list --left-right --count`)
- contenu des commits ahead (pour les branches non absorbées)
- présence du dossier chantier sur mainline
- closeout / checkpoint dans le dossier chantier

## Verdicts finaux

### KEEP_ARCHIVE (3)

Conservées comme archive historique. Aucune suppression.

| Branche | Justification finale |
| --- | --- |
| `save/student-2026-04-01` | Snapshot machine student ; rollback potentiel ; déjà KEEP_REFERENCE dans BRANCH_STATE |
| `feat/student-mimo-bitget-live-equity` | Branche historique pré-Ollama ; 23 commits ahead (bitget secrets, equity probe, qualification) ; conservée comme trace de la phase MIMO |
| `go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_01` | DEFERRED per doc-ops ; jamais ouvert formellement ; 2 commits ahead (ouverture cadrage) ; conservée comme reference d'intention |

### DELETE_CONFIRMED (30)

Suppression validée. Toutes ces branches ont leur contenu sur mainline (PR mergée ou chantier présent). Les commits ahead sont des artéfacts de branche (checkpoint, closeout, inventory) — pas de runtime perdu.

| # | Branche | Preuve de fusion |
| --- | --- | --- |
| 1 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | Closeout PASS ; 12 ahead commits = branch-only (checkpoint, inventory, index) |
| 2 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_CANONICAL_INDEX_AGGREGATION_01` | 1 ahead commit = branch-only index aggregation |
| 3 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_REVIEW_REALIGN_01` | PR #251 merged ; ABSORBED (ancestor) |
| 4 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_SELECTIVE_PROPAGATION_01` | 1 ahead commit = branch-only propagation doc |
| 5 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_CLOSEOUT_01` | Dossier chantier sur mainline |
| 6 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_GATEWAY_SESSION_FIX_01` | Dossier chantier sur mainline |
| 7 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_APPLY_01` | Dossier chantier sur mainline |
| 8 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_AUTHORIZATION_01` | Dossier chantier sur mainline |
| 9 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_DRYRUN_01` | Dossier chantier sur mainline |
| 10 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_INSTALL_SOURCE_PROOF_01` | Dossier chantier sur mainline |
| 11 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_LOCAL_OLLAMA_BINDING_SMOKE_01` | Dossier chantier sur mainline |
| 12 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01` | Dossier chantier sur mainline |
| 13 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_01_RETRY` | Dossier chantier sur mainline |
| 14 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_03` | Dossier chantier sur mainline |
| 15 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04` | Dossier chantier sur mainline |
| 16 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_MODEL_PULL_EVAL_04_RETRY` | Dossier chantier sur mainline |
| 17 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_NETWORK_DIAG_01` | Dossier chantier sur mainline |
| 18 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_DISK_FIX_01` | Dossier chantier sur mainline |
| 19 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_E2E_SMOKE_01` | Closeout PASS ; dossier chantier sur mainline |
| 20 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_MODEL_EVALUATION_01` | Dossier chantier sur mainline |
| 21 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_ROUTING_AUDIT_01` | Dossier chantier sur mainline |
| 22 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_APPLY_01` | Dossier chantier sur mainline |
| 23 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_OLLAMA_PROVIDER_SWITCH_DRYRUN_01` | Dossier chantier sur mainline |
| 24 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` | Dossier chantier sur mainline |
| 25 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_SCOPE_VALIDATION_01` | Dossier chantier sur mainline |
| 26 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01` | Dossier chantier sur mainline |
| 27 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01` | Closeout PASS ; dossier chantier sur mainline |
| 28 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CAPABILITY_GATE_AND_FALLBACK_01` | ABSORBED (ancestor) ; CHECKPOINT "Fermer après merge" |
| 29 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01` | ABSORBED (ancestor) ; FIRST_CONSUMER_PASS |
| 30 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01` | ABSORBED (ancestor) ; CHECKPOINT "Fermer après merge" |
| 31 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_RUNTIME_BASELINE_ADOPTION_01` | ABSORBED (ancestor) ; FULL_PASS |
| 32 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_POLICY_01` | ABSORBED (ancestor) ; politque documentée |
| 33 | `go/GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_SESSION_RETENTION_ENFORCEMENT_01` | ABSORBED (ancestor) ; enforcement scripts |

### REVIEW_BLOCKED (1)

| Branche | Verdict | Justification |
| --- | --- | --- |
| `go/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_REALIGN_01` | REVIEW_BLOCKED | Dossier chantier présent sur mainline mais branche introuvable sur remote (déjà supprimée). Aucune action requise. |

---

## Synthèse finale

| Verdict | Nombre | Action |
| --- | --- | --- |
| `KEEP_ARCHIVE` | 3 | Aucune suppression |
| `DELETE_CONFIRMED` | 30 | Suppression validée (GO d'exécution séparé) |
| `REVIEW_BLOCKED` | 1 | Déjà absent, aucune action |
| **Total** | **34** | |

## Recommandation

Ouvrir un GO d'exécution pour supprimer les 30 branches `DELETE_CONFIRMED` :
- localement : `git branch -d` pour les branches locales si présentes
- à distance : `git push origin --delete` pour chaque branche
- mettre à jour BRANCH_STATE.md après suppression effective

Les 3 branches `KEEP_ARCHIVE` restent en l'état.

## RISKS

- À qualifier.
