---
doc_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: docs_trae
go_id: GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - trae
  - trae_pack_texts
  - docs
  - reclass
surface: chantier
source_kind: canonical
updated_at: 2026-04-24
links:
  - docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/02_journal_technique.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/architecture/REPO_SURFACES_MAP.md
---

# 03_decisions — GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01

## D1 — Statut canonique
- `docs/ot/trae/trae_pack_texts/` est un helper legacy
- ce helper n’est pas opposable face au repo canonique

## D2 — Emplacement retenu
- le pack ne doit plus vivre à la racine
- son emplacement documentaire normalisé est `docs/ot/trae/trae_pack_texts/`

## D3 — Règle de precedence
- `workflow_ai/`, le starter pack, le kanban, `docs/ot/*` et `registry/*` priment
- le pack Trae sert d’aide de lecture, de cadrage ou de continuité IDE uniquement

## D4 — Suite du lot
- relire et qualifier le contenu du pack
- geler ce qui reste utile comme support
- identifier les redondances qui peuvent être absorbées par la doc canonique

## D5 — Entrée vivante retenue
- l'entrée vivante du support legacy Trae devient `docs/ot/trae/trae_pack_texts/README.md`
- cette entrée porte la synthèse d'usage, l'articulation avec `workflow_ai`, `modules/validated_prompt_factory/` et `deploy_module_multi_machine/`, ainsi que la qualification fichier par fichier

## D6 — Statut du dossier `trae_pack/`
- `docs/ot/trae/trae_pack_texts/trae_pack/` est requalifié en archive de lecture
- les fichiers historiques restent à leur emplacement actuel pour préserver la compatibilité des références déjà publiées
- le contenu du dossier n'est plus opposable comme doctrine active

## D7 — Absorption canonique retenue
- la chaîne Orchestrator -> Executor -> Reviewer, les verdicts et les exigences de preuve/rollback sont absorbés dans `workflow_ai/WORKFLOW.md`
- le contrat de mission bornée est absorbé dans `docs/master_pack/mission_starter_pack/01_mission_template.md`
- l'articulation du quatuor Trae/IDE est absorbée dans `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` et `docs/ot/trae/README.md`

## D8 — Qualification fichier par fichier
| Fichier | Statut retenu | Valeur restante | Relai canonique retenu |
| --- | --- | --- | --- |
| `ETABLI_TRAE_SOCLE_CANONIQUE.txt` | archive de lecture | rappel historique compact du socle Trae | `docs/ot/trae/trae_pack_texts/README.md`, `workflow_ai/WORKFLOW.md` |
| `MISSION_INDEX_UPDATE_ORCHESTRATOR.txt` | archive de lecture | trace d'un patch documentaire historique | historique seulement |
| `MISSION_TRAE_ORCHESTRATOR_CANONIZATION.txt` | archive de lecture | trace d'un patch documentaire historique | historique seulement |
| `TRAE_CANONICAL_INDEX_V1.2.txt` | archive de lecture | index legacy supersédé | `docs/ot/trae/trae_pack_texts/README.md` |
| `TRAE_CANONICAL_INDEX_V1.3.txt` | archive de lecture | dernière version de l'index legacy du pack | `docs/ot/trae/trae_pack_texts/README.md` |
| `TRAE_CLOSURE_TEMPLATE_V1.1.txt` | archive de lecture | template legacy de clôture | `workflow_ai/WORKFLOW.md`, `docs/ot/closings/OT_*_CLOSING.txt` |
| `TRAE_DOCTRINE_CHAIN_V1.1.txt` | archive de lecture | formulation historique de la chaîne de responsabilité | `workflow_ai/WORKFLOW.md` |
| `TRAE_DRIVE_REFERENCE_PACK_V1.1.txt` | archive de lecture | rappel du cache/transport legacy Trae | `docs/ot/trae/trae_pack_texts/README.md` |
| `TRAE_DRIVE_REFERENCE_PACK_V1.txt` | archive de lecture | version supersédée du pack de référence | `docs/ot/trae/trae_pack_texts/README.md` |
| `TRAE_EXECUTION_REPORT_TEMPLATE_V1.1.txt` | archive de lecture | checklist legacy sur preuves et rollback | `workflow_ai/WORKFLOW.md` |
| `TRAE_MISSION_TEMPLATE_V1.1.txt` | archive de lecture | contrat mission bornée en format legacy | `docs/master_pack/mission_starter_pack/01_mission_template.md` |
| `TRAE_ORCHESTRATOR_ROLE_V1.1.txt` | archive de lecture | description détaillée du rôle Orchestrator | `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt`, `workflow_ai/WORKFLOW.md` |
| `TRAE_REVIEW_VERDICT_TEMPLATE_V1.1.txt` | archive de lecture | vocabulaire et structure legacy de review | `workflow_ai/WORKFLOW.md` |
| `TRAE_SESSION_OPENING_PACK_V1.1.txt` | archive de lecture | pack legacy d'ouverture de session | `docs/master_pack/mission_starter_pack/00_mission_start_guide.md` |
| `TRAE_STATUS_POLICY_V1.1.txt` | archive de lecture | définitions legacy des statuts | `workflow_ai/WORKFLOW.md` |

## D9 — Synthèse du quatuor Trae/IDE
- `workflow_ai/` : doctrine opposable d'exécution
- `modules/validated_prompt_factory/` : génération de prompts structurés à partir d'une synthèse valide
- `deploy_module_multi_machine/` : continuité et déploiement multi-machine validés
- `docs/ot/trae/trae_pack_texts/README.md` + `trae_pack/` : mémoire legacy de lecture et continuité IDE, sans dépendance runtime prouvée

## REPRISE
- point de reprise local : `docs/chantiers/GO_OPT_TRADING_TRAE_PACK_TEXTS_REVISION_01/02_journal_technique.md`
- suite logique : vérifier après push si le lot peut être clos comme réalignement doc-only
