---
doc_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: ai_team_mvp
go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01
parent_go_id: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01
status: draft_for_review
lifecycle_stage: child_cadrage
surface: chantier
source_kind: canonical_draft
updated_at: 2026-05-09
topic_keys:
  - ai_team
  - openclaw
  - db-layer
  - fantome
  - remediation
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Section NEXT_GO"
links:
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01/03_REMOTE_EXEC_STATE.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md
---

# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01

## 1_MASTER_TARGET

Cadrer la remediation identity + sandbox + SSH alias pour le chemin d'execution remote `db-layer -> OpenClaw -> SSH -> fantome`, sans relancer le runtime avant gate explicite et sans rouvrir le closeout OpenClaw DB_LAYER.

## 2_INITIAL_PROJECT_DOC

Le present fichier ouvre le child de remediation Phase 6 apres merge de PR #259.

Le child canonique `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_CANONICALIZE_01` est mergé dans `sot/mainline`. Les preuves de la Phase 5 sont preservees. Il reste a decider et cadrer la Phase 6 de remediation avant toute relance runtime.

## 3_INITIAL_NEED

Apres merge de PR #259, le child remote exec est canonise. Les gaps identifies dans `03_REMOTE_EXEC_STATE.md` sont :

1. **Identity** : gateway et agent tournent sous `openclaw`, mais le chemin SSH operationnel est porte par `ghost`. Aucune identite d'execution unique n'est definie.
2. **Sandbox** : le sandbox agent OpenClaw ne rejoint pas `192.168.0.191:22`, alors que `ghost` y accede depuis le shell hote (`Connection refused`).
3. **SSH alias** : l'alias `fantome` est absent du `~/.ssh/config` courant sur `db-layer`.

Ces trois gaps doivent etre inventories et resolus avant toute nouvelle tentative d'execution remote.

## 4_MASTER_PLAN

1. Inventorier les gaps identity.
2. Inventorier les gaps sandbox.
3. Inventorier les gaps SSH alias.
4. Definir les gates PASS/FAIL pour chaque gap.
5. Produire un plan d'execution limite.

## 5_GO_PLAN

- GO_CHILD_01 : audit identity + proposition de chemin canonique (`openclaw direct SSH` ou `openclaw -> ghost wrapper`)
- GO_CHILD_02 : audit sandbox + test de contournement
- GO_CHILD_03 : restoration/canonisation de l'alias SSH `fantome`
- GO_CHILD_04 : rejeu controle du job OpenClaw Phase 5

## 6_FINAL_TARGET

Cadrer la remediation AI_TEAM db-layer/OpenClaw remote exec sur :
- identity
- sandbox
- SSH alias

## 7_CANONICAL_STATE

- PR #259 merged : `f8c98b8` (child canonique)
- merge commit : `445713e`
- OpenClaw DB_LAYER closeout preserve et non modifie
- parent AI_TEAM conserve son invariant doc-only

## 8_VALIDATED_PLAN

1. Valider ce cadrage.
2. Creer les fiches d'audit identity / sandbox / SSH alias.
3. Decider les gates avant toute relance runtime.
4. Produire closeout ou plan d'execution.

## 9_SELECTED_SOLUTION

Approche doc-first : auditer les trois gaps sans relancer le runtime, puis decider si la remediation justifie une execution reelle.

## 10_SELECTED_SETUP

- branche dediee : `go/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01`
- dossier : `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_DBLAYER_OPENCLAW_REMOTE_EXEC_REMEDIATION_01/`

## 11_KEY_DECISIONS

- Aucun runtime relance sans gate explicite
- Aucun WAN
- Aucun admin-trading
- Aucun bridge
- Aucun closeout OpenClaw DB_LAYER rouvert
- Le parent AI_TEAM conserve son invariant : pas d'execution implicite sans GO enfant

## 12_INVARIANTS

- Doc-first
- Aucun runtime relance sans gate explicite
- Aucun WAN
- Aucun admin-trading
- Aucun bridge
- Aucun closeout OpenClaw DB_LAYER rouvert
- Continuite parent d'abord dans docs/chantiers/
- Index globaux uniquement si instruction explicite ou changement global prouve

## 13_ETABLI

- Le child canonique est merge (PR #259)
- Les trois gaps sont documentes dans `03_REMOTE_EXEC_STATE.md`
- Les invariants du parent AI_TEAM sont respectes

## 14_HYPOTHESIS

- Une solution `openclaw -> sudo -n -u ghost -> ssh` peut suffire sans provisionner de cle SSH pour `openclaw`
- La restriction sandbox peut etre liee a un profil seccomp ou a un manque de capacite network dans le sandbox agent
- L'alias `fantome` peut etre restaure depuis les docs `reseau_ssh` ou recree avec l'IP documentee `192.168.0.191`

## 15_REMAINING_GAP

Les trois gaps identity / sandbox / SSH alias restent a auditer et resoudre. Aucune execution reelle n'a encore reussi via OpenClaw de bout en bout.

## 16_TODO

1. Inventorier les gaps identity.
2. Inventorier les gaps sandbox.
3. Inventorier les gaps SSH alias.
4. Definir les gates PASS/FAIL.
5. Produire un plan d'execution limite.

## 17_RESUME_POINT

Reprise depuis :
- PR #259 merged
- HEAD child source : `f8c98b8`
- merge commit : `445713e`
- NEXT_GO : ouvrir Phase 6 remediation doc-first

## 18_TO_DOCUMENT

TAGS :
- `CANONICAL_STATE`
- `ESTABLISHED`
- `REMAINING_GAP`
- `SELECTED_SOLUTION`
- `TODO`
- `RESUME_POINT`

## NEXT_GO

Creer les fiches d'audit pour les trois gaps (identity + sandbox + SSH alias), puis decider si remediation justifie une execution reelle.
