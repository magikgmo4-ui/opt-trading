---
doc_id: GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01_50_LIMITS
doc_type: chantier/limits_rollback
repo: opt-trading
branch: go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
machine: cursor-ai
status: active
lifecycle_stage: real_usage_test
links:
  - bundles/claude-artifacts/README.md
  - bundles/operator-export/EXPORT_MANIFEST.json
---

# 50_LIMITS_AND_ROLLBACK — Limites du test et plan de rollback

## Limites du test

### Ce que le test couvre

- Verification de la presence et de l'integrite des 6 artefacts du pack Claude artifacts.
- Validation que chaque artefact est lisible et utilisable par un operateur cursor-ai.
- Verification du flow handoff complet : reprise → pack → templates → checklists → merge → safety.
- Verification de la coherence entre le handoff (`operator-export/HANDOFF.md`) et le pack (`claude-artifacts/`).
- Verification des invariants (doc-only, no runtime, no secrets, no admin-trading).

### Ce que le test ne couvre PAS

- Execution runtime de trading (hors scope — doc-only).
- Test de merge reel d'une PR via `gh pr merge` (simulation uniquement — pas de PR a merger dans ce chantier).
- Test de push d'un commit avec secrets (par conception — no commit rules s'appliquent).
- Test de reprise depuis une conversation vierge (la conversation actuelle porte les artefacts).
- Performance ou scalabilite du pack (non pertinent pour un pack documentaire).
- Validation des PR #205 a #214 (elles sont mergees, hors scope du test).
- Ouverture d'admin-trading (ferme sans phrase d'activation).

### Perimetre strict

| Element | Dans le scope | Hors scope |
| --- | --- | --- |
| Fichiers `bundles/claude-artifacts/` | OUI — 6 fichiers | - |
| Fichiers `bundles/operator-export/` | OUI — references croisees | Modification |
| Chantiers existants | OUI — references documentaires | Modification |
| `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` | OUI — verification bloc CURSOR_AI | Modification |
| Fichiers runtime (`modules/`, `scripts/`, etc.) | NON | OUI — exclus |
| Admin-trading | NON | OUI — exclus |
| Secrets / .env | NON | OUI — exclus |
| PR #205 a #214 | NON | OUI — exclus (ne pas rouvrir) |

## Plan de rollback

### Cas 1 — Echec du test (verdict FAIL)

1. Documenter la raison du FAIL dans `90_CLOSEOUT.md`.
2. La branche `go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01` est conservee pour trace.
3. Aucun rollback de code necessaire (doc-only, pas de modification du runtime).
4. Le pack reste en l'etat ; le FAIL documente les corrections necessaires.

### Cas 2 — Contamination involontaire

Si des fichiers hors perimetre ont ete modifies :

```bash
git checkout sot/mainline -- <fichiers_hors_perimetre>
git commit -m "docs: rollback contamination dans GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01"
```

### Cas 3 — Branche inutilisable

```bash
git checkout sot/mainline
git branch -D go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
```

Puis recreer la branche proprement.

### Cas 4 — Suppression de la branche apres merge (si applicable)

```bash
git checkout sot/mainline
git pull --rebase origin sot/mainline
git branch -d go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
git push origin --delete go/GO_OPT_TRADING_CURSOR_AI_CLAUDE_ARTIFACTS_REAL_USAGE_TEST_01
```

## Evaluation du risque

| Risque | Probabilite | Impact | Mitigation |
| --- | --- | --- | --- |
| Modification involontaire de runtime | Faible | Haut | Verification pre-commit `git diff --cached --name-only \| grep -vE "^(docs/\|bundles/)"` |
| Inclusion de secret | Faible | Critique | Verification pre-commit `grep -iE "(password\|secret\|token..."` sur diff |
| Ouverture admin-trading | Nulle | Moyen | admin-trading explicitement ferme dans les invariants |
| Modification de chantiers existants | Nulle | Faible | Ce chantier cree de nouveaux fichiers uniquement |
| Reouverture PR #205-#214 | Nulle | Faible | Pas de merge, pas de rebase sur ces PR |

**Risque global** : TRES FAIBLE — operation doc-only, 0 fichier runtime touche, 0 secret, 0 admin-trading.
