---
doc_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01_ENV_PORTS_PATHS_ANALYSIS
doc_type: analysis
repo: opt-trading
go_id: GO_OPT_TRADING_RUNTIME_HEALTHCHECK_RESIDUAL_WARNINGS_01
status: active
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 20_ENV_PORTS_PATHS_ANALYSIS

## Objet

Classifier les warnings `ENV`, `PORTS`, `PATHS` du runtime healthcheck (STEP 5) en :

- warning signalant un défaut réel à corriger, ou
- warning “bruit” issu d’entrées optionnelles, à accepter explicitement ou à reparamétrer.

## ENV

### Mécanique de check

- Le check `ENV` vérifie uniquement la présence des clés dans l’environnement.
- Les valeurs ne sont jamais loggées.

Source : `modules/runtime_health/healthcheck.py` (`check_env_key`).

### Sources d’environnement (EnvironmentFiles)

Le service systemd charge, sans obligation d’existence (`EnvironmentFile=-...`) :

```text
/etc/trading/telegram.env
/etc/trading/runtime.env
/opt/trading/env/telegram.env
/opt/trading/env/runtime.env
/opt/trading/modules/bot_vision_step2/config/bot_vision.env
```

Source : `deploy/systemd/opt-trading-runtime-health.service`.

### Variables attendues (sans valeurs)

Deux sources repo-first possibles :

1) Base config `modules/runtime_health/config/runtime_health.yml` :

- required: `TELEGRAM_BOT_TOKEN`, `ALLOWED_CHAT_ID`, `OPENAI_API_KEY`
- optional: `TV_WEBHOOK_KEY`, `TELEGRAM_CHAT_ID`

2) Machine scope `config/machine_runtime_map.yml` (ex: `db-layer`) :

- required_env: `[]`
- optional_env: `TELEGRAM_BOT_TOKEN`, `ALLOWED_CHAT_ID`

### Diagnostic attendu (sans terrain)

Le warning résiduel `ENV=WARN` sur `db-layer` peut s’expliquer par :

- clés optionnelles absentes dans les EnvironmentFiles réellement présents sur la machine, ou
- EnvironmentFiles présents mais non chargés (erreur de déploiement), ou
- exécution non systemd (shell) sans export préalable.

Décision à prendre :

- si Telegram doit être actif pour ce healthcheck, basculer en `required_env` (et garantir présence via EnvironmentFiles), ou
- si Telegram est intentionnellement facultatif sur `db-layer`, accepter le WARN ou retirer ces clés de `optional_env` pour viser `PASS`.

## PORTS

### Mécanique de check

`check_port(host, port)` effectue un connect TCP (timeout 2s).

Conséquences :

- port fermé ou service absent => `WARN` (si optional) / `FAIL` (si required)
- port ouvert => `PASS`

### Ports attendus (db-layer)

Scope `db-layer` :

- optional: `127.0.0.1:18789` (`openclaw_gateway`)
- optional: `127.0.0.1:8000` (`algo_hf_api`)

### Classification attendue

Cas A — `openclaw_gateway` :

- si le gateway est réellement un prérequis fleet/runtime, promouvoir en `required_ports` (et viser `PASS`).

Cas B — `algo_hf_api` :

- si le service est rarement actif / non requis, retirer ce port de la scope machine pour supprimer un WARN bruité.

## PATHS

### Mécanique de check

`check_path(path, writable)` :

- absent => `WARN` (optional) / `FAIL` (required)
- présent mais non-writable quand `writable=true` => `WARN` (optional) / `FAIL` (required)
- présent => `PASS`

Limite : le check ne vérifie pas l’ownership ni les permissions détaillées (uniquement `os.access`).

### Paths attendus (db-layer)

Scope `db-layer` :

- required:
  - `/opt/trading` (non writable)
  - `/opt/trading/data` (writable)
- optional:
  - `/var/log/trading`
  - `/shared`

### Hypothèses de WARN (db-layer)

- `/var/log/trading` absent si la machine est “journald-first” et n’écrit pas de logs fichiers.
- `/shared` absent si le montage SSHFS n’est pas présent (ou chemin différent), même si `shared-sshfs.service` est “up”.

Action read-only recommandée (terrain) :

- vérifier existence + type + owner/group + permissions des chemins attendus
- confirmer le chemin de montage réel si `/shared` n’est pas la racine retenue

## Résultat terrain (2026-05-23) — classification db-layer

Source : lecture read-only de `/opt/trading/data/runtime_health/latest.json` sur `db-layer`.

### ENV

```text
WARN env:TELEGRAM_BOT_TOKEN present=False required=False
WARN env:ALLOWED_CHAT_ID    present=False required=False
```

Conclusion : warning “bruit” cohérent avec `optional_env` sur `db-layer`.

### PORTS

```text
WARN port:openclaw_gateway 127.0.0.1:18789 required=False Connection refused
WARN port:algo_hf_api      127.0.0.1:8000  required=False Connection refused
```

Conclusion : warning “bruit” si ces services sont volontairement off sur `db-layer` hors besoins du moment.

### PATHS

```text
WARN path:/var/log/trading required=False path does not exist
PASS path:/shared          required=False ok
```

Conclusion : warning “bruit” probable si `db-layer` est journald-first et n’utilise pas `/var/log/trading`.

