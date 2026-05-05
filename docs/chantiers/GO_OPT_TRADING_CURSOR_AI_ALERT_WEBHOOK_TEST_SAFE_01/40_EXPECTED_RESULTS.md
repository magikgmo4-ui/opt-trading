---
doc_id: GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01_40_EXPECTED_RESULTS
doc_type: chantier/expected_results
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_TEST_SAFE_01/30_TEST_PROCEDURE.md
---

# 40_EXPECTED_RESULTS — Resultats attendus

## Niveau 1 — Validation JSON sans envoi

### Resultats attendus

```
PASS: schema=opt_trading_tradingview_alert_template_v1
PASS: trade_allowed=False
PASS: admin_trading_runtime=False
PASS: mode=test_only
PASS: signal=TEST_ONLY
PASS: placeholder {{ticker}} present
PASS: placeholder {{exchange}} present
PASS: placeholder {{interval}} present
PASS: placeholder {{close}} present
PASS: placeholder {{volume}} present
PASS: placeholder {{time}} present
Niveau 1 termine
```

### Signaux de test local

- Le test utilise `ConvertFrom-Json` en local, aucun appel reseau.
- Aucune connexion a un serveur distant.
- Le template est lu depuis le filesystem local.

## Niveau 2 — Test avec mock local

### Resultats attendus (terminal 1 — listener)

```
Mock listening on http://127.0.0.1:9999/tv-test/ — attente de requete...
Received payload: {"schema":"opt_trading_tradingview_alert_template_v1","mode":"test_only","signal":"TEST_ONLY","trade_allowed":false,...}
```

### Resultats attendus (terminal 2 — envoi)

```
PASS: mock responded: {"status":"ok","mode":"test_only"}
```

### Signaux de test local

- L'IP est `127.0.0.1` → boucle locale, aucun trafic reseau externe.
- Le port `9999` est arbitraire → pas de conflit avec des services standard.
- La reponse est `{"status":"ok","mode":"test_only"}` → mock local, pas un vrai serveur.

## Niveau 3 — Non-regression admin-trading

### Resultats attendus

```
(no output) → PASS : aucun fichier non-doc
(no output) → PASS : aucun secret
(no output) → PASS : aucun endpoint production
```

### Signaux que le runtime n'est pas touche

- `git diff --name-only` ne montre que `docs/` et `bundles/`.
- `webhook_server.py` n'est pas dans le diff.
- Aucun fichier systemd n'est dans le diff.
- `modules/admin-trading/` n'est pas reference.

## Logs attendus (format)

```
[TEST SAFE] $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") — Niveau 1 : PASS
[TEST SAFE] $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") — Niveau 2 : PASS
[TEST SAFE] $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") — Niveau 3 : PASS
[TEST SAFE] $(Get-Date -Format "yyyy-MM-dd HH:mm:ss") — VERDICT : ALL PASS
```

## Ce qui prouve qu'aucun admin-trading n'est touche

- L'URL de test est `127.0.0.1:9999`, pas une URL de production.
- Le mock repond `{"status":"ok","mode":"test_only"}` sans routage.
- `trade_allowed=false` est present dans le payload.
- `admin_trading_runtime=false` est present dans le payload.
- Aucun import de `webhook_server` ou `admin_trading` dans les commandes.
