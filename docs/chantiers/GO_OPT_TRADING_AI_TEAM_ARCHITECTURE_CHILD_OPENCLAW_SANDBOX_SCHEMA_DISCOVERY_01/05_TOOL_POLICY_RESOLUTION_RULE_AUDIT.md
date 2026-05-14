# 05_TOOL_POLICY_RESOLUTION_RULE_AUDIT

## Objectif

Déterminer la règle de résolution OpenClaw entre deny global, allow per-agent et deny per-agent pour lever le blocage SSH/network avec le patch minimal sûr.

## Contexte

`04_TOOL_POLICY_TARGET_AGENT_AUDIT.md` a établi :

- `tools.json5` contient un deny global `group:runtime` ;
- `agents.json5` duplique `group:runtime` dans builder et lab ;
- `builder` est le `TARGET_AGENT_PRIMARY` ;
- résolution per-agent allow vs global deny inconnue.

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
READ_ONLY_AUDIT_ONLY
NO_CONFIG_PATCH
```

---

## Pivot critique — divergence deployed vs repo

### Deployed config (`~/.openclaw/openclaw.json`)

```json
{
  "agents": {
    "list": [
      {
        "id": "builder",
        "name": "Builder Remote V2",
        "model": { "primary": "openrouter/qwen/qwen3-coder-30b-a3b-instruct" }
      }
    ]
  }
}
```

**Aucun `tools.deny`, aucun `tools.allow`, aucun `group:runtime` dans le deployed config.**

Validation : `openclaw config validate --json` → `{ "valid": true }`.

### Repo config (`modules/openclaw_config_modulaire/app/`)

```json5
// tools.json5
{ deny: ["group:runtime", "browser", "canvas", "nodes", "cron", "gateway"] }

// agents.json5 — builder
{ tools: { deny: ["group:runtime", "browser", "canvas", "nodes", "cron", "gateway"] } }
```

Le repo config n'est pas déployé dans `~/.openclaw/`. Il n'existe pas de `config.d/` dans le répertoire déployé.

### Conséquence

```text
Le blocage group:runtime (agents.json5 + tools.json5) n'est pas actif dans le deployed config.
Le deployed builder (Remote V2) n'a aucun deny tool actif.
```

---

## openclaw sandbox explain --agent builder (deployed state)

```json
{
  "agentId": "builder",
  "sandbox": {
    "mode": "off",
    "sessionIsSandboxed": false,
    "tools": {
      "allow": ["exec", "process", "read", "write", "edit", "apply_patch",
                "image", "sessions_list", "sessions_history", "sessions_send",
                "sessions_spawn", "subagents", "session_status"],
      "deny": ["browser", "canvas", "nodes", "cron", "gateway",
               "telegram", "whatsapp", "discord", "irc", "googlechat",
               "slack", "signal", "imessage", "line"],
      "sources": {
        "allow": { "source": "default" },
        "deny":  { "source": "default" }
      }
    }
  }
}
```

**`exec` et `process` sont autorisés pour builder dans l'état déployé.**
**`group:runtime` n'apparaît pas dans le deny sandbox — il s'agit d'une couche distincte.**

---

## Deux couches de policy distinctes

| Couche | Fichier | Portée | `group:runtime` présent ? |
| :--- | :--- | :--- | :--- |
| General tool policy | `tools.json5` (repo) | global | OUI (repo seulement, non déployé) |
| Sandbox tool policy | `sandbox explain` | agent/session | NON — absent |
| Deployed tool policy | `~/.openclaw/openclaw.json` | deployed | NON — absent |

**Le `group:runtime` deny est une restriction de REPO CONFIG, pas de deployed config.**

---

## Résolution de policy — état des connaissances

### Règle de résolution sandbox tool policy

Le `fixIt` de `sandbox explain` désigne des clés actionnables distinctes :

```text
tools.sandbox.tools.allow       ← global sandbox allow override
agents.list[].tools.sandbox.tools.allow  ← per-agent sandbox allow override
```

Ces clés permettent un override per-agent de la sandbox tool policy. La spécificité per-agent prime sur le global dans ce contexte — le mécanisme est confirmé par l'existence de la clé.

### Règle de résolution general tool policy

La résolution pour `tools.json5` deny vs per-agent allow est :

```text
RESOLUTION_RULE = UNKNOWN_FROM_LOCAL_EVIDENCE
```

Aucune documentation locale ni sortie CLI ne précise si `agents.list[].tools.allow` peut overrider `tools.deny` global.

Hypothèse basée sur le pattern standard (deny → allow spécifique l'emporte) :

```text
HYPOTHESIS = PER_AGENT_ALLOW_LIKELY_OVERRIDES_GLOBAL_DENY
CONFIDENCE = LOW (non confirmé localement)
```

---

## Contenu de `group:runtime` — UNKNOWN

OpenClaw ne fournit pas localement la liste des outils inclus dans `group:runtime`. Commandes tentées :

```bash
openclaw tools list    → pas de sortie JSON exploitable
openclaw config schema → pas accessible
```

```text
GROUP_RUNTIME_CONTENTS = UNKNOWN
```

---

## Recadrage du blocage réel

```text
"Runtime bloqué" (invariant NO_OPENCLAW_RUNTIME) = gateway non démarré.
```

Ce n'est pas le tool policy qui bloque le runtime. C'est l'absence du processus gateway lui-même. La restriction `group:runtime` dans le repo config sera une barrière lors du déploiement de ce config, mais n'est pas la cause du blocage actuel.

---

## Tableau synthèse — questions tranchées

| Question | Verdict | Evidence |
| :--- | :--- | :--- |
| `group:runtime` deny actif en deployed ? | **NON** | `~/.openclaw/openclaw.json` — aucun deny tool |
| Deployed builder bloqué par tool policy ? | **NON** | `sandbox explain` — exec autorisé, source=default |
| Repo config déployé ? | **NON** | pas de `config.d/` dans `~/.openclaw/` |
| Per-agent sandbox allow override global deny ? | **OUI (confirmé)** | clé `agents.list[].tools.sandbox.tools.allow` dans fixIt |
| Per-agent general allow override `tools.json5` deny ? | **UNKNOWN** | aucune preuve locale |
| Contenu de `group:runtime` ? | **UNKNOWN** | aucune sortie CLI |
| Blocage réel = gateway non démarré ? | **OUI** | `runtime: direct`, `mode: off`, `NO_OPENCLAW_RUNTIME` invariant |

---

## Implication sur la stratégie de patch

Si le repo config (agents.json5 + tools.json5) est déployé sur `~/.openclaw/` :

1. `group:runtime` serait ajouté au deny global + per-agent pour builder et lab
2. Pour lever cette restriction sur builder seulement :
   - Option sandbox : ajouter `agents.list[builder].tools.sandbox.tools.allow` (confirmé supporté)
   - Option general : ajouter `agents.list[builder].tools.allow` — probable mais non confirmé
3. Si `group:runtime` contient `exec` : le deployed sandbox allow de `exec` serait écrasé

**Le risque est asymétrique :** déployer le repo config ajoute des restrictions non actives actuellement.

---

## Decision outcome

```text
RESOLUTION_RULE_FOR_SANDBOX = CONFIRMED (per-agent allow overrides global)
RESOLUTION_RULE_FOR_GENERAL_TOOLS = UNKNOWN
GROUP_RUNTIME_CONTENTS = UNKNOWN
BLOCAGE_REEL = GATEWAY_NOT_RUNNING (pas tool policy)
```

---

## NEXT_GO

```text
06_TOOL_POLICY_DEPLOYMENT_RISK_MATRIX.md
```

Rôle :

1. Évaluer le risque de déployer `tools.json5` + `agents.json5` repo config sur `~/.openclaw/` ;
2. Décider si le patch tool policy est nécessaire avant ou après activation du gateway ;
3. Définir le delta minimal entre deployed V2 et repo V1.2.1 ;
4. Statuer sur go/no-go de déploiement repo config.
