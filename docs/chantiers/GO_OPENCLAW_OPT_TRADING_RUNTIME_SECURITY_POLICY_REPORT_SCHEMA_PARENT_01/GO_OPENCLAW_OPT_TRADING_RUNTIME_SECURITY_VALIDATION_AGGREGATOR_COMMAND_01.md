---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
status: draft
lifecycle_stage: child_closeout
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - validation
  - aggregator
  - json_schema
  - warning_only
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_CLOSEOUT_01.md
  - tools/openclaw/validate_runtime_security_all.py
  - tools/openclaw/validate_skill_policy_static.py
  - tools/openclaw/validate_policy_json_report_schema.py
  - tests/openclaw/test_validate_runtime_security_all.py
  - https://github.com/magikgmo4-ui/opt-trading/pull/466
  - https://github.com/magikgmo4-ui/opt-trading/pull/469
  - https://github.com/magikgmo4-ui/opt-trading/pull/473
  - https://github.com/magikgmo4-ui/opt-trading/pull/476
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01

## 1_MASTER_TARGET

Ajouter une commande aggregatrice warning-only qui lance les validations OpenClaw runtime/security deja existantes, produit un resume JSON consolide et ne change aucun comportement runtime, service, secret, policy YAML ou workflow deja merge.

## 3_INITIAL_NEED

Le contrat schema, le validateur de schema, le wiring CI warning-only et la restauration canonique du document `JSON_SCHEMA_01` sont deja fermes.

Il manque encore une commande unique capable de rejouer localement la chaine de validation runtime/security la plus importante pour OpenClaw, sans introduire de runtime, sans nouveau workflow obligatoire et sans construire au-dessus d'un contrat documentaire ambigu.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
```

Branche :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
```

Plan valide :

- ajouter un script standard library only ;
- lancer le validateur statique `validate_skill_policy_static.py` en interne ;
- ecrire `openclaw-skill-policy-report.json` comme artefact explicite ;
- lancer ensuite `validate_policy_json_report_schema.py` sur ce rapport ;
- produire `openclaw-runtime-security-validation-summary.json` comme resume consolide ;
- rester `WARNING_ONLY` avec exit `0` par defaut ;
- garder `--strict-exit` strictement opt-in ;
- ajouter des tests dedies ;
- ne toucher ni runtime, ni service, ni secret, ni policy YAML, ni workflow obligatoire, ni index globaux.

## 6_FINAL_TARGET

**FINAL_TARGET : fournir une commande aggregatrice warning-only OpenClaw runtime/security, capable de consolider le validateur statique policy et le validateur de schema JSON dans un resume JSON unique, sans activer de runtime ni comportement bloquant par defaut.**

## WHY

Ce child existe pour donner un point d'entree local unique a la chaine de validation runtime/security deja stabilisee.

Le but n'est pas d'ajouter une nouvelle politique ou un nouveau workflow, mais de rendre la chaine existante rejouable en une seule commande, sur un contrat documentaire et code deja alignes.

## 7_CANONICAL_STATE

Etat cible obtenu :

- `tools/openclaw/validate_runtime_security_all.py` orchestre les validations existantes sans subprocess ni dependance externe ;
- l'agregateur charge le validateur statique et le validateur de schema en interne ;
- l'agregateur ecrit `openclaw-skill-policy-report.json` comme artefact JSON explicite ;
- l'agregateur produit `openclaw-runtime-security-validation-summary.json` comme resume consolide ;
- le resume consolide reste `WARNING_ONLY` ;
- `runtime_execution` reste `DISABLED` ;
- `mutation` reste `DISABLED` ;
- les deux validateurs sont representes dans le resume ;
- `findings_count` agrege reste coherent avec la liste consolidee ;
- `--strict-exit` retourne `1` seulement en opt-in et seulement si des findings existent ;
- aucun runtime, service, secret, policy YAML ou workflow obligatoire n'est introduit.

## 8_VALIDATED_PLAN

- Reutiliser strictement les validateurs deja merges.
- Eviter tout appel runtime ou shell externe.
- Ecrire seulement les artefacts JSON explicitement annonces.
- Aplatir les findings des deux validateurs dans un resume unique.
- Garder un rendu texte pour lecture humaine et un rendu JSON pour automatisation locale.
- Couvrir la commande avec des tests sur le chemin nominal et sur `--strict-exit`.

## 9_SELECTED_SOLUTION

Solution retenue : un script Python autonome qui importe les deux validateurs existants, reconstruit le rapport policy JSON, valide ce rapport contre le schema canonique, puis assemble un resume JSON contenant les sous-rapports et les findings agreges.

Cette approche evite de dupliquer la logique des validateurs, n'ajoute aucun workflow et garde la chaine locale purement observationnelle.

## 10_SELECTED_SETUP

Fichiers crees :

```text
tools/openclaw/validate_runtime_security_all.py
tests/openclaw/test_validate_runtime_security_all.py
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01.md
```

Commandes locales ciblees :

```text
python tools/openclaw/validate_runtime_security_all.py
python tools/openclaw/validate_runtime_security_all.py --format json
python -m unittest tests.openclaw.test_validate_skill_policy_static
python -m unittest tests.openclaw.test_validate_policy_json_report_schema
python -m unittest tests.openclaw.test_validate_runtime_security_all
```

## 11_KEY_DECISIONS

- Standard library only.
- Pas de subprocess ; chargement interne des validateurs existants.
- `openclaw-skill-policy-report.json` reste l'artefact policy JSON source.
- `openclaw-runtime-security-validation-summary.json` devient l'artefact consolide.
- Resume consolide en `WARNING_ONLY` avec exit `0` par defaut.
- `--strict-exit` reste opt-in seulement.
- Aucun nouveau workflow n'est requis dans ce child.

## 12_INVARIANTS

- `mode == WARNING_ONLY`.
- `runtime_execution == DISABLED`.
- `mutation == DISABLED`.
- Aucun runtime OpenClaw n'est execute.
- Aucun service ou secret n'est lu.
- Aucune policy YAML n'est modifiee.
- Aucun index global n'est modifie.
- Aucun workflow GitHub Actions n'est requis ni modifie.
- Seuls les artefacts de rapport explicitement annonces peuvent etre ecrits par la commande.

## 13_ESTABLISHED

Etabli avant ce child :

```text
PR #466 -> schema validator warning-only
PR #469 -> CI warning-only wiring
PR #473 -> parent closeout
PR #476 -> canonical JSON schema document restore
```

Etabli par cette implementation :

- une commande locale unique agrege les deux validateurs existants ;
- les tests prouvent la presence des deux validateurs dans le resume ;
- les tests prouvent la coherence de `findings_count` ;
- les tests prouvent `exit 0` par defaut et `exit 1` en `--strict-exit` seulement si findings ;
- aucun comportement runtime supplementaire n'est introduit.

## 14_HYPOTHESIS

- un futur wiring CI pourra reutiliser cette commande si un GO explicite l'autorise ;
- d'autres validateurs runtime/security pourront etre agreges plus tard ;
- une taxonomie plus stricte des findings consolides pourra etre normalisee ulterieurement.

## 15_REMAINING_GAP

- l'agregateur n'est pas encore branche dans un workflow dedie ;
- seuls les validateurs policy static et policy JSON schema sont agreges pour l'instant ;
- aucune taxonomie transverse plus stricte des findings agreges n'est encore definie.

## 16_TODO

1. Decider explicitement si l'agregateur doit etre branche en CI plus tard.
2. Ouvrir un GO separe si d'autres validateurs runtime/security doivent rejoindre l'agregateur.
3. Ouvrir un GO separe si `--strict-exit` doit devenir bloquant en CI.
4. Ouvrir un GO separe si une taxonomie consolidee des findings devient necessaire.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_VALIDATION_AGGREGATOR_COMMAND_01
```

Etat de reprise :

```text
OPENCLAW_RUNTIME_SECURITY_AGGREGATOR: LOCAL_WARNING_ONLY_READY
STATIC_VALIDATOR: INCLUDED
JSON_SCHEMA_VALIDATOR: INCLUDED
SUMMARY_REPORT: openclaw-runtime-security-validation-summary.json
STRICT_EXIT: OPT_IN_ONLY
```
