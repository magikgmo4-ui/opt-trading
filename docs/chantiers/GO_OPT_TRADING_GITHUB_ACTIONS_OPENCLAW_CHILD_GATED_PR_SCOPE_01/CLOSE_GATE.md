# CLOSE_GATE

## Gate de fermeture child

Ce GO est fermable si :

- `.github/workflows/gated-pr.yml` existe;
- `gate/preflight` existe;
- `gate/file-scope` existe;
- `gate/no-lock-overlap` existe;
- `gate/tests` existe;
- `FILE_SCOPE.txt` existe pour ce GO;
- la documentation branch protection existe.

## Hors scope

- Activation manuelle des required checks côté GitHub.
- Orchestration OpenClaw opérationnelle.
- Self-hosted runner.
