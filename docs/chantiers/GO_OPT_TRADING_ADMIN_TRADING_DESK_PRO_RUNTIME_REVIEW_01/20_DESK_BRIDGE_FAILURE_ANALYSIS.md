---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01_BRIDGE
doc_type: failure_analysis
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 20_DESK_BRIDGE_FAILURE_ANALYSIS

## Service

- **Nom**: desk_bridge.service
- **Description**: Desk Bridge (vision_processed -> inbox -> ingest_once)
- **Statut**: FAILED (depuis 2026-05-01)
- **Timer**: desk_bridge.timer (ACTIVE, every 10 min, retries continuent d'echouer)
- **Script**: scripts/desk_bridge/bridge_vision_to_desk_inbox.sh

## Pipeline attendu

```
ShareX screenshot -> SFTP -> vision_inbox/*.png
  -> vision_bot (OCR) -> vision_processed/*.png
  -> desk_bridge (crop 2x2) -> inbox/q_*.png
  -> desk_snapshot_ingest -> desk_inbox
```

## Erreur constatee

```
PIL.UnidentifiedImageError: cannot identify image file
'/srv/sftp/shared_files/shared/vision_inbox/screen_2026-03-06_04-07-07_7.png'
```

Le script tente `Image.open()` sur un fichier .png qui est en realite vide (0 octet).

## Root cause

### Cause primaire: Inputs corrompus

9 fichiers 0-byte dans /shared/vision_inbox/ :

| Fichier | Date | Taille |
| --- | --- | --- |
| screen_2026-03-05_23-08-47_8.png | 5 mar | 0 B |
| screen_2026-03-05_23-45-30_2.png | 5 mar | 0 B |
| screen_2026-03-05_23-55-30_0.png | 6 mar | 0 B |
| screen_2026-03-06_01-37-07_3.png | 6 mar | 0 B |
| screen_2026-03-06_01-57-07_9.png | 6 mar | 0 B |
| screen_2026-03-06_02-07-07_3.png | 6 mar | 0 B |
| screen_2026-03-06_03-37-07_9.png | 6 mar | 0 B |
| screen_2026-03-06_03-57-07_0.png | 6 mar | 0 B |
| screen_2026-03-06_04-07-07_7.png | 6 mar | 0 B |

Ces fichiers sont des echecs de transfert SFTP (ShareX -> admin-trading). La connexion SFTP a probablement ete interrompue pendant l'upload.

### Cause secondaire: Uploads partiels

5 fichiers `.uploading.*` dans vision_inbox (339-535 KB, avril 2026). Ce sont des uploads SFTP interrompus qui n'ont jamais ete renames en .png final.

### Cause tertiaire: Absence de garde-fou

Le script `bridge_vision_to_desk_inbox.sh` ne verifie pas si le fichier est valide (taille > 0, format detectable) avant d'appeler `Image.open()`. L'erreur PIL est non geree.

## Impact

- **Pipeline bloque**: desk_bridge ne peut traiter aucun screenshot tant qu'un fichier 0-byte est present
- **Retries inutiles**: timer declenche toutes les 10 minutes, echec systematique
- **Pas d'impact sur le core trading**: webhook, perf, Desk Pro runner non affectes
- **Vision/ShareX hors service**: aucune nouvelle capture ne peut etre analysee

## Classification

**BUG INPUT + ABSENCE DE GARDE-FOU**

- Ce n'est pas un bug du pipeline Desk Pro
- Ce n'est pas un bug de PIL/Image.open
- C'est un probleme de donnees d'entree corrompues (SFTP failures)
- Le script manque de validation prealable (taille > 0, format check)

## Recommandation

1. Nettoyer les fichiers 0-byte de vision_inbox
2. Nettoyer les .uploading partiels
3. Ajouter une garde `[ -s "$file" ]` dans le script bridge
4. Relancer desk_bridge pour deverouiller le pipeline
5. Verifier la stabilite SFTP ShareX -> admin-trading
