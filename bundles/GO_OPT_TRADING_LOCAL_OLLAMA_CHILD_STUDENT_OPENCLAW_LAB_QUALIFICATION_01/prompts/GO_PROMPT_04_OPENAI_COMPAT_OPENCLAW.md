# GO_PROMPT_04_OPENAI_COMPAT_OPENCLAW

## Objectif

Vérifier la compatibilité OpenAI locale pour préparer OpenClaw comme orchestrateur potentiel au-dessus d'Ollama.

## Test Python minimal

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://127.0.0.1:11434/v1/",
    api_key="ollama",
)

response = client.chat.completions.create(
    model="<model>",
    messages=[{"role": "user", "content": "Réponds OK."}],
)

print(response.choices[0].message.content)
```

## OpenClaw à vérifier

```text
OPENCLAW_INSTALLED=
OPENCLAW_VERSION=
OPENCLAW_PROVIDER_MODE=
OPENCLAW_BASE_URL=http://127.0.0.1:11434/v1/
OPENCLAW_MODEL=
OPENCLAW_LOGS=
TOOLS_ELEVATED_DISABLED=YES|NO|UNKNOWN
READ_ONLY_MODE=YES|NO|UNKNOWN
```

## Questions de validation

- OpenClaw peut-il utiliser `http://127.0.0.1:11434/v1/` ?
- Le modèle local est-il reconnu ?
- Les outils élevés sont-ils désactivables ?
- Les logs sont-ils lisibles ?
- Le mode lab/read-only est-il possible ?
- Y a-t-il un risque de shell libre ?

## Verdict

```text
OPENAI_COMPAT=PASS|FAIL
OPENCLAW_PROVIDER_READY=READY|LIMITED|LAB_ONLY|REJECT
RISK_LEVEL=LOW|MEDIUM|HIGH
NEXT_STEP=
```
