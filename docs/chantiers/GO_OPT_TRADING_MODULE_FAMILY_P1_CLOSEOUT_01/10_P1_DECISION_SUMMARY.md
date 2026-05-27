---
doc_id: GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01_P1_DECISION_SUMMARY
doc_type: decision_summary
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01
status: draft_for_review
lifecycle_stage: closeout
topic_keys:
  - opt-trading
  - modules
  - family
  - p1
  - decisions
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-23
links:
  - docs/chantiers/GO_OPT_TRADING_MODULE_FAMILY_P1_CLOSEOUT_01/00_INITIAL_PROJECT_DOC.md
---

# 10_P1_DECISION_SUMMARY

## P1 direct status

```text
P1_DIRECT_MODULE_FAMILY_CONSOLIDATION = COMPLETE_DOC_ONLY
Order completed: reseau_ssh -> vision -> perf -> journal
Working baseline: CURRENT_BASELINE_2026_05_20 = 98
Historical audit reference preserved: 87
```

## Family decisions

| Family | Decision | Verdict |
| --- | --- | --- |
| `reseau_ssh` | `modules/reseau_ssh` = unique owner canonique operationnel ; `reseau_ssh_step1b` et `scripts/reseau_ssh` = residuals retires ou archival candidates | `PASS` |
| `vision` | `vision_bot` = owner canonique documentaire + runtime utile ; `bot_vision_step2` = composant operatoire actif ; `bot_vision` = legacy preserve | `PASS` |
| `perf` | `perf` = owner canonique documentaire + facade compat/runtime utile ; `perf_engine` = moteur historique actif | `PASS` |
| `journal` | `journal_engine` = survivant canonique documentaire + moteur actif ; `journal_de_bord` = legacy retire hors parc courant | `PASS` |

## Decision notes by family

### `reseau_ssh`

- la famille est consideree canonisee en un seul owner top-level
- `modules/reseau_ssh` est le seul owner operationnel a conserver comme reference de famille
- les residuals restants ne rouvrent pas la dualite

### `vision`

- la famille ne se resout pas en survivant physique unique a ce stade
- la paire operatoire `vision_bot + bot_vision_step2` reste necessaire
- `bot_vision/headless_capture` reste un runtime utile encore mal heberge sous legacy

### `perf`

- la canonicalite de famille a bascule vers `modules/perf/*`
- l'implementation moteur reste historiquement logee sous `modules/perf_engine/*`
- la famille est donc stable mais encore split entre facade canonique et implementation moteur

### `journal`

- le parc courant n'expose plus de dualite vivante
- `journal_de_bord` n'est plus une surface active a consolider
- le survivant unique du parc courant est `journal_engine`

## P1 closeout conclusion

P1 directe ne laisse plus de famille ouverte parmi les quatre cibles prioritaires.

Les suites restantes sont de deux types :

- realignements registry/documentaires
- GOs physiques/runtime separes pour les noeuds encore mal heberges ou split
