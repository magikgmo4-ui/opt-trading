---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01_MT5_EXPORT_RUNBOOK
doc_type: runbook
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_XAUUSD_MT5_DUKASCOPY_IMPORT_01
status: open
updated_at: 2026-05-20
---

# 20_MT5_EXPORT_RUNBOOK

## Prérequis

- MetaTrader 5 installé (Windows ou Wine)
- Compte broker avec XAUUSD disponible (démo ou réel)
- Historique téléchargé pour XAUUSD M5 et M15

## Étape 1 — Télécharger l'historique dans MT5

```
MT5 → Outils → Centre des cotations (History Center)
  → Symboles → XAUUSD
  → Double-cliquer XAUUSD pour ouvrir les timeframes
  → M5 → Télécharger (Download)
  → M15 → Télécharger (Download)
  → Attendre que les barres soient disponibles (peut prendre plusieurs minutes)
```

Si `XAUUSD` n'est pas visible dans la liste :
```
MT5 → Affichage → Symboles → Chercher XAUUSD → Ajouter
```

## Étape 2 — Export CSV depuis le History Center

```
Centre des cotations → XAUUSD → M5
  → Sélectionner toutes les barres (Ctrl+A)
  → Clic droit → Exporter
  → Format : CSV
  → Nom fichier : xauusd_m5_raw_mt5.csv
  → Chemin : accessible depuis Linux (partagé ou Samba)
```

Répéter pour M15 → `xauusd_m15_raw_mt5.csv`.

## Format CSV MT5 standard

```text
<DATE>	<TIME>	<OPEN>	<HIGH>	<LOW>	<CLOSE>	<TICKVOL>	<VOL>	<SPREAD>
2024.01.02	08:00	2063.50	2065.10	2062.80	2064.30	1250	0	15
```

Notes :
- Séparateur peut être `\t` (tab) ou `,` selon MT5 version et paramètres
- `<TICKVOL>` = volume tick (toujours disponible), `<VOL>` = volume réel (souvent 0 pour XAUUSD)
- `<SPREAD>` = spread en points (ex: 15 = 1.5 pips = 0.15 USD pour XAUUSD)
- Timezone : dépend du broker (souvent UTC+2/UTC+3 EET — à vérifier dans MT5 → Outils → Serveur)

## Étape 3 — Copier vers le repo

```bash
# Placer les fichiers dans data/market/raw/
mkdir -p /opt/trading/data/market/raw
cp xauusd_m5_raw_mt5.csv /opt/trading/data/market/raw/
cp xauusd_m15_raw_mt5.csv /opt/trading/data/market/raw/
```

## Étape 4 — Normaliser avec normalize_mt5.py

```bash
python tools/strategy/daily_scalping/normalize_mt5.py \
    --input data/market/raw/xauusd_m5_raw_mt5.csv \
    --output data/market/xauusd_m5_canonical.csv \
    --timeframe M5 \
    --broker-tz UTC+2  # ajuster selon votre broker

python tools/strategy/daily_scalping/normalize_mt5.py \
    --input data/market/raw/xauusd_m15_raw_mt5.csv \
    --output data/market/xauusd_m15_canonical.csv \
    --timeframe M15 \
    --broker-tz UTC+2
```

## Vérification post-normalisation

```bash
# Vérifier le résultat
head -3 data/market/xauusd_m5_canonical.csv
# Attendu :
# timestamp,open,high,low,close,volume,bid,ask,spread,source,symbol,timeframe
# 2024-01-02 08:00:00+00:00,2063.50,...,mt5_export,XAUUSD,M5

# Compter les lignes
wc -l data/market/xauusd_m5_canonical.csv
# Attendu : >100 000 lignes pour 2 ans de M5
```

## Run backtest canonical

```bash
python tools/strategy/daily_scalping/run_backtest.py \
    --input data/market/xauusd_m5_canonical.csv \
    --context-input data/market/xauusd_m15_canonical.csv \
    --out artifacts/backtests/daily_scalping_canonical \
    --min-score 7
```

## Timezone broker — cas fréquents

| Broker | Timezone serveur | Offset UTC |
|---|---|---|
| ICMarkets | EET (Eastern European Time) | UTC+2 / UTC+3 (DST) |
| Pepperstone | EET | UTC+2 / UTC+3 |
| XM | GMT+2 | UTC+2 |
| Darwinex | GMT | UTC+0 |

`normalize_mt5.py` convertit automatiquement vers UTC sur la base du `--broker-tz`.
