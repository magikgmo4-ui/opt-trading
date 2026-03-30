# mimo_open_observer

## Description
Module doc-first pour observer XAUUSD à l'ouverture, détecter le premier FVG sur les 5 premières bougies M1 de 18:00 (America/Montreal), journaliser l'événement brut, puis enrichir avec des outcomes simples à +30m / +60m.

## Statut
- phase: K2 socle données
- doc pack: complet
- package Python: initialisé
- config loader: présent
- modèles: présents
- data_provider: présent (mode fixture)
- utils_time: présent
- fixtures: 3 scénarios (no_event, bullish_no_sweep, bearish_sweep)
- logique métier FVG: non implémentée
- provider réel: non branché

## Workflow retenu
Chaîne canonique:
1. detect
2. raw journal
3. outcome sampling
4. stats

## Périmètre V0
- symbol: XAUUSD
- timezone: America/Montreal
- fenêtre: 18:00
- jours: dim → jeu
- scope: M1x5
- signal: premier FVG seulement
- tag: sweep / no_sweep
- horizons: +30m / +60m

## Structure module
- `cmd.sh`
- `menu.sh`
- `sanity.sh`
- `config/mimo_open_observer.yaml`
- `app/` (package Python K1+K2)
- `fixtures/` (scénarios de test)
- `docs/`
- `registry_patch/`
- `scripts/`

## Remarque
Ce pack suit le modèle `opt-trading` (module durable + wrappers + registres) et l'esprit `localcms` (doc d'ouverture structurée, index compact, continuité de session).
