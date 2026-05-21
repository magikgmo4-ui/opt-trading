---
doc_id: G05_SOURCE_OF_TRUTH_COVERAGE
doc_type: transversal_coverage
gap_id: G05
parent_go: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: passed_with_evidence
---

# 70_G05_SOURCE_OF_TRUTH_COVERAGE.md

## Domaine → Source canonique → GO couvrant

| Domaine | Source canonique (rank 1) | Couvert par | Preuve |
|---|---|---|---|
| Machine/Service topology | `config/machine_runtime_map.yml` | G01 (M08, M13) | `10_CAPABILITY_MATRIX.md` evidence_ref |
| App bridge contracts | Bridge contracts docs | G04 | `20_BRIDGE_CONTRACTS.md` — 10 apps |
| Capability/permissions | `10_CAPABILITY_MATRIX.md` | G01 | Matrice 30 lignes, 3 scénarios validés |
| Ledger events | `data/runtime_health/ledger/events.jsonl` | G06 | Ledger schema + writer + replay |
| Worker definitions | `STRICT_WORKERS_AUTONOMIE_ETROITE_01.md` | G01, G02 | Evidence_ref dans matrice |
| Agent config | `agent_model_matrix.yaml` | G01 | M06 evidence_ref |
| Health status | `health_status.py` output | G09 | Status JSON validé |
| Kill switch | `data/runtime_health/kill_switch.state` | G08, G11 | `40_KILL_SWITCH.md` |
| UI surfaces | `registry/ui_surfaces_registry.yaml` | G11 | Cockpit pages |

## Règles de sync

- La source canonique (rank 1) fait autorité en cas de conflit
- Les rangs 2-5 sont des caches ou vues dérivées
- Aucune sync automatique inter-source sans HITL gate (G07)
- Le ledger (G06) trace toute mise à jour inter-source
