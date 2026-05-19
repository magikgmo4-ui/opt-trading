# CROSS_SURFACE_COMPLIANCE_AUDIT_01

Audit d'application du standard opératoire de routage modèle/provider sur les surfaces actives.

## Surfaces auditées

| Surface | Provider agent | Documentation routage | Gate capacité | Trace décision | Statut |
|---------|:--------------:|:---------------------:|:-------------:|:--------------:|:------:|
| Student/Ollama local | qwen2.5:0.5b-instruct | ✅ | ✅ | ✅ | ✅ COMPLIANT |
| Student/Cursor AI | N/A (hors scope) | ⏳ | ⏳ | ⏳ | NO_AGENT |
| Admin/Trading Desk Pro | N/A (hors scope) | ⏳ | ⏳ | ⏳ | NO_AGENT |
| DB Layer | N/A (hors scope) | ⏳ | ⏳ | ⏳ | NO_AGENT |

## Critères de conformité

| Critère | Description | Student/Ollama |
|---------|-------------|:--------------:|
| A1 | Un provider agent est documenté | ✅ |
| A2 | Le routage modèle/provider est défini | ✅ |
| A3 | La gate capacité/fallback est active | ✅ |
| A4 | Les traces de décision sont produites | ✅ |
| A5 | Aucun usage abusif du 0.5B | ✅ |
| A6 | Session fraîche obligatoire | ✅ |
| A7 | Rotation après 10 runs | ✅ |
| A8 | Aucun trade/worker non autorisé | ✅ |

## Résultat

- Student/Ollama : **COMPLIANT** (tous les critères ✅)
- Autres surfaces : **NO_AGENT** (pas d'agent OpenClaw configuré)

## Recommandations

1. Student/Ollama peut servir de référence pour auditer toute nouvelle surface agent
2. Les surfaces sans agent n'ont pas besoin d'appliquer le standard
3. Toute surface qui ajoute un agent OpenClaw à l'avenir doit passer ce même audit
4. Le template de précheck est disponible dans le standard opératoire
