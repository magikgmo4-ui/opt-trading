---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_03_ADMIN_TRADING
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - machine
  - admin-trading
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 03 - runbook `admin-trading`

## Ordre
Deuxième machine cible, après PASS sur `db-layer`.

## Sequence
1. Capturer le snapshot.
2. Vérifier l’état actuel des alias courts.
3. Vérifier la présence de `/opt/trading/modules/reseau_ssh`.
4. Lancer :

```bash
sudo bash /opt/trading/modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
```

5. Rejouer :

```bash
readlink -f /usr/local/bin/menu-reseau_ssh
readlink -f /usr/local/bin/cmd-reseau_ssh
readlink -f /usr/local/bin/sanity-reseau_ssh
sanity-reseau_ssh
cmd-reseau_ssh sanity
```

## Point de vigilance
Ne rien retirer sur `admin-trading` dans ce lot :
- ni `scripts/reseau_ssh`
- ni `*_reseau_ssh_step2`
- ni `step1b`

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
