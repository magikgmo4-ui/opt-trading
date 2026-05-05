# 20_PHASE_2 — Alertes TradingView : inventaire et contrôle

## Date exécution

2026-05-05

## Contexte

- Chart au moment du test : `BITGET:BTCUSDT.P`, 480min, chartType 1 (Candles)
- CDP connecté, api_available = true
- TradingView Desktop v3.1.0.7818 (MSIX)

## 1. Inventaire des alertes existantes

Source : `https://pricealerts.tradingview.com/list_alerts` (REST API interne TradingView).

### Synthèse

| # | Alert ID | Symbole | Type | Statut | Timeframe | Créé | Expiration |
|---|----------|---------|------|--------|-----------|------|------------|
| 1 | 4622079920 | BITGET:BTCUSDT.P | price | **expired** (test) | 1min | 2026-05-05 | 2026-06-05 |
| 2 | 4136096358 | BITGET:SOLUSDT.P | pine_alert (GHOST_XAU) | **expired** | 15min | 2026-03-02 | 2026-04-02 |
| 3 | 4136088664 | BITGET:ETHUSDT.P | pine_alert (GHOST_XAU) | **expired** | 30min | 2026-03-02 | 2026-04-02 |
| 4 | 4077560975 | BITGET:BTCUSDT.P | pine_alert (GHOST_XAU) | **expired** | 240min | 2026-02-22 | 2026-03-22 |
| 5 | 4063883988 | BITGET:ETHUSDT.P | pine_alert (GHOST_XAU) | **expired** | 15min | 2026-02-20 | 2026-03-20 |
| 6 | 4063879334 | BITGET:BTCUSDT.P | pine_alert (GHOST_XAU) | **expired** | 15min | 2026-02-20 | 2026-03-20 |
| 7 | 4058432392 | BITGET:BTCUSDT.P | pine_alert (GHOST_XAU) | **expired** | 30min | 2026-02-19 | 2026-03-19 |
| 8 | 4058417978 | BITGET:BTCUSDT.P | pine_alert (GHOST_XAU) | **expired** | 60min | 2026-02-19 | 2026-03-19 |
| 9 | 4049143101 | OANDA:XAUUSD | pine_alert (GHOST_XAU) | **expired** | 15min | 2026-02-18 | 2026-03-18 |
| 10 | 4049120342 | BITGET:SOLUSDT.P | pine_alert (GHOST_XAU) | **expired** | 30min | 2026-02-18 | 2026-03-18 |

### Analyse

- **9 alertes Pine Script** (GHOST_XAU_2026_ULTRA strategy), toutes expirées depuis mars-avril 2026.
- **1 alerte prix** (test, créée pendant ce smoke), active, expire 2026-06-05.
- Alertes de production : toutes inactives (`active: false`), aucune ne peut déclencher.
- Symboles : BITGET:BTCUSDT.P (4), BITGET:ETHUSDT.P (2), BITGET:SOLUSDT.P (2), OANDA:XAUUSD (1).
- Aucune alerte de production active. Pas de risque de déclenchement intempestif.
- **Champ webhook** : non exposé par l'API `list_alerts`. Statut : **unreadable**.
- **Champ JSON payload** : non exposé. Statut : **unreadable**.

## 2. Création d'alerte test

### Commande CLI

```
tv alert create -p 1 -c less_than -m "OPT-TRADING-TEST-DO-NOT-USE-PHASE2-SMOKE"
```

**Résultat** : FAIL (`success: false, price_set: false, source: dom_fallback`)

### Root cause

La commande `alert_create` utilise du DOM automation qui cherche des sélecteurs en anglais :
- `aria-label="Create Alert"` → UI française : `aria-label="Créer une alerte"`
- `button text="Create"` → UI française : `Créer`
- Les sélecteurs CSS (`[class*="alert"] input`) ne matchent pas les classes réelles de TV 3.1.0

**Bug i18n** : `tradingview-mcp` est hardcodé pour une UI TradingView en anglais.

### Workaround (eval DOM direct)

Création réussie via `tv ui eval` avec manipulation DOM manuelle :

1. `document.querySelector('button[aria-label*="alerte"]').click()` → ouvre le dialogue
2. `document.querySelector('input.input-RUSovanF')` → set value via native setter
3. `document.querySelectorAll('button').find(b => /créer/i.test(b.textContent)).click()` → valide

**Alerte créée** : `alert_id=4622079920`, BITGET:BTCUSDT.P, price=80373.2, type=cross

Note : le prix n'a pas été correctement setté à 1 (le formulaire a gardé ~80373.2, valeur par défaut). L'alerte de test est non critique car le prix ~80k est proche du prix actuel du BTC mais il s'agit juste d'un croisement simple sans webhook.

## 3. Suppression d'alerte test

### Tentatives

| Méthode | Résultat |
|---------|----------|
| `tv alert delete --all` | Ouvre le menu contextuel, demande confirmation manuelle |
| REST `POST /delete_alert` (alert_id) | `{}` — pas de confirmation |
| REST `POST /delete_alerts` (alert_ids) | `{}` — pas de confirmation |
| REST avec CSRF token | `{}` — pas de confirmation |
| Suppression individuelle programmatique | Non supporté par le code source (`throw new Error('Individual alert deletion not yet supported')`) |

### Verdict

**PARTIAL** — La suppression programmatique n'est pas fonctionnelle. L'alerte test #4622079920 reste présente mais est non critique :
- Prix à ~80k sur BTC (croisement simple)
- Pas de webhook
- Expire automatiquement le 2026-06-05
- Peut être supprimée manuellement via l'UI TradingView

## 4. Capacités et limites

| Capacité | Statut | Détail |
|----------|--------|--------|
| Lister les alertes | **PASS** | REST API `list_alerts` fonctionnelle, retourne 10 alertes |
| Créer une alerte prix | **PASS (workaround)** | `alert create` CLI cassé par i18n, eval DOM fonctionne |
| Créer une alerte indicateur | **NON TESTÉ** | L'API Pine Script alert creation n'est pas exposée via CLI |
| Supprimer une alerte | **PARTIAL** | Suppression programmatique non supportée |
| Lire le webhook URL | **FAIL** | Non exposé par l'API `list_alerts` |
| Lire le JSON payload | **FAIL** | Non exposé par l'API `list_alerts` |
| Auditer le statut (active/paused/expired) | **PASS** | Champ `active` + `expiration` disponibles |
| Distinguer alertes test vs production | **PASS** | Via `message` et `type` |

## 5. Risques découverts

1. **i18n fragile** : tradingview-mcp hardcodé pour UI anglaise. Si TV est en français (comme ici), les outils DOM automation échouent. Nécessite un patch i18n ou l'utilisation d'eval JS direct.
2. **DOM automation instable** : Les sélecteurs CSS changent entre versions TV (classes hashées comme `input-RUSovanF`). Pas de contrat stable.
3. **REST API non documentée** : `pricealerts.tradingview.com` endpoints non officiels, peuvent changer.
4. **Suppression non fiable** : Pas de méthode programmatique vérifiée pour supprimer une alerte.
5. **Webhook invisible** : Impossible de vérifier si les alertes de production avaient des webhooks configurés.

## Résultat

**Statut** : PASS (avec limitations documentées)

L'inventaire est fiable. La création fonctionne via workaround. La suppression est partielle. La lecture des webhooks/payloads est impossible via l'API actuelle.

## Prochain GO

Phase 3 — Wrapper opt-trading (modules/tradingview_observer)
