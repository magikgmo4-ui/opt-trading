---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_ROLLOUT_PLAN
doc_type: automation_rollout_plan
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: active
phase_p0: PASS_WITH_EVIDENCE
phase_p1: PASS_WITH_EVIDENCE
phase_p3: PASS_WITH_EVIDENCE
phase_p4: PASS_WITH_EVIDENCE
phase_p5: PASS_WITH_EVIDENCE
phase_p6: PASS_WITH_EVIDENCE
phase_p7: PASS_WITH_EVIDENCE
phase_p8: PASS_WITH_EVIDENCE
phase_p9: PASS_WITH_EVIDENCE
---

# 85_AUTOMATION_ROLLOUT_MASTER_PLAN

## 1_MASTER_TARGET

Passer des briques PASS_WITH_EVIDENCE vers une automatisation contrôlée par phases.
Aucun closeout tant que chaque phase n'a pas evidence.

## 7_CANONICAL_STATE

- PR #678 agrège les GO enfants (G01-G12) mergée dans `sot/mainline` ✅
- G01-G12 couverts avec preuves ✅
- ledger root path corrigé (parents[3]) ✅
- P0 Freeze baseline — PASS_WITH_EVIDENCE ✅
- P1 Observe-only — PASS_WITH_EVIDENCE ✅
- P3 Draft automation — PASS_WITH_EVIDENCE ✅
- parent GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01 non fermé

## 8_VALIDATED_PLAN

| Phase | Nom | Objectif | Gate |
|---|---|---|---|
| P0 | Freeze baseline ✅ | Figer PR #678 comme base evidence | merge + diff review — FAIT |

### P0 — Détail

- **preconditions** : G01-G12 tous PASS_WITH_EVIDENCE, PR #678 mergeable
- **allowed actions** : merge PR #678 dans sot/mainline
- **forbidden actions** : closeout parent, ouverture nouveau GO, modification des evidences
- **evidence required** : PR mergée, diff check clean, tous les tests passent
- **rollback** : revert commit merge PR #678
- **ledger event** : n/a (opération manuelle)
- **closeout eligibility** : P0 close dès que PR mergée et validée
- **Verdict** : ✅ PASS_WITH_EVIDENCE — PR #678 mergée à `sot/mainline` (commit `bb396eee`), 38 commits, 97 fichiers, 5575 additions, whitespace clean, 6 tests de validation PASS

| P1 | Observe-only ✅ | Lire, inventorier, journaliser | read-only — FAIT |

### P1 — Détail

- **preconditions** : P0 complété, PR #678 mergée, ledger path corrigé
- **allowed actions** : READ_INVENTORY sur toutes les surfaces (repo, Telegram, tmux, configs), health status check, journalisation dans le ledger
- **forbidden actions** : tout write (patch_draft, write_gated, app bridge write), modification de config runtime, activation de write
- **evidence required** : observe worker déployé, 3+ cycles d'observation réussis, ledger events produits, aucun write détecté
- **rollback** : désactiver le timer observe, supprimer les events de test du ledger
- **ledger event** : OBSERVE_CYCLE (PASS/FAIL)
- **closeout eligibility** : observe worker fonctionnel + preuve de 3 cycles read-only sans write
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `observe_worker.py` créé et exécuté (6 events ledger, 5 PASS + 1 WARN timer), 0 writes, observe cycle complet. P2 débloqué.
| P2 | Strict workers runtime | Exécuter jobs read-only bornés | runner + logs |
| P3 | Draft automation ✅ | Produire patchs / docs / propositions sans write | dry-run — FAIT |

### P3 — Détail

- **preconditions** : P0+P1 complétés, observe worker fonctionnel, ledger opérationnel
- **allowed actions** : lire surfaces, produire drafts (patch/doc/proposal) dans `data/drafts/`, journaliser dans le ledger
- **forbidden actions** : write sur surface cible, write sur surfaces observées, modification runtime
- **evidence required** : draft worker déployé, 3 drafts produits (patch+doc+proposal), dry_run=True, write_executed=False
- **rollback** : supprimer `data/drafts/<id>/`, revert ledger events si nécessaire
- **ledger event** : DRAFT_CYCLE (READ/PRODUCE/VERIFY)
- **closeout eligibility** : draft worker fonctionnel + 3 drafts dry-run avec 0 write
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `draft_worker.py` créé, 4 drafts produits (2 patch, 1 doc, 1 proposal), tous dry_run=True, 0 writes target. P4 débloqué.
| P4 | HITL write-gated ✅ | Exécuter seulement après approval humain | approval packet — FAIT |

### P4 — Détail

- **preconditions** : P3 complété, drafts disponibles, ledger opérationnel
- **allowed actions** : exécuter write après approval packet valide, produire artifacts dans `data/executed/`
- **forbidden actions** : write sans approval, write sans proposal packet, contournement du gate
- **evidence required** : hitl_gate testé sans approval (BLOCKED) + avec approval (EXECUTED), tous les events dans ledger
- **rollback** : revert du write exécuté, supprimer `data/executed/<id>.json`
- **ledger event** : HITL_GATE (LOAD_DRAFT → CREATE_PROPOSAL → WRITE_GATED/BLOCKED | PROPOSAL_APPROVED → WRITE_EXECUTED)
- **closeout eligibility** : hitl_gate fonctionnel + 2 scénarios validés (sans=BLOCKED, avec=EXECUTED)
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `hitl_gate.py` créé, testé sans approval (BLOCKED, 0 writes) et avec approval (EXECUTED, write logged). P5 débloqué.
| P5 | App bridges ✅ | Airtable / Sheets / Telegram / LocalCMS sous contrat | bridge contract — FAIT |

### P5 — Détail

- **preconditions** : P4 complété, orchestration contract existant (external_apps_orchestration_contract.json), APP_BRIDGES défini pour airtable/google_sheets/telegram/localcms
- **allowed actions** : READ_INVENTORY sur les 4 bridges, DRAFT_ONLY (dry-run), WRITE_GATED avec approval token
- **forbidden actions** : write sans approval token, write en mode READ_ONLY/DRAFT_ONLY, write sur app non supportée, contournement du contract
- **evidence required** : bridge_worker testé sur 4 apps × 3 modes, contract validation PASS/FAIL, ledger events produits
- **rollback** : supprimer `reports/ai/workers/bridge_<app>_<timestamp>.json`, revert ledger events
- **ledger event** : BRIDGE_CYCLE (CONTRACT_VALIDATION → READ_INVENTORY → WRITE_BLOCKED/BLOCKED_BY_MODE/DRAFT_ONLY/EXECUTED → BRIDGE_CYCLE_COMPLETE)
- **closeout eligibility** : bridge_worker fonctionnel sur 4 apps, 3 modes, contract validé, ledger events produits
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `bridge_worker.py` créé, testé sur 4 apps (airtable, google_sheets, telegram, localcms) × 3 modes (READ_ONLY BLOCKED, DRAFT_ONLY BLOCKED, WRITE_GATED PASS avec approval), contract validation intégré, 15+ events ledger, 9 reports dans `reports/ai/workers/`. P6 débloqué.
| P6 | Signal dry-run ✅ | Signaux → validation → journal → backtest, sans ordre live | dry-run guard — FAIT |

### P6 — Détail

- **preconditions** : P5 complété, signal infrastructure existante (webhook, signal_router, signal_event_adapter), dry-run pipeline testé
- **allowed actions** : LOAD_SIGNAL (synthetic ou fixture), NORMALIZE V0→V1, VALIDATE, SIGNAL_JOURNALED → ledger, BACKTEST simulé, DRY_RUN_CYCLE_COMPLETE
- **forbidden actions** : live order, vraie exécution, modification de positions, tout write sur exchange
- **evidence required** : signal_dry_run_worker testé avec signal synthétique + fixture, validation V1 OK, backtest simulé, guard actif, 0 live orders
- **rollback** : supprimer `reports/ai/workers/signal_dry_run_<ts>_<cycle>.json`, revert ledger events
- **ledger event** : SIGNAL_DRY_RUN (LOAD_SIGNAL → NORMALIZE → VALIDATE → SIGNAL_JOURNALED → DRY_RUN_GUARD → BACKTEST → DRY_RUN_CYCLE_COMPLETE)
- **closeout eligibility** : signal_dry_run_worker fonctionnel, 3 scénarios validés (synthetic, fixture, no-backtest), guard prouvé, 0 live orders
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `signal_dry_run_worker.py` créé, testé avec signal synthétique (coinm SELL BTCUSDT.P), fixture (USDTM_LONG BUY BTCUSDT), et --no-backtest. Validation V1, journalisation ledger, guard actif (live_order_placed=False), backtest simulé WIN/LOSS. 21+ events ledger. P7 débloqué.
| P7 | Cockpit LocalCMS ✅ | Supervision, boutons sûrs, kill switch | UI safe buttons — FAIT |

### P7 — Détail

- **preconditions** : P6 complété, LocalCMS existant (FastAPI, routes UI, metrics, journal), orchestration contract défini
- **allowed actions** : GET /kill-switch (lecture état), POST /kill-switch/engage (activer), POST /kill-switch/disengage (désactiver), GET /safe-actions (lister actions), GET /kill-switch/history (historique)
- **forbidden actions** : engager/disengager sans autorisation, modification directe du fichier sans journal, actions dangereuses avec kill switch engagé
- **evidence required** : kill switch mécanisme file-based, 4 transitions testées (init→engage→disengage→re-engage), historique journalisé, safe actions listées, UI mise à jour
- **rollback** : supprimer `data/kill_switch/`, revert modifications à `modules/localcms/app/main.py`
- **ledger event** : n/a (kill switch utilise son propre history.jsonl, les events ajoutés à LocalCMS ne sont pas dans le ledger global car c'est un composant existant — pourrait être migré)
- **closeout eligibility** : kill switch fonctionnel (engage/disengage/history), safe actions endpoint, UI indicators
- **Verdict** : ✅ PASS_WITH_EVIDENCE — Kill switch file-based ajouté à `modules/localcms/app/main.py` avec endpoints GET /kill-switch, POST /engage, POST /disengage, GET /history. Safe actions endpoint (GET /safe-actions) listant 8 actions safe + 4 actions dangereuses. UI mise à jour avec indicateur kill switch dans la summary bar + sections dédiées. 4 transitions testées. P8 débloqué.
| P8 | Scheduler/CI ✅ | Jobs planifiés, retries, dead-letter, alerting | CI + ledger — FAIT |

### P8 — Détail

- **preconditions** : P7 complété, scheduling infra existante (systemd timers, GitHub Actions), retry patterns existants
- **allowed actions** : SUBMIT job (9 actions supportées), RUN scheduler cycle, LIST jobs, DEAD-LETTER view, ALERTS view
- **forbidden actions** : exécuter job sans retry, supprimer dead-letter sans review, ignorer alertes critiques
- **evidence required** : scheduler_worker testé avec jobs réussis + échec + retry + dead-letter + alertes, tout dans ledger
- **rollback** : supprimer `data/scheduler/`, revert `scheduler_worker.py`
- **ledger event** : SCHEDULER (JOB_SUBMIT → JOB_START → JOB_SUCCESS | JOB_FAILED | JOB_DEAD_LETTER → JOB_RETRY_SCHEDULED → SCHEDULER_CYCLE)
- **closeout eligibility** : scheduler_worker fonctionnel avec les 5 commands (list/submit/run/dead-letter/alerts), retry × dead-letter × alert prouvés
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `scheduler_worker.py` créé avec 5 subcommands (list, submit, run, dead-letter, alerts). 9 actions supportées. Retry × 3 avec backoff exponentiel (10s/60s/300s). Dead-letter automatique après 3 échecs. Alertes critiques générées sur dead-letter. Backend file-based (data/scheduler/{jobs,dead_letter,alerts}/). Testé avec 4 jobs réussis + 1 job échec → retry → dead-letter → alerte. Ledger events produits. P9 débloqué.
| P9 | Canary automation ✅ | Petite automation réelle non critique (premier write !) | dual confirm — FAIT |

### P9 — Détail

- **preconditions** : P8 complété, scheduler worker fonctionnel, kill switch en place, HITL gate validé
- **allowed actions** : PROPOSE canary action (3 actions supportées), CONFIRM avec dual approval (2 confirms), EXECUTE non-dry-run write, LIST proposals, HISTORY des exécutions
- **forbidden actions** : exécuter avec 0 ou 1 confirmation, exécuter une action critique, exécuter sans ledger, ignorer le dual confirm
- **evidence required** : canary_worker testé full cycle (propose → confirm1 → confirm2 → execute), marker écrit avec dry_run=false, ledger events produits, dual confirm vérifié
- **rollback** : supprimer `data/canary/`, revert `canary_worker.py`
- **ledger event** : CANARY (CANARY_PROPOSE → CANARY_CONFIRM → CANARY_WRITE_MARKER/CANARY_SEND_NOTIFICATION/CANARY_LOG_UPDATE)
- **closeout eligibility** : canary_worker fonctionnel, cycle complet validé, premier write non-dry-run réussi, dual confirm prouvé, ledger events OK
- **Verdict** : ✅ PASS_WITH_EVIDENCE — `canary_worker.py` créé. **Premier write non-dry-run du projet** : marker écrit dans `data/canary/markers/98cd0510ec21.json` avec `dry_run: false`, après dual confirm (human_01 + human_02). 3 canary actions supportées. Cycle complet testé (propose → confirmed_once → executed). 8+ events ledger. P10 débloqué.
| P10 | Parent closeout | Seulement quand tout est prouvé | PASS_WITH_EVIDENCE total |

## 12_INVARIANTS

```
Aucune action trading live.
Aucun write autonome.
Aucune app externe ne devient source de vérité.
Tout write passe par HITL.
Tout job écrit dans le ledger.
Tout échec a rollback ou dead-letter.
Tout bouton cockpit dangereux est bloqué par kill switch / dual confirm.
```

## Roles

| Role | Périmètre | Phase min |
|---|---|---|
| Human Owner | Décisions L6+, closeout, override | P0+ |
| Runtime Operator | Exécution, monitoring, alertes | P2+ |
| Security Gatekeeper | Kill switch, anti-leak, permissions | P1+ |
| AI Team Manager | Orchestration, validation, escalation | P3+ |
| Strict Worker | Lecture seule, inventaire borné | P2+ |
| Specialist Worker | Draft, analyse, proposition | P3+ |
| App Bridge | Écriture bridgée sous contrat | P5+ |
| LocalCMS Cockpit | Visualisation, supervision | P7+ |
| CI Scheduler | Jobs planifiés, retry, dead-letter | P8+ |

## Checklist par phase

Chaque phase doit fournir :

- **preconditions** : état requis avant activation
- **allowed actions** : actions autorisées dans la phase
- **forbidden actions** : actions bloquées
- **evidence required** : preuve attendue pour passer à la phase suivante
- **rollback** : comment annuler la phase
- **ledger event** : event type écrit dans le ledger
- **closeout eligibility** : condition pour fermer la phase

## No-live-trading policy

- Toute chaîne de signal reste en dry-run (P6)
- Aucun ordre live n'est émis par la stack d'automatisation
- Toute suggestion de trading est journalisée et non exécutée
- Les invariants G10 (dry-run guard) et G07 (HITL) sont verrouillés

## NEXT_GO candidates (P3 complété — P4 ouvrable)

| Candidat | Description | Dépend de |
|---|---|---|
| `GO_AUTOMATION_ROLLOUT_PHASE_01_OBSERVE_ONLY_01` | Phase observe-only runtime | P0 ✅ |
| `GO_AUTOMATION_ROLLOUT_PHASE_02_STRICT_WORKERS_READONLY_RUNTIME_01` | Strict workers en production | P1 ✅ |
| `GO_AUTOMATION_ROLLOUT_PHASE_03_DRAFT_AUTOMATION_01` | Draft pipeline actif | P2, P3 ✅ |
