---
doc_id: GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: apps_orchestration
go_id: GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01
status: open
lifecycle_stage: validated_plan
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "17_RESUME_POINT - reprendre par le plan apps valide avant execution ClickUp"
updated_at: 2026-05-06
topic_keys:
  - opt-trading
  - apps
  - clickup
  - repo_kg
  - airtable
  - botpress
  - validated_plan
  - fantome
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/index/BRANCH_STATE.md
  - docs/index/GO_INDEX.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/INDEX.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/01_cadrage_parent.md
---

# GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Documenter le plan apps valide avant toute execution, afin de figer l'ordre logique d'utilisation des quatre branches apps retenues pour `opt-trading` : ClickUp, Repo KG, Airtable et Botpress.

Ce parent ne remplace aucun parent app existant. Il sert uniquement de couche de coordination documentaire et de point de reprise avant execution.

## 2_INITIAL_PROJECT_DOC

Le present fichier est le document transporteur initial du plan apps valide :

`docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md`

Statut :
- doc-only ;
- plan valide ;
- aucun runtime modifie ;
- aucune execution ClickUp/Airtable/Botpress/Repo KG dans ce lot ;
- parent de coordination documentaire avant demarrage operationnel.

## 3_INITIAL_NEED

Avant de demarrer l'execution du cockpit ClickUp ou des autres apps, figer proprement dans le repo le plan valide par l'utilisateur :

1. ClickUp : creer le cockpit de pilotage des GO.
2. Repo KG : produire une carte lisible du repo pour naviguer les chantiers.
3. Airtable : tester en cockpit data leger pour journal, backtests et signaux.
4. Botpress : brancher l'operateur conversationnel seulement apres surfaces cadrees.

## 4_MASTER_PROJECT_PLAN

Ordre apps valide :

| Ordre | App | Role retenu | Branche parent |
| --- | --- | --- | --- |
| 1 | ClickUp | Cockpit de pilotage GO / machines / branches / statuts / reprises | `go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01` |
| 2 | Repo KG | Cartographie visuelle repo-first / knowledge graph / navigation multi-angles | `go/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01` |
| 3 | Airtable | Cockpit data leger / journal / backtests / signaux / validation humaine | `go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01` |
| 4 | Botpress | Operateur conversationnel / routage Telegram / OpenClaw / trading labs | `go/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01` |

## 5_GO_PLAN

### GO 1 — ClickUp

But : creer le cockpit de pilotage initial des GO.

Livrables attendus :
- workspace / structure de pilotage ;
- statuts ;
- champs GO_ID, parent, machine, branche, doc path, PR/commit, validation, NEXT_GO, RESUME_POINT ;
- dashboard minimal ;
- import initial ou dry-run documente.

### GO 2 — Repo KG

But : rendre le repo navigable visuellement.

Livrables attendus :
- schema graph V1 ;
- Producer lecture seule ;
- `graph_bundle.json` ;
- vues GO, docs, modules, branches, machines, reprises, risques.

### GO 3 — Airtable

But : tester un cockpit data leger pour les usages operateur.

Livrables attendus :
- schema MVP journal/backtests/signaux ;
- verdict GO / NO_GO / GO_LIMITED ;
- strategie de sortie vers DB ou fichiers canoniques ;
- separation claire avec Google Sheets, LocalCMS et DB layer.

### GO 4 — Botpress

But : connecter l'operateur conversationnel une fois les surfaces precedentes cadrees.

Livrables attendus :
- intentions / workflows Botpress ;
- safety gate ;
- contrat API OpenClaw Gateway ;
- smoke Telegram -> Botpress -> surfaces trading -> retour Telegram ;
- zero trade reel automatique en V1.

## 6_FINAL_TARGET

Avoir une chaine apps progressive, gouvernee et repo-first :

```text
ClickUp pilote les GO
Repo KG cartographie le repo
Airtable journalise / structure les donnees legeres
Botpress orchestre la conversation apres stabilisation des surfaces
```

## 7_CANONICAL_STATE

Etat canonique courant :
- plan apps valide par l'utilisateur le 2026-05-06 ;
- quatre apps retenues : ClickUp, Repo KG, Airtable, Botpress ;
- aucun demarrage d'execution autorise avant documentation du plan ;
- ce parent documente l'ordre valide sans modifier les parents apps existants ;
- les branches apps restent proprietaires de leur execution respective ;
- `opt-trading` reste la source canonique.

NEXT_GO logique apres ce lot documentaire :
`GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01`.

## 8_VALIDATED_PLAN

Plan valide :
1. Documenter ce plan dans le repo.
2. Ne pas executer ClickUp avant documentation PASS.
3. Ne pas ouvrir Repo KG avant cockpit ClickUp initial ou decision explicite.
4. Ne pas tester Airtable avant cadrage des vues et donnees attendues.
5. Ne pas brancher Botpress avant surfaces amont stabilisees.

## 9_SELECTED_SOLUTION

Solution retenue :
- creer un parent documentaire de coordination ;
- garder les quatre parents apps separes ;
- utiliser ClickUp comme premiere app operationnelle ;
- utiliser Repo KG comme second levier de comprehension ;
- repousser Airtable et Botpress apres stabilisation des bases.

## 10_SELECTED_SETUP

Setup de documentation :
- branche dediee : `go/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01` ;
- dossier : `docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/` ;
- entree courte : `docs/index/inbox/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01.md` ;
- aucun runtime ;
- aucun fichier des parents apps modifie.

## 11_KEY_DECISIONS

- ClickUp passe en premier.
- Repo KG passe en second.
- Airtable passe en troisieme.
- Botpress passe en dernier.
- Le plan est valide avant execution.
- Les apps sont des couches d'usage, pas des sources canoniques.
- Le repo, les docs, les commits, les PR et l'etat Git reel restent les preuves.

## 12_INVARIANTS

- Ne pas remplacer `GO_INDEX.md`, `BRANCH_STATE.md`, `REPRISE.md` ou les docs parent par une app externe.
- Ne pas inventer de GO depuis ClickUp, Airtable, Botpress ou Repo KG.
- Ne pas traiter Repo KG comme source canonique.
- Ne pas traiter Airtable comme moteur trading live ou DB massive.
- Ne pas autoriser Botpress a trader, pousser Git ou modifier production automatiquement.
- Ne pas melanger les branches apps dans une meme execution technique.

## 13_ESTABLISHED

- ClickUp = cockpit de pilotage GO.
- Repo KG = carte / knowledge graph repo-first.
- Airtable = cockpit data leger et validation humaine potentielle.
- Botpress = operateur conversationnel apres stabilisation des surfaces.
- L'ordre valide est ClickUp -> Repo KG -> Airtable -> Botpress.

## 14_HYPOTHESIS

- ClickUp sera le meilleur premier levier de pilotage transverse.
- Repo KG reduira les pertes de contexte avant d'elargir les integrations.
- Airtable sera utile si son role reste leger et exportable.
- Botpress deviendra utile apres clarification des routes et contrats API.

## 15_REMAINING_GAP

- Documenter / verifier le closeout de ce parent de plan.
- Executer ClickUp seulement apres PASS de ce lot doc.
- Confirmer les mappings exacts d'import ClickUp depuis les index actuels.
- Definir le premier output minimum Repo KG apres ClickUp.
- Revalider Airtable contre Google Sheets / LocalCMS / DB layer.
- Reporter Botpress tant que les surfaces amont ne sont pas stables.

## 16_TODO

1. Committer ce parent doc-only.
2. Verifier que le dossier et l'entree inbox existent.
3. Produire un checkpoint/closeout minimal du plan valide.
4. Ensuite seulement ouvrir ou reprendre `GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01`.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
```

Puis executer :

```text
GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01
```

Ne pas passer a Repo KG, Airtable ou Botpress tant que ClickUp cockpit initial n'est pas PASS ou qu'une decision explicite ne change pas l'ordre.

## 18_TO_DOCUMENT

TAGS :
- `1_MASTER_TARGET`
- `4_MASTER_PROJECT_PLAN`
- `7_CANONICAL_STATE`
- `11_KEY_DECISIONS`
- `12_INVARIANTS`
- `16_TODO`
- `17_RESUME_POINT`

Blocs a extraire :
- `APPS_VALIDATED_PLAN_ORDER_01`
- `APPS_VALIDATED_PLAN_INVARIANTS_01`
- `APPS_VALIDATED_PLAN_REPRISE_01`

## 19_TO_REMEMBER

TAGS :
- `NO_MEMORY`

Bloc :
- `AUCUN_AJOUT_MEMOIRE_DURABLE_AUTOMATIQUE`

## RISKS

- À qualifier.
