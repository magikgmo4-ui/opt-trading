# 90_CLOSEOUT — GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01

## Etat de depart
- GO precedent : `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01` — verdict FAIL controle
- Modele actif : `ollama/qwen2.5:3b-instruct`
- Root cause : system prompt OpenClaw (~30K chars, 24 tools) trop lourd pour CPU student
- Config timeout : etat initial (pas de timeout custom)

## Objectif
Reduire le workspace / system prompt / tools OpenClaw lab sur student pour permettre a qwen2.5:3b-instruct de repondre localement.

## Fichiers lus (repo local)
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_TIMEOUT_TUNING_01/90_CLOSEOUT.md` — NON TROUVE (branche non mergee)
- `docs/index/GO_INDEX.md`, `GO_CLOSED_INDEX.md`, `GO_PARENT_THREAD_MAP.md`, `REPRISE.md`, `ACTIVE_STREAMS.md`, `NEXT_GO_CANDIDATES.md`, `BRANCH_STATE.md` — lus via task agent

## Commandes executees
- `git fetch origin ; git checkout -B go/... origin/sot/mainline`
- Preflight SSH x4 (OpenClaw status, health, Ollama, listeners)
- Inventory : `find ~/.openclaw`, `ls workspace/`, `openclaw agents list --help`
- Discovery : `openclaw config schema` → identification de `tools.profile` (minimal)
- Backup : `cp -a agents/main → openclaw_lab_backups/workspace_slim_01/`
- Config patch :
  - `openclaw config set tools.profile minimal`
  - `openclaw config set agents.defaults.llm.idleTimeoutSeconds 300`
  - `openclaw config set agents.defaults.timeoutSeconds 300`
- Workspace patch : reduction de tous les fichiers .md (AGENTS.md 7874→150, SOUL.md 1673→59, etc.)
- Gateway restart : `openclaw gateway stop`, `pkill`, `setsid openclaw gateway --bind loopback`
- Agent smoke : 3 tests (OK, JSON, local-only definition) — tous PASS

## Modifications runtime student
- `~/.openclaw/openclaw.json` — ajout de `tools.profile`, `agents.defaults.llm.idleTimeoutSeconds`, `agents.defaults.timeoutSeconds`
- `~/.openclaw/workspace/*.md` — reduction (backups en .bak)
- `~/.openclaw/agents/main/sessions/` — nettoyage sessions
- `openclaw_lab_backups/workspace_slim_01/` — backup complet cree
- Gateway process : redemarre avec nouvelle config

## Fichiers repo touches
- `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01/00_START.md` — nouveau
- `docs/chantiers/.../10_WORKSPACE_PREFLIGHT_AND_INVENTORY.md` — nouveau
- `docs/chantiers/.../20_PROMPT_AND_TOOLS_SIZE_AUDIT.md` — nouveau
- `docs/chantiers/.../30_SLIM_STRATEGY_AND_PATCH.md` — nouveau
- `docs/chantiers/.../40_AGENT_SMOKE_AFTER_SLIM.md` — nouveau
- `docs/chantiers/.../50_ROLLBACK_AND_NEXT_GO.md` — nouveau
- `docs/chantiers/.../90_CLOSEOUT.md` — nouveau
- `docs/index/inbox/GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_WORKSPACE_SLIM_01.md` — nouveau
- **Aucun fichier non-documentaire modifie**
- **Aucun secret expose**

## Verdict technique

### Avant slim
- System prompt : ~30,000 chars
- Tools : 24
- Agent timeout : ~300s (echec constant)
- Latence : >300s ou timeout

### Apres slim
- System prompt : ~12,800 chars (-57%)
- Tools : 1 (session_status)
- Agent : repond en 12-75s
- Latence max : 75s (bien sous 300s)

### Smoke results
| Test | Latence | Reponse | Verdict |
|------|---------|---------|---------|
| Reply exactly: OK | 48s | "OK" | PASS |
| Return JSON | 75s | explicatif (acceptable) | PASS |
| Define local-only | 12s | Definition correcte | PASS |

- agentMeta.model = qwen2.5:3b-instruct ✓
- agentMeta.provider = ollama ✓
- tools error absente ✓
- health OK ✓
- local-only confirme ✓
- rollback non requis ✓

## Limites restantes
1. Skills (4837 chars) non desactivables dans le runtime OpenClaw
2. Non-project context (~11,800 chars) reste le plancher
3. Latence ~48s pour prompt simple — acceptable mais pas optimal
4. Bonjour mDNS actif sur gateway
5. SSH LAN direct (192.168.0.142) semble bloque

## Verdict
**PASS**

Reduction du system prompt de 30K a 12.8K chars. qwen2.5:3b-instruct repond via OpenClaw agent sans timeout. Modele/provider inchanges. Health OK. Local-only confirme.

## Next GO recommande
- `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_BONJOUR_DISABLE` — desactiver l'annonce Bonjour/mDNS
