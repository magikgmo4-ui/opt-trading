# 10_GATEWAY_POST_START_RUNTIME_GATE

## Objectif

Définir les conditions et le plan du premier test runtime contrôlé via le gateway OpenClaw actif.

**Ce document ne lance pas de session runtime.**

## Source

- `09_GATEWAY_ACTIVATION_EXECUTION_LOG.md` — GATEWAY_STATUS = UP

## État courant

```text
GATEWAY_STATUS = UP
PID = 9541
URL = ws://127.0.0.1:18789
RUNTIME_JOB = 0 sessions actives
RUNTIME_GATE = PENDING_HUMAN_VALIDATION
SSH_REAL_CONNECTION = BLOCKED
```

---

## Agents disponibles

| Agent | Modèle | Sessions | Heartbeat | Default |
| :--- | :--- | :--- | :--- | :--- |
| orchestrateur | openrouter/qwen/qwen3-32b | 0 | activé (30m) | **OUI** |
| builder | openrouter/qwen/qwen3-coder-30b-a3b-instruct | 0 | désactivé | non |
| reviewer | openrouter/deepseek/deepseek-r1 | 0 | désactivé | non |
| lab | openrouter/qwen/qwen3-14b | 0 | désactivé | non |

---

## Prérequis auth — gate critique

Tous les agents utilisent des modèles **openrouter**. Un premier runtime requiert :

```text
OPENROUTER_API_KEY = configurée dans l'environment ou dans le auth store OpenClaw
```

À vérifier avant exécution :

```bash
openclaw models list --json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print('models_ok:', bool(d))" || true
# ou:
env | grep -i "openrouter\|openai\|api_key" | grep -v "=" | head -5 || true
```

**Si auth absente → runtime échouera avec erreur d'authentification.**

---

## Test runtime prévu — non destructif

### Cible primaire : `orchestrateur` (agent default)

```bash
openclaw agent \
  --agent orchestrateur \
  --message "Reply with exactly: GATEWAY_TEST_OK" \
  --json
```

Attendu :

```json
{ "ok": true, "reply": "GATEWAY_TEST_OK" }
```

Raison du choix :
- Agent default, le plus simple à tester
- Heartbeat déjà configuré — preuve que le routing est opérationnel
- Modèle léger (qwen3-32b via openrouter)
- Aucune commande SSH ni remote exec dans le message

### Cible secondaire : `builder` (si orchestrateur passe)

```bash
openclaw agent \
  --agent builder \
  --message "Reply with exactly: BUILDER_ALIVE" \
  --json
```

Raison du choix différé :
- builder est le TARGET_AGENT_PRIMARY pour SSH/runtime future
- Test d'abord orchestrateur pour valider le routing gateway

---

## Stop conditions

Arrêt immédiat si :

```text
- Erreur d'authentification openrouter (STOP → vérifier auth avant relance)
- Session créée mais aucune réponse après 60s timeout
- Agent lance un job autonome non sollicité (SSH, exec remote, etc.)
- Réponse contient un token, une clé ou un secret
- Session_count > 1 sans action explicite
- WAN inattendu dans les logs gateway
- Gateway crash (PID 9541 absent)
```

---

## Invariants runtime

```text
NO_SSH_REAL_CONNECTION
NO_REMOTE_EXEC
NO_ADMIN_TRADING_INTERACTION
NO_WAN_BRIDGE
NO_CLOSEOUT_DBLAYER_REOPEN
NO_SECRET_IN_REPO
FIRST_SESSION_MUST_BE_NON_DESTRUCTIVE
```

---

## Rollback session

```bash
# Si session bloquée
openclaw sessions --all-agents --json
# → noter session_id

# Stop gateway (rollback total)
kill 9541
```

---

## Gate — validation humaine requise

```text
RUNTIME_GATE_STATUS = PENDING_HUMAN_VALIDATION
```

Conditions pour obtenir la validation :

1. Auth openrouter confirmée dans l'environment.
2. Opérateur confirme que la commande `openclaw agent --agent orchestrateur --message "..."` est non destructive.
3. Opérateur accepte qu'une session soit créée dans `/home/ghost/.openclaw/agents/orchestrateur/sessions/`.
4. Stop conditions comprises et opérateur prêt à intervenir.

---

## NEXT_GO (si validation humaine obtenue)

```text
11_RUNTIME_FIRST_SESSION_EXECUTION_LOG.md
```

Rôle :

1. Exécuter le test orchestrateur non destructif ;
2. Enregistrer le résultat (ok/KO) ;
3. Si OK : lancer le test builder ;
4. Si builder OK : statuer `RUNTIME_BUILDER_ALIVE` ;
5. Si KO à n'importe quelle étape : documenter le blocage.

## RISKS

- À qualifier.
