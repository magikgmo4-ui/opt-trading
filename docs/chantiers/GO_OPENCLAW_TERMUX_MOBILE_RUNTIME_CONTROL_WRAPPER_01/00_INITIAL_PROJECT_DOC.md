---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: openclaw_mobile_control
go_id: GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01
status: open
lifecycle_stage: opening
parent_go: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
surface: runtime
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-05-21
topic_keys:
  - openclaw
  - termux
  - mobile
  - runtime
  - wrapper
  - job_control
  - non_trading_automation
links:
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/20_TERMUX_OPENCLAW_ENTRYPOINTS.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/30_MOBILE_ALLOWED_ACTIONS_MATRIX.md
  - docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/40_PHASE01_MOBILE_CONTROL_DRY_RUN.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/80_PHASE_01_EXECUTION_PACKET.md
  - docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/82_PHASE_01_GATE_DECISION.md
---

# GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01

## 1_MASTER_TARGET

Deriver un wrapper runtime minimal `openclaw_mobile_control` permettant a Termux/mobile de consulter, preflight et declencher des jobs OpenClaw non-trading autorises, avec ledger/evidence et sans write externe libre.

## 2_INITIAL_PROJECT_DOC

Ce fichier est la fiche transporteur initiale du GO runtime. Il ouvre le chantier d'implementation du wrapper mobile-control, separe du GO doc-only `GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01` deja merge.

## 3_INITIAL_NEED

Le cadrage mobile est valide. Il faut maintenant deriver un wrapper executable borne, capable de :
- lire une phase/job autorisee ;
- verifier le gate mobile ;
- produire un preflight ;
- lancer uniquement les actions read-only/dry-run/local-only initiales ;
- produire evidence + ledger ;
- bloquer tout ce qui sort du perimetre.

## 4_MASTER_PROJECT_PLAN

1. Formaliser le contrat runtime du wrapper.
2. Definir le scope d'implementation initial.
3. Implementer un wrapper minimal local-only.
4. Tester sur Phase 01 mobile dry-run.
5. Produire evidence et closeout.

## 5_GO_PLAN

Livrables prevus :
- `00_INITIAL_PROJECT_DOC.md`
- `10_RUNTIME_SCOPE_AND_GATES.md`
- `20_WRAPPER_CONTRACT.md`
- `30_PHASE01B_IMPLEMENTATION_PLAN.md`
- `40_TEST_AND_EVIDENCE_PLAN.md`
- `BRANCH_STATE.md`

## 6_FINAL_TARGET

Un premier wrapper runtime borne et testable, sans activation scheduler, sans write externe, sans signal/trading, permettant d'executer un dry-run Phase 01 mobile-control et de produire les artefacts d'evidence attendus.

## 7_CANONICAL_STATE

- PR #685 est mergee et pose le cadrage mobile/Termux.
- Phase 01 non-trading est `PASS_WITH_FOLLOWUP`.
- Le follow-up utile reste le controle mobile et l'execution borneee des jobs Phase 01 read-only/dry-run/local-only.
- Le runtime doit deriver du registre et des phase packets, pas l'inverse.

## 8_VALIDATED_PLAN

Ce GO ouvre une branche runtime dediee mais le premier patch reste cadrage/contrat. L'implementation executable devra suivre le contrat et rester testable avant merge.

## 9_SELECTED_SOLUTION

Wrapper unique propose : `openclaw_mobile_control`.

Mode initial :
- `status`
- `list-jobs`
- `preflight`
- `run-dry`
- `evidence`

Les actions write-gated et external-app canary restent hors implementation initiale.

## 10_SELECTED_SETUP

- Branche : `go/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01`
- Parent : `GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01`
- Scope runtime futur : `scripts/ai/workers/openclaw_mobile_control.py`
- Evidence future : `reports/ai/mobile_control/`

## 11_KEY_DECISIONS

- Ne pas integrer de signal/trading.
- Ne pas integrer de write externe dans la premiere implementation.
- Ne pas integrer de scheduler activation dans ce GO.
- Ne pas contourner HITL.
- Ne pas promouvoir le mobile en source canonique.

## 12_INVARIANTS

- NON_TRADING_AUTOMATION_ONLY.
- Local-only/read-only/dry-run pour la premiere implementation.
- Evidence obligatoire par run.
- Ledger obligatoire ou fallback report si ledger indisponible.
- Fail ferme en `BLOCKED_WITH_REASON`.
- Aucun secret dans les rapports.

## 13_ESTABLISHED

- Le cadrage mobile est merge via PR #685.
- Le parent non-trading fournit les jobs et phase packets.
- Phase 01 fournit une base de test bornee.

## 14_HYPOTHESIS

- Un wrapper minimal peut couvrir Phase 01A sans besoin de scheduler.
- Le wrapper peut rester portable Termux/machine si les paths sont resolus depuis repo root.
- Le premier risque est le scope creep vers external write ou signal/trading.

## 15_REMAINING_GAP

- Implementer le wrapper.
- Ajouter tests locaux.
- Produire evidence Phase 01 dry-run.
- Decider si `strict-worker-readonly-smoke` E2E est inclus dans ce GO ou dans un sous-GO separe.

## 16_TODO

1. Verifier le contrat runtime.
2. Implementer le wrapper minimal.
3. Ajouter test/preflight.
4. Executer dry-run Phase 01.
5. Produire evidence.
6. Ouvrir PR de runtime implementation si ce patch d'ouverture est accepte.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`. Le but est d'implementer `openclaw_mobile_control` comme wrapper runtime borne pour Termux/mobile vers OpenClaw jobs non-trading, en commencant par Phase 01 read-only/dry-run/local-only.
