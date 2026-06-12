# 04_TOOL_POLICY_TARGET_AGENT_AUDIT

## Objectif

Identifier l'agent exact devant recevoir le patch tool-policy pour lever le blocage SSH/network OpenClaw.

## Contexte

`03_TOOL_POLICY_PATCH_PLAN.md` a établi que :

- `builder` contient `group:runtime` dans son deny ;
- `lab` contient `group:runtime` dans son deny ;
- `reviewer` ne contient pas `group:runtime` ;
- `orchestrateur` n'est pas candidat patch immédiat.

## Runtime lock

```text
NO_OPENCLAW_RUNTIME
NO_SSH_CONNECTION
NO_REMOTE_COMMAND
NO_CONFIG_PATCH
READ_ONLY_AUDIT_ONLY
```

---

## Trouvaille critique — pivot de stratégie

### `group:runtime` est un deny GLOBAL

Le fichier `modules/openclaw_config_modulaire/app/tools.json5` contient :

```json5
{
  profile: "coding",
  deny: [
    "group:runtime",   // ← ligne 5 — deny GLOBAL
    "browser",
    "canvas",
    "nodes",
    "cron",
    "gateway",
  ],
}
```

**Conséquence :**

```text
Retirer "group:runtime" du deny d'un agent dans agents.json5 ne suffit pas.
Le deny global dans tools.json5 reste actif pour tous les agents.
```

Le patch per-agent dans `agents.json5` (builder/lab) duplique ce que `tools.json5` établit déjà globalement.

### Nouveau scope de patch

Deux leviers sont maintenant visibles :

| Levier | Fichier | Portée | Action possible |
| :--- | :--- | :--- | :--- |
| Global deny | `tools.json5:5` | tous les agents | retirer `group:runtime` du deny global |
| Per-agent deny | `agents.json5:65` (builder), `:111` (lab) | agent seul | retirer `group:runtime` du deny agent |
| Per-agent allow override | `agents.json5` (à ajouter) | agent seul | ajouter allow explicite pour les outils SSH nécessaires |

**Question ouverte :**

```text
Un allow explicite per-agent peut-il overrider le global deny de tools.json5 ?
Si oui : Option B per-agent est viable.
Si non : le patch doit modifier tools.json5 (scope global).
```

---

## Rôles canoniques des agents

Source : `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md`

| Agent | Rôle canonique | Provider | Statut |
| :--- | :--- | :--- | :--- |
| orchestrateur | route mission locale bornée | policy V1 | canonique |
| builder | génération patch/script borné | policy V1 + fallback | canonique |
| reviewer | vérification scope/preuve | policy V1, écart runtime | canonique |
| lab | expérimentation locale / Ollama sandbox | local ou fallback | canonique ; fallback runtime observé |

Source complémentaire : `modules/model_provider_openclaw/docs/GO_OPENCLAW_ALIGNMENT_DECISION_07.md`

```text
builder : aligné policy/runtime
lab : configuré en runtime sur openrouter/qwen/qwen3-14b — correspond au fallback policy
```

---

## Agent target — décision

### Verdict

| Agent | `group:runtime` bloquant | Rôle | Besoin SSH/network | Verdict |
| :--- | :--- | :--- | :--- | :--- |
| orchestrateur | NON (allow list ciblée) | routing interne | improbable | SKIP |
| builder | OUI | génération patch/script | **probable** | **TARGET_CANDIDATE** |
| reviewer | NON | vérification scope | improbable | SKIP |
| lab | OUI | expérimentation locale | possible (exécution locale seulement) | SECONDARY_CANDIDATE |

```text
TARGET_AGENT_PRIMARY = builder
RATIONALE = "génération patch/script borné" implique exec, apply_patch, scripts
             qui peuvent requérir runtime tools selon le job OpenClaw concerné.

TARGET_AGENT_SECONDARY = lab
RATIONALE = expérimentation locale — moins probable pour SSH réseau,
             mais possible pour exec local runtime.
```

### Gate

```text
TARGET_AGENT_CONFIRMED = PARTIAL
```

`builder` est le candidat principal, mais la confirmation complète nécessite :

1. Identifier le job OpenClaw spécifique bloqué (quel agent exécute quoi).
2. Vérifier si per-agent allow overrides global deny dans tools.json5.

---

## Analyse stratégie de patch — révisée

### Scénario 1 — Per-agent allow override (si supporté)

Si un `allow` explicite per-agent peut overrider le deny global :

```json5
// agents.json5 — builder uniquement
tools: {
  profile: "coding",
  allow: [
    "<ssh-tool-name>",   // à identifier
  ],
  deny: [
    "group:runtime",
    ...
  ],
},
```

**Risque :** noms d'outils SSH exacts non encore confirmés localement.

### Scénario 2 — Retrait global dans tools.json5

Si le per-agent allow ne peut pas overrider le global :

```json5
// tools.json5 — modification globale
deny: [
  // "group:runtime",  ← retirer
  "browser",
  "canvas",
  "nodes",
  "cron",
  "gateway",
],
```

**Risque :** ouvre runtime pour TOUS les agents, pas seulement builder.

### Recommandation

```text
Préférer Scénario 1 si la résolution de policy le supporte.
Bloquer Scénario 2 jusqu'à confirmation que per-agent allow ne suffit pas.
```

---

## Questions restantes

| Question | Verdict | Next action |
| :--- | :--- | :--- |
| Per-agent allow override global deny ? | UNKNOWN | `openclaw config get` ou doc interne à lire |
| Noms exacts des outils SSH/runtime ? | UNKNOWN | `openclaw tools list` ou doc à consulter |
| Job OpenClaw exact bloqué ? | UNKNOWN | Retracer le chantier parent DBLAYER_REMOTE_EXEC |
| Patch tools.json5 global nécessaire ? | PENDING | Dépend de la réponse ci-dessus |

---

## Decision outcome

```text
TARGET_AGENT_PRIMARY = builder
TARGET_AGENT_CONFIRMED = PARTIAL
PATCH_STRATEGY = PENDING_POLICY_RESOLUTION_RULE
```

## NEXT_GO

```text
05_TOOL_POLICY_RESOLUTION_RULE_AUDIT.md
```

Rôle :

1. Déterminer si un `allow` per-agent peut overrider le `deny` dans `tools.json5` global.
2. Identifier les noms exacts des outils SSH/runtime dans OpenClaw.
3. Confirmer définitivement `TARGET_AGENT_CONFIRMED = true` ou bloquer.
4. Statuer sur le périmètre minimal du patch (agent seul vs global tools.json5).

## RISKS

- À qualifier.
