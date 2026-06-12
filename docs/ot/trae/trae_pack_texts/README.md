# trae_pack_texts

## Statut retenu
- ce `README.md` est l'entree documentaire vivante du support Trae legacy
- `trae_pack/` est conserve comme archive de lecture pour compatibilite doc/IDE
- aucun fichier de `trae_pack/` n'est opposable face au canon repo-first

En cas de conflit, l'ordre de precedence reste :
1. `workflow_ai/WORKFLOW.md`
2. `docs/master_pack/mission_starter_pack/*`
3. `docs/ot/kanban/*` et `docs/ot/*`
4. `registry/*`
5. `docs/ot/trae/trae_pack_texts/trae_pack/*`

## Quatuor Trae/IDE
| Surface | Role retenu | Dependance / reference utile |
| --- | --- | --- |
| `workflow_ai/` | doctrine d'execution opposable | `workflow_ai/WORKFLOW.md` |
| `modules/validated_prompt_factory/` | generation de prompts structures a partir d'une synthese validee | `modules/validated_prompt_factory/README.md` |
| `deploy_module_multi_machine/` | continuite et deploiement multi-machine valides | `docs/deploy_module_multi_machine_continuity.md` |
| `docs/ot/trae/trae_pack_texts/` | memoire legacy Trae/IDE pour lecture et continuite | ce `README.md` + `trae_pack/` |

Constats prouvés :
- aucune dependance runtime directe de `workflow_ai`, `modules/validated_prompt_factory/` ou `deploy_module_multi_machine/` vers `trae_pack_texts/`
- les dependances observees vers `trae_pack_texts/` sont documentaires uniquement

## Qualification fichier par fichier
| Fichier | Statut retenu | Valeur restante | Relai canonique retenu |
| --- | --- | --- | --- |
| `ETABLI_TRAE_SOCLE_CANONIQUE.txt` | archive de lecture | rappel historique compact du socle Trae | ce `README.md`, `workflow_ai/WORKFLOW.md` |
| `MISSION_INDEX_UPDATE_ORCHESTRATOR.txt` | archive de lecture | trace d'un patch documentaire historique | historique seulement |
| `MISSION_TRAE_ORCHESTRATOR_CANONIZATION.txt` | archive de lecture | trace d'un patch documentaire historique | historique seulement |
| `TRAE_CANONICAL_INDEX_V1.2.txt` | archive de lecture | index legacy supersede | ce `README.md` |
| `TRAE_CANONICAL_INDEX_V1.3.txt` | archive de lecture | derniere version de l'index legacy du pack | ce `README.md` |
| `TRAE_CLOSURE_TEMPLATE_V1.1.txt` | archive de lecture | template legacy de cloture | `workflow_ai/WORKFLOW.md`, `docs/ot/closings/OT_*_CLOSING.txt` |
| `TRAE_DOCTRINE_CHAIN_V1.1.txt` | archive de lecture | formulation historique de la chaine de responsabilite | `workflow_ai/WORKFLOW.md` |
| `TRAE_DRIVE_REFERENCE_PACK_V1.1.txt` | archive de lecture | rappel du cache/transport legacy Trae | ce `README.md` |
| `TRAE_DRIVE_REFERENCE_PACK_V1.txt` | archive de lecture | version supersedee du pack de reference | ce `README.md` |
| `TRAE_EXECUTION_REPORT_TEMPLATE_V1.1.txt` | archive de lecture | checklist legacy sur preuves et rollback | `workflow_ai/WORKFLOW.md` |
| `TRAE_MISSION_TEMPLATE_V1.1.txt` | archive de lecture | contrat mission bornee en format legacy | `docs/master_pack/mission_starter_pack/01_mission_template.md` |
| `TRAE_ORCHESTRATOR_ROLE_V1.1.txt` | archive de lecture | description detaillee du role Orchestrator | `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt`, `workflow_ai/WORKFLOW.md` |
| `TRAE_REVIEW_VERDICT_TEMPLATE_V1.1.txt` | archive de lecture | vocabulaire et structure legacy de review | `workflow_ai/WORKFLOW.md` |
| `TRAE_SESSION_OPENING_PACK_V1.1.txt` | archive de lecture | pack legacy d'ouverture de session | `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` |
| `TRAE_STATUS_POLICY_V1.1.txt` | archive de lecture | definitions legacy des statuts | `workflow_ai/WORKFLOW.md` |

## Regles d'usage
- ouvrir ce dossier par ce `README.md`, pas par les anciens `.txt`
- ne pas reutiliser `trae_pack/*` comme templates vivants pour une nouvelle mission
- si une formulation legacy manque vraiment au canon, l'absorber dans une doc repo-native plutot que re-promouvoir le pack
- plusieurs chemins absolus presents dans `trae_pack/*` sont historiques et peuvent etre desormais stale apres la sortie de la racine

## RISKS

- À qualifier.
