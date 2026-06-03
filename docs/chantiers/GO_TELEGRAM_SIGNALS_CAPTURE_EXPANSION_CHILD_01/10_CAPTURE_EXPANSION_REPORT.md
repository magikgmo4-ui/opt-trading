# Capture expansion — coinglass 20 + glassnode + whale_alert_io

**Generated:** 2026-06-03 05:22 UTC  
**Branch:** `go/GO_TELEGRAM_SIGNALS_CAPTURE_EXPANSION_CHILD_01`  
**Base:** `sot/mainline` (PR #1071 merged: `a956fc21`)

---

## 1. Runs

| Channel | `--limit` | Messages | Run ID |
|---|---|---|---|
| coinglass_alerts | 20 | 20 | `20260603T052159Z-85c50467` |
| glassnode | 20 | 20 | `20260603T052200Z-65a5e2b5` |
| whale_alert_io | 20 | 20 | `20260603T052200Z-615bc8ff` |

**Total:** 60 messages, 0 errors.

---

## 2. Comparaison parsing qualité

| Métrique | coinglass_alerts | whale_alert_io | glassnode |
|---|---|---|---|
| Messages | 20 | 20 | 20 |
| Parsed | **19** (95%) | **18** (90%) | **12** (60%) |
| Unknown | 1 | 2 | 8 |
| Noise | 0 | 0 | 0 |
| Avg parser score | **0.78** | **0.79** | **0.58** |
| Types dominants | MARKET_STRUCTURE | MARKET_STRUCTURE, NEWS_CATALYST | NEWS_CATALYST |

### 2.1 coinglass_alerts — 19/20 parsed

19 whale alerts Hyperliquid (chinois) + 1 transfer on-chain (`大额转账` WBTC $422M).

Format très structuré :
```
实时监控：Hyperliquid巨鲸**(0x89e2)** 以 **40x** 杠杆做空**BTC**,
开仓价格 **$67070.4**,仓位价值**134.2万**美元.
```

Champs extractibles : adresse whale, levier, direction (long/short), symbole, prix entrée, valeur position. Score 0.78 stable depuis la phase 1.

Le 1 unknown est un format différent (transfer notification, pas whale position). À ajouter au parser si pertinent.

### 2.2 whale_alert_io — 18/20 parsed

Mix de :
- **Transfers gros montants** (BTC, USDT, USDC, ETH, XLM) entre exchanges et wallets — 15 messages
- **News/crash headlines** — 3 messages (market liquidation, Radiant shutdown, Sui outage)
- **2 unknown** — formats non reconnus

Score 0.79 — meilleur score des 3. Excellente source pour tracking whales et flux exchange.

### 2.3 glassnode — 12/20 parsed

Contenu analytique long-form (recherche on-chain). 8 messages vides (just `\n`). Les 12 parsés sont des NEWS_CATALYST.

Score 0.58 — significativement plus bas. Les messages sont des pavés de texte, pas des alertes structurées. Utile pour contexte macro mais difficile à parser automatiquement.

---

## 3. Distribution par type

| Type | coinglass | whale_alert | glassnode | Total |
|---|---|---|---|---|
| MARKET_STRUCTURE | 19 | 12 | 0 | 31 |
| NEWS_CATALYST | 0 | 6 | 12 | 18 |
| UNKNOWN_RAW | 1 | 2 | 8 | 11 |

---

## 4. Décision

| Canal | Valeur signal | Qualité parse | Recommandation |
|---|---|---|---|
| coinglass_alerts | 🟢 Très haute (whales temps réel) | 🟢 0.78 — stable | **Activer en production** — limit=50 |
| whale_alert_io | 🟢 Haute (flux exchange) | 🟢 0.79 — meilleur score | **Activer en production** — limit=50 |
| glassnode | 🟡 Moyenne (analyses long-form) | 🟠 0.58 — perfectible | **Garder en veille** — utiles pour contexte mais parsing difficile |

### Recommandation immédiate

1. Activer coinglass_alerts et whale_alert_io en capture régulière (limit=50)
2. Améliorer le parser coinglass : ajouter le format `大额转账` (transfer notification)
3. Améliorer le parser glassnode : filtrer les messages vides, extraire les résumés
4. Ajouter un canal supplémentaire : `cryptoquant_official` (data on-chain)

---

## 5. Outputs

| Fichier | Chemin |
|---|---|
| Raw coinglass_alerts | `outputs/raw/coinglass_alerts.jsonl` |
| Raw glassnode | `outputs/raw/glassnode.jsonl` |
| Raw whale_alert_io | `outputs/raw/whale_alert_io.jsonl` |
| Results coinglass | `outputs/channel_results/channel_results_20260603T052159Z-85c50467.json` |
| Results glassnode | `outputs/channel_results/channel_results_20260603T052200Z-65a5e2b5.json` |
| Results whale_alert | `outputs/channel_results/channel_results_20260603T052200Z-615bc8ff.json` |
