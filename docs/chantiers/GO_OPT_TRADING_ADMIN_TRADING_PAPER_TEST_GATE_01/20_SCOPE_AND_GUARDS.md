# 20_SCOPE_AND_GUARDS

## Réponses aux questions de cadrage

1. **PAPER_TEST écrit-il seulement dans un ledger paper ?**
   - Oui, tout log d'exécution `PAPER_TEST` doit être écrit dans un ledger dédié `ledger_paper.json` et non dans `ledger_live.json`.

2. **PAPER_TEST peut-il appeler un service runner ?**
   - Oui, mais le service runner doit être configuré en mode `simulation` ou `sandbox`. Aucun appel API réel ne doit atteindre le broker.

3. **Quel service doit rester désactivé ?**
   - L'accès réel au compte broker.

4. **Quel flag bloque tout ordre réel ?**
   - `TRADE_ALLOWED=false` (systémique).
   - En mode `PAPER_TEST`, le flag `SIMULATION_MODE=true` est obligatoire.

5. **Comment prouver zéro ordre broker ?**
   - Vérification des logs de sortie du `runner` : aucune requête HTTP vers l'API du broker.
   - Surveillance des logs Telegram : réception de "PAPER_ORDER_SIMULATED".

6. **Quel payload PAPER_TEST est autorisé ?**
   - Uniquement les signaux venant de TradingView, traités via le flux validé, et routés vers le module de simulation.

7. **Différence stricte**
   - `TV_TEST`: Flux de données uniquement (pas de décision de trade).
   - `PAPER_TEST`: Flux de données + décision de trade + simulation d'ordre (pas d'ordre réel).
   - `LIVE`: Flux de données + décision de trade + exécution d'ordre réel.

## Guards obligatoires
- `if (config.mode !== 'PAPER' && config.mode !== 'SIMULATION') throw Error('UNAUTHORIZED_MODE');`
- `if (order.isReal()) throw Error('CRITICAL_SECURITY_VIOLATION');`

## RISKS

- À qualifier.
