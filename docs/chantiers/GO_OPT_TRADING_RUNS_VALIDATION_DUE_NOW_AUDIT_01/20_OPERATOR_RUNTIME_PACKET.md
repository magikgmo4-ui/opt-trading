---
doc_id: GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01_OPERATOR_RUNTIME_PACKET
doc_type: operator_packet
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01
status: active
source_kind: canonical
created_at: 2026-05-30
updated_at: 2026-05-30
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_RUNS_VALIDATION_DUE_NOW_AUDIT_01/20_OPERATOR_RUNTIME_PACKET.md
point_de_reprise: "Section 4 - Commandes"
---

# 20_OPERATOR_RUNTIME_PACKET

## 1. Objectif

Executer les deux validations `DUE_NOW` impossibles a prouver par le connecteur GitHub seul :

1. `PHASE_01_STRICT_WORKER_READONLY_SMOKE`
2. `PHASE_5_DBLAYER_TO_FANTOME_OPENCLAW_REMOTE_EXEC`

## 2. Contraintes globales

```text
NO_SECRET_READ
NO_ENV_READ
NO_PARENT_CLOSEOUT
NO_GLOBAL_INDEX_UPDATE
NO_GITHUB_ACTIONS_RERUN
NO_RUNTIME_TRADING
```

## 3. Precheck commun

```bash
git fetch origin

git switch sot/mainline

git pull --ff-only origin sot/mainline

git status --short --branch

git diff --check
```

Stop si :

- worktree sale ;
- conflit ;
- branche non alignee ;
- fichiers secrets visibles dans les diffs.

## 4. Commandes

### 4.1 Strict worker readonly smoke

But : produire une vraie sortie worker DRAFT_ONLY, pas seulement le prompt runner.

```bash
bash scripts/ai/workers/run_task.sh scripts/ai/workers/job_packets/GO_STRICT_WORKERS_READONLY_SMOKE_01.json
```

Puis lire le prompt genere :

```bash
sed -n '1,220p' reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01_PROMPT.txt
```

Executer ensuite le worker modele indique par le prompt selon le runner local autorise, en respectant strictement :

```text
allowed_inputs only
no repo modification
no git command from worker
no secrets
output = reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01.md
verdict final = ## VERDICT_DRAFT_ONLY
```

Verifier ensuite :

```bash
test -f reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01.md

grep -n "VERDICT_DRAFT_ONLY" reports/ai/workers/GO_STRICT_WORKERS_READONLY_SMOKE_01.md

git status --short --branch
```

Attendu :

```text
STRICT_WORKER_READONLY_SMOKE = PASS_DRAFT_ONLY_MODEL_EXECUTED
```

### 4.2 OpenClaw db-layer -> fantome applicative replay

But : verifier le chemin OpenClaw applicatif reel apres clearance non-runtime.

Precheck db-layer :

```bash
hostname && whoami && pwd

sudo -n -u openclaw openclaw gateway status

sudo -n -u openclaw openclaw gateway call health

sudo -n -u openclaw openclaw agents list
```

Verifier alias non-connectif :

```bash
ssh -G fantome | sed -n '1,80p'
```

Run applicatif borne a tenter seulement si les gates precedents passent :

```bash
sudo -n -u openclaw openclaw agent --agent orchestrateur --json --timeout 180 --message "On db-layer, execute exactly this shell command and nothing else: sudo -n -u ghost bash -lc 'ssh -o BatchMode=yes fantome \"cd /home/fantome/opt-trading && python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/orchestrator_chain_v2.json\"'. Return only the raw stdout/stderr lines needed to prove execution."
```

Attendu si success :

```text
CHAIN COMPLETE: all steps executed successfully.
VERDICT: DRAFT_ONLY - validation humaine requise.
```

Verifier ensuite cote fantome si accessible directement :

```bash
ssh -o BatchMode=yes fantome "cd /home/fantome/opt-trading && git status --short && ls -lt modules/ai_team_mvp/drafts | head"
```

Attendu :

```text
OPENCLAW_DBLAYER_FANTOME = PASS_APP_RUNTIME
```

Stop si :

- gateway unhealthy ;
- sandbox refuse SSH ;
- alias fantome change ;
- commande tente d'acceder a secrets ;
- output hors `modules/ai_team_mvp/drafts/` ;
- git write non prevu.

## 5. Evidence a reporter

Creer ensuite, dans le chantier approprie ou dans un nouveau child GO de verification :

```text
STRICT_WORKER_OUTPUT_PATH
OPENCLAW_RUNTIME_OUTPUT
GIT_STATUS_AFTER
VERDICT
NEXT_GAP
```

## 6. Statuts a mettre a jour seulement apres preuve

Si strict worker passe :

```text
PHASE_01_STRICT_WORKER_READONLY_SMOKE = PASS_DRAFT_ONLY_MODEL_EXECUTED
```

Si OpenClaw replay passe :

```text
PHASE_5_DBLAYER_TO_FANTOME_OPENCLAW_REMOTE_EXEC = PASS_APP_RUNTIME
```

Sinon conserver :

```text
STILL_DUE_NOW
```
