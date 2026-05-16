---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_CLOSEOUT_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_CLOSEOUT_01
chantier_parent: GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01
status: draft
lifecycle_stage: closeout
surface: docs/chantiers
source_kind: canonical_child_closeout
updated_at: 2026-05-16
topic_keys:
  - why_lint
  - static_validator
  - refinement
  - closeout
  - warning_only
  - doc_ops
links:
  - https://github.com/magikgmo4-ui/opt-trading/pull/479
---

# GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_CLOSEOUT_01

## 1_MASTER_TARGET

Fermer le raffinement WHY lint apres adoption upstream, sans rouvrir le code ni elargir le scope au-dela du closeout documentaire.

## 3_INITIAL_NEED

Documenter l'etat final post-merge de `PR #479` pour figer les changements adoptes, les validations post-merge, les invariants de non-reouverture et le point de reprise futur.

## 6_FINAL_TARGET

**FINAL_TARGET: clore proprement le chantier de raffinement WHY lint par un closeout doc-only qui acte l'adoption de `PR #479`, confirme les validations post-merge et interdit toute reouverture implicite du validator, des tests, du README ou des index globaux.**

## 7_CANONICAL_STATE

Etat final confirme :

- `PR #479` : `MERGED`
- merge commit : `a726ec609b20429da7bfb4218fb9c46c07feb546`
- base : `sot/mainline`
- verdict final : `WHY lint refinement adopted`
- `git fetch origin` : `OK`
- `origin/sot/mainline` contient le merge commit `a726ec609b20429da7bfb4218fb9c46c07feb546`
- worktree isole utilise : `C:\Users\ghost\AppData\Local\Temp\opencode\w\repo`
- etat final du worktree isole : propre
- delta hors scope constate : aucun

## 8_VALIDATED_PLAN

- Conserver le resultat de `PR #479` comme etat canonique livre.
- Limiter ce GO a un closeout documentaire du raffinement WHY lint.
- Figer les validations post-merge sans requalifier ni rouvrir le validator.
- Enoncer explicitement les invariants de non-reouverture pour les futurs chantiers.

## 12_INVARIANTS

- Ne pas rouvrir `GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_01` sans nouveau finding explicite.
- Ne pas modifier le validator depuis ce closeout.
- Ne pas modifier les tests depuis ce closeout.
- Ne pas modifier `README` sans besoin explicite prouve.
- Ne pas elargir `STATIC_VALIDATOR` sans nouveau triage.
- Ne pas toucher aux index globaux depuis ce closeout.
- Ne pas creer de nouveau raffinement fonctionnel depuis ce closeout.

## 13_ESTABLISHED

Changements adoptes et etablis par `PR #479` :

- gating GO borne aux docs avec headings `H2` numerotes ;
- equivalent WHY pour `STATIC_VALIDATOR` via `1_MASTER_TARGET` et `3_INITIAL_NEED` ;
- champs interdits ignores dans les code fences Markdown ;
- `README` et doc chantier coherents avec le comportement livre.

Validations post-merge confirmees :

- le merge est present sur `origin/sot/mainline` ;
- le worktree isole de verification a ete laisse propre ;
- aucun delta hors scope n'a ete constate pendant la verification finale.

## 14_HYPOTHESIS

Risque residuel accepte : la tolerance `STATIC_VALIDATOR` reste volontairement bornee aux noms de fichiers contenant ce token.

Toute extension future de cette tolerance doit etre explicite, triee et traitee comme un nouveau besoin, pas comme une continuation implicite de ce closeout.

## 16_TODO

- Aucun `TODO` fonctionnel restant pour ce raffinement.
- Repartir de `origin/sot/mainline` pour tout futur chantier WHY lint.

## 17_RESUME_POINT

Etat de reprise :

```text
PR #479 MERGED / WHY lint refinement adopted
```

Condition de reprise future :

```text
Futur chantier WHY lint uniquement si nouveau finding ou nouveau besoin explicite.
```

## 18_VERDICT

```text
GO_OPT_TRADING_DOC_OPS_WHY_LINT_RULE_REFINEMENT_CLOSEOUT_01 PASS / DOC_ONLY_CLOSEOUT
```
