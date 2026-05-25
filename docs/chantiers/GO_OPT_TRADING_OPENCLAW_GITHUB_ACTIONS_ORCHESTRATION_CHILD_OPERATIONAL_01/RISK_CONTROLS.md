---
doc_id: GO_OPT_TRADING_OPENCLAW_GITHUB_ACTIONS_ORCHESTRATION_CHILD_OPERATIONAL_01_RISK
doc_type: risk_controls
---

# Risk Controls — Orchestration Opérationnelle

## Matrice des risques

| Risque | Probabilité | Impact | Contrôle |
|---|---|---|---|
| Workflow mal configuré (YAML invalide) | Low | High | Gated PR checks valident le YAML avant merge |
| Token GitHub insuffisant | Medium | High | Vérifier les permissions du token avant trigger |
| Run bloquée indéfiniment (boucle) | Low | Medium | Timeout polling à 300s, timeout max |
| Orchestration déclenchée sur mauvais job | Low | High | Filtre `orchestrable_by_openclaw=true`, liste avant trigger |
| Run non trouvée après dispatch | Medium | Medium | Délai d'attente + retry |
| Changement breaking dans le registry | Low | Medium | Registry validé par un workflow GitHub Actions |
| Contournement de gated-pr | Low | High | Les runs déclenchées par workflow_dispatch ne bypassent pas les required checks — les PR les ont |

## Contrôles activés

1. **Gated PR obligatoire** : toute modification du bridge ou du script passe par PR avec required checks
2. **Registry validation** : le registry est validé par `github-actions-registry-check`
3. **Read-only d'abord** : phase initiale = read + trigger + poll sans mutation locale
4. **Pas d'auto-execution** : le script propose l'action suivante mais ne l'exécute pas
5. **Scope FILE_SCOPE** : seuls les chemins autorisés sont modifiés
6. **Token scope** : le GITHUB_TOKEN doit avoir `actions:write` pour dispatcher, `actions:read` pour poller

## Procédure d'arrêt d'urgence

```bash
# Si un trigger intempestif est détecté
# 1. Canceller le run
gh run cancel <RUN_ID>

# 2. Vérifier les permissions du token
# 3. Corriger le registry si nécessaire
# 4. Re-valider via PR gated
```
