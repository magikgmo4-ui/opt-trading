# GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_MAINLINE_AUDIT_01

## Objectif

Lancer une boucle semi-auto réelle contrôlée sur `sot/mainline` après les merges récents (#922, #924, #875, #923, #925). Produire preuve JSON + Markdown. Aucune mutation.

## Parent GO

`GO_AUTOMATION_OPS_OPT_TRADING_PARENT_SEMIAUTO_RUNTIME_PILOT_01`

## Contexte

| PR | Contenu | État |
|----|---------|------|
| #922 | Pilote semi-auto runtime v1 | MERGED |
| #924 | Premier run réel pilote semi-auto | MERGED |
| #875 | Android Termux/Tasker runtime proof | MERGED |
| #923 | GitHub Actions openclaw gated PR scope bypass | MERGED |
| #925 | Mimo open observer state clarification | MERGED |

`sot/mainline` est en état post-merge propre. Aucune PR ouverte.

## Contraintes

- Pas de merge.
- Pas de fermeture de PR.
- Pas de modification de workflows.
- `secrets/` non touché.
- `human_gate_required: true`.
- Mode `dry_run` uniquement.

## Livrables

```
docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_MAINLINE_AUDIT_01/
  00_INITIAL_PROJECT_DOC.md
  10_AUDIT_SCOPE.md
  20_RUN_REPORT.md
  30_PROOF_INDEX.md
  40_GAPS_AND_NEXT_GO.md

artifacts/automation_ops/semiauto_pilot/pilot_0e1e6443/
  proof.json
  proof_summary.md
```
