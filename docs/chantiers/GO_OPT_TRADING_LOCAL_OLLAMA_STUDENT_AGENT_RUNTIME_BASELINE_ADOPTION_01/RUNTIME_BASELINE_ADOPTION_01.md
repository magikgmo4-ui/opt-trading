# RUNTIME_BASELINE_ADOPTION_01

Adoption canonique du runtime local Student/Ollama pour les chantiers futurs.

## Spécification du runtime

| Attribut | Valeur |
|----------|--------|
| Provider | Ollama local |
| Modèle | `qwen2.5:0.5b-instruct` |
| Type | CPU local |
| Port Ollama | `127.0.0.1:11434` |
| Port Gateway | `127.0.0.1:18790` |
| Contexte | `n_ctx=4096` tokens |
| System prompt | ~3500 tokens |
| Budget historique | ~600 tokens |

## Performance

| Scénario | Latence |
|----------|:-------:|
| Prewarm Ollama | ~2s |
| Cold smoke (session vierge) | ~52-60s |
| Warm smoke (même session) | ~5-10s |

## Quand utiliser

- Tâches agent OpenClaw ne nécessitant pas de raisonnement profond
- Tests de configuration gateway/routing
- Diagnostics de session agent
- Développement de skills ou plugins simples
- Smoke tests avant validation provider distant

## Quand ne pas utiliser

- Tâches avec historique session > 600 tokens (~10 runs)
- Requêtes nécessitant > 4096 tokens de contexte
- Raisonnement multi-étapes complexes (trop lent sur CPU)
- Trading réel ou quasi-réel

## Procédure avant exécution agent

```bash
# 1. Vérifier gateway
curl http://127.0.0.1:18790/health

# 2. Vérifier session active
ls /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl 2>/dev/null
# Si session > 10 runs ou multiple erreurs → rotation

# 3. Rotation si nécessaire
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/*.jsonl /tmp/opencode/
sudo mv /home/openclaw-lab/.openclaw/agents/main/sessions/sessions.json /tmp/opencode/

# 4. Prewarm Ollama
curl http://127.0.0.1:11434/api/generate \
  -d '{"model":"qwen2.5:0.5b-instruct","prompt":"warm","stream":false}'
```

## Procédure après saturation

1. Exécuter `session_diagnostic.sh`
2. Si saturation détectée → archiver session active
3. Exécuter `purge_old_sessions.sh`
4. Créer session vierge (automatique au prochain run)
5. Exécuter smoke canonique de vérification

## Seuils d'alerte

| Métrique | Seuil | Action |
|----------|:-----:|--------|
| Runs par session | > 8 | Planifier rotation |
| Runs par session | > 10 | Rotation immédiate |
| PROMPT_ERROR consécutifs | ≥ 3 | Rotation immédiate |
| Age session | > 7 jours | Rotation forcée |
| Archives | > 30 jours | Purge automatique |

## Liens utiles

- Politique rétention : `docs/chantiers/.../SESSION_RETENTION_POLICY_01.md`
- Script diagnostic : `docs/chantiers/.../scripts/session_diagnostic.sh`
- Script purge : `docs/chantiers/.../scripts/purge_old_sessions.sh`
- Runbook rotation : `docs/chantiers/.../RUNBOOK_SESSION_ROTATION_01.md`
