---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
status: draft
lifecycle_stage: child_closeout
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_report
  - json_schema
  - ci
  - warning_only
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01.md
  - .github/workflows/openclaw-skill-policy-warning-only.yml
  - tools/openclaw/validate_policy_json_report_schema.py
  - tests/openclaw/test_validate_policy_json_report_schema.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01

## 1_MASTER_TARGET

Brancher le validateur de schema JSON du rapport OpenClaw policy dans la boucle CI warning-only existante, sans rendre la CI bloquante par defaut et sans toucher runtime, services, secrets ou policy YAML.

## 3_INITIAL_NEED

Le contrat canonique `1.0` existe et le validateur statique dedie existe aussi depuis `JSON_SCHEMA_VALIDATOR_01`, mais le workflow warning-only existant ne l'execute pas encore.

Il manque donc le wiring minimal qui verifie automatiquement le rapport JSON exporte contre son schema canonique, tout en preservant l'observation non bloquante et l'absence de runtime.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Children precedents :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01
```

Plan valide :

- reutiliser le workflow manual warning-only existant ;
- generer le rapport JSON policy comme avant ;
- executer ensuite le validateur de schema sur ce rapport ;
- exporter un rapport JSON de validation de schema ;
- executer les tests du validateur de schema ;
- ne pas activer `--strict-exit` ;
- ne pas modifier runtime, services, secrets, policy YAML ou index globaux.

## 6_FINAL_TARGET

**FINAL_TARGET : brancher le validateur JSON schema dans une CI warning-only OpenClaw, en gardant le comportement non bloquant par defaut et `--strict-exit` strictement opt-in.**

## WHY

Ce child existe pour transformer le validateur de schema deja implemente en controle operationnel reutilise par la boucle CI warning-only, sans changer la nature observationnelle du systeme.

## 7_CANONICAL_STATE

Etat cible obtenu :

- le workflow `openclaw-skill-policy-warning-only.yml` continue d'executer le validateur statique principal ;
- le workflow valide ensuite `openclaw-skill-policy-report.json` avec `validate_policy_json_report_schema.py` ;
- le workflow exporte un artefact dedie `openclaw-skill-policy-report-schema-validation.json` ;
- le workflow execute aussi `tests.openclaw.test_validate_policy_json_report_schema` ;
- aucun `--strict-exit` n'est active dans le wiring ;
- le comportement global reste warning-only ;
- aucun runtime, service, secret, policy YAML ou index global n'est modifie.

## 8_VALIDATED_PLAN

- Partir du workflow manuel deja prouve.
- Inserer le controle de schema apres la generation du rapport JSON.
- Garder le rapport policy historique intact comme artefact principal.
- Ajouter un second artefact pour la validation de schema.
- Ajouter une preuve de compatibilite generateur -> validateur dans les tests.

## 9_SELECTED_SOLUTION

Solution retenue : wiring minimal dans le workflow existant, sans nouvelle commande globale ni changement semantique du validateur principal.

Le workflow exporte d'abord `openclaw-skill-policy-report.json`, puis lance le validateur de schema en mode texte et JSON, et publie le rapport de validation de schema comme artefact separe pour ne pas perturber l'artefact legacy deja etabli.

## 11_KEY_DECISIONS

- Brancher le controle dans le workflow existant plutot que creer un nouveau workflow.
- Garder `openclaw-skill-policy-report` comme artefact principal inchange.
- Publier la validation de schema dans un second artefact dedie.
- Ne pas utiliser `--strict-exit` dans le wiring CI.
- Ajouter un test d'integration leger prouvant que le JSON reel produit par le validateur principal est accepte comme `legacy_baseline`.

## 12_INVARIANTS

- le workflow reste warning-only par defaut ;
- `--strict-exit` reste opt-in et non active par ce child ;
- aucun runtime OpenClaw n'est execute ;
- aucune mutation n'est introduite ;
- aucun service ou secret n'est lu ;
- aucune policy YAML n'est modifiee ;
- aucun index global n'est modifie.

## 13_ESTABLISHED

Etabli par implementation :

- le workflow lance desormais le validateur de schema sur le rapport JSON exporte ;
- le workflow exporte aussi un JSON de validation de schema ;
- les tests couvrent toujours le validateur de schema et prouvent en plus la compatibilite avec le rapport genere par `validate_skill_policy_static.py` ;
- le wiring ne rend pas la CI bloquante par defaut.

## 14_HYPOTHESIS

- une commande globale de validation pourra etre utile plus tard si plusieurs validateurs doivent etre orchestras ;
- une future version canonique `1.x` ou `2.0` pourra exiger un wiring complementaire ;
- un passage a `--strict-exit` devra faire l'objet d'un GO explicite et separe.

## 15_REMAINING_GAP

- aucune commande globale agregatrice n'existe encore ;
- la CI reste manuelle `workflow_dispatch` ;
- aucun statut GitHub supplementaire n'est ajoute hors de ce workflow ;
- la taxonomie stricte des `finding.code` du rapport source n'est pas encore normalisee.

## 16_TODO

1. Decider explicitement si une commande globale de validation doit etre introduite.
2. Ouvrir un child separe si un mode blocking ou `--strict-exit` doit etre etudie.
3. Ouvrir un child separe si le schema `1.x` ou `2.0` doit etre supporte en CI.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01
```

Point de reprise concret :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01.md
```
