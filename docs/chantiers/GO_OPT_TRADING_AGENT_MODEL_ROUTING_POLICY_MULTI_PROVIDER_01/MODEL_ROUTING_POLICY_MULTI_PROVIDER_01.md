# MODEL_ROUTING_POLICY_MULTI_PROVIDER_01

Politique canonique de routage modèle/provider pour les tâches agent.

## Fournisseurs disponibles

| Provider | Type | Modèle | Pipeline agent | Usage |
|----------|------|--------|:--------------:|-------|
| Ollama local | CPU | qwen2.5:0.5b-instruct | ✅ PASS | Smoke, probe, read-only simple |
| Ollama local | CPU | qwen2.5:1.5b-instruct | ✅ PASS (131s) | Backup non interactif |
| — | — | Autres modèles locaux | ❌ | Voir gate capacité/fallback |

## Arbre de décision

```text
Tâche reçue
├─ Trading ou worker continu ?
│   └── REFUS (hors scope cette politique)
│
├─ Format exact / obéissance stricte requis ?
│   ├─ OUI → Provider distant nécessaire (non configuré actuellement)
│   │         ou → Direct Ollama 1.5B avec prompt contrôlé (pas agent chain)
│   │         ou → REFUS si pas de fallback viable
│   └─ NON → Peut utiliser agent chain 0.5B ?
│       ├─ OUI, tâche simple, read-only, risque faible
│       │   └── qwen2.5:0.5b-instruct via agent chain
│       └─ NON, trop complexe ou trop long
│           └── qwen2.5:1.5b-instruct direct Ollama (pas agent chain)
│               ou → REFUS
│
└─ Session fraîche ?
    ├─ OUI → Procéder
    └─ NON → Rotation obligatoire avant
```

## Niveaux de risque

| Niveau | Usage modèle | Exemples |
|--------|--------------|----------|
| Faible | 0.5B agent chain | Smoke pipeline, diagnostic session, read-only non structuré |
| Moyen | 1.5B direct Ollama | Résumé court, classification simple, format libre |
| Élevé | Provider distant (N/A) | Format strict, décision, trading |
| Bloqué | REFUS | Trading, worker, critique, pas de fallback |

## Règles

1. **Par défaut** : 0.5B agent chain pour toute tâche à risque faible
2. **Si format exact** : 1.5B direct Ollama ou REFUS
3. **Si tâche critique** : REFUS tant qu'aucun provider distant n'est configuré
4. **Session toujours fraîche** : rotation si > 5 runs sur la session active
5. **Pas de fallback = refus propre**, pas de dégradation silencieuse

## RISKS

- À qualifier.
