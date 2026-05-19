---
doc_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_APPLY_FANTOME_01_RUNBOOK
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_STEP1B_APPLY_FANTOME_01
status: open
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - step1b
  - db-layer
  - fantome
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
---

# Runbook — step1b apply sur db-layer et fantome

## Séquence commune (sur chaque machine)

### 1. git pull

```bash
cd /opt/trading
git pull origin sot/mainline
```

Vérifier que le commit `5f282f8` est présent :

```bash
git log --oneline -3
```

### 2. Dry-run (vérification avant apply)

```bash
bash modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/apply_linux.sh
```

Sortie attendue :
- `Would install: .../ssh_config.linux -> ~/.ssh/config`
- `Would update:  /etc/hosts (managed block from .../hosts.block)`

### 3. Apply

```bash
bash modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/apply_linux.sh --apply
```

### 4. Validation

```bash
# Vérifier /etc/hosts
grep -A7 "reseau_ssh BEGIN" /etc/hosts

# Vérifier ~/.ssh/config
grep -A3 "Host fantome" ~/.ssh/config

# Test connectivité (depuis db-layer ou fantome)
ssh -o BatchMode=yes -o ConnectTimeout=5 admin-trading 'echo HOST=$(hostname)'
ssh -o BatchMode=yes -o ConnectTimeout=5 db-layer     'echo HOST=$(hostname)'
ssh -o BatchMode=yes -o ConnectTimeout=5 fantome       'echo HOST=$(hostname)'
```

---

## Sur db-layer

Ordre : machine déjà connue, refresh IPs + ajout alias fantome.

Backup automatique créé par le script : `/etc/hosts.bak.reseau_ssh.<date>` et `~/.ssh/config.bak.<date>`.

---

## Sur fantome

Ordre : première application. Le repo `/opt/trading` doit être présent (confirmé dans les docs chantier).

Vérifier avant :

```bash
ls /opt/trading/modules/reseau_ssh_step1b/
```

---

## Rollback

Si problème :

```bash
# Restaurer /etc/hosts
sudo cp /etc/hosts.bak.reseau_ssh.<date> /etc/hosts

# Restaurer ~/.ssh/config
cp ~/.ssh/config.bak.<date> ~/.ssh/config
```

---

## Critère de succès

- [ ] `db-layer` : `/etc/hosts` contient `192.168.0.191 fantome` et IPs `192.168.0.x`
- [ ] `db-layer` : `~/.ssh/config` contient `Host fantome`
- [ ] `fantome` : même état que ci-dessus
- [ ] `ssh fantome` depuis `db-layer` : `HOST=fantome`
