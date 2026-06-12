---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_04_RESEAU_SHARE_TRANSFER_ROLE_MAP
doc_type: chantier_execution_note
repo: opt-trading
project: opt-trading
module: modules
go_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01
status: complete
lifecycle_stage: execution
topic_keys:
  - opt-trading
  - modules
  - step-04
  - reseau
  - shared
  - transfer
  - role-map
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/reseau_ssh_canonique.md
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/11_step_03b_consolidation_eval_reseau_share_transfer.md
  - scripts/reseau_ssh/reseau_ssh_cmd.sh
  - modules/reseau_ssh/README.md
  - modules/reseau_ssh_step1b/README.md
  - modules/reseau_ssh_step2/README.md
  - modules/shared/README.md
  - modules/shared_files_sftp/README.md
  - modules/shared_sshfs_permanent/README.md
  - modules/winscp_transfer/README.md
---

# Step 04 - role map `reseau/share/transfer`

## Statut
Complete.

## Objet
Produire la carte de role de la suite elargie `reseau / partage / transfert` sans la confondre avec une seule lignee de consolidation.

## Verifications utilisees
- lecture de `docs/status/reseau_ssh_canonique.md`
- lecture de `docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/11_step_03b_consolidation_eval_reseau_share_transfer.md`
- lecture de `scripts/reseau_ssh/reseau_ssh_cmd.sh`
- lecture des README de :
  - `modules/reseau_ssh`
  - `modules/reseau_ssh_step1b`
  - `modules/reseau_ssh_step2`
  - `modules/shared`
  - `modules/shared_files_sftp`
  - `modules/shared_sshfs_permanent`
  - `modules/winscp_transfer`

## Hierarchie d'entrypoints
| Couche | Entree retenue | Role |
|---|---|---|
| baseline SSH / WireGuard | `scripts/reseau_ssh/reseau_ssh_cmd.sh` | bootstrap, hardening, WireGuard, sanity |
| surface canonique inter-machines | `cmd-shared` | UX quotidienne sur `/shared` |
| exposition serveur | `cmd-shared_files_sftp` | couche SFTP cote `admin-trading` |
| montage client Linux | `cmd-shared_sshfs_permanent` | montage permanent `/shared` |
| workflow Windows | `cmd-winscp_transfer` | inbox / outbox / send / fetch / deploy |

## Carte de role
| Composant | Statut | Role retenu | Ownership machine dominant |
|---|---|---|---|
| `reseau_ssh_step2` | survivant | baseline SSH / WireGuard | infra de base |
| `reseau_ssh_step1b` | transition | prerequis intermediaire | infra de base |
| `reseau_ssh` | legacy | etape historique | historique |
| `shared` | actif | surface canonique inter-machines | usage quotidien multi-machines |
| `shared_files_sftp` | actif | exposition serveur SFTP de `shared` | `admin-trading` |
| `shared_sshfs_permanent` | actif | montage Linux de `shared` | `student`, `db-layer` |
| `winscp_transfer` | actif | workflow Windows inbox/outbox | Windows + `admin-trading` |

## Frontieres operationnelles
- `reseau_ssh_step2` fournit la baseline reseau et la connectivite securisee. Il ne possede pas la surface metier `/shared`.
- `shared` definit l'UX et la doctrine de la surface de fichiers inter-machines. Il ne possede pas lui-meme la couche transport.
- `shared_files_sftp` expose la surface cote serveur.
- `shared_sshfs_permanent` monte la surface cote clients Linux.
- `winscp_transfer` specialise le flux Windows vers `inbox` / `outbox` et le push-pull operatoire.

## Points de duplication ou d'ambiguite
- plusieurs modules manipulent la meme surface `/shared`, mais a des niveaux differents :
  - doctrine et UX
  - exposition serveur
  - montage client
  - workflow Windows
- les notions de `status`, `path`, `host` et `sanity` existent dans plusieurs wrappers sans contrat unique encore formalise.
- les noms hote / LAN / WireGuard de la baseline `reseau_ssh*` irriguent ensuite les couches `sshfs` et WinSCP, ce qui cree un couplage sans identite de module commune.
- `shared` pourrait etre lu a tort comme sous-produit de `reseau_ssh*`, alors qu'il s'agit d'une surface de travail canonique distincte.

## Risques de consolidation
- fusionner `winscp_transfer` dans `shared_files_sftp` melangerait exposition serveur et workflow operatoire Windows.
- absorber `shared_sshfs_permanent` dans `reseau_ssh_step2` ferait disparaitre la frontiere entre baseline reseau et montage client.
- reclasser `shared` dans la lignee `reseau_ssh*` brouillerait la distinction entre transport et surface canonique de travail.
- chercher un survivant unique pour l'ensemble ferait perdre la separation utile par couche.

## Decision retenue
- oui a une suite fonctionnelle elargie `reseau / partage / transfert`
- non a une fusion physique dans ce lot
- baseline confirmee :
  - `reseau_ssh_step2` pour la lignee `reseau_ssh*`
  - `shared` pour la surface canonique
  - `shared_files_sftp`, `shared_sshfs_permanent`, `winscp_transfer` pour les modes d'acces specialises

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Carte P1 `reseau/share/transfer` complete. Basculer en `Step 05` pour les suites P2.

## RISKS

- À qualifier.
