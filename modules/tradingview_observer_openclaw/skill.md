# tradingview_observer

## ROLE
Permettre a OpenClaw de lire l'etat TradingView Desktop via le wrapper opt-trading read-only.
Ce skill est un orchestrateur de lecture seule. Il ne modifie jamais TradingView, les alertes, ou admin-trading.

## ENTRYPOINT
```
C:\Users\ghost\opt-trading\modules\tradingview_observer_openclaw\run.ps1
```

## ALLOWED_COMMANDS

Toutes les commandes ci-dessous sont read-only et sans effet sur TradingView :

```
.\run.ps1 sanity
```

Verifie :
- Node.js present
- tradingview-mcp CLI accessible
- Port CDP 9222 repond
- tv status (cdp_connected)
- tv state (symbol, TF, studies)
- tv quote (OHLC)
- tv alert list (alert count)
- tv values (indicator values)

```
.\run.ps1 snapshot
```

Execute sanity puis exporte les resultats JSON dans :
```
modules/tradingview_observer/output/
  latest_status.json
  latest_quote.json
  latest_state.json
  latest_alert_inventory.json
  latest_values.json
  latest_report.json
```

## READ_OUTPUTS

Apres snapshot, OpenClaw peut lire directement :

- `..\tradingview_observer\output\latest_report.json` — rapport combine
- `..\tradingview_observer\output\latest_status.json` — sante CDP + chart
- `..\tradingview_observer\output\latest_quote.json` — OHLC courant
- `..\tradingview_observer\output\latest_state.json` — etat graphique
- `..\tradingview_observer\output\latest_alert_inventory.json` — inventaire alertes
- `..\tradingview_observer\output\latest_values.json` — valeurs indicateurs

## FORBIDDEN

OpenClaw ne doit JAMAIS :

- Acceder directement au port 9222 (CDP)
- Appeler tradingview-mcp directement (node ...\src\cli\index.js)
- Creer une alerte (alert_create)
- Supprimer une alerte (alert_delete)
- Modifier une alerte existante
- Configurer un webhook
- Executer un trade
- Modifier admin-trading
- Lancer tv launch (demander a l'operateur humain si TradingView est ferme)
- Contourner le module `tradingview_observer`

## OPERATION_FLOW

1. Lancer `.\run.ps1 sanity`
2. Si sanity FAIL, informer l'operateur de la cause exacte et STOPPER
3. Si sanity PASS, lancer `.\run.ps1 snapshot`
4. Lire `..\tradingview_observer\output\latest_report.json`
5. Produire une synthese :
   - Symbole et timeframe courant
   - Dernier prix (OHLC)
   - Nombre d'etudes visibles
   - Valeurs des indicateurs si disponibles
   - Nombre d'alertes (actives / expirees / total)
   - Limites connues (webhook invisible, suppression non supportee)
6. Retourner l'analyse en read-only
7. NE JAMAIS proposer de mutation sans GO explicite

## FAILURE_MODES

| Erreur | Cause probable | Action OpenClaw |
|--------|---------------|-----------------|
| CDP port closed | TradingView Desktop ferme | Demander a l'operateur de lancer TradingView |
| tradingview-mcp CLI missing | Installation incomplete | Signaler le chemin manquant |
| JSON parse error | Donnees corrompues | Relire le fichier, signaler l'erreur |
| report missing | Snapshot non execute | Lancer snapshot d'abord |

## SAFE_RESPONSE

En cas d'echec, retourner `PARTIAL` avec l'erreur exacte. Ne jamais tenter de reparer en modifiant TradingView, les alertes, ou admin-trading.
