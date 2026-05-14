# GO_OPT_TRADING_LOCAL_OLLAMA_STUDENT_AGENT_CONTROLLED_USAGE_RUNBOOK_01

## Prérequis

- Gateway live : `curl http://127.0.0.1:18790/health` renvoie `200`
- Ollama opérationnel : `curl http://127.0.0.1:11434/api/generate -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm"}'`
- Session active non saturée (voir `session_diagnostic.sh`)
- Aucun trade ou worker en cours (vérifier avec `ps aux | grep -i trade`)

## Quand utiliser ce runtime

- Tâches d'exploration ou diagnostic OpenClaw gateway
- Tests de routage, skills, sessions sans trading réel
- Développement de scripts ou runbooks annexes
- Smoke tests préalables à un changement provider
- Travaux nécessitant un agent local sans dépendance réseau externe

## Quand ne PAS utiliser

- Trading réel ou paper-trading : **INTERDIT** sans GO runtime dédié
- Worker de collecte ou d'exécution continue : **INTERDIT**
- Tâches nécessitant > 4096 tokens de contexte
- Sessions nécessitant une latence < 5s (le warm est à 5-10s)
- Enchaînement de > 10 runs sans rotation

## Format de tâche acceptable

| Type | Acceptable | Exemple |
|------|:----------:|---------|
| Smoke test | ✅ | `Reply with exactly one word: ALIVE` |
| Diagnostic gateway | ✅ | `/status` via agent |
| Lecture workspace | ✅ | `List files in workspace` |
| Test skill | ✅ | `Run skill X and report` |
| Tâche multi-étapes | ⚠️ | Max 3-4 étapes, sinon trop lent |
| Trading | ❌ | Bloqué par invariant |
| Worker continu | ❌ | Bloqué par invariant |

## Procédure de lancement

```bash
# 1. Vérifier gateway
GATEWAY_OK=$(curl -s -o /dev/null -w "%{http_code}" http://127.0.0.1:18790/health)
if [ "$GATEWAY_OK" != "200" ]; then
  echo "Gateway hors-service"
  exit 1
fi

# 2. Vérifier session
SESSION_COUNT=$(sudo ls /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | wc -l)
if [ "$SESSION_COUNT" -gt 0 ]; then
  echo "Session(s) active(s) présente(s). Rotation si > 8 runs."
  sudo bash docs/chantiers/.../scripts/session_diagnostic.sh
fi

# 3. Prewarm Ollama
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}' \
  >/dev/null

# 4. Lancer agent
sudo -u openclaw-lab /home/openclaw-lab/.npm-global/bin/openclaw agent \
  --agent main \
  --message "<votre message>" \
  --json
```

## Diagnostic avant retry

Si l'agent ne répond pas dans les 180s :

```bash
# 1. Vérifier session
sudo grep -c '"error":"request timed out"' \
  /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null

# 2. Si > 3 timeouts → rotation
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl /tmp/opencode/
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/sessions.json /tmp/opencode/

# 3. Prewarm et retenter
```

## Fallback si latence ou saturation

| Problème | Action |
|----------|--------|
| Latence cold > 120s | Attendre prewarm complet, réessayer |
| Latence warm > 30s | Rotation session, retenter |
| Timeout > 180s | Rotation immédiate, `session_diagnostic.sh` |
| Session saturée | Archiver, créer vierge |
| Provider indisponible | Vérifier Ollama, gateway, disque |

## Liens vers les ressources

- Baseline adoption : `docs/chantiers/.../RUNTIME_BASELINE_ADOPTION_01.md`
- Runbook startup : `docs/chantiers/.../RUNBOOK_AGENT_STARTUP_WITH_SESSION_GUARDS_01.md`
- Politique rétention : `docs/chantiers/.../SESSION_RETENTION_POLICY_01.md`
- Script diagnostic : `docs/chantiers/.../scripts/session_diagnostic.sh`
- Script purge : `docs/chantiers/.../scripts/purge_old_sessions.sh`
