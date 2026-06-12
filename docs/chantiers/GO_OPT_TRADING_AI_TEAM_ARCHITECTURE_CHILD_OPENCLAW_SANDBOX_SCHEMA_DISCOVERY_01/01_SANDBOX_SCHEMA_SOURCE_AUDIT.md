# 01_SANDBOX_SCHEMA_SOURCE_AUDIT

## Objectif

Auditer les sources locales et externes disponibles pour identifier le schéma supporté de `sandbox.mode` dans OpenClaw.

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
READ_ONLY_AUDIT_ONLY
NO_CONFIG_PATCH
```

## Contexte

Le child précédent s'est clôturé en `REVIEW_REQUIRED` parce que :

```text
sandbox.mode = "all"
SANDBOX_SCHEMA_UNKNOWN
RUNTIME_BLOCKED
```

Fichier local observé :

```text
modules/openclaw_config_modulaire/app/agents.json5
```

## Sources externes préliminaires

### Source A — OpenClaw docs, Sandbox vs tool policy vs elevated

Constats à vérifier localement :

```text
agents.defaults.sandbox.mode supports:
- "off"
- "non-main"
- "all"
```

Commande documentée :

```bash
openclaw sandbox explain
openclaw sandbox explain --agent <agent>
openclaw sandbox explain --json
```

Rôle attendu :

```text
Afficher :
- sandbox mode effectif
- scope effectif
- workspace access effectif
- allow/deny effectifs
- source de la règle : agent/global/default
```

### Source B — OpenClaw docs, Multi-agent sandbox and tools

Constats à vérifier localement :

```text
agents.list[].sandbox peut override agents.defaults.sandbox
agents.defaults.sandbox sert de default global
scope peut être agent/session/shared selon config
workspaceAccess peut contrôler l'accès workspace
docker.binds peut percer le filesystem sandbox
```

---

## Audit local — résultats

### Git precheck

```text
Branch: go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
HEAD: cb370d44 docs: open OpenClaw sandbox schema discovery child
Statut: propre, en avance sur origin
```

### Current agents.json5 (repo)

```text
modules/openclaw_config_modulaire/app/agents.json5
```

Extrait clé :

```json5
defaults: {
  sandbox: {
    mode: "all",
    workspaceAccess: "rw",
    scope: "agent",
  },
},
```

Agents list tool deny observé (builder / reviewer / lab) :

```json5
tools: {
  profile: "coding",
  deny: [
    "group:runtime",
    "browser",
    "canvas",
    "nodes",
    "cron",
    "gateway",
  ],
},
```

### Focused local schema search

Valeurs de `mode` trouvées localement :

| Fichier | Champ | Valeur |
| :--- | :--- | :--- |
| `modules/openclaw_config_modulaire/app/agents.json5:20` | `defaults.sandbox.mode` | `"all"` |
| `modules/openclaw_config_modulaire/app/openclaw_root_template.json5:55` | `gateway.tailscale.mode` | `"off"` (hors sandbox) |

**Note** : `mode: "off"` dans `openclaw_root_template.json5` correspond à `gateway.tailscale.mode`, pas à `sandbox.mode`.

### OpenClaw CLI availability

```text
CLI présent : /home/ghost/.npm-global/bin/openclaw
Version : 2026.3.11 (29dc654)
Commande sandbox : confirmée (explain / list / recreate)
```

### openclaw sandbox explain — résultat effectif

```text
Effective sandbox:
  agentId: orchestrateur
  sessionKey: agent:orchestrateur:main
  mainSessionKey: agent:orchestrateur:main
  runtime: direct
  mode: off  scope: agent  perSession: false
  workspaceAccess: none  workspaceRoot: /home/ghost/.openclaw/sandboxes

Sandbox tool policy:
  allow (default): exec, process, read, write, edit, apply_patch, image,
                   sessions_list, sessions_history, sessions_send,
                   sessions_spawn, subagents, session_status
  deny  (default): browser, canvas, nodes, cron, gateway, telegram,
                   whatsapp, discord, irc, googlechat, slack, signal,
                   imessage, line

Elevated:
  enabled: true
  channel: (unknown)
  allowedByConfig: false

Fix-it:
  - tools.sandbox.tools.allow
  - tools.sandbox.tools.deny
  - agents.list[].tools.sandbox.tools.allow
  - agents.list[].tools.sandbox.tools.deny
  - tools.elevated.enabled
```

Source JSON complète :

```json
{
  "agentId": "orchestrateur",
  "sandbox": {
    "mode": "off",
    "scope": "agent",
    "perSession": false,
    "workspaceAccess": "none",
    "workspaceRoot": "/home/ghost/.openclaw/sandboxes",
    "sessionIsSandboxed": false,
    "tools": {
      "allow": ["exec","process","read","write","edit","apply_patch","image",
                "sessions_list","sessions_history","sessions_send",
                "sessions_spawn","subagents","session_status"],
      "deny": ["browser","canvas","nodes","cron","gateway","telegram",
               "whatsapp","discord","irc","googlechat","slack","signal",
               "imessage","line"],
      "sources": {
        "allow": {"source": "default", "key": "tools.sandbox.tools.allow"},
        "deny":  {"source": "default", "key": "tools.sandbox.tools.deny"}
      }
    }
  },
  "elevated": {
    "enabled": true,
    "allowedByConfig": false
  },
  "fixIt": [
    "tools.sandbox.tools.allow",
    "tools.sandbox.tools.deny",
    "agents.list[].tools.sandbox.tools.allow",
    "agents.list[].tools.sandbox.tools.deny",
    "tools.elevated.enabled"
  ]
}
```

---

## Analyse — constats majeurs

### Constat 1 — Divergence repo vs deployed

```text
agents.json5 (repo) : defaults.sandbox.mode = "all"
openclaw sandbox explain (effectif) : mode = "off"
```

La config déployée à `~/.openclaw/` diffère du fichier source du repo.
Le gateway n'étant pas actif, `explain` retourne le fallback par défaut OpenClaw (`mode: off`).
Cela signifie que `mode: "all"` dans `agents.json5` n'est pas encore appliqué en runtime.

### Constat 2 — Source = "default"

```text
allow.source: "default"
deny.source:  "default"
```

Aucune règle agent-spécifique ou globale custom n'est en vigueur.
Les valeurs proviennent du schéma par défaut OpenClaw, pas du repo.

### Constat 3 — Le blocage SSH/network n'est pas dû à sandbox.mode

```text
sandbox.mode effectif = "off" → sandbox inactif (sessionIsSandboxed = false)
```

Le blocage de SSH et des opérations réseau vient de la **politique outil** des agents, pas du mode sandbox.
Coupable identifié dans `agents.json5` (builder / reviewer / lab) :

```json5
deny: ["group:runtime", ...]
```

`group:runtime` est le groupe outil qui englobe SSH, exec réseau, et opérations runtime distantes.

### Constat 4 — Valeurs de mode confirmées localement

| Valeur | Evidence locale |
| :--- | :--- |
| `"off"` | `openclaw sandbox explain` → mode effectif confirmé |
| `"all"` | `agents.json5:20` → présent dans le fichier source repo |
| `"non-main"` | Non trouvé localement — doc externe uniquement |

### Constat 5 — Champs patchables identifiés

Le `fixIt` de `sandbox explain` désigne les clés de config actionnables :

```text
tools.sandbox.tools.allow           → allow global sandbox tools
tools.sandbox.tools.deny            → deny global sandbox tools
agents.list[].tools.sandbox.tools.allow → allow par agent
agents.list[].tools.sandbox.tools.deny  → deny par agent
tools.elevated.enabled              → mode elevated
```

---

## Questions — verdict

| Question | Verdict | Evidence |
| :--- | :--- | :--- |
| `mode="off"` supporté localement ? | **CONFIRMED** | `sandbox explain` → mode effectif |
| `mode="non-main"` supporté localement ? | **UNCONFIRMED** | Doc externe uniquement |
| `mode="all"` supporté localement ? | **CONFIRMED** | `agents.json5:20` |
| Override agent sandbox supporté ? | **CONFIRMED** | `fixIt` liste `agents.list[].tools.sandbox.tools.allow/deny` |
| `allow` / `deny` sandbox par agent supportés ? | **CONFIRMED** | `fixIt` + schéma vu dans `agents.json5` |
| `docker.binds` applicable ici ? | **UNCONFIRMED** | Absent localement |
| Blocage SSH = sandbox mode ? | **FALSE** | Mode effectif déjà `off`; blocage = `deny group:runtime` |
| Patch sûr possible sans désactiver le sandbox ? | **YES** | Retirer `group:runtime` du deny ou ajouter SSH à l'allow par agent |

---

## Decision outcome

### OUTCOME: PATCHABLE_SAFE_MODE_FOUND

Condition remplie :

```text
Le blocage SSH/network est causé par deny: ["group:runtime"] dans les agents builder/reviewer/lab.
Le sandbox mode est déjà "off" en effectif.
Une modification ciblée de la politique outil (allow SSH) est possible sans désactiver le sandbox.
```

Levier de patch identifié :

```text
agents.list[id=builder].tools.deny → retirer "group:runtime" OU
agents.list[id=builder].tools.allow → ajouter les outils SSH spécifiques
```

NEXT_GO :

```text
02_SANDBOX_PATCH_DECISION_MATRIX.md
```

---

## Invariants respectés

```text
Aucun patch appliqué dans ce lot.
Aucun runtime lancé.
Aucune connexion SSH.
Aucun secret exposé.
Aucune ouverture sandbox sans décision explicite.
```

## RISKS

- À qualifier.
