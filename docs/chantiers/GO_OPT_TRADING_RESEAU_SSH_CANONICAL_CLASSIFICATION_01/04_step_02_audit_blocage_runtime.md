---
doc_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01_STEP_02_RUNTIME_BLOCK
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_RESEAU_SSH_CANONICAL_CLASSIFICATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - reseau_ssh
  - runtime
  - blockers
  - modules
surface: chantier
source_kind: canonical
updated_at: 2026-04-25
links:
  - modules/reseau_ssh/scripts/cmd.sh
  - modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2/scripts/reseau_ssh_cmd.sh
  - modules/reseau_ssh_step1b/modules/reseau_ssh/reseau_ssh_step1b/scripts/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
  - scripts/reseau_ssh/reseau_ssh_menu.sh
  - scripts/reseau_ssh/sanity_reseau_ssh.sh
---

# Step 02 - audit du blocage runtime

## Constat principal
La convergence vers `1 module canonique par famille` est acquise cote repo-side.

Elle reste bloquee cote runtime machine-side par une separation de publication encore reelle.

## Capacites par surface

### `modules/reseau_ssh`
Capacites top-level publiees repo-side :
- `info`
- `readme`
- `menu`
- `sanity`
- commandes WG/firewall deleguees
- commandes `baseline-*` deleguees

### `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
Capacites propres :
- WireGuard
- rendu de config WG
- application WG
- firewall UFW lie au reseau de gestion

### `modules/reseau_ssh_step1b`
Capacite utile distincte :
- appliquer `/etc/hosts`
- appliquer `~/.ssh/config`
- fixer hostname Linux
- sanity/connectivite SSH de base

### `scripts/reseau_ssh`
Surface runtime machine-side encore active :
- publication des alias courts
- backend operateur historique
- installateur encore utilise pour `menu/cmd/sanity-reseau_ssh`

## Conclusion
Le blocage n'est plus la presence d'un faux survivant top-level dans `modules/`.

Le blocage est maintenant :
- la publication machine-side encore externe au module canonique
- plus la baseline `step1b` encore gardee en compat

## Target
1 module canonique par famille.

## RISKS

- À qualifier.
