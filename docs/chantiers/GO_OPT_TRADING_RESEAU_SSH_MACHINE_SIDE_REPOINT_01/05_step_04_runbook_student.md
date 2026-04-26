---
doc_id: GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01_STEP_04_STUDENT
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
  - student
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_MACHINE_SIDE_REPOINT_01/02_step_01_inventaire_et_rollback.md
  - modules/reseau_ssh/scripts/install_canonical_shortcuts.sh
---

# Step 04 - runbook `student`

## Ordre
Troisième machine cible de production, seulement après PASS sur `db-layer` et `admin-trading`.

## Risque spécifique
`student` garde l’historique le plus sensible autour de `step1b`.

## Sequence
1. Capturer le snapshot complet.
2. Vérifier `sanity-reseau_ssh` avant action.
3. Vérifier la présence de `/opt/trading/modules/reseau_ssh_step1b`.
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

## Critère d’arrêt renforcé
Rollback immédiat si :
- le snapshot diffère d’un état attendu non expliqué
- `sanity-reseau_ssh` échoue après repointage
- une dépendance `step1b` implicite apparaît pendant le test

## Target
1 module canonique par famille.
