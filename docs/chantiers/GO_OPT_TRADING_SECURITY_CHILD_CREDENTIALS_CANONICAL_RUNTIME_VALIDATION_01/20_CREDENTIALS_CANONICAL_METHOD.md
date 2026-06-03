---
doc_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01_METHOD
doc_type: canonical_method
repo: opt-trading
go_id: GO_OPT_TRADING_SECURITY_CHILD_CREDENTIALS_CANONICAL_RUNTIME_VALIDATION_01
status: canonical
created_at: 2026-06-03
---

# Méthode canonique — Credentials & Rotation

## Principe général

```text
Git = registre/templates/docs (jamais de valeurs)
Secrets = filesystem local uniquement
Rotation = CLI interactif ou sync SSH
Audit = LocalCMS /credentials (lecture seule, statuts uniquement)
```

## Storage types

| Type | Localisation | Accès | Exemple credentials |
|------|-------------|-------|-------------------|
| `env` | `/opt/trading/.env` | user direct | BOT_TOKEN, TV_WEBHOOK_KEY, DB_* |
| `role` | `/etc/opt-trading/env.d/roles/<role>.env` | sudo requis | CHAT_ID_*, AIRTABLE_*, CLICKUP_* |
| `openclaw` | `~/.openclaw/openclaw.json` | user direct | OPENAI_API_KEY, ANTHROPIC_API_KEY |
| `system` | `/etc/wireguard/`, `~/.ssh/` | system/user | WG_PRIVATE_KEY, termux_ssh_key |

## Règle git anti-fuite

```text
git diff --cached --check  # avant chaque commit
.gitignore bloque : .env, .secrets/, /etc/opt-trading/
```

Les fichiers `.env.example` dans `configs/env/roles/` ne contiennent que des clés vides.

## Rotation par type

### env (`.env` à la racine)

```bash
# Méthode interactive (recommandée)
python3 scripts/credentials_form.py --provider <Provider>

# Méthode manuelle
vim /opt/trading/.env
# Format : KEY=value (une ligne par credential)
```

### role (fichiers `/etc/opt-trading/env.d/roles/`)

```bash
# Import depuis une autre machine
scripts/env_role_sync.sh pull <machine> <role>

# Push vers une autre machine
scripts/env_role_sync.sh push <machine> <role>

# Diff clés (sans valeurs)
scripts/env_role_sync.sh diff <machine> <role>

# Via CLI interactif (écrit via sudo tee + chmod 600)
python3 scripts/credentials_form.py --provider <Provider>
```

Propriétés : chmod 600, root-owned.

### openclaw (LLM cloud)

```bash
openclaw configure
# Wizard interactif — ne pas utiliser openclaw config set pour les clés API
```

### system (SSH/WireGuard)

Voir : `docs/chantiers/GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01/60_ROTATION_RUNBOOK.md`

## Inspection statut (sans valeurs)

```bash
# CLI — statut par provider avec couleurs ANSI
python3 scripts/credentials_form.py --status

# CLI — un provider spécifique
python3 scripts/credentials_form.py --status --provider Telegram

# LocalCMS — panel HTML
http://localhost:8700/credentials

# LocalCMS — JSON machine-readable
http://localhost:8700/credentials/json
```

## Sync multi-machine

```bash
# Lister les rôles déployés sur une machine
scripts/env_role_sync.sh list fantome

# Pull depuis fantome
scripts/env_role_sync.sh pull fantome telegram_collector

# Push vers fantome
scripts/env_role_sync.sh push admin-trading airtable_user
```

## Modèle de change request

Toute modification du registre (ajout/suppression de credential, rôle, machine)
produit un `CREDENTIAL_CHANGE_REQUEST` dans le chantier concerné :

```
docs/chantiers/<GO_ID>/10_CREDENTIAL_CHANGE_REQUEST.md
Type : ADD | REMOVE | MODIFY
Contenu : clés uniquement, jamais de valeurs
```

## Registre canonique (git)

```
configs/env/registry/credentials.yaml  — 35 credentials, 15 providers
configs/env/registry/roles.yaml        — 13 rôles
configs/env/registry/machines.yaml     — 5 machines
configs/env/roles/*.env.example        — templates vides par rôle
```

## Règle de vérification post-rotation

```bash
# 1. Syntax check
python3 -c "import ast; ast.parse(open('modules/localcms/app/main.py').read())"

# 2. Statut credentials
python3 scripts/credentials_form.py --status

# 3. Smoke system
./scripts/verify_all.sh

# 4. Si role file modifié, sync vers autres machines
scripts/env_role_sync.sh push <machine> <role>
```
