---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_ROLLOUT_PLAN
doc_type: automation_rollout_plan
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: draft
---

# 85_AUTOMATION_ROLLOUT_MASTER_PLAN

## 1_MASTER_TARGET

Passer des briques PASS_WITH_EVIDENCE vers une automatisation contrôlée par phases.
Aucun closeout tant que chaque phase n'a pas evidence.

## 7_CANONICAL_STATE

- PR #678 agrège les GO enfants (G01-G12) mergée dans `sot/mainline`
- G01-G12 couverts avec preuves
- ledger root path corrigé (parents[3])
- parent GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01 non fermé

## 8_VALIDATED_PLAN

| Phase | Nom | Objectif | Gate |
|---|---|---|---|
| P0 | Freeze baseline | Figer PR #678 comme base evidence | merge + diff review |
| P1 | Observe-only | Lire, inventorier, journaliser | read-only |
| P2 | Strict workers runtime | Exécuter jobs read-only bornés | runner + logs |
| P3 | Draft automation | Produire patchs / docs / propositions sans write | dry-run |
| P4 | HITL write-gated | Exécuter seulement après approval humain | approval packet |
| P5 | App bridges | Airtable / Sheets / Telegram / LocalCMS sous contrat | bridge contract |
| P6 | Signal dry-run | Signaux → validation → journal → backtest, sans ordre live | dry-run guard |
| P7 | Cockpit LocalCMS | Supervision, boutons sûrs, kill switch | UI safe buttons |
| P8 | Scheduler/CI | Jobs planifiés, retries, dead-letter, alerting | CI + ledger |
| P9 | Canary automation | Petite automation réelle non critique | dual confirm |
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

## NEXT_GO candidates (ouverts après P1)

| Candidat | Description | Dépend de |
|---|---|---|
| `GO_AUTOMATION_ROLLOUT_PHASE_01_OBSERVE_ONLY_01` | Phase observe-only runtime | P0 |
| `GO_AUTOMATION_ROLLOUT_PHASE_02_STRICT_WORKERS_READONLY_RUNTIME_01` | Strict workers en production | P1 |
| `GO_AUTOMATION_ROLLOUT_PHASE_03_DRAFT_AUTOMATION_01` | Draft pipeline actif | P2 |
