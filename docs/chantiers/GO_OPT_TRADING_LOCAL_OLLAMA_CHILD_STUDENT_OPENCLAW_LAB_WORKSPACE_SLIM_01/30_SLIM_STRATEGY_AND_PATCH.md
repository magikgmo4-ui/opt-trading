# 30_SLIM_STRATEGY_AND_PATCH

## Strategie retenue
**Strategie C** — Patch minimal sur l'agent main avec backup complet.

Justification : OpenClaw ne supporte pas de mecanisme de workspace slim separe natif (les skills et l'internal prompt sont partages). Creer un nouvel agent (`openclaw agents add`) ne reduirait pas les skills ni l'internal prompt. La strategie la plus efficace est de patcher directement :

1. Reduire les tools via `tools.profile = minimal`
2. Slimmer les fichiers workspace (AGENTS.md, SOUL.md, etc.)
3. Ajuster les timeouts pour accommoder le prompt restant (~12K chars)

## Backup
- Path : `/home/openclaw-lab/openclaw_lab_backups/workspace_slim_01/`
- Contenu :
  - `main.bak/` — copie complete de `~/.openclaw/agents/main`
  - `openclaw.json.bak` — copie de la config originale

## Patches effectues

### Config (`~/.openclaw/openclaw.json`)
1. `tools.profile` : non defini → `minimal`
2. `agents.defaults.llm.idleTimeoutSeconds` : non defini (60s default) → `300`
3. `agents.defaults.timeoutSeconds` : non defini (60s default) → `300`

### Workspace files (`~/.openclaw/workspace/`)

| Fichier | Avant | Apres | Backup |
|---------|-------|-------|--------|
| AGENTS.md | 7874 chars | 150 chars | .bak |
| SOUL.md | 1673 chars | 59 chars | .bak |
| BOOTSTRAP.md | 1471 chars | 36 chars | .bak |
| TOOLS.md | 860 chars | 44 chars | .bak |
| IDENTITY.md | 636 chars | 50 chars | .bak |
| USER.md | 477 chars | 37 chars | .bak |
| HEARTBEAT.md | 193 chars | 22 chars | .bak |
| **Total** | **~13,184** | **398** | |

### Contenu AGENTS.md final
```
You are a local lab assistant. Answer briefly and concisely.
Do not use unnecessary tools.
You can read, write, edit files and execute safe commands.
```

### Contenu SOUL.md final
```
Be concise. Answer briefly. You are a local lab assistant.
```

## Resultat
- System prompt : 30K → 12.8K chars (-57%)
- Tools : 24 → 1 (session_status)
- Prompt tokens : ~3,300 (au lieu de ~8,000+)

## Limites
- Les 9 skills (4837 chars) ne sont pas desactivables — ils font partie du runtime OpenClaw
- Le non-project context (~11,800 chars) reste eleve car il inclut l'internal prompt + skills
- Le workspace ne peut pas etre reduit en dessous de ~400 chars sans risquer de casser le fonctionnement

## RISKS

- À qualifier.
