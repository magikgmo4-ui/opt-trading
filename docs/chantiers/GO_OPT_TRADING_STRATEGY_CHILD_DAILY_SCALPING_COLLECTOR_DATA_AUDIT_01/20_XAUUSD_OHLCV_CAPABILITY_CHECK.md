---
doc_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01_XAUUSD_OHLCV_CAPABILITY_CHECK
doc_type: capability_check
go_id: GO_OPT_TRADING_STRATEGY_CHILD_DAILY_SCALPING_COLLECTOR_DATA_AUDIT_01
status: closed
audited_at: 2026-05-20
---

# 20_XAUUSD_OHLCV_CAPABILITY_CHECK

## Candidat : simex_bitget_bridge

Seul collector du repo capable de fournir des klines OHLCV sur un instrument gold.

### Ce qu'il fait déjà

```
API Bitget : /api/v2/mix/market/candles
Symbole    : XAUUSDT (USDT-FUTURES)
Granularité: M5 par défaut (300s), configurable via SIMEX_GRANULARITY_SEC
Champs     : timestamp, open, high, low, close, baseVolume, quoteVolume
Output     : HTTP POST vers PERF_EVENT endpoint (perf/event)
```

### Gaps vs contrat XAUUSD_M5_CANONICAL

| Champ / Propriété | Contrat canonique | simex_bitget_bridge | Gap |
|---|---|---|---|
| `timestamp` | UTC, ISO 8601 | présent (ms epoch) | conversion nécessaire |
| `open` | float | présent | OK |
| `high` | float | présent | OK |
| `low` | float | présent | OK |
| `close` | float | présent | OK |
| `volume` | int | baseVolume présent | OK (quoteVolume bonus) |
| `bid` | float obligatoire | **absent** | GAP CRITIQUE |
| `ask` | float obligatoire | **absent** | GAP CRITIQUE |
| `spread` | float obligatoire | **absent** | GAP CRITIQUE |
| `source` | string explicite | absent | ajouter `bitget_futures` |
| `symbol` | XAUUSD | XAUUSDT | GAP INSTRUMENT |
| `timeframe` | M5 | configurable | OK |
| Output format | CSV fichier | HTTP push seulement | GAP OUTPUT |
| Pattern famille | manifest/status/events | absent | GAP PATTERN |
| Profondeur historique | ≥ 180 jours | **non documentée** | GAP HISTORIQUE |

### Analyse des gaps

#### GAP 1 — Bid/Ask/Spread (CRITIQUE)

Bitget `/api/v2/mix/market/candles` ne fournit pas bid/ask dans les klines. Pour obtenir le spread :

- Option A : Appeler séparément `/api/v2/mix/market/ticker` qui fournit `bidPrice`/`askPrice` par snapshot (1 valeur par requête, pas par bar M5)
- Option B : Utiliser le `quoteVolume` / `baseVolume` pour estimer le prix moyen pondéré — ne donne pas le spread
- Option C : Fixer un spread estimé depuis la config (comme PR #658 hardcodait 3.0 pips) — acceptable comme fallback mais pas canonique

**Recommandation** : Option A + C — ajouter un appel ticker simultané au moment du fetch klines pour capturer le spread instantané, et conserver le spread config comme fallback si non disponible.

#### GAP 2 — Instrument XAUUSDT vs XAUUSD (MODÉRÉ)

XAUUSDT = contrat futures perpétuel or sur Bitget, libellé en USDT. XAUUSD = spot forex/CFD oro vs dollar.

Différences pratiques :
- Prix légèrement différent (basis futures vs spot, typiquement quelques $/oz)
- XAUUSDT a un funding rate (impact sur le hold overnight)
- Volume XAUUSDT ≠ volume XAUUSD spot

Pour un backtest scalping M5 avec entrées/sorties intraday, le pricing est proche. Acceptable si documenté. Le `source` doit clairement indiquer `bitget_xauusdt_futures`.

#### GAP 3 — Output HTTP push (BLOQUANT pour backtest fichier)

Le bridge pousse vers un endpoint HTTP. Pour le backtest, on a besoin d'un CSV fichier.

Solution : ajouter un mode `--mode export_csv` qui écrit directement dans `data/market/xauusd_m5_bitget.csv` au lieu de pousser vers perf/event.

#### GAP 4 — Profondeur historique (INCONNU, CRITIQUE)

L'API Bitget `/api/v2/mix/market/candles` a une limite par requête (typiquement 200 bougies max). Pour 180 jours de M5 = 180 × 24h × 12 bougies/h = ~51 840 bougies. Il faut paginer.

À vérifier :
- Limite de pagination de l'API Bitget (max `startTime`/`endTime` range)
- Si 180 jours de data historique sont disponibles via l'API (futures data peut avoir une fenêtre limitée)

#### GAP 5 — Pattern collector famille (FAIBLE PRIORITÉ)

Le bridge ne génère pas de manifest/status/events artifacts comme les autres collectors. Gap de cohérence interne mais non bloquant pour le backtest.

### Estimation effort pour rendre PRIMARY_READY

| Adaptation | Effort | Priorité |
|---|---|---|
| Mode export CSV (au lieu de HTTP push) | 1-2h | BLOQUANT |
| Pagination historique 180j | 2-4h | BLOQUANT |
| Capture spread via ticker API | 2-3h | IMPORTANT |
| Documenter XAUUSDT vs XAUUSD dans source field | 30min | FAIBLE |
| Pattern famille (manifest/status) | 4-8h | NON PRIORITAIRE |

**Total pour PRIMARY_READY minimum** : ~6-9h de développement (mode CSV + pagination + spread approximatif).

### Verdict simex_bitget_bridge

```
Classification : PRIMARY_WITH_GAPS
Adaptable en  : PRIMARY_READY avec ~1 journée de développement
Bloquants     : export CSV, pagination 180j, spread (fallback acceptable)
Non bloquant  : pattern famille, XAUUSDT vs XAUUSD (si documenté)
```
