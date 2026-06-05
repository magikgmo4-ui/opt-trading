---
doc_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01_SPEC
doc_type: chantier_parent_spec
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01
status: draft
lifecycle_stage: reprise
topic_keys:
  - why_lint
  - consolidation
  - governance
  - runtime_security
  - why_runtime_graph
  - openclaw_central
  - warning_only
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01/00_INITIAL_PROJECT_DOC.md
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/00_CONSOLIDATION_MAP_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/03_EXISTING_SOURCE_MANIFEST_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/04_DEPENDENCY_GRAPH_4_AXES_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/05_WHY_LINT_WARNING_MODEL_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/06_CROSS_AXIS_GATE_BINDING_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/07_AXIS_IMPLEMENTATION_ROADMAP_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/140_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/150_BRANCH_DISPOSITION_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_CHILD_WHY_LINT_STATIC_VALIDATOR_SPEC_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_IMPLEMENTATION_READONLY_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_SPEC_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REPORT_V1_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_TRIAGE_V1_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md
  - docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md
---

# SPEC_WHY_LINT_EXPERIMENT_01

## 1_MASTER_TARGET

Consolider les 4 axes documentaires de controle (Gouvernance, WHY/runtime graph, Runtime Security, WHY lint) + la cible produit OpenClaw central en un chantier parent unique, sans doublons, contradictions ni autorisations implicites.

Le WHY lint est la couche warning-only de detection de contradictions entre ces axes. Il n'autorise aucune action, ne bloque pas la CI, n'applique aucun correctif automatique.

## 2_INITIAL_PROJECT_DOC

Document transporteur principal du chantier :

`docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md`

Ce document fige le cadrage parent, separe le chantier de la session conversationnelle et sert de reference de reprise locale.

## 3_INITIAL_NEED

Le systeme `opt-trading` a vu emerger plusieurs axes documentaires de controle :

- La gouvernance (MATRICE_DOC_OPS_MASTER_MATRIX_01) fixe les regles stables.
- Le WHY/runtime graph rend le systeme explicable.
- La securite runtime (GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01) pose les garde-fous d'execution.
- OpenClaw central est la cible produit operationnelle.

Ces axes risquent de devenir des verites concurrentes si leurs frontieres ne sont pas explicitement consolidees.

Besoin initial : poser un cadre de consolidation qui evite que les sessions Gouvernance, WHY, WHY lint et OpenClaw central deviennent des verites concurrentes.

## 4_MASTER_PROJECT_PLAN

1. Creer le chantier parent sur une branche dediee.
2. Lire les sources existantes par axe.
3. Poser la carte de consolidation.
4. Poser le plan d'implementation des 4 axes.
5. Poser la matrice de non-duplication.
6. Poser le manifeste des sources existantes.
7. Poser le graphe de dependances.
8. Poser le modele de warnings WHY lint.
9. Poser le binding warnings-gates.
10. Poser le roadmap d'implementation.
11. Poser la SPEC de reference.
12. Poser le closeout d'ouverture.
13. Creer l'entree inbox locale.
14. Mettre a jour MACHINE_WORK_SPLIT (bloc cursor-ai uniquement).
15. Commiter doc-only.

## 5_GO_PLAN

GO parent : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

Branche dediee : `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

Dossier chantier : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/`

Inbox : `docs/index/inbox/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01.md`

## 6_FINAL_TARGET

**FINAL_TARGET : produire un chantier parent documentaire de consolidation des 4 axes de controle + cible produit OpenClaw central, avec un modele de warnings WHY lint warning-only, sans autorisation runtime, sans autofix, sans blocage CI, sans modification d'index globaux.**

## 7_CANONICAL_STATE

Etat valide a l'ouverture :

- Branche dediee `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` creee et realignee sur `origin/sot/mainline`.
- Dossier chantier parent cree : `docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/`.
- 10 fichiers de cadrage produits.
- Entree inbox locale creee.
- Bloc cursor-ai dans MACHINE_WORK_SPLIT mis a jour.
- Aucun index global modifie.
- Aucune action runtime.
- Aucun secret.
- Aucun autofix.
- Aucun MCP live.
- Aucun trade.
- Aucun shell libre.
- Documentation seulement.

## 8_VALIDATED_PLAN

Etapes validees :

1. Verification initiale Git (status, branch, log, remote, fetch).
2. Verification branche distante (361 behind sot/mainline, 0 ahead — safe to realign).
3. Realignement branche sur `origin/sot/mainline`.
4. Lecture des sources existantes (MATRICE_MASTER, MACHINE_WORK_SPLIT, WHY runtime graph, RUNTIME_SECURITY_PARENT, childs).
5. Constat des sources absentes (6 chantiers OpenClaw governance non trouves).
6. Creation du dossier chantier.
7. Redaction des 10 fichiers de cadrage.
8. Creation de l'entree inbox.
9. Mise a jour MACHINE_WORK_SPLIT (bloc cursor-ai).
10. Commit doc-only.

## 9_SELECTED_SOLUTION

Approche retenue : consolidation documentaire avant toute implementation.

Le chantier parent pose les frontieres, le modele de warnings, les gates et le roadmap. Aucun code, aucun runtime, aucun autofix.

Le WHY lint reste perpetuellement en mode WARNING_ONLY.

## 10_SELECTED_SETUP

Structure retenue :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/
  00_CONSOLIDATION_MAP_01.md
  01_IMPLEMENTATION_MASTER_PLAN_4_AXES_01.md
  02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md
  03_EXISTING_SOURCE_MANIFEST_01.md
  04_DEPENDENCY_GRAPH_4_AXES_01.md
  05_WHY_LINT_WARNING_MODEL_01.md
  06_CROSS_AXIS_GATE_BINDING_01.md
  07_AXIS_IMPLEMENTATION_ROADMAP_01.md
  SPEC_WHY_LINT_EXPERIMENT_01.md
  90_CLOSEOUT_OPENING_01.md

docs/index/inbox/
  GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01.md

docs/index/
  MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md (bloc cursor-ai uniquement)
```

Branche : `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01`

## 11_KEY_DECISIONS

- Chantier parent ouvert comme consolidation documentaire.
- Branche dediee obligatoire.
- Scope initial : documentation uniquement.
- WHY lint = warning-only, perpetuellement.
- autofix_allowed: false pour tous les warnings.
- runtime_binding: false pour tous les warnings.
- can_fail_ci: false pour tous les warnings.
- Pas de runtime.
- Pas d'autofix.
- Pas de secret.
- Pas de MCP live.
- Pas de modification d'index global (sauf MACHINE_WORK_SPLIT cursor-ai).
- Continuite parent d'abord dans `docs/chantiers/<GO_PARENT>/`.
- Inbox atomique autorisee pour aggregation future.

## 12_INVARIANTS

- WHY lint ne cree pas une 5e verite.
- WHY lint detecte et signale seulement.
- WHY lint n'autorise aucune action.
- WHY lint ne remplace pas la gouvernance.
- WHY lint ne remplace pas la securite runtime.
- WHY lint ne remplace pas le graph WHY/runtime.
- WHY lint ne definit pas la cible produit OpenClaw.
- WHY lint ne bloque pas la CI.
- WHY lint n'applique aucun correctif automatique.
- Toute correction remonte a l'axe source, jamais a WHY lint.
- Aucun index global n'est modifie (sauf MACHINE_WORK_SPLIT cursor-ai).
- Aucun runtime n'est autorise.
- Aucun secret n'est expose.
- Aucun trade n'est execute.

## 13_ESTABLISHED

- Le besoin de consolidation des axes de controle est etabli.
- Le chantier parent est valide.
- La branche dediee est validee et realignee sur sot/mainline.
- Le plan documentaire est valide.
- Le modele de warnings est defini.
- Les gates sont bindees.
- Le roadmap est pose.
- Le bloc cursor-ai dans MACHINE_WORK_SPLIT est a jour.
- Etat de reprise 2026-05-19 : la branche parent `go/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` est absorbee par `origin/sot/mainline` et ne porte plus de delta propre.
- Le validateur statique WHY lint a maintenant une spec, un corpus de fixtures, une implementation locale read-only/report-only, un scan V1 de docs reelles, un triage, une baseline V1 et un plan de remediation documentaire.

## 14_HYPOTHESIS

Hypotheses restantes apres reprise 2026-05-19 :

- Certains findings V1 sont probablement des vrais gaps documentaires.
- Certains findings V1 sont probablement du bruit structurel lie au scan de rapports produits dans le dossier source.
- Les exceptions de baseline doivent rester documentees avant tout elargissement repo-wide.
- Les corrections doivent rester dans des child GO explicites, sans autofix et sans mutation runtime.
- Toute integration CI future doit rester non bloquante tant que la gouvernance ne l'autorise pas explicitement.

## 15_REMAINING_GAP

Etat clos ou deplace :

- Le validateur statique n'est plus un gap : il est specifie et implemente localement en read-only/report-only sous `tools/why_lint_static_validator/`.
- Le corpus de fixtures n'est plus un gap : `GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_FIXTURE_CORPUS_01.md` formalise 40 fixtures.
- Le scan de docs reelles n'est plus un gap initial : V1 dispose d'un rapport, d'un triage, d'une baseline et d'un plan de remediation.

Gaps restants :

- Pas encore de baseline V2.
- Pas encore de correction des vrais gaps documentaires.
- Pas encore de regles d'exception codifiees pour le bruit V1.
- Pas encore de scan repo-wide.
- Pas encore d'integration OpenClaw.
- Pas encore d'integration MCP live.
- Pas encore de CI ; toute CI future reste non bloquante par invariant.
- Pas encore de SPEC canonique unifiee OpenClaw central.
- 6 chantiers OpenClaw governance references par l'instruction mais absents du repo.
- Skill registry futur non specifie.

## 16_TODO

Suite documentaire proposee apres reprise :

1. Ne pas rouvrir le parent WHY lint comme chantier actif par la seule existence de la branche.
2. Reprendre depuis le plan de remediation V1.
3. Ouvrir un child GO cible pour les vrais gaps documentaires.
4. Ouvrir un child GO separe pour les exceptions ou raffinements de regles V1 si le bruit est confirme.
5. Produire une baseline V2 apres corrections explicites.
6. Maintenir les invariants : doc-only, read-only, warning-only, aucun runtime, aucun autofix, aucun MCP live, aucun trade, aucun secret.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_REMEDIATION_PLAN_V1_01.md
```

Contexte a relire avant action :

```text
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/SPEC_WHY_LINT_EXPERIMENT_01.md
docs/chantiers/GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01/GO_OPT_TRADING_DOC_OPS_WHY_LINT_STATIC_VALIDATOR_REAL_DOCS_SCAN_BASELINE_V1_01.md
```

Point d'action suivant : child GO documentaire cible, soit pour vrais gaps, soit pour exceptions/regles V1. Aucune correction automatique.

## 18_TO_DOCUMENT

TAGS :

- WHY_LINT
- WHY_LINT_CONSOLIDATION
- WHY_LINT_WARNING_MODEL
- WHY_LINT_NO_DUPLICATION
- WHY_LINT_GATE_BINDING
- WHY_LINT_ROADMAP
- OPT_TRADING_DOC_ONLY_PARENT

Blocs a extraire :

- WHY
- 6_FINAL_TARGET
- 12_INVARIANTS
- 15_REMAINING_GAP
- 17_RESUME_POINT

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `GO_OPT_TRADING_DOC_OPS_WHY_LINT_EXPERIMENT_01` etablit la consolidation des 4 axes de controle + cible produit OpenClaw central.
- Le WHY lint est la couche warning-only de detection de contradictions entre axes. Il ne cree pas une 5e verite.
- Tous les warnings ont autofix_allowed: false, runtime_binding: false, can_fail_ci: false.
- La gouvernance reste l'arbitre ultime en cas de conflit structurel.
- Le validateur statique existe maintenant en local read-only/report-only ; ses findings restent des warnings, pas des permissions.
- Suite logique actuelle : remediation V1 par child GO cible, puis baseline V2.

## WHY

Ce chantier existe pour eviter que les sessions Gouvernance, WHY, WHY lint et OpenClaw central deviennent des verites concurrentes.

Le WHY lint consolide les frontieres et detecte les contradictions.

Il n'autorise aucune action.
Il ne remplace pas la gouvernance.
Il ne remplace pas la securite runtime.
Il ne remplace pas le graph WHY/runtime.
Il ne definit pas la cible produit OpenClaw.

Il signale uniquement les gaps de coherence en warning-only.

Le but n'est pas de ralentir le developpement, mais d'empecher que des sessions paralleles produisent des verites incompatibles, des doublons, des contradictions ou des autorisations implicites.

## Governance Binding

Le WHY lint est subordonne a la gouvernance :

- Source souveraine : `MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- Toute regle de gouvernance prime sur un warning WHY lint.
- WHY lint ne peut pas invalider une regle de gouvernance.
- WHY lint peut signaler un GOVERNANCE_DRIFT si un document s'ecarte de la matrice maitre.

## Runtime Security Binding

Le WHY lint est subordonne a la securite runtime :

- Source souveraine : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`
- Toute permission runtime prime sur un warning WHY lint.
- WHY lint peut signaler un RUNTIME_SECURITY_GAP si un garde-fou est absent.
- WHY lint ne definit jamais de permission runtime.

## WHY Runtime Graph Binding

Le WHY lint est subordonne au WHY/runtime graph :

- Source souveraine : `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_LOCAL_VIEW_REAL_01`
- Le WHY graph represente ; WHY lint verifie.
- WHY lint peut signaler un WHY_GAP si une section WHY est absente.
- WHY lint ne produit pas de representation graphique.

## OpenClaw Central Target Binding

Le WHY lint est subordonne a la cible produit :

- OpenClaw central est la cible a stabiliser.
- WHY lint verifie la coherence des axes de controle autour de cette cible.
- WHY lint ne definit pas l'architecture d'OpenClaw central.
- WHY lint signale les gaps (CONTROL_PLANE_GAP, SKILL_REGISTRY_GAP, etc.) sans les corriger.

## No Duplication Rules

1. Gouvernance = regles, permissions documentaires, gates, traces, evals, deny-by-default.
2. Runtime Security = garde-fous d'execution pour skills/workers/runtime.
3. WHY / WHY-runtime graph = representation explicable, overlays, snapshots, review outputs.
4. WHY lint = couche warning-only de detection de contradictions.
5. OpenClaw central = cible operationnelle Telegram/Gateway/Supervisor/Workers/Memory/Machines.

Aucun axe ne remplace un autre. Chaque sujet a un seul axe souverain (voir 02_NO_DUPLICATION_BOUNDARY_MATRIX_01.md).

## Warning Model

11 familles de warnings definies (voir 05_WHY_LINT_WARNING_MODEL_01.md) :

WHY_GAP, GOVERNANCE_DRIFT, RUNTIME_SECURITY_GAP, MACHINE_SCOPE_GAP, WORKER_OWNER_GAP, MEMORY_SCOPE_GAP, CONTROL_PLANE_GAP, SKILL_REGISTRY_GAP, TRACE_EVAL_GAP, OBSERVABILITY_GAP, BRANCH_CHANTIER_GAP.

Severite R0 (critique) a R5 (informatif).
Tous les warnings : autofix_allowed=false, runtime_binding=false, can_fail_ci=false.

## Gate / Trace / Eval Binding

11 gates definies (voir 06_CROSS_AXIS_GATE_BINDING_01.md).
Chaque famille de warning est bindee a une ou plusieurs gates.
WHY lint ne franchit jamais un gate. Il recommande seulement.

## No Runtime / No Autofix / No CI Blocking

- WHY lint n'execute aucun runtime.
- WHY lint n'applique aucun correctif automatique.
- WHY lint ne bloque jamais la CI.
- Ces trois proprietes sont des invariants perpetuel du WHY lint.

## Future Implementation Path

1. Child GO : spec validateur statique (DONE, doc-only).
2. Child GO : corpus de fixtures (DONE, doc-only).
3. Child GO : implementation locale read-only/report-only (DONE, can_fail_ci=false).
4. Child GO : scan de docs reelles V1 (DONE, report-only).
5. Child GO : triage, baseline V1 et plan de remediation (DONE).
6. Child GO suivant : corrections documentaires ciblees ou exceptions/regles V1, sans autofix.
7. Integration future avec OpenClaw central uniquement quand les garde-fous seront prouves et documentes.

## RISKS

- À qualifier.
