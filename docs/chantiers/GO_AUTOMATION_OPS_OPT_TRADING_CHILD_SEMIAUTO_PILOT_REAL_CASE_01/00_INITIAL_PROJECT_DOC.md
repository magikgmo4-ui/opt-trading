# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01

## Objectif

Utiliser le pilote semi-auto runtime v1 sur un cas réel borné, non destructif et vérifiable.

## Parent GO

`GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01`

## Contexte

`GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_SCOPE_01` est mergé (PR #922). Le runner
`scripts/automation_ops/run_semiauto_pilot.sh` et le module `modules/automation_ops/semiauto_pilot/`
sont opérationnels avec 17/17 tests PASS.

Ce child GO constitue le **premier run réel** du pilote sur un cas d'audit doc-only / état repo.

## Cas réel choisi

Audit de l'état courant :
- PRs ouvertes sur `sot/mainline`
- Chantiers sans `90_CLOSEOUT.md`

Aucune mutation. Lecture seule. Gate humain obligatoire.

## Contraintes

- Pas de merge automatique.
- Pas de modification de workflows.
- Pas de suppression de fichiers.
- `secrets/` non touché.
- `human_gate_required: true`.
- Mode `dry_run` uniquement.

## Livrables

```
docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_PILOT_REAL_CASE_01/
  00_INITIAL_PROJECT_DOC.md
  10_REAL_CASE_SCOPE.md
  20_RUN_REPORT.md
  30_PROOF_INDEX.md
  40_GAPS_AND_NEXT_GO.md

artifacts/automation_ops/semiauto_pilot/pilot_b4812d88/
  proof.json
  proof_summary.md
```
