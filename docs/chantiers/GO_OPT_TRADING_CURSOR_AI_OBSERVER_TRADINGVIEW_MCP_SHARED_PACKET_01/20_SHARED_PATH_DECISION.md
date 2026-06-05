# 20_SHARED_PATH_DECISION — Decision de chemin

## Decision

**Option B.1 — Local staging** est le chemin actif pour Phase 9.

## Justification

- Le montage SFTP partage n'est pas prouve depuis cursor-ai (Windows)
- Le transfert reseau automatise n'est pas securise sans GO dedie
- Le dossier local `_shared_packets/` est ignore par git (`.gitignore`)
- Le script `export_shared_packet.ps1` est dry-run safe par defaut (flag `-DryRun`)

## Chemins

| Option | Chemin | Statut | Transfert |
|--------|--------|--------|-----------|
| B.1 | `_shared_packets/tradingview_observer/` | ACTIF | Manuel local |
| B.2 | `/srv/sftp/shared_files/shared/tradingview_observer/` | CANDIDAT | WinSCP manuel futur |

## Gitignore

```gitignore
# shared packet staging
_shared_packets/
```

Ajoute au `.gitignore` racine. Tout contenu sous `_shared_packets/` est exclu des commits.

## Dossier staging

```
_shared_packets/tradingview_observer/
  BITGET:BTCUSDT.P/
    20260505_003000_bridge_packet_v1.json
    latest_bridge_packet.json
```

## RISKS

- À qualifier.
