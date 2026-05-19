# 10_WORKSPACE_PREFLIGHT_AND_INVENTORY

## Etat OpenClaw/Ollama (preflight)
- OpenClaw 2026.4.2 (d74a122)
- Modele actif : `ollama/qwen2.5:3b-instruct`
- Provider : `ollama`
- Health : `{"ok":true,"status":"live"}`
- Listeners : 127.0.0.1:18790, 127.0.0.1:18792, 127.0.0.1:11434 — tous loopback-only
- Ollama models : qwen2.5:3b, qwen2.5:1.5b, qwen2.5:0.5b, deepseek-r1:1.5b

## Fichiers agent/workspace trouves
- Agent principal : `~/.openclaw/agents/main/agent/`
  - `auth-profiles.json` (384 bytes)
  - `models.json` (1723 bytes)
- Workspace : `~/.openclaw/workspace/`
  - `AGENTS.md` (7874 chars) — comportement principal
  - `SOUL.md` (1673 chars) — personnalite
  - `TOOLS.md` (860 chars) — notes environnement
  - `BOOTSTRAP.md` (1471 chars) — setup initial
  - `IDENTITY.md` (636 chars) — metadonnees
  - `USER.md` (477 chars) — info utilisateur
  - `HEARTBEAT.md` (193 chars) — heartbeat
- Sessions : `~/.openclaw/agents/main/sessions/` (3 fichiers .jsonl)
- Config : `~/.openclaw/openclaw.json`

## Capacites decouvertes
- `openclaw agents add` — permet de creer un nouvel agent isole avec son propre workspace
- `openclaw config schema` — expose `tools.profile` (minimal/coding/messaging/full) et `tools.allow`/`tools.deny`
- `openclaw hooks list` — 4 hooks internes (boot-md, bootstrap-extra-files, command-logger, session-memory)

## Risques secrets
- `auth-profiles.json` contient une cle API ollama — non expose
- `openclaw.json` contient un token gateway — non expose
