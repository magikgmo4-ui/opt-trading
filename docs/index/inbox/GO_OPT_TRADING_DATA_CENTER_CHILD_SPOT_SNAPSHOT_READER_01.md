---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01_INBOX
doc_type: inbox
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_OPEN_01
status: open
created_at: 2026-05-25
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_SPOT_SNAPSHOT_READER_01

Flux `pair_market_snapshot.v1` câblé : collector → DC producer path → view → Desk Pro reader.

- **Tests** : 105 PASS (97 DC + 8 reader) + sanity PASS
- **Nouveaux fichiers** : `spot_snapshot_dc_writer.py`, `spot_snapshot_reader.py`, 10+8 tests
- **consumers.json** : `desk_pro__spot_snapshot = implemented`
- **GAP-P03 fermé** : collector_binance_spot bridge vers DC (fixture-first)
- **Runtime collector inchangé** : câblage runtime = phase 2
- **Prochaine étape** : GO_OPT_TRADING_DATA_CENTER_CHILD_REFS_TIMESTAMPS_PRODUCER_STANDARD_01
