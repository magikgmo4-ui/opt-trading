# GO_SPACEX_SUPER_DESK_PARENT_01

Status: PARENT_APPROVED_IMPL_V2

Docs:

- docs/chantiers/GO_SPACEX_SUPER_DESK_PARENT_01/00_INITIAL_PROJECT_DOC.md
- docs/chantiers/GO_SPACEX_SUPER_DESK_PARENT_01/KANBAN.md
- docs/chantiers/GO_SPACEX_SUPER_DESK_PARENT_01/90_REPRISE_POINT.md
- docs/chantiers/GO_SPACEX_SOURCE_INVENTORY_CHILD_01/SPACEX_SOURCE_MAP.md
- docs/chantiers/GO_SPACEX_SOURCE_INVENTORY_CHILD_01/SPACEX_DATA_FLOW.md
- docs/chantiers/GO_SPACEX_SOURCE_INVENTORY_CHILD_01/SPACEX_GAP_ANALYSIS.md

Run:

```bash
bash scripts/ipo/spacex_collect_once.sh
bash scripts/ipo/spacex_report_daily.sh
python3 -m modules.ipo_tracking.cli smoke
```
