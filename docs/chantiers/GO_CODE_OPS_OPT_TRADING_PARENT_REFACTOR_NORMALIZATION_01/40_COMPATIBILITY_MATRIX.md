---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_COMPATIBILITY_MATRIX
doc_type: compatibility_matrix
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: design
topic_keys:
  - compatibility
  - windows
  - debian
  - wsl
  - tmux
  - github_actions
  - code_ops
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 40_COMPATIBILITY_MATRIX

## Objectif

Définir les contraintes de compatibilité avant refactor.

Un refactor est acceptable seulement s'il préserve les surfaces réellement utilisées.

## Surfaces à valider

| Surface | Risque typique | Validation attendue |
|---|---|---|
| Debian / Bash | chemins, permissions, venv, shebang | commandes Bash contrôlées |
| Windows / PowerShell | quoting, encodage, chemins longs | commandes PowerShell contrôlées |
| WSL | chemins `/mnt/c`, permissions, fin de ligne | smoke local |
| tmux | environnement non interactif, sessions | dry-run contrôlé |
| GitHub Actions | dépendances, working directory | workflow ou validation locale équivalente |
| Mobile / remote | consultation, pas forcément exécution | docs et outputs lisibles |
| JSON outputs | parsing strict | parse JSON strict |
| UTF-8 | accents et logs | lecture sans mojibake |
| path length | Windows long path | chemins courts si nécessaire |

## Matrice de compatibilité par fichier

| path | debian_bash | windows_pwsh | wsl | tmux | gha | json | utf8 | verdict |
|---|---|---|---|---|---|---|---|---|
| à remplir | unknown | unknown | unknown | unknown | unknown | unknown | unknown | PENDING |

## Critères de verdict

| Verdict | Sens |
|---|---|
| `PASS` | compatible sur surfaces déclarées |
| `PASS_WITH_LIMITS` | compatible sauf limite documentée |
| `REWORK` | refactor requis avant usage durable |
| `BLOCKED` | risque de casse ou manque preuve |
| `N/A` | surface non concernée |

## Points sensibles connus

- chemins Windows longs ;
- scripts Python appelés depuis PowerShell et Bash ;
- outputs JSON utilisés par validateurs ;
- runbooks Markdown contenant commandes ;
- sessions tmux et wrappers opératoires ;
- machines distinctes : `cursor-ai`, `admin-trading`, `db-layer`, `student`, `fantome`.

## Exigence pour chaque refactor batch

Chaque batch doit préciser :

- plateformes concernées ;
- plateformes non concernées ;
- commandes de validation ;
- sorties attendues ;
- limites connues ;
- rollback possible.

## Invariants

- Ne pas déclarer compatible sans test ou justification.
- Ne pas casser PowerShell en normalisant uniquement pour Bash.
- Ne pas casser Bash en normalisant uniquement pour PowerShell.
- Ne pas transformer un wrapper OS-spécifique en doublon à supprimer sans preuve.
- Ne pas mélanger compatibilité et performance.
