# 30_SHARED_PACKET_OPTION_B — GO child 2

## GO ID

`GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_SHARED_PACKET_01`

## Phase

Phase 9 — Shared packet Option B

## Objectif

Preparer un export du bridge packet V1 vers le shared folder SFTP (`/srv/sftp/shared_files/shared/...`) sans automatisation, sans ingestion admin-trading, sans service systemd.

## Contexte

- Option A (local manuel) est le mode actif depuis Phase 5.
- Option B a ete documentee mais non activee.
- Le shared folder existe via `modules/shared_files_sftp/`.
- Le transfert Windows -> Linux existe via `modules/winscp_transfer/`.

## Actions attendues

1. Ajouter un flag optionnel a `export_bridge_packet.ps1` pour cibler un dossier de sortie.
2. Documenter la procedure manuelle WinSCP pour deposer le packet vers `/srv/sftp/shared_files/shared/observer_bridge/`.
3. Ne pas automatiser le transfert.
4. Ne pas activer de cron/systemd/watch.
5. Ne pas creer de module admin-trading de lecture.
6. Commit + push.

## Invariants

- Transfert manuel uniquement.
- Aucun admin-trading runtime touche.
- Aucun webhook modifie.
- Aucun service systemd cree ou modifie.
- Aucun trade.

## Statut

PENDING
