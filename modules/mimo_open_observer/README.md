# mimo_open_observer

## Description
Module doc-first pour observer XAUUSD à l'ouverture, détecter le premier FVG sur les 5 premières bougies M1 de 18:00 (America/Montreal), journaliser l'événement brut, puis enrichir avec des outcomes simples à +30m / +60m.

## Statut
- phase: K8.3 market calendar
- doc pack: complet
- package Python: complet (K1..K8)
- runners CLI: detect_once, detect_range, replay, check_window, sample_pending, build_stats, show_stats
- cmd.sh: façade shell opérationnelle (10 commandes)
- menu.sh: menu interactif opérationnel (10 options)
- flux nominal: detect → sample → stats
- flux replay: `cmd.sh replay --csv <file>` (detect + sample + stats en un)
- calendrier: fenêtres marché configurables (open_1800 activé, open_0000 prêt)
- providers:
  - fixture (tests, inchangé)
  - csv_replay (données M1 réelles/semi-réelles)
    - `fixtures/sample_xauusd_m1.csv` → no_event (dérive baissière, 60 bars)
    - `fixtures/sample_xauusd_m1_signal.csv` → bullish FVG + sweep, 95 bars
  - ccxt (Binance XAUUSDT M1, proxy live)
- scheduler/dashboard: non implémentés

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
- `app/` (package Python K1..K8)
- `fixtures/` (scénarios de test + CSV replay)
- `docs/`
- `registry_patch/`
- `scripts/`

## CSV Replay Format
Colonnes attendues :
```
ts_open,ts_close,open,high,low,close
```
- timestamps en ISO 8601 (ex: `2026-03-22T18:00:00-04:00`)
- OHLC en float
- une ligne = une bougie M1
- trié par `ts_open` croissant

## Replay Usage
```bash
# full pipeline in one command
cmd.sh replay --csv fixtures/sample_xauusd_m1.csv

# or step by step
cmd.sh detect_once
cmd.sh sample_pending
cmd.sh build_stats
cmd.sh show_stats
```

## CCXT Provider
Mode `ccxt` pour données live M1 depuis Binance.

Instrument par défaut : `XAUUSDT` (proxy, pas XAUUSD spot pur).

```yaml
provider:
  mode: ccxt
  ccxt:
    exchange: binance
    symbol: XAUUSDT
    timeframe: 1m
    limit: 500
```

Dépendance : `pip install ccxt`

## Remarque
Ce pack suit le modèle `opt-trading` (module durable + wrappers + registres) et l'esprit `localcms` (doc d'ouverture structurée, index compact, continuité de session).
