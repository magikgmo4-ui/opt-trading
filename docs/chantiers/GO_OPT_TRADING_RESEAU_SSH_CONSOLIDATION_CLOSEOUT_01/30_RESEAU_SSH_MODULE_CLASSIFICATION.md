# Classification de la famille reseau_ssh

## Decision retenue

- surface canonique top-level retenue : `modules/reseau_ssh`
- implementation interne active : `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2`
- prerequis conserve : `modules/reseau_ssh_step1b`
- backend legacy / rollback : `scripts/reseau_ssh`
- `compat` est un statut de coexistence, pas un module top-level autonome supplementaire sur cette branche

## Matrice de classification

| Surface | Role constate | Statut retenu | Preuves lues | Ce qu'il ne faut pas faire maintenant |
| --- | --- | --- | --- | --- |
| `modules/reseau_ssh` | facade canonique top-level de la famille | `CANONIQUE` | `modules/reseau_ssh/README.md`, `modules/reseau_ssh/scripts/install_canonical_shortcuts.sh`, `modules/reseau_ssh/scripts/cmd.sh`, `modules/reseau_ssh/scripts/_reseau_ssh_common.sh` | ne pas le redescendre en simple compat ; ne pas casser la facade |
| `modules/reseau_ssh/modules/reseau_ssh/reseau_ssh_step2` | implementation WireGuard / firewall derriere la facade | `ACTIVE_INTERNE` | `.../reseau_ssh_step2/README.md`, `.../inventory.yaml` | ne pas le re-promouvoir comme surface top-level separee |
| `modules/reseau_ssh_step1b` | baseline hosts / ssh config / key tests | `PREREQUIS_COMPAT_TEMPORAIRE` | `modules/reseau_ssh_step1b/README.md`, `.../reseau_ssh_step1b/README.md` | ne pas le fusionner brutalement ni l'archiver sans audit des appels `baseline-*` |
| `scripts/reseau_ssh` | backend legacy garde pour rollback et appel explicite | `ROLLBACK_ONLY` | `scripts/reseau_ssh/README.md`, `scripts/reseau_ssh/README_RUNTIME_STATUS.md`, `scripts/reseau_ssh/install_reseau_ssh.sh` | ne pas le re-promouvoir comme canonique ; ne pas l'archiver directement tant que la sortie n'est pas revalidee |
| `compat` | coexistence transitoire entre facade canonique, `step1b` et backend legacy | `STATUT_LOGIQUE` | `modules/reseau_ssh/scripts/cmd.sh`, `modules/reseau_ssh/scripts/_reseau_ssh_transition.sh`, `modules/reseau_ssh/scripts/_reseau_ssh_common.sh` | ne pas confondre ce statut avec un nouveau module ou un nouveau parent |

## Lecture fonctionnelle de la facade canonique

`modules/reseau_ssh/scripts/cmd.sh` montre une facade deja consolidee mais encore transitoire :

- les commandes `wg-*` deleguent a l'implementation interne `reseau_ssh_step2`
- les commandes `baseline-*` deleguent a `modules/reseau_ssh_step1b`
- `bootstrap`, `ssh-hardening-safe` et `ssh-lockdown` passent par la couche transitoire `_reseau_ssh_transition.sh`
- certains verbes legacy ne sont plus exposes par la facade et exigent un appel explicite du backend legacy si necessaire

## Canonique retenu pour ce closeout

Le canonique de famille retenu reste :

- `modules/reseau_ssh`

Ce verdict est coherent avec :

- le README top-level du module
- l'installeur `install_canonical_shortcuts.sh`
- les liens machine-side constates sur `db-layer`, `admin-trading`, `student` et `fantome`

## Elements a ne pas fusionner maintenant

- ne pas fusionner physiquement `step1b` et `step2` dans ce lot
- ne pas archiver `scripts/reseau_ssh` avant une coupe explicite de tous les usages de rollback / compat
- ne pas remplacer automatiquement la config SSH globale locale ou machine-side
- ne pas normaliser en force le chemin repo de `fantome` sans GO dedie
