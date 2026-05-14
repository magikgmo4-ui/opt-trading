# PATCH_DRAFT — GO_STRICT_WORKERS_PATCH_DRAFT_IMPL_01
## WORKER: glm-5.1 (VERIFIED, A2)
## STATUT: DRAFT_ONLY

---

## OBJECTIF_PATCH

Ajouter une section `## Historique commits` dans le `BRANCH_STATE.md` du child runtime, listant les commits de la branche depuis sa creation. Le parent `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` dispose deja d'une section `COMMITS_CLES` dans son `90_CLOSEOUT.md` ; le child gagnerait a tracer son propre historique de branche pour la reprise et la continuite.

## FICHIERS_TOUCHES

| Fichier | Action |
| --- | --- |
| `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/BRANCH_STATE.md` | Ajout section `## Historique commits` apres `## Invariants Git` |

## FICHIERS_LUS

- `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/BRANCH_STATE.md` (78 lignes)
- `docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_PARENT_01/BRANCH_STATE.md` (reference de structure)

## DIFF_ATTENDU

```diff
--- a/docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/BRANCH_STATE.md
+++ b/docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01/BRANCH_STATE.md
@@ -75,4 +75,19 @@
 - pas de modification des index globaux
 - pas de PATCH_DRAFT sans validation externe
 - stash branch_arbitration preserve
+
+## Historique commits
+
+| SHA | Message |
+| --- | --- |
+| `9f1b675` | docs: open child GO — strict workers runtime lock and E2E (cadrage) |
+| `73ace3e` | docs: add strict workers runner lock — run_task.sh (Phase A) |
+| `92fc570` | fix: correct REPO_ROOT path in run_task.sh |
+| `b459417` | fix: safe REPO_ROOT resolution in run_task.sh |
+| `f63b678` | fix: rewrite run_task.sh with separate python validator |
+| `ee7b7ce` | fix: relative path matching for allowed_outputs in validator |
+| `39c2553` | fix: pipe heredoc conflict — use temp file for validation JSON |
+| `0299e96` | docs: Phase A PASS — runner lock operational, validation report |
+| `b3d13d5` | docs: add PATCH_DRAFT job packet for Phase B |
+
+_9 commits, du plus ancien (cadrage) au plus recent (job packet Phase B)._
```

## RISQUES

| Risque | Niveau | Mitigation |
| --- | --- | --- |
| La liste de commits devient obsolete | Faible | Mise a jour lors de chaque phase (A/B/C/D) |
| SHA de commit change apres rebase | Faible | La branche est en `--no-ff`, pas de rebase prevu |
| Doublon avec le log git | Nul | Cette section est une trace documentaire, pas un remplacement de `git log` |
| Aucun risque secret/security | Nul | Aucun chemin sensible dans les messages de commit |

## TESTS_A_EXECUTER

1. Appliquer le patch sur une copie de travail
2. Verifier que la section `## Historique commits` apparait apres `## Invariants Git`
3. Verifier que le nombre de commits correspond a `git log --oneline origin/sot/mainline..HEAD | wc -l`
4. Verifier que les SHA sont corrects (comparer avec `git log --oneline --format="%h %s"`)
5. Verifier que le markdown est valide (tableau bien forme)
6. Verifier que `git diff` ne montre aucun autre fichier modifie

## ETAT_GIT_AVANT/APRES

- **AVANT** : `git status --short` = vide (clean)
- **APRES** : `git status --short` = vide (patch non applique, aucun fichier modifie)
- **Aucune commande git d'ecriture executee**
- **Aucun fichier source modifie**

## VERDICT_DRAFT_ONLY

```text
PATCH_DRAFT_VALID — patch propose, non applique.

Le patch est borne a 1 fichier, 15 lignes ajoutees, 0 ligne supprimee.
Aucun secret, aucun .env, aucun token.
Aucune commande git d'ecriture executee.
Aucun runtime modifie.
Validation externe requise avant application.
```
