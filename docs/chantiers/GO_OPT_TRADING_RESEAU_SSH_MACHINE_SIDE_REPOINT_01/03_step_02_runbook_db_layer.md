---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_02_DB_LAYER
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
  - db-layer
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 02 - runbook `db-layer`

## Ordre
Première machine cible.

## Sequence
1. Capturer le snapshot.
2. Vérifier `sanity-reseau_ssh` avant changement.
3. Vérifier la présence de `menu/cmd/sanity-reseau_ssh_step2` si déjà installés.
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

## Verdict attendu
- alias courts -> `modules/reseau_ssh/scripts/*`
- `sanity-reseau_ssh` = PASS
- compat `*_reseau_ssh_step2` toujours disponible

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
