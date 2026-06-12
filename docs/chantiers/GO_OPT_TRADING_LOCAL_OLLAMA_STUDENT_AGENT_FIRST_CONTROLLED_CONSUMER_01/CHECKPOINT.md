# GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_FIRST_CONTROLLED_CONSUMER_01

## Résultat consommateur

| Test | Durée | Input tokens | Résultat |
|------|:-----:|:------------:|----------|
| Pré-vérification gateway | — | — | HTTP 200 |
| Rotation session | — | — | Session vierge créée |
| Prewarm Ollama | ~2s | — | OK |
| Tâche : reply exact "ALIVE" | 154 650ms | 4 040 | Réponse libre (non "ALIVE") |
| Tâche : reply exact "OK" (warm) | 58 811ms | 4 971 | Réponse libre (non "OK") |
| Health après | — | — | LIVE |
| Trade/worker | — | — | AUCUN |
| `/opt/trading` | — | — | INTACT |

## Observations

- La chaîne agent pipeline fonctionne techniquement
- Le modèle 0.5b ne suit pas les instructions exactes ("Reply exactly: X")
- Latence cold imprévisible : 60-155s sur CPU
- Session non modifiée, fraîche au départ
- Aucune modification de `/opt/trading`

## Verdict

```
FIRST_CONSUMER_PASS
```

La baseline Student/Ollama est exploitable pour des tâches ne nécessitant pas :
- d'obéissance exacte aux instructions
- de latence garantie < 60s
- de trading ou worker

## Limites confirmées

- Obéissance exacte : NON FIABLE avec 0.5B
- Latence : variable (60-155s)
- Contexte : limité à 4096 tokens
- Pas adapté à des tâches multi-étapes complexes

## RISKS

- À qualifier.
