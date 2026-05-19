---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: review_required
lifecycle_stage: child_cadrage
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-08
topic_keys:
  - ai_team
  - openclaw
  - db-layer
  - fantome
  - remote_exec
  - canonicalize
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/03_decisions.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_CLOSEOUT_01/CLOSEOUT_20260505.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/01_REMOTE_EXEC_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/02_REMOTE_EXEC_LOG.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01

## Classification

- type : child doc-only de canonisation
- statut : review_required
- parent : `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- machine source : `db-layer`
- cible distante : `fantome`

## But

Canoniser, dans un GO enfant explicite, une sequence AI team deja documentee d'execution distante `db-layer -> OpenClaw -> SSH -> fantome`, sans rouvrir le closeout OpenClaw `DB_LAYER` deja clos sur `sot/mainline`.

## 1_MASTER_TARGET

Sortir du parent AI_TEAM trois fichiers de preuve `109/110/111` restes non suivis, les rattacher a un child explicite, et preserver leur valeur documentaire sans promouvoir implicitement le parent vers une execution technique non canonisee.

## 2_INITIAL_PROJECT_DOC

Le present fichier ouvre le child de canonisation et fixe ses bornes :

- doc-only uniquement
- aucune relance runtime
- aucune action sur `admin-trading`
- aucune modification du closeout OpenClaw `DB_LAYER`
- preservation integrale de la preuve contenue dans le plan, le log et l'etat

## 3_INITIAL_NEED

Le parent `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` reste decrit comme un parent doc-only sans GO enfant d'execution explicite, alors que trois fichiers non suivis documentent deja une sequence reelle AI team a travers OpenClaw et SSH.

Il faut donc :

1. conserver cette preuve ;
2. la sortir du parent brut ;
3. la placer sous un GO enfant nomme ;
4. rendre l'entree visible dans `GO_INDEX.md` ;
5. ne pas confondre ce chantier avec le closeout OpenClaw `DB_LAYER` deja termine.

## 7_CANONICAL_STATE

- OpenClaw `DB_LAYER` est clos et indexe sur `sot/mainline`
- les fichiers `109/110/111` sont hors perimetre du closeout OpenClaw
- leur contenu releve du parent `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`
- la sequence documentee est applicative : `db-layer -> OpenClaw -> SSH -> fantome`
- le parent AI_TEAM ne doit pas porter implicitement ce niveau d'execution sans child dedie
- ce child sert de conteneur canonique minimal pour la phase `REVIEW_REQUIRED`

## ETABLI

- les fichiers sources non suivis existaient sous `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/`
- leur audit a conclu `REVIEW_REQUIRED` avec decision recommandee `MOVE`
- la couche OpenClaw concernee cote `DB_LAYER` est deja closee et ne doit pas etre modifiee par ce child

## HYPOTHESE

- le contenu repris ici pourra ensuite etre soit poursuivi comme child AI_TEAM autonome, soit absorbe dans une sequence AI_TEAM plus large avec closeout explicite

## Invariants

- ne pas relancer de runtime
- ne pas toucher `admin-trading`
- ne pas exposer WAN
- ne pas inventer d'etat Git
- ne pas rouvrir le closeout OpenClaw `DB_LAYER`
- ne pas perdre les preuves presentes dans `109/110/111`
- conserver le parent AI_TEAM conforme a son invariant : pas d'execution implicite sans GO enfant

## Decision retenue

- verdict d'audit : `REVIEW_REQUIRED`
- traitement : `MOVE`
- `DROP` refuse
- commit direct sous le parent refuse

## Perimetre

- ouverture du child canonique
- reprise des fichiers plan / log / state sous noms canoniques
- mise a jour minimale de `docs/index/GO_INDEX.md`

## Hors Perimetre

- runtime OpenClaw
- runtime AI team
- `admin-trading`
- `GO_CLOSED_INDEX.md`
- `BRANCH_STATE.md`

## NEXT_GO

Relecture du child canonique nouvellement pose, puis decision explicite entre :

1. poursuivre une phase AI_TEAM de remediation `identity + sandbox + SSH alias`, ou
2. archiver ce child comme preuve de tentative et garder le parent AI_TEAM au niveau documentaire.
