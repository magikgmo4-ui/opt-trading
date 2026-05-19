# Architecture Decision — Orchestration Runner

## Constat

GitHub Actions est un validateur/sentinelle, pas un exécuteur d'IA ou d'apps externes :
- Pas de modèle de langage disponible
- Pas d'accès aux credentials des bridges (airtable_bridge, ClickUp API, etc.)
- Pas de session interactive pour validation humaine
- Timeout limité (10 min), pas de persistance de run

## Séparation des responsabilités

```
GitHub Actions
├── validate.yml      → valide la structure des job packets (22/22)
├── smoke.yml         → dry-run run_task.sh, vérifie 0 fichier modifié
├── schedule.yml      → déclenche un signal programmé (cron hebdo)
└── (signal)          → ne fait PAS l'orchestration

OpenClaw (couche orchestration)
├── reçoit le signal (manuel ou programmé)
├── sélectionne le job packet depuis le repo
├── applique les gates (read-only / draft / write_gated)
├── délègue à OpenCode l'exécution
└── collecte le verdict

OpenCode (environnement opératoire)
├── exécute le job packet validé
├── dispose de l'accès modèle (via endpoint zen)
├── dispose des credentials bridge (via environnement local)
├── produit le rapport DRAFT_ONLY
└── ne commit/push jamais automatiquement

App bridges (couche accès externe)
├── airtable_bridge/
├── execute_clickup.py (cockpit ClickUp)
├── Botpress → OpenClaw Gateway
├── Telegram (notification only)
└── Google Sheets (journal/reporting only)
```

## Flux complet

1. Déclencheur : GitHub (schedule cron / workflow_dispatch / PR merge) ou humain
2. OpenClaw lit le job packet depuis `scripts/ai/workers/job_packets/`
3. OpenClaw valide le mode (READ_ONLY / DRAFT_ONLY / WRITE_GATED)
4. OpenClaw sélectionne le worker modèle depuis `tasks.index.json`
5. OpenCode exécute `run_task.sh <packet>` avec les credentials bridge
6. OpenCode génère le rapport DRAFT_ONLY dans `reports/ai/workers/`
7. OpenClaw vérifie le verdict
8. Si WRITE_GATED : validation externe (humain ou modèle fort) avant write
9. Rapport final stocké dans le repo

## Principe

**GitHub Actions ne fait pas l'orchestration réelle.**
**Le repo reste la source canonique de vérité.**
