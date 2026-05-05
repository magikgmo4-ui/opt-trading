# AI Team MVP

Runner securise read-only pour l'AI Team MVP, compatible Strict Workers.

## Architecture

```
modules/ai_team_mvp/
  runner.py                    # Runner read-only, stdlib only
  tasks/
    read_inventory.json        # Task packet Strict Workers
  README.md                    # Ce fichier
```

## Contrat Strict Workers

- `no_secrets: true`
- `no_env_files: true`
- `no_git_write_ops: true`
- `no_runtime_write_by_default: true`
- `requires_external_validation: true`
- `output_status: DRAFT_ONLY`
- `only_verified_models: true`

## Usage

```bash
cd /opt/trading
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/read_inventory.json
```

## Verification

```bash
python3 -c "import json; d=json.load(open('modules/ai_team_mvp/tasks/read_inventory.json')); print('OK:', d['task_id'])"
```

## Smoke

```bash
python3 modules/ai_team_mvp/runner.py modules/ai_team_mvp/tasks/read_inventory.json
git diff --stat
```

## Artefacts reutilises

| Artefact | Role |
|:---------|:-----|
| Strict Workers | Securite + execution |
| Architecture Canon AI Team | Structure cible |
| validated_prompt_factory | Standardisation prompts |
| Multi-Agents Canon Parent | Doctrine multi-agent |
