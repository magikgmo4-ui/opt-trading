---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_mobile_control
go_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
lifecycle_stage: opening
parent_go: GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-05-21
topic_keys:
  - openclaw
  - termux
  - mobile
  - job_control
  - non_trading_automation
  - hitl
  - ledger
links:
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/10_NON_TRADING_JOBS_REGISTER.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/20_SCHEDULER_ROLLOUT_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/80_PHASE_01_EXECUTION_PACKET.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/82_PHASE_01_GATE_DECISION.md
---

# GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01

## 1_MASTER_TARGET

Cadrer Termux/mobile comme surface operateur OpenClaw pour consulter, declencher et valider des jobs `NON_TRADING_AUTOMATION_ONLY`, sans transformer le mobile en runtime libre ni en surface de write non controlee.

## 2_INITIAL_PROJECT_DOC

Le present document est la fiche transporteur initiale du GO. Il fige le perimetre, les invariants, les livrables attendus, les gaps et le point de reprise pour l'integration mobile/Termux avec OpenClaw et les jobs non-trading.

## 3_INITIAL_NEED

Besoin utilisateur : conserver l'objectif Termux/OpenClaw/jobs via mobile ou depuis une machine, tout en s'appuyant sur le socle recent du rollout non-trading : registre complet, Phase 01 `PASS_WITH_FOLLOWUP`, ledger, HITL, LocalCMS snapshot et gates.

## 4_MASTER_PROJECT_PLAN

1. Definir le scope mobile operateur.
2. Definir les entrypoints Termux/OpenClaw autorises.
3. Definir la matrice actions autorisees/interdites.
4. Preparer un dry-run Phase 01 mobile-control.
5. Garder le GO strictement doc-only avant toute implementation runtime.

## 5_GO_PLAN

Livrables du dossier :
- `00_INITIAL_PROJECT_DOC.md`
- `10_MOBILE_OPERATOR_SCOPE.md`
- `20_TERMUX_OPENCLAW_ENTRYPOINTS.md`
- `30_MOBILE_ALLOWED_ACTIONS_MATRIX.md`
- `40_PHASE01_MOBILE_CONTROL_DRY_RUN.md`
- `BRANCH_STATE.md`

## 6_FINAL_TARGET

Obtenir un cadrage exploitable pour qu'un operateur mobile puisse consulter l'etat OpenClaw/non-trading, declencher des jobs read-only/dry-run/local-only, consulter les preuves ledger/report/LocalCMS, et effectuer une validation humaine lorsque le gate le demande.

## 7_CANONICAL_STATE

- PR #678 a livre les preuves d'automation gaps G01-G12.
- PR #676 a recanonise le parent non-trading en doc-only et separe le runtime.
- PR #680 est le point de reprise immediat : registre complet, Phase 01 documentee, Phase 01 gate `PASS_WITH_FOLLOWUP`.
- Phase 01 contient 12 jobs read-only/dry-run/local-only, avec 11 PASS, 1 PRECHECK_PASS, 0 FAIL.
- Le follow-up ouvert reste `strict-worker-readonly-smoke` en execution modele end-to-end.

## 8_VALIDATED_PLAN

Ce GO ne change pas les abonnements, ne change pas le runtime, ne change pas les jobs trading et ne modifie aucun index global. Il pose uniquement la politique mobile/Termux pour OpenClaw job control.

## 9_SELECTED_SOLUTION

Solution retenue : Termux/mobile = surface operateur bornee. OpenClaw reste l'orchestrateur. Le registre non-trading et les phase packets restent la source de selection des jobs. Le mobile ne devient ni source canonique, ni executor autonome, ni surface de write externe.

## 10_SELECTED_SETUP

- Machine possible : mobile Termux, db-layer, admin-trading ou autre machine autorisee.
- Mode initial : doc-only / dry-run.
- Entry command future : wrapper OpenClaw mobile-control a definir.
- Evidence obligatoire : ledger + report + LocalCMS snapshot quand applicable.

## 11_KEY_DECISIONS

- Mobile peut consulter et declencher des jobs A1/read-only/dry-run/local-only.
- Mobile peut participer a HITL comme validation humaine, mais pas contourner HITL.
- Mobile ne peut pas declencher d'action destructive, de write externe libre ou de signal/trading live.
- Signal/trading reste hors scope de ce GO.

## 12_INVARIANTS

- NON_TRADING_AUTOMATION_ONLY uniquement.
- Aucun live trading.
- Aucun write externe libre.
- Aucun secret ou credential dans les prompts ou rapports.
- Aucune operation Git destructive depuis mobile.
- Toute action doit produire une preuve.
- Tout job orchestre doit pouvoir etre relu depuis le ledger ou un rapport.
- LocalCMS est cockpit/snapshot, pas source canonique.

## 13_ESTABLISHED

- Le socle non-trading existe dans le repo.
- Phase 01 est documentee comme `PASS_WITH_FOLLOWUP`.
- `localcms_automation_status_sync.py` existe comme runner local-only.
- Le registre non-trading liste 114 jobs affectes a phases.

## 14_HYPOTHESIS

- Termux peut devenir une surface de controle efficace si les commandes restent wrapperisees et non destructives.
- OpenClaw peut servir de routeur unique entre mobile, machines, phase packets, ledger et LocalCMS.
- Le premier test utile est un dry-run de consultation/declenchement Phase 01 depuis mobile.

## 15_REMAINING_GAP

- Definir les entrypoints mobiles exacts.
- Definir le format de commande OpenClaw mobile-control.
- Definir les outputs attendus cote mobile.
- Definir le premier dry-run mobile sur Phase 01A/01B.
- Verifier si PR #680 doit etre mergee avant implementation runtime.

## 16_TODO

1. Rediger le scope mobile operateur.
2. Rediger les entrypoints Termux/OpenClaw.
3. Rediger la matrice actions autorisees/interdites.
4. Rediger le dry-run Phase 01 mobile-control.
5. Revoir/merger ce GO doc-only avant implementation.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`. Le but n'est pas le cout IA, mais l'orchestration : Termux/mobile doit devenir une surface operateur OpenClaw bornee pour jobs non-trading, avec evidence ledger/report/LocalCMS et gates HITL.
