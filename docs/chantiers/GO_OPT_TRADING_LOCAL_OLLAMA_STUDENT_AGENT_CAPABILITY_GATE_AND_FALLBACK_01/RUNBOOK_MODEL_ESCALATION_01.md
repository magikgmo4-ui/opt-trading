# RUNBOOK_MODEL_ESCALATION_01

Procédure quand le modèle 0.5B ne suffit pas.

## Quand escalader

1. La tâche nécessite un format de réponse exact (JSON, CSV, mot précis)
2. La tâche dépasse 3 étapes
3. La tâche nécessite une décision sans supervision humaine
4. Le 0.5B a déjà échoué 2 fois sur la même tâche

## Options d'escalade

### Option A : Direct Ollama (contournement agent)

```bash
curl -s http://127.0.0.1:11434/api/chat \
  -d '{
    "model":"qwen2.5:1.5b-instruct",
    "messages":[{"role":"user","content":"<votre instruction exacte>"}],
    "stream":false,
    "format":"json"
  }'
```

Avantage : format contrôlé, pas de surcharge agent.  
Inconvénient : pas d'accès aux tools/workspace.

### Option B : Agent chain avec modèle plus fort

```bash
# Modifier config temporairement
# Changer agents.defaults.model.primary en ollama/qwen2.5:1.5b-instruct
# Puis lancer openclaw agent
```

Inconvénient : latence ~131s, pas interactif.

### Option C : Provider distant (si configuré)

Vérifier les providers disponibles :
```bash
sudo cat /home/openclaw-lab/.openclaw/openclaw.json | python3 -c "
import sys,json;c=json.load(sys.stdin)
for p,m in c.get('agents',{}).get('defaults',{}).get('models',{}).items():
    print(p)
"
```

## Si aucun fallback viable

Documenter le gap et marquer la tâche comme **BLOCKED**.
Ne pas utiliser le 0.5B pour une tâche qu'on sait hors de ses capacités.

## RISKS

- À qualifier.
