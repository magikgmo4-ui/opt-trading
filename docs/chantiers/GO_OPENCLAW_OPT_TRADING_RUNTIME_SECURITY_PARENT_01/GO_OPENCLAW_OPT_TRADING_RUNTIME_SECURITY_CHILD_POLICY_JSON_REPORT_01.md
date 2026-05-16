---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_json_report
  - warning_only
  - machine_readable
  - no_runtime
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_STATIC_VALIDATOR_01.md
  - tools/openclaw/validate_skill_policy_static.py
  - tests/openclaw/test_validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01

## 1_MASTER_TARGET

Ajouter une sortie rapport JSON machine-readable au validateur statique OpenClaw skill policy, sans changer son comportement warning-only par defaut.

## 3_INITIAL_NEED

Le validateur produit deja un rapport texte utile pour lecture humaine.

Besoin courant : permettre a un futur job, dashboard ou collector de lire les findings sous forme structuree, tout en conservant les garanties : aucun runtime, aucune mutation, aucun auto-fix et exit `0` par defaut.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_REPORT_01
```

Fichiers modifies :

```text
tools/openclaw/validate_skill_policy_static.py
tests/openclaw/test_validate_skill_policy_static.py
```

## 6_FINAL_TARGET

**FINAL_TARGET : ajouter l'option `--format json` au validateur statique OpenClaw skill policy, avec un rapport JSON stable contenant `validator`, `policy_path`, `mode`, `runtime_execution`, `mutation`, `findings_count` et `findings`, sans modifier le mode texte par defaut ni l'exit code warning-only.**

## WHY

Ce child existe pour rendre les warnings exploitables par machine sans transformer le validateur en gate bloquant.

Le JSON doit permettre l'observation future, pas l'execution. Il prepare une surface lisible par CI non bloquante, dashboard, collector ou skill registry, tout en gardant le contrat de securite : signaler sans modifier ni bloquer.

## 7_CANONICAL_STATE

Etat valide :

- PR #451 mergee ;
- compatibilite Python 3.14 du test corrigee ;
- validateur warning-only disponible ;
- tests stdlib disponibles ;
- branche child dediee creee ;
- runtime non modifie ;
- workflow CI non modifie ;
- index globaux non modifies.

## 8_VALIDATED_PLAN

- Ajouter `--format text|json`.
- Garder `text` comme defaut.
- Construire un rapport commun via `build_report()`.
- Rendre le JSON via `json.dumps` stdlib.
- Tester le JSON sur policy reelle.
- Tester le JSON sur policy manquante.
- Garder exit `0` par defaut.

## 9_SELECTED_SOLUTION

Solution retenue : option CLI explicite.

```bash
python tools/openclaw/validate_skill_policy_static.py --format json
```

Le rapport JSON contient :

```text
validator
policy_path
mode
runtime_execution
mutation
findings_count
findings
```

## 11_KEY_DECISIONS

- Le format texte reste le default.
- Le JSON est opt-in via `--format json`.
- Aucun fichier de rapport n'est ecrit par defaut.
- Aucun runtime n'est appele.
- Aucun secret n'est lu.
- Aucun workflow CI n'est modifie.
- Les tests restent en `unittest` stdlib.

## 12_INVARIANTS

- Warning-only par defaut.
- Exit `0` par defaut.
- Aucun runtime.
- Aucun service.
- Aucun secret.
- Aucun index global.
- Aucun auto-fix.
- Aucune mutation de fichier.
- Aucune CI bloquante.

## 13_ESTABLISHED

Commande texte existante conservee :

```bash
python tools/openclaw/validate_skill_policy_static.py
```

Nouvelle commande JSON :

```bash
python tools/openclaw/validate_skill_policy_static.py --format json
```

Tests ajoutes :

- JSON sur policy reelle ;
- JSON sur policy manquante ;
- conservation de l'exit `0` par defaut.

## 14_HYPOTHESIS

A valider ensuite :

- besoin d'ecrire un artefact JSON en CI ;
- besoin de schema JSON formel ;
- besoin d'un dashboard de lecture des findings ;
- besoin de rattachement au futur skill registry.

## 15_REMAINING_GAP

- Pas encore d'artefact JSON publie par workflow.
- Pas encore de schema JSON.
- Pas encore de dashboard.
- Pas encore de collector.
- Pas encore de liaison skill registry.

## 16_TODO

Suite logique :

1. Reviewer le JSON report.
2. Merge PR du child.
3. Ouvrir un child pour artefact CI JSON si utile.
4. Optionnellement definir un schema JSON stable.

## 17_RESUME_POINT

Reprendre ici :

```text
tools/openclaw/validate_skill_policy_static.py
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01
```

Objectif prochain : faire produire le rapport JSON par le workflow manuel warning-only comme artefact, sans rendre la CI bloquante.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_JSON_REPORT
- OPENCLAW_WARNING_ONLY
- OPENCLAW_MACHINE_READABLE
- OPENCLAW_NO_RUNTIME_EXECUTION

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `validate_skill_policy_static.py --format json` produit un rapport JSON machine-readable warning-only.
- Le format texte reste le default.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_CI_ARTIFACT_01`.
