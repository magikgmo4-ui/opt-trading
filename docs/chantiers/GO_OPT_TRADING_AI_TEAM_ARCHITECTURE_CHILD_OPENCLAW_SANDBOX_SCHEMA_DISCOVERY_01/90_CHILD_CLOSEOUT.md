# 90_CHILD_CLOSEOUT

## Verdict

```text
CHILD_STATUS = PASS_WITH_PIVOTS
GATEWAY_STATUS = UP_AND_STABLE
RUNTIME_ORCHESTRATEUR = ALIVE
RUNTIME_BUILDER = ALIVE
```

## Objectif initial

Découvrir, documenter et canoniser le schéma supporté de `sandbox.mode` avant toute reprise runtime.

## Résultat réel

Le diagnostic initial a été corrigé :

```text
sandbox.mode n'était pas le vrai bloqueur actif.
tool policy repo V1.2.1 n'était pas la policy effective.
config effective = Remote V2 sous ~/.openclaw/openclaw.json.
gateway non démarré = vrai blocage opérationnel.
```

---

## Pivots canoniques

### Pivot 1 — sandbox.mode

`agents.json5` contenait `sandbox.mode = "all"`, mais `openclaw sandbox explain` a montré que la config effective était `mode = off`.

```text
sandbox.mode = not active blocker
```

### Pivot 2 — tool policy

`group:runtime` était présent dans la config repo V1.2.1, mais non actif dans la config effective V2.

```text
repo config V1.2.1 != deployed config V2
```

### Pivot 3 — déploiement V1.2.1

Le déploiement brut de V1.2.1 a été refusé pour trois raisons critiques :

```text
1. mismatch /home/openclaw vs /home/ghost (agentDir cassé)
2. token gateway réel risquant d'être écrasé par le placeholder
3. deny global group:runtime risquant d'être importé sur V2 propre
DEPLOYMENT_NO_GO_FOR_V121_RAW
```

### Pivot 4 — gateway V2

Le gateway a été démarré avec la config effective V2.

```text
GATEWAY_STATUS = UP_AND_STABLE
URL = ws://127.0.0.1:18789
PID = 9541
WAN exposure = absent (loopback uniquement)
```

### Pivot 5 — premier runtime contrôlé

Tests non destructifs réussis :

| Agent | Message | Résultat | Modèle | Durée | Sandbox |
| :--- | :--- | :--- | :--- | :--- | :--- |
| orchestrateur | `GATEWAY_TEST_OK` | **PASS** | qwen3-32b | 23s | off |
| builder | `BUILDER_ALIVE` | **PASS** | qwen3-coder-30b | 3.4s | off |

---

## Documents produits

| Fichier | Contenu | Verdict |
| :--- | :--- | :--- |
| `01_SANDBOX_SCHEMA_SOURCE_AUDIT.md` | Audit schéma sandbox.mode | PATCHABLE_SAFE_MODE_FOUND |
| `02_SANDBOX_PATCH_DECISION_MATRIX.md` | Reclasse le bloquant vers tool policy | pivot confirmé |
| `03_TOOL_POLICY_PATCH_PLAN.md` | Plan patch tool policy | PENDING gate |
| `04_TOOL_POLICY_TARGET_AGENT_AUDIT.md` | builder = TARGET, group:runtime dans tools.json5 global | pivot global |
| `05_TOOL_POLICY_RESOLUTION_RULE_AUDIT.md` | Deployed V2 sans group:runtime — blocage = gateway off | pivot majeur |
| `06_TOOL_POLICY_DEPLOYMENT_RISK_MATRIX.md` | 3 risques critiques V1.2.1 brute | DEPLOYMENT_NO_GO |
| `07_GATEWAY_ACTIVATION_PREFLIGHT.md` | Preflight gateway V2 | PREFLIGHT_STATUS = PASS |
| `08_GATEWAY_ACTIVATION_EXECUTION_PLAN.md` | Plan démarrage gateway | gate humain requis |
| `09_GATEWAY_ACTIVATION_EXECUTION_LOG.md` | Démarrage gateway | GATEWAY_UP |
| `10_GATEWAY_POST_START_RUNTIME_GATE.md` | Gate runtime | PENDING_HUMAN_VALIDATION |
| `11_RUNTIME_FIRST_SESSION_EXECUTION_LOG.md` | Tests orchestrateur + builder | RUNTIME_BUILDER_ALIVE |

---

## Sécurité — éléments respectés

```text
Aucun SSH réel exécuté.
Aucune commande remote exécutée.
Aucun patch appliqué sur agents.json5 ou tools.json5.
Aucun secret imprimé dans le repo.
Aucune exposition WAN.
Aucun bridge.
Aucun admin-trading.
Aucun closeout DB_LAYER rouvert.
Aucun index global modifié hors de ce chantier.
```

---

## État final

```text
Gateway OpenClaw actif (foreground, loopback:18789).
Runtime minimal validé : orchestrateur + builder répondent.
Builder vivant via gateway, sans SSH ni remote exec.
Config effective V2 stable.
Repo config V1.2.1 documentée comme non déployable brute.
```

---

## NEXT_GO recommandé

```text
GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_CONTROLLED_JOB_01
```

Objectif :

- utiliser le builder via gateway pour un job borné réel ;
- aucune SSH réelle au départ ;
- aucune commande remote au départ ;
- preuve de réponse structurée ;
- stop conditions strictes.
