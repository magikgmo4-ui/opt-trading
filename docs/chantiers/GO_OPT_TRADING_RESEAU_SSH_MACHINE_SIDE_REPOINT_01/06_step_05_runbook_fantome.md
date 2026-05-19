---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_05_FANTOME
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
  - fantome
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 05 - runbook `fantome`

## Ordre
Quatrième machine cible.

`fantome` est traitée comme machine distincte, pas comme simple variante de `student`.

## Hypothèse de travail
Le repo la traite historiquement comme surface dev dédiée.

Donc :
- qualification séparée
- même snapshot et même rollback
- aucune supposition automatique de parité avec `student`

## Sequence
1. Capturer le snapshot complet.
2. Vérifier `sanity-reseau_ssh` avant action.
3. Vérifier la présence de `/opt/trading/modules/reseau_ssh`.
4. Vérifier si `step1b` est présent ou non, sans l’imposer.
5. Lancer :

```bash
sudo bash /opt/trading/modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
```

6. Rejouer :

```bash
readlink -f /usr/local/bin/menu-reseau_ssh
readlink -f /usr/local/bin/cmd-reseau_ssh
readlink -f /usr/local/bin/sanity-reseau_ssh
sanity-reseau_ssh
cmd-reseau_ssh sanity
```

## Critère d’arrêt
Rollback immédiat si :
- les alias courts ne résolvent pas vers `modules/reseau_ssh/scripts/*`
- `sanity-reseau_ssh` échoue après repointage
- une spécificité locale `fantome` apparaît et n’est pas documentée

## Target
1 module canonique par famille.
