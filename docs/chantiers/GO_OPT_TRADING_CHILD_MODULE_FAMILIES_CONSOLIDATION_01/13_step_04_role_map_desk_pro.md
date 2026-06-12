---
doc_id: GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01_STEP_04_DESK_PRO_ROLE_MAP
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
  - desk-pro
  - role-map
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_CHILD_MODULE_FAMILIES_CONSOLIDATION_01/03_plan_operationnel_step_by_step.md
  - docs/status/desk_pro_stack_canonique.md
  - docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md
  - docs/ot/project_cards/PROJECT_CARD_DESKPRO_01.md
  - docs/desk_pro_multi_machine_map.md
  - docs/admin_trading_desk_pro_runbook.md
  - scripts/admin_trading/desk_pro_cmd.sh
  - modules/desk_pro/README.md
  - modules/desk_common/README.md
  - modules/desk_pro_runner/README.md
  - modules/desk_pro_orchestrator/README.md
  - modules/desk_pro_dashboard/README.md
  - modules/desk_snapshot_ingest/README.md
  - modules/desk_capture_inputs/README.md
  - modules/desk_analyze/README.md
  - modules/desk_state/README.md
  - modules/desk_retention/README.md
---

# Step 04 - role map `Desk Pro`

## Statut
Complete.

## Objet
Produire une carte de role exploitable de la suite `Desk Pro`, avec frontieres explicites entre coeur produit, facade operatoire, pipeline, visualisation et satellites adjacents.

## Verifications utilisees
- lecture de `docs/status/desk_pro_stack_canonique.md`
- lecture de `docs/governance/DESK_PRO_CANONICAL_PRODUCT_SYNTH_01.md`
- lecture de `docs/ot/project_cards/PROJECT_CARD_DESKPRO_01.md`
- lecture de `docs/desk_pro_multi_machine_map.md`
- lecture de `docs/admin_trading_desk_pro_runbook.md`
- lecture de `scripts/admin_trading/desk_pro_cmd.sh`
- lecture des README de :
  - `modules/desk_pro`
  - `modules/desk_common`
  - `modules/desk_pro_runner`
  - `modules/desk_pro_orchestrator`
  - `modules/desk_pro_dashboard`
  - `modules/desk_snapshot_ingest`
  - `modules/desk_capture_inputs`
  - `modules/desk_analyze`
  - `modules/desk_state`
  - `modules/desk_retention`

## Hierarchie d'entrypoints
| Niveau | Surface | Entree retenue | Role |
|---|---|---|---|
| session operateur | ops hub | `menu-ops_menu_hub` | point d'entree unique de session |
| admin / debug | admin-trading | `scripts/admin_trading/desk_pro_cmd.sh` | wrapper operatoire reel, avec helpers admin |
| backend direct | module | `cmd-desk_pro_runner` | facade CLI directe vers le runner |
| compat legacy | shell scripts | `scripts/desk_pro_*.sh` | compatibilite seulement, ne pas promouvoir |

## Carte de role
| Composant | Statut | Role retenu | Frontiere |
|---|---|---|---|
| `desk_pro` | actif | coeur partage API / UI / service | porte la logique commune, pas la facade operateur |
| `desk_pro_runner` | actif | facade operatoire module | enrobe orchestrateur et dashboard pour la CLI |
| `desk_pro_orchestrator` | actif | pipeline d'execution | produit les runs et les resumes de run |
| `desk_pro_dashboard` | actif | visualisation / export | consomme les runs et rend JSON / HTML |
| `desk_common` | actif | support shared minimal | chemins et wrappers generiques, pas de logique produit |

## Satellites adjacents
| Composant | Role retenu |
|---|---|
| `desk_snapshot_ingest` | ingestion d'entrees ou snapshots |
| `desk_capture_inputs` | capture des intrants operatoires |
| `desk_analyze` | analyse adjacente a la stack |
| `desk_state` | etat ou persistence adjacente |
| `desk_retention` | retention / hygiene des sorties |

Ces satellites restent dans la suite `desk_*`, mais ne sont pas promus coeur minimal de `Desk Pro`.

## Points de duplication ou d'ambiguite
- `scripts/admin_trading/desk_pro_cmd.sh` et `cmd-desk_pro_runner` se recouvrent partiellement, mais le wrapper admin ajoute des helpers operatoires que le runner n'expose pas.
- `desk_pro` et `desk_common` sont proches dans la lecture de surface, mais leur frontiere doit rester nette :
  - `desk_pro` porte la logique produit
  - `desk_common` porte seulement le support shared minimal
- `desk_pro_dashboard` produit des exports, mais la publication inter-machines passe ensuite par le wrapper admin vers `/shared`.
- la stack utilise a la fois des chemins runtime locaux `desk/*` et des sorties data `data/desk_runs/` / `data/dashboard/`, ce qui interdit une fusion rapide sans contrat de chemins explicite.

## Risques de consolidation
- promouvoir `desk_pro_runner` comme unique verite runtime effacerait le role reel du wrapper admin et de l'ops hub.
- fusionner trop vite les satellites dans `desk_pro` rendrait la stack moins lisible sans preuve que leurs cycles de vie sont alignes.
- rabattre `desk_common` dans `desk_pro` sans contrat clair de support ferait disparaitre une frontiere utile entre socle shared et logique produit.
- confondre export dashboard et diffusion `/shared` melangerait rendu local et flux multi-machines.

## Decision retenue
- suite `Desk Pro` confirmee comme stack multi-composants
- aucun survivant unique nouveau
- frontieres P1 fixees entre :
  - coeur produit `desk_pro`
  - facade operatoire `desk_pro_runner`
  - pipeline `desk_pro_orchestrator`
  - rendu `desk_pro_dashboard`
  - support minimal `desk_common`
- aucun move physique autorise dans ce lot

## Rollback
- revert doc-only de cette note
- revert doc-only du plan si besoin

## Point de reprise
Carte P1 `Desk Pro` complete. Poursuivre avec les cartes `DeepSeek/student` et `reseau/share/transfer`, puis basculer en `Step 05`.

## RISKS

- À qualifier.
