---
doc_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_HYGIENE_AUDIT_01_RESULTS
doc_type: evidence
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_HYGIENE_AUDIT_01
parent_go_id: GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01
status: open
source_kind: canonical
updated_at: 2026-05-26
---

# 58 — Fleet hygiene audit (post db-layer recovery)

## Resume

Contexte :

- strict read-only 1–10 : `PASS_WITH_WARNINGS` (post recovery db-layer)
- objectif : clarifier ce qui reste en `WARN` (hygiene runtime-local + fleet stale/unreachable)

Verdict :

```text
HYGIENE_STATUS = WARNING_ACCEPTABLE_FOR_NEXT_TESTS
CLOSEOUT_STATUS = STILL_BLOCKED
```

## db-layer (read-only)

### Repo

```text
branch = sot/mainline...origin/sot/mainline
HEAD = 626b96ac
git diff = empty
```

Evidence :

```bash
ssh db-layer 'cd /opt/trading && git status --short --branch'
ssh db-layer 'cd /opt/trading && git log -1 --oneline --decorate'
ssh db-layer 'cd /opt/trading && git diff --name-only'
```

### Untracked (runtime-local)

```text
.claude/
artifacts/backtests/
secrets/
```

Evidence :

```bash
ssh db-layer 'cd /opt/trading && git ls-files --others --exclude-standard'
```

### Runtime

```text
18789 = LISTEN (127.0.0.1 + ::1)
tmux db-layer = OK (openclaw-core)
```

Evidence :

```bash
ssh db-layer 'ss -lnt 2>/dev/null | grep 18789 || true'
ssh db-layer 'tmux ls || true'
```

Verdict db-layer :

```text
PASS_WITH_WARNINGS
```

## admin-trading (read-only)

### Repo

```text
branch = sot/mainline...origin/sot/mainline
HEAD = 91ff36db
git diff = empty
```

Evidence :

```bash
ssh admin-trading 'cd /opt/trading && git status --short --branch'
ssh admin-trading 'cd /opt/trading && git log -1 --oneline --decorate'
ssh admin-trading 'cd /opt/trading && git diff --name-only'
```

### Untracked (runtime-local)

```text
secrets/
```

Evidence :

```bash
ssh admin-trading 'cd /opt/trading && git ls-files --others --exclude-standard'
```

### Runtime

```text
tmux admin-trading = OK
desk-pro = OK
screeners = OK
```

Evidence :

```bash
ssh admin-trading 'tmux ls || true'
ssh admin-trading 'tmux has-session -t desk-pro; echo rc=$?'
ssh admin-trading 'tmux has-session -t screeners; echo rc=$?'
```

Verdict admin-trading :

```text
PASS_WITH_WARNINGS
```

## fleet (read-only)

Etat rapporte (db-layer) :

```text
fleet_status = WARN
unreachable = [student]
stale = [cursor-ai, fantome]
```

Evidence :

```bash
ssh db-layer 'cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run'
```

Verdict fleet :

```text
WARN
```

## Decision

Contraintes maintenues :

- ne pas supprimer `secrets/`
- ne pas `git clean`
- ne pas `git restore`
- ne pas ecrire sur les machines distantes dans ce GO (read-only strict)

Decision :

- considerer les `untracked` runtime-local comme `WARN` acceptable pour continuer (mobile smoke / e2e)
- closeout propre impossible tant que ces `untracked` ne sont pas classes/masques/externalises, et tant que fleet reste en `WARN`

## Options futures (write-allowed, GO separe)

- Option A : accepter comme runtime-local `WARN` permanent (formaliser et documenter)
- Option B : quarantaine hors repo (ex: `/opt/runtime_artifacts/...`) pour `artifacts/backtests/` et lockfiles
- Option C : `.git/info/exclude` local-only pour masquer `artifacts/backtests/`, `.claude/`, `secrets/`

## Next

```text
NEXT = mobile smoke ou e2e dry-run suivant
PARENT_CLOSEOUT = toujours bloque
```
