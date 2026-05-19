---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01
parent_go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: opening
topic_keys:
  - why_lint
  - static_validator
  - doc_only
  - warning_only
  - read_only
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/100_LINT_REPORTING_ARCHITECTURE.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/110_LINT_CI_EXPERIMENT_PREPARATION.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md
---

# GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01

## 1_MASTER_TARGET

Specifier un validateur statique WHY lint strictement documentaire, warning-only et read-only.

Le livrable doit decrire le contrat attendu du validateur, ses entrees, ses sorties, son modele de warnings et ses limites, sans implementation runtime.

## 3_INITIAL_NEED

Le parent `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` a etabli le cadre WHY lint, mais pas encore le contrat operatoire minimal d'un validateur statique.

Il manque encore :

- les surfaces d'entree exactes du validateur,
- les sorties attendues pour revue humaine,
- le format minimal des warnings,
- les regles de non-action explicites,
- le point de passage entre cadrage documentaire et implementation future.

## 5_GO_PLAN

1. Reprendre le cadre parent deja publie.
2. Lister les entrees documentaires autorisees du validateur.
3. Definir les sorties attendues et leur granularite.
4. Poser le contrat minimal d'un warning WHY lint.
5. Poser les interdits permanents: runtime, auto-fix, CI bloquante, action autonome.
6. Laisser un handoff clair pour un futur chantier fixtures ou implementation.

## 6_FINAL_TARGET

Produire une specification enfant doc-only capable de cadrer un futur validateur statique WHY lint avec:

- des entrees documentaires explicites,
- des sorties machine-readable et reviewable humainement,
- un contrat warning-only,
- des invariants read-only permanents,
- aucun runtime, aucun auto-fix, aucune validation autonome.

## 7_CANONICAL_STATE

- La reprise du parent a ete publiee dans `140_CLOSEOUT.md` sur `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` puis poussee sur `origin`.
- Le parent reste la source canonique du cadre WHY lint.
- Ce child GO est ouvert comme specification documentaire seulement.
- Aucun index global n'est modifie dans ce passage.
- Aucune branche Claude/artifacts non classee n'est rouverte.
- Aucun code runtime n'est ajoute.

## 8_VALIDATED_PLAN

Plan valide pour ce child GO:

1. Reprendre les invariants du parent publie.
2. S'appuyer sur le warning model et le gate binding existants.
3. Definir les entrees autorisees du validateur comme surfaces documentaires en lecture seule.
4. Definir des sorties standard de revue sans execution autonome.
5. Definir un contrat de warning suffisamment precis pour un futur corpus de fixtures.
6. Reporter toute implementation executable dans un chantier separe.

## 12_INVARIANTS

- Doc-only.
- Warning-only.
- Read-only.
- Aucun runtime.
- Aucun auto-fix.
- Aucune CI bloquante.
- Aucune permission runtime implicite.
- Aucune ouverture vers MCP live.
- Aucun secret.
- Aucun trade.
- Aucun index global modifie dans ce passage.

## 13_ESTABLISHED

- Le parent a deja etabli 11 familles de warnings WHY lint.
- Le parent a deja etabli un binding warnings -> gates.
- Le parent a deja etabli des sorties candidates: `lint_report.json`, `lint_summary.md`, `lint_runtime_alignment.md`, `lint_warning_map.md`, `lint_review_gates.md`.
- Le parent a deja etabli qu'une CI future resterait experimentale et non bloquante.
- Le besoin restant n'est pas un nouveau cadre WHY lint, mais la specification du validateur statique associe.

## 14_HYPOTHESIS

- Un futur validateur pourra parser uniquement des surfaces documentaires explicitement whitelistees.
- Le contrat de warning pourra rester stable meme si l'implementation future change d'outil ou de langage.
- Un corpus de fixtures separe sera necessaire pour eviter de melanger specification et validation.
- Une branche enfant dediee pourra etre ouverte plus tard si le chantier quitte le simple cadrage documentaire.

## 15_REMAINING_GAP

- La liste canonique des entrees documentaires n'est pas encore figee.
- Le schema exact des sorties n'est pas encore defini.
- Le contrat minimal d'un warning unitaire n'est pas encore redige.
- Le corpus de fixtures n'est pas encore ouvert.
- Aucune implementation executable n'est encore cadree.

## 16_TODO

1. Definir les entrees whitelistees du validateur statique.
2. Definir le format minimal des sorties de rapport.
3. Definir le contrat d'un warning WHY lint unitaire.
4. Definir la place de la revue humaine dans la boucle de validation.
5. Ouvrir ensuite le child GO de corpus de fixtures si necessaire.
6. Reporter l'implementation executable a un chantier distinct.

## 17_RESUME_POINT

Reprendre depuis:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
```

Contexte parent immediat:

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
```

Point d'action suivant: figer le contrat entrees/sorties du validateur statique WHY lint sans ouvrir d'implementation runtime.
