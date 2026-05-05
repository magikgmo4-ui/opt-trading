# 30_TEST_PROCEDURE — Procedure de test safe

## Prerequis

- TradingView Desktop ouvert avec le symbole cible
- Flag `-AllowMutation` sur `cmd.ps1` (deverrouillage explicite)
- Aucun webhook pointe vers admin-trading ou une URL de production

## Test local safe

### Etape 1 — Lancer un receiver webhook local (optionnel)

```powershell
# Dans un terminal separe, lancer un receiver HTTP local
# Exemple avec netcat ou un script Python minimal
python -c "
from http.server import HTTPServer, BaseHTTPRequestHandler
import json

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length)
        print(json.dumps(json.loads(body), indent=2))
        self.send_response(200)
        self.end_headers()

HTTPServer(('localhost', 9999), Handler).serve_forever()
"
```

### Etape 2 — Verifier l'etat avant test

```powershell
cd C:\Users\ghost\opt-trading\modules\tradingview_observer
.\sanity_check.ps1
# Verifier alert_count avant test
```

### Etape 3 — Creer l'alerte test

```powershell
# Commande conceptuelle — necessite tradingview-mcp CLI avec alert create
# Le flag -AllowMutation est OBLIGATOIRE
.\cmd.ps1 -AllowMutation

# Puis via tradingview-mcp (hors wrapper, manuel) :
# node $env:USERPROFILE\.claude\tools\tradingview-mcp\src\cli\index.js alert create
#   --symbol BITGET:BTCUSDT.P
#   --condition "RSI > 70"
#   --webhook http://localhost:9999/test-webhook
#   --message "Test webhook RSI > 70"
```

### Etape 4 — Valider le payload recu

Verifier que le receiver local affiche le payload JSON correspondant au template.

### Etape 5 — Supprimer l'alerte test

```powershell
# Suppression via tradingview-mcp (si supportee)
# node ... alert delete --id <alert_id>
```

## Regles de securite

- **Jamais** de webhook pointe vers l'URL admin-trading (`https://.../webhook`)
- **Jamais** de webhook pointe vers Telegram (bot token)
- **Toujours** `localhost` ou une URL de test non critique
- **Toujours** supprimer l'alerte test apres validation
- **Toujours** `-AllowMutation` avant toute creation
