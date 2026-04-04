# TRADING REALTIME V1 — SKELETON PASS 01

Date (America/Montreal) : 2026-04-04

## RÔLE

Cette passe ouvre le squelette **REALTIME V1** comme module séparé du LAB.

## MODULE OUVERT

- `modules/trading_realtime_v1/`

## STRUCTURE POSÉE

### Docs
- `modules/trading_realtime_v1/docs/README.md`
- `modules/trading_realtime_v1/docs/ETABLI.txt`
- `modules/trading_realtime_v1/docs/RUNBOOK.txt`

### Scripts standards
- `modules/trading_realtime_v1/scripts/cmd.sh`
- `modules/trading_realtime_v1/scripts/menu.sh`
- `modules/trading_realtime_v1/scripts/sanity.sh`
- `modules/trading_realtime_v1/scripts/install_shortcuts.sh`

### App minimale
- `modules/trading_realtime_v1/app/trading_realtime_v1.py`

## CAPACITÉS ACTUELLES

Le module sait déjà :
- afficher son état ;
- pointer vers le profil V1 et les schémas V1 ;
- pointer vers la source LIVE sample ;
- lire le dernier enregistrement LIVE ;
- écrire une observation runtime minimale dans un journal séparé ;
- écrire un résumé de run runtime.

## DÉCISION

Cette passe reste **observation only** :
- pas d’ordre réel ;
- pas d’exécution broker ;
- pas d’auto-trading.

## TRIGGER NATUREL SUIVANT

`GO_OT_TRADING_REALTIME_V1_EVENT_BRIDGE_PASS_01`
