---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01_GAPS_AND_NEXT_GO
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_FIXTURES_01
status: active
source_kind: canonical
updated_at: 2026-05-25
---

# 40_GAPS_AND_NEXT_GO — Google Sheets fixtures V1

## Gaps résiduels — hors scope accepté

| Gap | Raison | Action future |
|---|---|---|
| Écriture Google Sheets API réelle | Credentials non configurés ; hors scope fixtures | Child : GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01 |
| Mapping Data Center → Sheets runtime | consumer `google_sheets__market_reporting` = not_started | Child : GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01 |
| `datasheet_writer` runtime → Sheets | module ouvert ; pas de Sheets writer câblé | Child post-datasheet_writer V2 |
| `learning_feeder` runtime → Sheets | module ouvert ; pas de Sheets writer câblé | Child post-learning_feeder V2 |
| Contrôle des permissions Google | pas de service account / ADC configuré | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_GOOGLE_SHEETS_CREDENTIALS_* existants |
| strategy_events runtime writer | Desk Pro ne produit pas encore vers Sheets | Phase 2 Desk Pro |
| Fixture `strategy_gates.decision = retire` | Enum partiel en fixture | Tolérance V1 documentée |
| Migration daily_sessions worksheet title | Worksheet actuel = "sheet1" ; canonical = "daily_sessions" | Futur child mapping |

## Prochains GOs recommandés

### GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_API_WRITE_01 (priorité 1 si credentials disponibles)

Objectif : prouver un write contrôlé sur `daily_sessions` uniquement (seul tab write-enabled V1).

Prérequis :
- Service account ou ADC configuré (via GO_OPENCLAW credentials chain)
- dry-run default activé

### GO_OPT_TRADING_DATA_CENTER_CHILD_GOOGLE_SHEETS_CONSUMER_01 (priorité 2)

Objectif : câbler `google_sheets__market_reporting` consumer sur `market_metrics.v1` views.

Prérequis :
- market_metrics.v1 views stables (OK : PR #795 merged)
- Google write credentials configurés

### GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_CHILD_DAILY_SESSIONS_TAB_MIGRATION_01 (priorité 3)

Objectif : corriger le worksheet title "sheet1" → "daily_sessions" en cohérence avec le schéma canonique.

## État parent GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01

Ce child marque le milestone **fixtures-first prouvé**. Le schéma V1 est validable localement sans Google API.

Remaining before CLOSE_GATE parent :
- [ ] API write proof (1 tab)
- [ ] Runtime consumer market_metrics → Sheets
- [ ] Tab migration daily_sessions
