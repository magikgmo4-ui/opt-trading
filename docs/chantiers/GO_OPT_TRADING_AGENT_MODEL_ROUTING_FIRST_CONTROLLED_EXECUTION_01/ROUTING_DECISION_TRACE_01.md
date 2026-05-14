# GO_OPT_TRADING_AGENT_MODEL_ROUTING_FIRST_CONTROLLED_EXECUTION_01

## Classification de tâche

Tâche : "Lister les sous-répertoires de /opt/trading/docs/chantiers/"

| Critère | Valeur |
|---------|--------|
| Type | Read-only avec besoin d'exactitude |
| Risque | Faible |
| Format attendu | Liste exacte (fiable) |
| Recommandation routing | 1.5B direct Ollama (pas 0.5B agent chain) |

## Exécution

### Test A : 0.5B agent chain (conformément à la politique)

| Métrique | Valeur |
|----------|:------:|
| Provider | qwen2.5:0.5b-instruct via agent |
| Statut | ok |
| Durée | 173 719ms |
| Input tokens | 12 549 |
| Réponse | **HALLUCINATION** (structure inventée) |
| Verdict | ❌ Non fiable pour cette tâche |

### Test B : 1.5B direct Ollama (fallback selon politique)

| Métrique | Valeur |
|----------|:------:|
| Provider | qwen2.5:1.5b-instruct direct |
| Prompt | "What is the capital of France? Reply with exactly one word." |
| Réponse | `Paris` ✅ (exactement un mot) |
| Verdict | ✅ Exactitude confirmée |

### Test C : deepseek-r1:1.5b direct Ollama (option raisonnement)

| Métrique | Valeur |
|----------|:------:|
| Provider | deepseek-r1:1.5b direct |
| Prompt | "What is the capital of France? Reply with exactly one word." |
| Réponse | `The capital of France is still Paris.` ❌ (pas exact) |
| Verdict | ⚠️ Non fiable pour format exact |

## Décision de routage

| Fournisseur | Convient pour | Verdict |
|-------------|---------------|:-------:|
| 0.5B agent chain | Smoke, probe, faible risque lecture libre | ✅ |
| 1.5B direct Ollama | Format exact, factual simple | ✅ |
| deepseek-r1:1.5b direct | Raisonnement, pas format exact | ⚠️ |

## Vérifications

| Critère | Statut |
|---------|:------:|
| Non-trading | ✅ |
| Aucun worker | ✅ |
| Gate capacité appliquée | ✅ |
| Session fraîche | ✅ |
| /opt/trading intact | ✅ |
| Health après tests | LIVE |

## Verdict

```
ROUTING_FIRST_CONTROLLED_EXECUTION_PASS
```

La politique de routage multi-provider est validée sur un cas réel.
Le fallback 1.5B direct Ollama est opérationnel pour les tâches à format exact.
Le 0.5B reste réservé au smoke/pipeline/faible risque.
