# KANBAN — GO_SPACEX_SUPER_DESK_PARENT_01

## TODO

- Brancher route Desk Pro native `/desk/spacex`.
- Brancher Telegram réel via rôle `telegram_collector` ou dispatcher existant.
- Brancher Google Sheets réel via `google_sheets_global_schema`.
- Ajouter profil Bot Vision à runtime si accepté.
- Ajouter template TradingView Pine/alert actif.
- Enrichir collectors SEC/news avec clés disponibles.
- Ajouter backtest Trading Lab quand données SPCX disponibles.

## IN_PROGRESS

- Bundle V2 : implémentation sérieuse, dry-run autonome, stockage, scoring, UI, rapports.

## DONE

- Parent validé.
- Source map initiale créée.
- Config SpaceX Super Desk créée.
- Scripts opérateur créés.
- Collecteur public/fallback créé.
- Scoring initial créé.
- UI statique créée.

## VALIDATION GATES

- G1 : `python3 -m modules.ipo_tracking.cli collect-once --offline-ok` retourne ok.
- G2 : `data/ipo/spacex/raw/spacex_snapshots.jsonl` contient un snapshot.
- G3 : `data/data_center/views/spacex_super_desk/latest.json` existe.
- G4 : `reports/ipo/spacex/spacex_daily_YYYYMMDD.md` existe.
- G5 : aucun secret écrit.
- G6 : aucune exécution trading.
