---
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_PLAYWRIGHT_RUNTIME_REPAIR_01
surface: ADMIN_TRADING
source_kind: smoke_result
updated_at: 2026-05-19
---

# 20_SMOKE_RESULT

## Objectif

Prouver la chaine minimale apres reparation Playwright :

```text
capture_headless.js
-> PNG + JSON sidecar
-> vision_processed
-> vision_outbox .txt/.md
```

## Commande executee

Commande manuelle unique executee depuis :

`/opt/trading/modules/bot_vision/headless_capture`

```bash
BOT_VISION_OUT=/srv/sftp/shared_files/shared/vision_inbox npm run capture:example
```

Le profil utilise est `profiles.example.json`, sans modification.

## Fenetre temporelle

| Evenement | Horodatage |
| --- | --- |
| smoke start | `2026-05-19T03:05:45-04:00` |
| capture timestamp | `2026-05-19_03-05-46` |
| smoke end | `2026-05-19T03:06:09-04:00` |

## Sortie capture

Capture observee :

```text
[2026-05-19_03-05-46] Capturing: tradingview BTCUSDT.P (https://www.tradingview.com/chart/?symbol=BTCUSDT.P)
OK: /srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.png (172202B)
OK: /srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.json (497B)
DONE: tradingview -> screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.png
Capture cycle complete.
```

## Artefacts observes apres ingestion

Le PNG a ete deplace par l'ingestion downstream :

```text
/srv/sftp/shared_files/shared/vision_processed/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.png
size=172202
```

Le JSON sidecar est reste dans `vision_inbox` :

```text
/srv/sftp/shared_files/shared/vision_inbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.json
size=497
```

Sorties extraction observees dans `vision_outbox` :

```text
/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.txt
size=1197

/srv/sftp/shared_files/shared/vision_outbox/screen_tradingview_BTCUSDT.P_H1_2026-05-19_03-05-46.md
size=1348
```

## Controle `.uploading`

Recherche read-only :

```bash
find /srv/sftp/shared_files/shared/vision_inbox -maxdepth 1 -type f -name '*.uploading'
```

Resultat : aucune sortie.

## Services actifs observes

Services/timers actifs pertinents :

```text
bot_vision_step2.service          active running
vision_bot.service                active running
bot-vision-headless-capture.timer active waiting
bot_vision_step2_prune.timer      active waiting
```

Unit files pertinents :

```text
bot-vision-headless-capture.service disabled enabled
bot_vision_step2.service            enabled  enabled
vision_bot.service                  enabled  enabled
bot-vision-headless-capture.timer   enabled  enabled
```

Le service headless apres correction a ete observe avec :

```text
Result=success
ExecMainStatus=0
ActiveState=inactive
SubState=dead
```

Le timer etait reste actif et a declenche automatiquement a :

```text
LastTriggerUSec=Tue 2026-05-19 03:04:51 EDT
```

Aucun restart manuel n'a ete effectue.

## Desk bridge

`desk/snapshots` n'a pas ete valide dans ce run. Le point reste hors scope de cette reparation et doit etre traite dans un chantier separe si necessaire.

## Verdict smoke

Criteres valides :

| Check | Resultat |
| --- | --- |
| PNG cree | PASS, `172202` bytes |
| JSON sidecar cree | PASS, `497` bytes |
| `.uploading` stale | PASS, aucun fichier observe |
| ingestion `vision_processed` | PASS, PNG deplace |
| extraction `vision_outbox` | PASS, `.txt` et `.md` crees |
| `desk/snapshots` | non valide dans ce run |

Verdict :

`PASS_SMOKE_CAPTURE_INGESTION_EXTRACTION`
