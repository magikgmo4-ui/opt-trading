# 06_TOOL_POLICY_DEPLOYMENT_RISK_MATRIX

## Objectif

Évaluer le risque de déployer la configuration repo OpenClaw V1.2.1 vers la configuration effective déployée Remote V2.

Ce document ne déploie rien.

## Source

- `01_SANDBOX_SCHEMA_SOURCE_AUDIT.md` à `05_TOOL_POLICY_RESOLUTION_RULE_AUDIT.md`

## Pivot canonique

```text
Le repo config n'est pas la config effective.
~/.openclaw/openclaw.json = Remote V2 (user ghost)
repo modules/openclaw_config_modulaire/app/*.json5 = Borne V1.2.1 (user openclaw — DIFFÉRENT)
```

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_CONFIG_DEPLOYMENT
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
READ_ONLY_MATRIX_ONLY
NO_SECRET_LOGGED
```

---

## Audit local — état établi

### Git precheck

```text
Branch: go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
HEAD: 7475c908
Status: propre
```

### Deployed config — `~/.openclaw/openclaw.json`

Dernière modification : `2026-03-14T18:37:09` (après réalignement runtime).

Contenu significatif :

```json
{
  "agents": {
    "defaults": { "model": { "primary": "openai/gpt-5.4" }, "maxConcurrent": 4 },
    "list": [
      { "id": "orchestrateur", "name": "Orchestrateur Remote V2",
        "workspace": "~/.openclaw/workspace-orchestrateur",
        "agentDir": "~/.openclaw/agents/orchestrateur/agent",
        "model": { "primary": "openrouter/qwen/qwen3-32b" } },
      { "id": "builder", "name": "Builder Remote V2",
        "workspace": "~/.openclaw/workspace-builder",
        "agentDir": "~/.openclaw/agents/builder/agent",
        "model": { "primary": "openrouter/qwen/qwen3-coder-30b-a3b-instruct" } },
      { "id": "reviewer", "name": "Reviewer Remote V2",
        "workspace": "~/.openclaw/workspace-reviewer",
        "agentDir": "~/.openclaw/agents/reviewer/agent",
        "model": { "primary": "openrouter/deepseek/deepseek-r1" } },
      { "id": "lab", "name": "Lab Remote V2",
        "workspace": "~/.openclaw/workspace-lab",
        "agentDir": "~/.openclaw/agents/lab/agent",
        "model": { "primary": "openrouter/qwen/qwen3-14b" } }
    ]
  },
  "tools": { "web": { "search": { "enabled": false }, "fetch": { "enabled": false } } },
  "gateway": { "mode": "local", "auth": { "mode": "token", "token": "[REDACTED]" } }
}
```

**Aucun `sandbox`, aucun `tools.deny`, aucun `tools.allow` per-agent.**

### Repo config — V1.2.1 (`modules/openclaw_config_modulaire/app/`)

Fichiers : `agents.json5`, `tools.json5`, `openclaw_root_template.json5`

Éléments significatifs :

```json5
// tools.json5
{ profile: "coding", deny: ["group:runtime", "browser", "canvas", "nodes", "cron", "gateway"] }

// agents.json5 defaults
{ sandbox: { mode: "all", workspaceAccess: "rw", scope: "agent" } }

// agents.json5 builder
{ name: "Builder Borne V1.2.1",
  agentDir: "/home/openclaw/.openclaw/agents/builder/agent",
  tools: { deny: ["group:runtime", "browser", "canvas", "nodes", "cron", "gateway"] } }
```

---

## Delta — V2 deployed vs V1.2.1 repo

| Dimension | Deployed V2 | Repo V1.2.1 | Risque si déploiement brut |
| :--- | :--- | :--- | :--- |
| **User path** | `~/.openclaw/` → `/home/ghost/` | `/home/openclaw/.openclaw/` | **CRITIQUE** — agentDir pointe vers un user inexistant |
| Agent names | "Remote V2" | "Borne V1.2.1" | cosmétique |
| Builder model | `openrouter/qwen/qwen3-coder` | `openai/gpt-5.4` | régression modèle |
| `tools.deny` global | absent | `group:runtime` + 5 autres | **ÉLEVÉ** — bloque runtime pour tous les agents |
| `sandbox` global | absent | `mode:"all"`, `scope:"agent"` | **ÉLEVÉ** — active containérisation Docker |
| Per-agent `allowAgents` | absent | présent (restrictions subagents) | moyen |
| `gateway.auth.token` | présent [REDACTED] | `__OPENCLAW_GATEWAY_TOKEN__` (placeholder) | **CRITIQUE** — écraserait le token réel si déployé brut |
| `tools.web` | `{search:false, fetch:false}` | absent | serait perdu |
| `compaction.mode` | `safeguard` | absent | serait perdu |
| `maxConcurrent` | 4 | absent (dans subagents) | serait perdu |

---

## Risques critiques identifiés

### Risque 1 — Path user mismatch (CRITIQUE)

```text
Repo V1.2.1 : agentDir = "/home/openclaw/.openclaw/agents/builder/agent"
Deployed V2 : agentDir = "~/.openclaw/agents/builder/agent" (résout /home/ghost/)
```

Déployer V1.2.1 brut casserait les agentDirs pour l'utilisateur `ghost`. Le répertoire `/home/openclaw/` n'existe pas sur cette machine pour ce processus.

### Risque 2 — Gateway token écrasement (CRITIQUE)

```text
openclaw.json deployed : gateway.auth.token = [REDACTED valeur réelle]
openclaw_root_template.json5 repo : gateway.auth.token = "__OPENCLAW_GATEWAY_TOKEN__"
```

Un déploiement brut du template écraserait le token d'authentification actif.

### Risque 3 — group:runtime deny global (ÉLEVÉ)

```text
tools.json5 : deny = ["group:runtime", ...]
```

Déployer `tools.json5` ajouterait un deny global non présent dans V2. Le builder (actuellement sans restriction runtime) serait bloqué.

### Risque 4 — sandbox mode:all (ÉLEVÉ)

```text
agents.json5 defaults : sandbox.mode = "all"
```

Activer le sandbox Docker pour tous les agents nécessite Docker disponible et des containers configurés. Non vérifié localement.

---

## Options de décision

| Option | Description | Verdict |
| :--- | :--- | :--- |
| A — Déployer toute V1.2.1 brut | écrase token, casse paths, ajoute deny global | **REJECTED** |
| B — Delta minimal : modèles + agents seulement | préserve token, no tool policy, no sandbox | **PREFERRED** |
| C — Garder V2 telle quelle | aucun risque mais runtime reste bloqué | **FALLBACK** |
| D — Patch repo V1.2.1 d'abord (paths, token, sandbox off) puis déployer | propre mais nécessite validation humaine | **CANDIDATE** |
| E — Démarrer gateway avec V2 actuelle | minimal, controllé, sandbox off confirmé | **CANDIDATE** |

---

## Décision provisoire

```text
DEPLOYMENT_NO_GO pour V1.2.1 brute — 3 risques critiques.
DEPLOYMENT_PARTIAL_CANDIDATE pour delta minimal (Option B ou E).
```

**La config effective V2 est plus propre pour un démarrage gateway :**

- aucun `group:runtime` deny ;
- aucun sandbox Docker requis ;
- token réel présent ;
- paths resolvent correctement pour user `ghost`.

---

## Gate avant tout déploiement

| Gate | Requis | Statut |
| :--- | :--- | :--- |
| Backup `openclaw.json` confirmé | REQUIRED | backups V2 présents (`.bak`, `.backup_before_runtime_realign`) |
| Path user mismatch résolu | REQUIRED | PENDING |
| Gateway token préservé | REQUIRED | PENDING |
| `group:runtime` deny non importé | REQUIRED | PENDING |
| Sandbox mode désactivé ou Docker vérifié | REQUIRED | PENDING |
| Rollback command documentée | REQUIRED | PENDING |

---

## NEXT_GO

```text
07_GATEWAY_ACTIVATION_PREFLIGHT.md
```

Rôle :

1. Évaluer si le gateway peut être démarré avec la config V2 actuelle sans déploiement V1.2.1 ;
2. Identifier les prérequis (token valide, port, mode local) ;
3. Définir le plan de démarrage minimal isolé ;
4. Statuer go/no-go sur l'activation gateway.

**Alternative si gateway non prioritaire :**

```text
07_REPO_CONFIG_V121_PATCH_PLAN.md
```

Corriger les 3 risques critiques dans le repo avant tout déploiement :
1. Remplacer `/home/openclaw/` → `~/.openclaw/` dans `agents.json5` ;
2. Retirer ou conditionner `group:runtime` deny ;
3. Documenter le token placeholder comme non-déployable brut.
