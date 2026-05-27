---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-26
updated_at: 2026-05-26
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
SURFACE_LINK: PF_GOOGLE_SHEETS_CONSUMER
---

# 40_GAPS_AND_NEXT_GO — Lacunes et prochains GOs

## Ce GO ne livre pas

| Hors scope | Raison |
|---|---|
| Google Sheets API réelle (credentials + spreadsheet_id) | Activation runtime séparée |
| Orchestrateur / scheduler | Géré par un GO orchestrator |
| Support multi-symbol | Consumer reste `latest_only` |
| Contrats producers (côté derivatives / spot) | Chaîne producer contractuelle = GOs dédiés |
| Registry runtime “consumers last run” | Non requis pour valider le contrat consumer |

## Prochains GOs (ordre logique)

1. **GO_OPT_TRADING_DATA_CENTER_CHILD_REGISTRY_STORAGE_01** — stockage/rotation/latence autour de `data/data_center/_registry/`
2. **GO_OPT_TRADING_DATA_CENTER_CHILD_PRODUCER_CONTRACTS_01** — cadrer les producers contractuels ≥2 requis par le close-gate parent
3. **GO_OPT_TRADING_ORCHESTRATOR_CHILD_DATASHEET_WRITER_V1_IMPL_01** — wiring runtime vers SheetsWriter (activation contrôlée)
