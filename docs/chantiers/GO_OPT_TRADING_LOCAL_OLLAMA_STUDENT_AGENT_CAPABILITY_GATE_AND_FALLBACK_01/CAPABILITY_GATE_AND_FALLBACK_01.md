# CAPABILITY_GATE_AND_FALLBACK_01

Définit les conditions d'usage du modèle `qwen2.5:0.5b-instruct` et les règles d'escalade.

## Principe

Le modèle 0.5B valide le pipeline agent mais n'est **pas fiable** pour :
- instructions exactes
- format structuré
- décisions sans supervision
- tâches multi-étapes complexes

Il est **fiable** pour :
- smoke test de connectivité agent
- diagnostic de session/gateway
- tâches read-only simples (réponse libre acceptable)

## Gate d'usage

| Condition | Utiliser 0.5B | Escalader |
|-----------|:-------------:|:---------:|
| Smoke test pipeline | ✅ OUI | — |
| Diagnostic session | ✅ OUI | — |
| Tâche read-only simple | ✅ OUI | — |
| Format de réponse exact exigé | ❌ NON | ✅ OUI |
| Tâche structurée (JSON, CSV) | ❌ NON | ✅ OUI |
| Décision sans supervision | ❌ NON | ✅ OUI |
| Multi-étapes (> 3 étapes) | ⚠️ Possible mais lent | ✅ Recommandé |
| Trading ou signal | ❌ INTERDIT | ❌ INTERDIT (hors scope) |

## Modèles de fallback disponibles

| Modèle | Taille | Agent chain | Usage |
|--------|:-----:|:-----------:|-------|
| `qwen2.5:0.5b-instruct` | 0.5B | ✅ PASS | Smoke, diagnostic, read-only simple |
| `qwen2.5:1.5b-instruct` | 1.5B | ✅ PASS (lent) | Backup non interactif (~131s) |
| `qwen2.5:3b-instruct` | 3B | ❌ timeout | Non viable CPU |
| `deepseek-r1:1.5b` | 1.5B | ❌ tool error | Incompatible agent chain |

## Procédure d'escalade

```bash
# 1. Tâche nécessitant format exact ou fiabilité ?
# → Ne pas utiliser 0.5B

# 2. Fallback local disponible ?
# → qwen2.5:1.5b-instruct (lent ~131s, non interactif)

# 3. Fallback distant configuré ?
# → Vérifier providers distants dans ~/.openclaw/openclaw.json

# 4. Aucun fallback viable ?
# → Refuser la tâche, documenter le gap
```

## Règles

1. Le 0.5B est un **probe de pipeline**, pas un **worker décisionnel**
2. Toute tâche à format strict → escalader ou refuser
3. Toute tâche de trading → **REFUSÉ** (hors scope de cette baseline)
4. L'absence de fallback viable n'est pas un bug mais une **limitation documentée**
5. Ne pas utiliser le 1.5B pour usage interactif (> 120s)
