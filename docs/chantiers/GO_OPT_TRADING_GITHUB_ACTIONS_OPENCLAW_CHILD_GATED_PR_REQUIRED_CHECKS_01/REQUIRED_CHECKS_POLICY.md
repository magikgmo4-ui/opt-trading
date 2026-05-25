---
doc_id: GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_CHILD_GATED_PR_REQUIRED_CHECKS_01_POLICY
doc_type: policy
---

# Required Checks Policy — `sot/mainline`

## Principe

Toute PR vers `sot/mainline` doit passer les 4 checks `gate/*` avant merge.
Ces checks constituent la gate d'entrée minimale pour garantir :

- La cible de la PR est correcte (`sot/mainline`)
- Un seul GO chantier est modifié
- Les fichiers modifiés respectent le FILE_SCOPE du GO
- Aucun overlap avec un autre GO actif
- Hygiene de diff (pas d'espaces parasites, etc.)

## Checks obligatoires

| Nom exact dans GitHub | Job YAML | Seuil |
|---|---|---|
| `gate/preflight` | `gate-preflight` | must pass |
| `gate/file-scope` | `gate-file-scope` | must pass |
| `gate/no-lock-overlap` | `gate-no-lock-overlap` | must pass |
| `gate/tests` | `gate-tests` | must pass |

## Comportement attendu

- Une PR qui échoue un check `gate/*` est bloquée (merge button désactivé)
- Une PR qui passe les 4 checks peut être mergée manuellement
- `workflow_dispatch` sur `sot/mainline` sans PR doit échouer sur `gate/preflight` (pas de contexte PR — normal)
- Les runs `push` sur `sot/mainline` (merges) peuvent inclure des fichiers multi-GO — `gate/file-scope` et `gate/no-lock-overlap` peuvent échouer sans bloquer (les merges bypassent les required checks)

## Interaction avec les autres règles

- Les required checks s'ajoutent aux éventuelles règles existantes (review approvals, etc.)
- Les runs `push` sur `sot/mainline` ne sont pas soumis aux required checks — seules les PR le sont
