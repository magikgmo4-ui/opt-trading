---
doc_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01_SEMIAUTO_RUN_REPORT
doc_type: semiauto_run_report
go_id: GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01
run_id: pilot_808f90b9
verdict: PASS_DRY_RUN
status: GATE_HUMAIN_REQUIS
created_at: 2026-05-30
---

# 20_SEMIAUTO_RUN_REPORT

## 1_VERDICT_RUN

```
run_id  : pilot_808f90b9
verdict : PASS_DRY_RUN
mode    : dry_run
gate    : human_gate_required = true
proof   : artifacts/automation_ops/semiauto_pilot/pilot_808f90b9/proof.json
```

## 2_ACTIONS_EXÉCUTÉES

| Action planifiée | Exécutée | Note |
|-----------------|:--------:|------|
| Lire go_prompt.json | oui | handoff contract validé |
| Valider handoff contract | oui | PASS |
| Vérifier stop conditions | oui | aucune stop condition active |
| Lire 10_STRATEGY_SPEC_SMC_ICT_CHOCH_BOS_RETEST.md | non | gap G02 — délégation opérateur |
| Lire 50_OBSERVATION_EVENT_MAPPING.md | non | gap G02 |
| Lire 60_SCORING_INITIAL.md | non | gap G02 |
| Produire résumé activation | non | gap G02 — fait par opérateur (30_ACTIVATION_SUMMARY.md) |
| Écrire proof artifacts | oui | pilot_808f90b9/proof.json + proof_summary.md |
| Soumettre au gate humain | oui | ce document |

> Gap G02 (REAL_CASE_01) confirmé comme pour les pilots précédents :
> le pilot_runner valide le contrat et arrête — les actions de lecture/analyse
> sont réalisées par l'opérateur et documentées dans 30_ACTIVATION_SUMMARY.md.

## 3_PHASE1_GATE

```
date_gate               : 2026-05-30  ✓
runs_actual             : 248         ✓ (≥30)
days_elapsed            : 14          ✓ (≥14)
fail_count              : 7           EXCEPTION acceptée (infra transients 2026-05-26)
operator_verdict        : PASS_WITH_INFRA_EXCEPTION
```

## 4_HANDOFF_CONTRACT

```json
{
  "run_id": "pilot_808f90b9",
  "go_id": "GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01",
  "parent_go_id": "GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01",
  "mode": "dry_run",
  "input_prompt_path": "docs/chantiers/GO_STRATEGY_SMC_ICT_CHILD_LIVE_OBSERVATION_01/go_prompt.json",
  "human_gate_required": true,
  "verdict": "PASS_DRY_RUN"
}
```

## 5_GATE_HUMAIN — DÉCISION_REQUISE

| # | Question | Décision opérateur |
|---|----------|--------------------|
| H1 | Activer SMC_ICT_CHOCH_BOS_RETEST CANDIDATE → ACTIVE_PAPER ? | **OUI** |
| H2 | Fenêtre observation : 14 jours à partir de 2026-05-30 ? | **OUI** |
| H3 | Télégram watch signal activé (confidence ≥ 0.60) ? | Décision opérateur |
| H4 | Modifier 95_STRATEGY_REGISTRY.md (seule mutation autorisée) ? | Décision opérateur |
