# GO_PROMPT_03_OLLAMA_API_TESTS

## Objectif

Vérifier Ollama local, API, modèles, JSON structuré.

## Commandes

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

ollama --version || true
ollama list || true
ollama ps || true
ss -lntp | grep 11434 || true
curl -sS http://127.0.0.1:11434/api/version || true
curl -sS http://127.0.0.1:11434/api/tags || true
```

## Chat simple

```bash
MODEL="<model>"
curl -sS http://127.0.0.1:11434/api/chat -d "{
  \"model\": \"$MODEL\",
  \"messages\": [{\"role\":\"user\",\"content\":\"Réponds OK en une phrase.\"}],
  \"stream\": false
}"
```

## JSON structuré

```bash
MODEL="<model>"
curl -sS http://127.0.0.1:11434/api/chat -d "{
  \"model\": \"$MODEL\",
  \"messages\": [{\"role\":\"user\",\"content\":\"Retourne un JSON avec status, risk, next_action.\"}],
  \"format\": \"json\",
  \"stream\": false,
  \"options\": {\"temperature\": 0}
}"
```

## Verdict

```text
OLLAMA_VERSION=
PORT_11434=LOCALHOST|LAN|ABSENT
API_LOCAL=PASS|FAIL
MODELS=PASS|FAIL
CHAT_SIMPLE=PASS|FAIL
JSON_STRUCTURED=PASS|FAIL
```
