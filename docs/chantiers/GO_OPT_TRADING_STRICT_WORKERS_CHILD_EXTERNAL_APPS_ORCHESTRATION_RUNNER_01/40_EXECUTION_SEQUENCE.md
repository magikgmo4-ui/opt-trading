# Execution Sequence — Orchestration Runner

## Séquence complète

```
DÉCLENCHEUR
├── GitHub schedule cron (0 8 * * 1)
├── workflow_dispatch (manuel GitHub)
├── PR merge (webhook → notification)
└── humain (commande locale OpenCode)

       │
       ▼

OPENCLAW (orchestrateur)
├── 1. Lire le job packet depuis scripts/ai/workers/job_packets/
├── 2. Valide le mode : READ_ONLY / DRAFT_ONLY / WRITE_GATED
├── 3. Résout le worker modèle depuis tasks.index.json
├── 4. Vérifie que le modèle est VERIFIED dans models.registry.json
├── 5. Prépare le contexte d'exécution :
│   ├── job_packet_path
│   ├── trigger_source
│   ├── requested_app (si bridge)
│   ├── mode
│   ├── dry_run (défaut: true)
│   └── validation_token (si WRITE_GATED)
│
       ▼

OPENCODE (exécuteur)
├── 6. git checkout sot/mainline (propre)
├── 7. Lance run_task.sh <job_packet.json>
│   ├── VALIDATION PASS → continue
│   └── VALIDATION FAIL → BLOCKED, rapport FAILED
├── 8. Lit le prompt généré (PROMPT.txt)
├── 9. Appelle le modèle worker via endpoint zen
├── 10. Sauvegarde le rapport DRAFT_ONLY dans reports/ai/workers/
│
       ▼

APP BRIDGE (si mode > READ_ONLY et requested_app défini)
├── 11. Applique les gates de l'app cible
├── 12. Action READ_ONLY → exécute immédiatement
├── 13. Action DRAFT_ONLY → génère le diff sans write
├── 14. Action WRITE_GATED → attend validation externe
│
       ▼

VALIDATION EXTERNE (si WRITE_GATED)
├── 15. Humain ou modèle fort examine le diff proposé
├── 16. APPROVED → write réel (scope limité)
├── 17. REJECTED → close, rapport DRAFT_ONLY uniquement
│
       ▼

CLÔTURE
├── 18. Rapport final écrit dans reports/ai/workers/
├── 19. OpenClaw stocke le verdict (PASS / FAIL / BLOCKED)
├── 20. Si write réel : notification (Telegram, Airtable GO_Status)
└── 21. Aucun commit/push automatique
```

## Cas d'usage typiques

### A) Schedule hebdo — READ_INVENTORY sur Airtable
```
GitHub schedule → OpenClaw → OpenCode run_task.sh → worker lit Airtable
→ rapport DRAFT_ONLY dans reports/ai/workers/ → close
```

### B) Manual dispatch — PATCH_DRAFT sur ClickUp
```
workflow_dispatch → OpenClaw → OpenCode → worker lit ClickUp
→ propose statuts → rapport DRAFT_ONLY → humain valide
→ write ClickUp avec validation externe
```

### C) WRITE_GATED sur Airtable GO_Status
```
PR merge → notification → OpenClaw → OpenCode
→ WRITE_GATED dry-run → rapport + diff attendu
→ validation externe → write réel Airtable
```
