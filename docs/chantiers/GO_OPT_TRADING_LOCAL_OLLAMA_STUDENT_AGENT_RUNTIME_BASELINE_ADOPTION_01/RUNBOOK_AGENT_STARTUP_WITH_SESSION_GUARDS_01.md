# RUNBOOK_AGENT_STARTUP_WITH_SESSION_GUARDS_01

Procédure de démarrage agent OpenClaw avec protection session.

## Quick start

```bash
# 1. Vérifier l'état
curl http://127.0.0.1:18790/health

# 2. Pré-chauffer le modèle
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}' \
  >/dev/null

# 3. Vérifier la session active
SESSIONS=$(sudo ls /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | wc -l)
if [ "$SESSIONS" -gt 0 ]; then
  echo "ATTENTION: session(s) active(s) présente(s) - rotation recommandée si > 10 runs"
fi

# 4. Lancer l'agent
sudo -u openclaw-lab /home/openclaw-lab/.npm-global/bin/openclaw agent \
  --agent main \
  --message "votre message ici" \
  --json
```

## Rotation rapide

```bash
# Archiver la session en cours
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl /tmp/opencode/ 2>/dev/null
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/sessions.json /tmp/opencode/ 2>/dev/null

# La prochaine commande agent créera une session vierge
```

## Smoke minimal

```bash
# Prewarm
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}' \
  >/dev/null

# Smoke cold
time sudo -u openclaw-lab /home/openclaw-lab/.npm-global/bin/openclaw agent \
  --agent main \
  --message "You must reply with exactly one word: ALIVE" \
  --json | python3 -c "import sys,json;d=json.load(sys.stdin);print(f\"{d['result']['meta']['durationMs']}ms - {d['status']}\")"
```

## Dépannage

| Problème | Cause probable | Action |
|----------|---------------|--------|
| Timeout > 180s | Session saturée | Archiver session, créer nouvelle |
| Empty response | NO_REPLY (rien à signaler) | Message plus direct |
| Gateway refuse | Port occupé ou PID mort | `openclaw gateway stop && openclaw gateway start` |
| Ollama lent | Modèle froid | Attendre prewarm ~2s |

## RISKS

- À qualifier.
