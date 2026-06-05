# STRICT_WORKERS_OPERATIONAL_RUNBOOK_01

doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_OPERATIONAL_RUNBOOK_01_RUNBOOK
doc_type: runbook_operational
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_OPERATIONAL_RUNBOOK_01
status: canonical
lifecycle_stage: operational
topic_keys:
  - strict_workers
  - runbook
  - operational
  - read_inventory
  - draft_only
  - write_gated
  - A4
source_kind: canonical
updated_at: 2026-05-14
version: 1.0
---

## 1. OVERVIEW

`strict_workers` est un cadre pour une equipe de modeles IA specialises executant des micro-taches bornees,
dans un couloir ferme, sans secrets, avec validation externe obligatoire avant tout effet durable.

Architecture :

```text
Prompt standard → task index → runner securise → rapport DRAFT_ONLY → consolidation externe
```

## 2. QUICK REFERENCE

| Mode | Autonomie | Write? | Approval | Exemple |
|------|-----------|--------|----------|---------|
| A1 — READ_ONLY | Lire, inventorier | Non | Aucune | Lire des fichiers cibles, produire inventaire |
| A2 — DRAFT_ONLY | Proposer, brouillon | Non | Aucune | Proposer un patch theorique, doc draft |
| A4 — WRITE_GATED | Ecrire (borne) | Oui | HUMAIN obligatoire | Creer un fichier dans allowlist |

## 3. FICHIERS CLES

| Fichier | Role |
|---------|------|
| `scripts/ai/workers/tasks.index.json` | Catalogue des taches autorisees (8 types) |
| `scripts/ai/workers/models.registry.json` | Registre des modeles (24 entres, 15 VERIFIED) |
| `scripts/ai/workers/run_task.sh` | Runner shell principal |
| `scripts/ai/workers/_validate_job.py` | Validateur Python des job packets |
| `scripts/ai/workers/job_packets/` | Dossier des job packets JSON |
| `reports/ai/workers/` | Dossier de sortie des rapports |

## 4. TASK TYPES

### A1 — READ_ONLY

```text
READ_INVENTORY — Lire et inventorier des fichiers cibles (pas de write)
FAST_TRIAGE     — Classer rapidement des elements (priorite, risque)
ENDPOINT_AUDIT  — Revalider un endpoint modele
```

### A2 — DRAFT_ONLY

```text
PATCH_DRAFT           — Proposer un diff theorique (pas de write)
DOC_DRAFT             — Produire une documentation brouillon
TESTPLAN              — Lister tests et criteres PASS/FAIL
CHERRY_PICK_INVENTORY — Classer commits et dependances
```

### A4 — WRITE_GATED

```text
WRITE_GATED — Ecrire dans l'allowlist avec approval humaine explicite
```

## 5. JOB PACKET FORMAT

Un job packet JSON minimal :

```json
{
  "job_packet_id": "GO_EXAMPLE_01",
  "go_id": "GO_...",
  "task_type": "READ_INVENTORY",
  "worker_assigned": "qwen3.5-plus",
  "scope": {
    "allowed_inputs": ["fichiers/a/lire.md"],
    "allowed_outputs": ["reports/ai/workers/GO_EXAMPLE_01.md"]
  }
}
```

Pour WRITE_GATED, ajouter OBLIGATOIREMENT :

```json
{
  "explicit_write_approval": {
    "approved": true,
    "approver": "humain",
    "approval_date": "2026-05-14",
    "scope_files": ["reports/ai/workers/cible.md"],
    "max_lines_change": 50,
    "dry_run": true,
    "validation_required": ["git_diff", "strong_model_review", "human_approval"],
    "rollback_plan": "rm reports/ai/workers/cible.md"
  }
}
```

## 6. WORKER SELECTION

Choisir le worker selon le task type :

| Task type | Workers recommandes |
|-----------|---------------------|
| READ_INVENTORY | qwen3.5-plus, minimax-m2.5, kimi-k2.5, big-pickle |
| PATCH_DRAFT | glm-5.1, kimi-k2.6, glm-5, qwen3.6-plus |
| DOC_DRAFT | qwen3.5-plus, qwen3.6-plus, minimax-m2.5 |
| WRITE_GATED | glm-5.1, qwen3.6-plus, kimi-k2.6, big-pickle |

Tous les workers doivent etre VERIFIED ou VERIFIED_FREE dans `models.registry.json`.

## 7. GARDE-FOUS PERMANENTS

### Interdits absolus

```text
- .env, tokens, cles SSH/API
- secrets exchange
- strategies trading privees completes
- git add, git commit, git push, git rebase, git merge autonomes
- rm -rf, chmod -R, chown -R
- migration destructive
- write sur index globaux (GO_INDEX.md, BRANCH_STATE.md racine, MACHINE_WORK_SPLIT.md)
- write sur modules/ sans GO dedie
```

### Regles A4 (WRITE_GATED)

```text
R1: explicit_write_approval absent → REFUSE
R2: Fichier cible hors write_allowlist → REFUSE
R3: Fichier cible est un index global → REFUSE
R4: Input contient un motif de secret → REFUSE
R5: Commande demandee dans denied_commands → REFUSE
R6: Job packet invalide → REFUSE
R7: Modele non A4 capable → REFUSE
R8: dry_run est false → REFUSE
```

### Write allowlist (A4 uniquement)

```text
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/*.md
docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_**/BRANCH_STATE.md
reports/ai/workers/*.md
scripts/ai/workers/job_packets/*.json
```

## 8. PIPELINE A4 — WRITE REEL

```text
1. DRY-RUN     → Produire le diff simule, verifier allowlist, verifier limites
2. ARRET        → Stop. Demander approval humaine explicite.
3. APPROVAL     → Humain repond "APPROVED: execute write reel phase D"
4. WRITE        → Executer le write (CREATE_FILE ou MODIFY_FILE)
5. VERIFICATION → Verifier le fichier cree/modifie, git status
6. REPORT       → Produire le rapport d'execution avec preuves
7. ROLLBACK     → Si test : supprimer/annuler le write
8. CLEAN        → Git status propre
```

## 9. COMMANDES AUTORISEES

```text
# Lire des fichiers
cat, head, rg, grep, ls, find (read only)

# Ecrire via le runner
./run_task.sh <job_packet.json>

# Verifier l'etat
git status, git diff, git log, wc -l

# Operer dans un worktree dedie
git worktree add /tmp/opencode/<go-id> <branche>
```

## 10. COMMANDES INTERDITES

```text
git add
git commit
git push
git rebase
git merge
rm -rf
chmod -R
chown -R
```

Sauf pour la PR finale de closeout — alors git add/commit/push sont autorises explicitement.

## 11. VERIFICATION CHECKLIST

Avant tout merge :

```text
[x] git status --porcelain = propre (ou fichiers attendus uniquement)
[x] git diff --stat = perimetre conforme
[x] Aucun secret expose
[x] Aucun index global modifie
[x] Stash branch_arbitration preserve
[x] Tous les fichiers dans docs/chantiers/ ou scripts/ai/workers/ ou reports/ai/workers/
[x] Tous les preferred_workers sont VERIFIED
[x] Runner run_task.sh intact (0 diff)
```

## 12. WORKTREE PATTERN

Toujours operer dans un worktree dedie :

```bash
# Creer le worktree
git worktree add /tmp/opencode/<go-id> <branche>

# Travailler dedans
cd /tmp/opencode/<go-id>

# Nettoyer apres merge
git worktree remove /tmp/opencode/<go-id>
```

## 13. LIMITES CONNUES

```text
- Max 2 workers paralleles (teste)
- Timeout 120s par job
- Sorties ≤ 500 lignes par rapport
- A4 : max 50 lignes par write
- A4 : dry-run obligatoire avant write reel
- A4 : rollback obligatoire pour test
- Worktree dedie obligatoire (ne pas utiliser le worktree principal)
```

## 14. EXEMPLES

### Exemple 1 : Lancer un READ_INVENTORY

```bash
./run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

### Exemple 2 : Produire un PATCH_DRAFT

```bash
# Creer le job packet avec task_type: PATCH_DRAFT
# Executer
./run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_PATCH_DRAFT_IMPL_01.json
# Le patch est propose, pas applique
```

### Exemple 3 : Write reel A4

```bash
# 1. Dry-run
./run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_A4_WRITE_REEL_TEST.json
# → DRY_RUN ACCEPTE / EN ATTENTE APPROVAL

# 2. Arret et demande approval humaine

# 3. Apres approval : write reel
# (execute manuellement apres validation humaine)
echo "contenu" > reports/ai/workers/test.md

# 4. Verification
git status --porcelain

# 5. Rollback
rm reports/ai/workers/test.md

# 6. Clean
git status --porcelain  # doit etre propre
```

## 15. POOL MODELES COURANT

15 modeles VERIFIED/VERIFIED_FREE (2026-05-14) :

| Modele | Statut | Autonomie max |
|--------|--------|---------------|
| glm-5.1 | VERIFIED | A2 |
| glm-5 | VERIFIED | A2 |
| kimi-k2.5 | VERIFIED | A2 |
| kimi-k2.6 | VERIFIED | A2 |
| minimax-m2.7 | VERIFIED | A2 |
| minimax-m2.5 | VERIFIED | A2 |
| minimax-m2.5-free | VERIFIED_FREE | A1 |
| qwen3.6-plus | VERIFIED | A2 |
| qwen3.5-plus | VERIFIED | A2 |
| big-pickle | VERIFIED | A2 |
| nemotron-3-super-free | VERIFIED_FREE | A1 |
| gpt-5-nano | VERIFIED | A1 |
| deepseek-v4-flash-free | VERIFIED_FREE | A1 |
| ring-2.6-1t-free | VERIFIED_FREE | A1 |
| trinity-large-preview-free | VERIFIED_FREE | A1 |

## RISKS

- À qualifier.
