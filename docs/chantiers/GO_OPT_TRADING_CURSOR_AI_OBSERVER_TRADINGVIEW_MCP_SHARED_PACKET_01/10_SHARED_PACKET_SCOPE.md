# 10_SHARED_PACKET_SCOPE — Scope Option B

## Objectif

Permettre un export controle du bridge packet V1 vers un dossier de staging local. Le packet peut ensuite etre transfere manuellement (WinSCP) vers le shared folder admin-trading si necessaire.

## Ce qui est active

- Script `export_shared_packet.ps1` ajoute au module `tradingview_observer/`
- Dossier de staging local : `_shared_packets/tradingview_observer/` (ignore par git)
- Export horodate : `SYMBOL_TF_YYYYMMDD_HHMMSS_bridge_packet_v1.json`
- Copie `latest_bridge_packet.json` maintenue dans le dossier staging

## Ce qui n'est PAS active

- Aucun transfert automatique (SSH, SFTP, WinSCP automatise)
- Aucune ingestion admin-trading
- Aucun cron/systemd/watch
- Aucun module admin-trading de lecture
- Aucune modification du runtime webhook admin-trading
- Aucune copie du rapport complet (seulement le bridge packet synthetique)

## Chemins

### Option B.1 — Local staging (ACTIF)

```
C:\Users\ghost\opt-trading\_shared_packets\tradingview_observer\
```

Utilise pour stocker les exports horodates localement, sans transfert reseau.

### Option B.2 — Shared SFTP folder (CANDIDAT)

```
/srv/sftp/shared_files/shared/tradingview_observer/
```

Cible pour le transfert manuel WinSCP. Non automatise. Reserve a un GO futur si le besoin admin-trading est prouve.

## Transfert manuel (procedure documentee)

1. Executer `.\export_shared_packet.ps1` sur cursor-ai
2. Ouvrir WinSCP
3. Naviguer vers `_shared_packets\tradingview_observer\`
4. Copier le fichier horodate vers `/srv/sftp/shared_files/shared/tradingview_observer/`
5. Cote admin-trading, le fichier est lisible manuellement

## RISKS

- À qualifier.
