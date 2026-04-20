# GO_GIT_BRANCH_DROP_SAFE_ABSORBED_01 - decisions

## Decisions

| branche | presence locale | presence remote | merge dans `origin/sot/mainline` | action locale recommandee | action remote recommandee |
| --- | --- | --- | --- | --- | --- |
| `feat/GO_OPT_TRADING_GO_INDEX_CLOSED_ENTRIES_CANON_01` | non | oui | oui | aucune | suppression remote candidate |
| `feat/project-card-deskpro-01` | non | oui | oui | aucune | suppression remote candidate |
| `feat/reseau-ssh-consolidation-lot2-freeze-01` | non | oui | oui | aucune | suppression remote candidate |
| `feat/reseau-ssh-consolidation-lot3-minimal-01` | non | oui | oui | aucune | suppression remote candidate |
| `feat/student-validation-bitget-readonly-01` | oui | oui | oui | differee, worktree actif | suppression remote candidate |
| `feat/workflow-post-change-consolidation-03` | non | oui | oui | aucune | suppression remote candidate |
| `fix/collectors-lifecycle-compat-relref-01b` | non | oui | oui | aucune | suppression remote candidate |

## Preuves

- **Branches distantes presentes** : les sept refs `origin/*` du lot ont ete observees dans le repo reel
- **Branches deja absorbees** : chacune ressort merged dans `origin/sot/mainline`
- **Aucune suppression locale dans ce passage** : le lot d'execution est borne aux suppressions remote puis au `fetch --prune`
- **Blocage local explicite** : `feat/student-validation-bitget-readonly-01` reste differee en local, car montee dans le worktree `/tmp/opt-trading-consolidate-validated-extracts-01`
- **Hors perimetre explicite** : `backup/main-before-filter` n'entre pas dans ce GO

## Commandes ciblees

```bash
git push origin --delete feat/GO_OPT_TRADING_GO_INDEX_CLOSED_ENTRIES_CANON_01 feat/project-card-deskpro-01 feat/reseau-ssh-consolidation-lot2-freeze-01 feat/reseau-ssh-consolidation-lot3-minimal-01 feat/student-validation-bitget-readonly-01 feat/workflow-post-change-consolidation-03 fix/collectors-lifecycle-compat-relref-01b
git fetch origin --prune
git branch -r | grep -E 'origin/(feat/GO_OPT_TRADING_GO_INDEX_CLOSED_ENTRIES_CANON_01|feat/project-card-deskpro-01|feat/reseau-ssh-consolidation-lot2-freeze-01|feat/reseau-ssh-consolidation-lot3-minimal-01|feat/student-validation-bitget-readonly-01|feat/workflow-post-change-consolidation-03|fix/collectors-lifecycle-compat-relref-01b)$' || true
```

## Garde

- ne faire aucune suppression locale dans ce passage
- ne pas tenter de supprimer localement `feat/student-validation-bitget-readonly-01` tant que le worktree `/tmp/opt-trading-consolidate-validated-extracts-01` existe
- ne pas melanger ce GO avec `backup/main-before-filter`
