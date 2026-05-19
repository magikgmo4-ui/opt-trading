# Closeout — GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01` |
| Branche | `go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_EXTERNAL_APPS_ORCHESTRATION_RUNNER_01` |
| Objet | Définir architecture + contrat du runner d'orchestration pour strict workers + apps externes |
| Livrables | 7 fichiers docs (architecture, runner contract, app bridges gates, execution sequence, security & stop) |
| Base | `sot/mainline` |

## Décision clé

**GitHub Actions = validation/smoke/sentinel. OpenClaw = orchestration. OpenCode = exécution. App bridges = accès contrôlé.**

La chaîne CI strict workers est validée (22/22 PASS). Le prochain niveau n'est pas plus de CI — c'est l'orchestration réelle par OpenClaw/OpenCode avec bridges app gated.

## Contraintes respectées

- `tasks.index.json` : non modifié
- `models.registry.json` : non modifié
- `_validate_job.py` : non modifié
- Workflows CI : non modifiés
- Aucun write réel, aucun secret exposé
- Aucun code d'exécution créé

## Verdict

```
PASS_EXTERNAL_APPS_ORCHESTRATION_RUNNER_SPEC_READY
```

## Prochain GO recommandé

```text
GO_OPT_TRADING_STRICT_WORKERS_CHILD_OPENCLAW_ADAPTER_IMPL_01
```

Implémenter l'adaptateur OpenClaw qui :
- Lit un job packet validé
- Applique le runner contract
- Délègue à OpenCode
- Vérifie le verdict
- Applique les gates par app bridge
- Gère les stop conditions
