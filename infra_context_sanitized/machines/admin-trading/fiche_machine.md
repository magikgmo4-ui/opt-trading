# Fiche Machine — admin-trading

## Identité
- Hostname: admin-trading
- OS: Debian GNU/Linux 12 (bookworm)
- Kernel: Linux admin-trading 6.1.0-42-amd64 #1 SMP PREEMPT_DYNAMIC Debian 6.1.159-1 (2025-12-30) x86_64 GNU/Linux
- CPU: 
- CPU details: CPU(s)= sockets= cores/socket=
- RAM: 7,7Gi       4,2Gi       360Mi       719Mi       4,1Gi       3,5Gi

## Réseau (LAN)
- Subnet: 192.168.0.0/24
- Interface: wlo1
- IP: 192.168.0.111/24
- Gateway: 192.168.0.1
- DNS: 192.168.0.1
- Ports en écoute (snapshot): 22, 631, 4040, 5353, 8000, 8010, 42029, 51385, 51820

Note 2026-04-20: `192.168.16.155/24` est une valeur de snapshot historique (ancien routeur).

## Stockage (extrait)
### df / volumes
```
Sys. de fichiers Type     Taille Utilisé Dispo Uti% Monté sur
udev             devtmpfs   3,8G       0  3,8G   0% /dev
tmpfs            tmpfs      784M    1,8M  782M   1% /run
/dev/sda1        ext4       219G    9,0G  198G   5% /
tmpfs            tmpfs      3,9G       0  3,9G   0% /dev/shm
tmpfs            tmpfs      5,0M     16K  5,0M   1% /run/lock
tmpfs            tmpfs      784M    112K  784M   1% /run/user/1000
```

### lsblk
```
NAME   FSTYPE FSVER LABEL UUID                                 FSAVAIL FSUSE% MOUNTPOINTS
sda                                                                           
├─sda1 ext4   1.0         c18c8ef7-b793-41f5-a42b-5e75a7645e4d  197,9G     4% /
├─sda2                                                                        
└─sda5 swap   1           97370712-1c22-4e39-b233-fd00f66eb807                [SWAP]
```

## Services (extrait)
```
<REDACTED_TUNNEL>-tv.service              loaded active running <REDACTED_TUNNEL> tunnel for TradingView webhook
tv-bitget-runner.service      loaded active running Bitget -> TV runner (poll candles and send /tv)
tv-webhook.service            loaded active running TradingView Webhook Server (FastAPI/Uvicorn)
```

## Docker (extrait)
```
docker not installed / not running
```

> Généré automatiquement depuis le snapshot le 2026-02-26T17:55:55.
