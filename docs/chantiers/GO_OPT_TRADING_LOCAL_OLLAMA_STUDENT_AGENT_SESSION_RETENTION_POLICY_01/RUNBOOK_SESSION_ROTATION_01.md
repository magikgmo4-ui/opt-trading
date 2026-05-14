# RUNBOOK_SESSION_ROTATION_01

Rotation manuelle ou automatisée des sessions agent OpenClaw.

## Prérequis

- Gateway live : `curl http://127.0.0.1:18790/health`
- Accès sudo au répertoire `openclaw-lab`
- Destination archive : `/tmp/opencode/`

## Rotation manuelle

```bash
# 1. Trouver la session active
ls /home/openclaw-lab/.openclaw/agents/main/sessions/

# 2. Archiver les fichiers session
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/<sessionId>.jsonl /tmp/opencode/
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/sessions.json /tmp/opencode/sessions_index.<date>.archived

# 3. Vérifier que le répertoire est vide
sudo ls /home/openclaw-lab/.openclaw/agents/main/sessions/

# 4. La prochaine commande openclaw agent créera automatiquement une session vierge
```

## Test après rotation

```bash
# Prewarm
curl -s http://127.0.0.1:11434/api/generate \
  -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}'

# Cold smoke
sudo -u openclaw-lab /home/openclaw-lab/.npm-global/bin/openclaw agent \
  --agent main \
  --message "Reply with a short confirmation that the agent is alive. Do not mention trading." \
  --json

# Vérifier
# - durationMs < 180000
# - status = "ok"
# - inputTokens > 0
```

## Automatisation (cron)

```cron
# Toutes les semaines, rotation forcée
0 3 * * 0  sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl /tmp/opencode/ && sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/sessions.json /tmp/opencode/sessions_index.$(date +\%Y\%m\%d).archived
```

## Restauration d'archive

```bash
# Remettre une session archivée
sudo cp /tmp/opencode/<sessionId>.jsonl \
  /home/openclaw-lab/.openclaw/agents/main/sessions/
```

Restauration utile uniquement pour diagnostic — ne pas utiliser en production.

## Vérification rapide

```bash
# État actuel
echo "Nb sessions: $(sudo ls /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null | wc -l)"
echo "Dernière archive: $(ls -t /tmp/opencode/sessions_index.*.archived 2>/dev/null | head -1)"
```
