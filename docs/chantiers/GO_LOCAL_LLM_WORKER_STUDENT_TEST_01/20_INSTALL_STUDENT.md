# Install Student — Local LLM Worker

## Runtime recommandé

Option par défaut :

```text
Ollama
```

Option alternative :

```text
llama.cpp
```

## Vérifications système

```bash
python --version
git status -sb
```

## Vérification Ollama

```bash
ollama --version
ollama list
```

## Modèles candidats

Priorité :

```text
Gemma 4E2B / Gemma 2B / Gemma 3 4B / Qwen petit modèle instruction
```

Le modèle exact peut varier selon la disponibilité locale.

## Smoke test CLI

```bash
ollama run <model> "Réponds seulement: OK_LOCAL_MODEL"
```

## Smoke test script

```bash
python tools/local_llm_worker/scripts/model_smoke_test.py --model <model>
```

## Variables de configuration

Le fichier principal est :

```text
tools/local_llm_worker/config.yaml
```

Paramètres à valider :

- `model`
- `runtime`
- `input_roots`
- `max_files`
- `max_chars_per_file`
- `output_dir`
