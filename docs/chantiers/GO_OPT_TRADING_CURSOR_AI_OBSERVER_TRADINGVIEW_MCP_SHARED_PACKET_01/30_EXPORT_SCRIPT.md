# 30_EXPORT_SCRIPT — export_shared_packet.ps1

## Fichier

`modules/tradingview_observer/export_shared_packet.ps1`

## Usage

```powershell
# Dry-run (affiche ce qui serait copie)
.\export_shared_packet.ps1 -DryRun

# Export reel vers staging local
.\export_shared_packet.ps1

# Export vers un dossier specifique
.\export_shared_packet.ps1 -OutputDir "D:\backups\tv_observer"
```

## Comportement

1. Verifie que `latest_bridge_packet.json` existe
2. Si absent, lance `export_bridge_packet.ps1` pour le generer
3. Cree le dossier de staging `_shared_packets/tradingview_observer/SYMBOL/`
4. Copie le packet avec nom horodate : `SYMBOL_TF_YYYYMMDD_HHMMSS_bridge_packet_v1.json`
5. Copie egalement `latest_bridge_packet.json` dans le dossier staging
6. Aucun transfert reseau
7. Aucune ecriture dans admin-trading
8. Aucun appel SSH/SFTP/WinSCP

## Parametres

| Parametre | Defaut | Description |
|-----------|--------|-------------|
| `-OutputDir` | `_shared_packets\tradingview_observer\` | Dossier staging cible |
| `-DryRun` | `$false` | Affiche les actions sans ecrire |

## Securite

- Read-only : ne modifie jamais TradingView
- Local only : aucun acces reseau
- Git-ignored : le dossier `_shared_packets/` est dans `.gitignore`
- Pas de secrets : le bridge packet ne contient ni tokens ni .env ni API keys

## RISKS

- À qualifier.
