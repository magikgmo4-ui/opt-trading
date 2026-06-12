# Critères de refus — conditions de blocage du passage live

Un seul critère de refus suffit à bloquer le passage live.
Aucune exception n'est admise sans un GO séparé documentant le risque accepté.

---

## Refus automatique (hard block)

| Critère                                            | Raison                                      |
| -------------------------------------------------- | ------------------------------------------- |
| `fail_count > 0` sur les 30 derniers runs          | Pipeline instable                           |
| Kill switch non testé                              | Absence de garantie d'arrêt d'urgence       |
| Clés API Bitget dans le repo ou les logs           | Risque de compromission irréversible        |
| BitgetAdapter non implémenté ou non testé testnet  | Pas d'intégration live validée              |
| Telegram alerting non testé end-to-end             | Absence de monitoring en prod               |
| Operator gate stuck (timeout non configuré)        | Risque de blocage silencieux                |
| Plafond journalier non configuré                   | Risque de perte non bornée                  |
| Capital alloué non défini                          | Sizing non validé                           |
| `win_rate < 50%` sur les 30 derniers runs paper    | Signal peu fiable                           |
| `N runs paper < 30`                                | Observation insuffisante                    |
| `N jours < 14`                                     | Fenêtre temporelle trop courte              |
| TMUX session critique DOWN au moment du lancement  | Stack instable                              |
| LocalCMS unreachable au moment du lancement        | Monitoring absent                           |

---

## Refus conditionnel (nécessite GO dédié)

| Situation                                          | Condition de levée                          |
| -------------------------------------------------- | ------------------------------------------- |
| `win_rate ∈ [50%, 60%)` sur paper                  | GO dédié avec analyse signal + approbation  |
| Nouveau ticker non observé ≥ 14 jours en paper     | GO dédié d'observation ticker               |
| Risk engine modifié récemment (< 7 jours)          | GO dédié de validation risk                 |
| Validation gate modifiée récemment (< 7 jours)     | GO dédié de validation gate                 |
| Telegram alerting dégradé                          | GO fix alerting avant live                  |
| Bitget testnet OK mais prod non testée             | Considéré comme refus hard en pratique      |

---

## Conditions d'arrêt automatique en live (à implémenter)

Ces conditions doivent déclencher `TRADING_KILL_SWITCH=1` sans intervention humaine :

| Condition                                          | Action                                      |
| -------------------------------------------------- | ------------------------------------------- |
| Perte journalière > seuil configuré                | Halt immédiat + Telegram                    |
| N ordres/jour > plafond                            | Halt immédiat + Telegram                    |
| API Bitget timeout > 3 tentatives                  | Halt + alerte + log                         |
| Signal confidence < `GATE_MIN_CONFIDENCE`          | Bloc silencieux (déjà implémenté)           |
| TMUX session critique DOWN                         | Alerte Telegram (halt à valider)            |
| LocalCMS unreachable                               | Alerte Telegram (halt à valider)            |

---

## Principe directeur

```
EN CAS DE DOUTE = PAS DE LIVE

La prudence a un coût nul.
Un ordre live erroné a un coût réel et potentiellement irréversible.
```

Le passage live est une décision irrévocable dans sa fenêtre d'exécution.
Elle ne peut être annulée qu'avec un kill switch fonctionnel,
dont le test doit être confirmé avant toute activation.

## RISKS

- À qualifier.
