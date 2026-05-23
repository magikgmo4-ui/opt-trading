---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01_FIX_OPTIONS
doc_type: options
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_PYTHON_ENV_FIX_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_FIX_OPTIONS

## Option A - Installer PyYAML dans le venv principal

Statut : non retenue en premier choix.

Raison :

- implique une mutation directe du runtime distant ;
- suppose que `/opt/trading/venv` est le runtime canonique du service ;
- ne corrige pas la logique fragile du wrapper.

## Option B - Forcer `/usr/bin/python3`

Statut : non retenue.

Raison :

- corrige le cas observe mais retire la possibilite d'utiliser un venv sain ;
- rend le wrapper moins portable.

## Option C - Selectionner un Python capable d'importer `yaml`

Statut : retenue.

Logique :

```bash
for candidate in /opt/trading/venv/bin/python3 /usr/bin/python3 python3; do
  if "$candidate" -c "import yaml" >/dev/null 2>&1; then
    PYTHON="$candidate"
    break
  fi
done
```

Avantages :

- aucune installation de dependance ;
- conserve le venv s'il devient sain ;
- bascule vers `/usr/bin/python3` quand le venv est incomplet ;
- echoue clairement si aucun Python ne peut charger PyYAML.

## Decision

Appliquer Option C dans `scripts/runtime_healthcheck.sh`.
