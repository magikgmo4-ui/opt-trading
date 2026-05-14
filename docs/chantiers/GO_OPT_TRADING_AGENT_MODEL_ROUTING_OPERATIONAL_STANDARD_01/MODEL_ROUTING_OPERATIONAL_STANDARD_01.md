# MODEL_ROUTING_OPERATIONAL_STANDARD_01

Standard opératoire obligatoire pour tout usage agent OpenClaw sur ce runtime.

## 1. Prérequis avant toute exécution agent

- [ ] Gateway live (`curl http://127.0.0.1:18790/health` → 200)
- [ ] Session fraîche ou rotée après diagnostic
- [ ] Tâche classée selon la matrice de routage
- [ ] Provider choisi selon la politique multi-provider
- [ ] Aucun trade/worker en cours
- [ ] Décision de routage journalisée

## 2. Classification obligatoire de la tâche

Toute tâche soumise à l'agent doit être classée :

| Critère | Options |
|---------|---------|
| Type | smoke / diagnostic / read-only / format-exact / raisonnement / trading |
| Risque | faible / moyen / élevé / bloqué |
| Format attendu | libre / exact / structuré |
| Tolérance latence | oui / non |

## 3. Règle de routage

| Classification | Provider | Pipeline |
|---------------|----------|:--------:|
| Smoke / diagnostic | 0.5B agent chain | ✅ |
| Read-only, format libre | 0.5B agent chain | ✅ |
| Format exact | 1.5B direct Ollama | ❌ |
| Raisonnement | deepseek-r1:1.5b direct | ❌ |
| Critique / trading | REFUS | ❌ |
| Worker continu | REFUS | ❌ |

## 4. Journalisation minimale

Chaque exécution agent doit produire :

```
Tâche: <description>
Type: <smoke|diagnostic|read-only|...>
Provider: <modèle>
Pipeline: <agent chain|direct|refus>
Durée: <ms>
Session: <id>
Verdict: <PASS|FAIL|REFUS>
```

## 5. Fallback obligatoire

Si le modèle choisi échoue :

1. **0.5B échoue** → 1.5B direct Ollama
2. **1.5B échoue** → deepseek-r1:1.5b direct
3. **deepseek échoue** → REFUS documenté

Pas de dégradation silencieuse.

## 6. Interdictions

- Le 0.5B ne doit jamais être utilisé pour une tâche à format exact ou décisionnelle
- Aucun provider local ne doit être utilisé pour du trading ou worker continu
- Toute exécution sans classification préalable est interdite
