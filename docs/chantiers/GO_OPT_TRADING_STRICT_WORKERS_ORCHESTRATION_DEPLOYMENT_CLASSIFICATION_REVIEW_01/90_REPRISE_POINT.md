# GO_OPT_TRADING_STRICT_WORKERS_ORCHESTRATION_DEPLOYMENT_CLASSIFICATION_REVIEW_01 — 90_REPRISE_POINT

## Point de reprise

Le bucket 1 de PR #645 est maintenant ouvert en GO separe, doc-first et read-only.

Etat canonique de depart:

- `sot/mainline` propre
- PR #617 mergee: registry + template master targets
- PR #619 mergee: validator `master_target_id` warning-only
- PR #645 mergee: matrice de classification AI / Strict Workers / Apps

Travail realise dans ce GO:

- bornage du scope workflows + `systemd` + `machine_runtime_map`
- exclusion explicite de `strict-workers-schedule.yml` vers le bucket 2
- inventaire des surfaces `modules/*/systemd/*` comme adjacences de deploiement

Prochain geste si validation humaine:

1. decider si le bucket 1 reste un simple review GO ou ouvre ensuite un GO d'implementation repo-only
2. si implementation, separer strictement:
   - adaptations workflows/deploy
   - adaptations `machine_runtime_map`
3. conserver hors scope toute surface strategy, airtable, OpenClaw policy, OpenClaw DBLayer, Botpress et Ollama
