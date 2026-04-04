# ShareX Capture Watchdog

## But

Ajouter un check minimal et non destructif pour detecter une panne silencieuse de ShareX AutoCapture cote Windows.

## Script

- `modules/bot_vision_step2/scripts/sharex_capture_watchdog.ps1`

## Hypothese runtime retenue

- dossier surveille par defaut: `C:\monitor\screens`
- motif surveille: `screen_*.png`
- seuil par defaut: `15` minutes

Le chemin par defaut vient du residuel canonique mentionnant `watch_telegram.ps1` sur `C:\monitor\screens` dans `docs/RESIDUEL_BOT_VISION.txt`.
Le script reste configurable via `-WatchPath` si le poste Windows utilise un autre dossier local ShareX.

## Usage nominal

```powershell
powershell -ExecutionPolicy Bypass -File .\sharex_capture_watchdog.ps1
```

## Usage avec seuil explicite

```powershell
powershell -ExecutionPolicy Bypass -File .\sharex_capture_watchdog.ps1 -WatchPath "C:\monitor\screens" -MaxAgeMinutes 15
```

## Sorties

- `STATUS: OK` si le dernier `screen_*.png` est plus recent que le seuil
- `STATUS: ALERT` si le dossier est absent, s'il n'y a aucun fichier, ou si le dernier fichier est trop ancien
- code de sortie `0` pour `OK`, `1` pour `ALERT`

## Validation rapide

### Nominal

```powershell
powershell -ExecutionPolicy Bypass -File .\sharex_capture_watchdog.ps1 -WatchPath "C:\monitor\screens" -MaxAgeMinutes 15
```

### Simulation d'alerte

```powershell
$old = (Get-Date).AddMinutes(-20).ToString("o")
powershell -ExecutionPolicy Bypass -File .\sharex_capture_watchdog.ps1 -WatchPath "C:\monitor\screens" -MaxAgeMinutes 15 -NowIso $old
```

## Portee V1

- aucun changement de `send_vision_inbox.ps1`
- aucun changement du handler `/analyze`
- aucune tache planifiee imposee dans ce patch
- check CLI lisible uniquement
