# RUNBOOK_PROVIDER_ESCALATION_01

Procédure d'escalade provider quand le modèle local ne suffit pas.

## Quand escalader

1. Tâche nécessitant format exact → format non supporté par 0.5B agent chain
2. Latence trop élevée → 1.5B direct peut être plus rapide pour tâche simple
3. Raisonnement nécessaire → 1.5B direct avec deepseek-r1 si besoin
4. Risque élevé → REFUS si pas de provider distant configuré

## Options

### Option 1 : Direct Ollama (contournement agent chain)

```bash
curl -s http://127.0.0.1:11434/api/chat \
  -d '{
    "model":"qwen2.5:1.5b-instruct",
    "messages":[{"role":"user","content":"<votre instruction>"}],
    "stream":false
  }'
```

Utilisation : format exact, classification, résumé.

### Option 2 : Deepseek-r1 direct (raisonnement)

```bash
curl -s http://127.0.0.1:11434/api/chat \
  -d '{
    "model":"deepseek-r1:1.5b",
    "messages":[{"role":"user","content":"<besoin de raisonnement>"}],
    "stream":false
  }'
```

Utilisation : tâche nécessitant raisonnement (mais pas de tools).

### Option 3 : Provider distant (non configuré actuellement)

Vérifier les providers disponibles dans la config OpenClaw. Si aucun, → REFUS.

## Blocage

Si aucun fallback viable → REFUS explicite.
Ne pas dégrader silencieusement vers un modèle incapable de la tâche.

## RISKS

- À qualifier.
