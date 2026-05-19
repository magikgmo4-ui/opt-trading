---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
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
  - validator
  - warning_only
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md
  - tools/openclaw/validate_policy_json_report_schema.py
  - tests/openclaw/test_validate_policy_json_report_schema.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01

## 1_MASTER_TARGET

Ajouter un validateur statique warning-only du rapport JSON OpenClaw policy contre le schema canonique etabli par `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01`, sans activer de runtime ni rendre la CI bloquante.

## 3_INITIAL_NEED

Le schema canonique `1.0` du rapport JSON OpenClaw policy est documente, mais aucun controle statique autonome ne verifie encore qu'un rapport reel respecte ce contrat.

Il faut donc materialiser un validateur de schema reutilisable, capable d'accepter la baseline legacy non versionnee observee en production tout en validant les futurs rapports `schema_version: "1.0"`.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Base de contrat :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
```

Plan valide :

- creer un validateur Python standard library only ;
- accepter explicitement le rapport reel non versionne comme `legacy_baseline` ;
- valider les rapports `schema_version: "1.0"` ;
- verifier les champs requis et invariants documentes ;
- garder `WARNING_ONLY`, `runtime_execution: DISABLED`, `mutation: DISABLED` et exit `0` par defaut ;
- tester les cas legacy, valides et invalides ;
- documenter la solution sans toucher runtime, services, secrets, workflow, policy YAML ou index globaux.

## 6_FINAL_TARGET

**FINAL_TARGET : ajouter un validateur statique warning-only du rapport JSON OpenClaw policy contre le schema canonique, en acceptant la baseline legacy non versionnee et les futurs rapports `schema_version: "1.0"`.**

## WHY

Ce child existe pour transformer le schema documentaire du rapport JSON en controle statique reutilisable, sans activer de runtime ni rendre la CI bloquante.

## 7_CANONICAL_STATE

Etat cible obtenu :

- script dedie `tools/openclaw/validate_policy_json_report_schema.py` ;
- tests dedies `tests/openclaw/test_validate_policy_json_report_schema.py` ;
- mode purement statique, lecture JSON seule ;
- acceptation explicite du rapport legacy non versionne comme `legacy_baseline` ;
- validation des rapports `schema_version: "1.0"` ;
- verification des champs requis `validator`, `policy_path`, `mode`, `runtime_execution`, `mutation`, `findings_count`, `findings` ;
- verification des invariants `WARNING_ONLY`, `DISABLED`, liste de `findings`, coherence `findings_count == len(findings)` et presence de `level`, `code`, `message` sur chaque finding ;
- exit `0` par defaut meme en presence de warnings ;
- `--strict-exit` disponible pour usage futur explicite.

## 8_VALIDATED_PLAN

- S'appuyer sur le rapport reel observe comme baseline legacy.
- Traiter l'absence de `schema_version` comme cas accepte et qualifie.
- Traiter `schema_version: "1.0"` comme contrat canonique versionne.
- Retourner des findings warning-only sur toute derive structurelle ou semantique.
- Garder le validateur autonome et non branche au workflow existant.

## 9_SELECTED_SOLUTION

Solution retenue : un validateur Python autonome qui lit un rapport JSON, le classe comme `legacy_baseline`, `schema_1_0` ou etat invalide, puis emet des findings warning-only sans rien modifier.

Le script n'altere pas le validateur principal, ne change pas le rapport produit, n'active aucun runtime et n'introduit aucun comportement bloquant par defaut.

## 11_KEY_DECISIONS

- Creer un validateur separe plutot qu'etendre le validateur principal.
- Accepter sans warning la baseline legacy reelle quand `schema_version` est absent.
- Considerer `schema_version: "1.0"` comme seule version canonique supportee actuellement.
- Garder `--strict-exit` optionnel et opt-in seulement.
- Limiter les controles au contrat documentaire etabli, sans integration workflow dans ce child.

## 12_INVARIANTS

- `mode` doit rester `WARNING_ONLY` ;
- `runtime_execution` doit rester `DISABLED` ;
- `mutation` doit rester `DISABLED` ;
- `findings` doit etre une liste ;
- `findings_count` doit rester coherent avec `len(findings)` ;
- chaque finding doit contenir `level`, `code`, `message` ;
- le validateur reste warning-only avec exit `0` par defaut ;
- aucun runtime, service, secret, workflow, policy YAML ou index global n'est modifie.

## 13_ESTABLISHED

Etabli par implementation et tests :

- le rapport legacy non versionne est accepte comme `legacy_baseline` ;
- un rapport `1.0` valide est accepte sans findings ;
- les incoherences `findings_count`, champs requis manquants, findings incomplets et `mode` non conforme sont detectes ;
- la sortie reste `WARNING_ONLY` avec exit `0` par defaut ;
- `--strict-exit` retourne `1` en presence de findings.

## 14_HYPOTHESIS

- une integration future dans la CI pourra etre utile, mais elle doit faire l'objet d'un GO explicite ;
- des versions canoniques ulterieures `1.x` ou `2.0` pourront necessiter de nouvelles regles de compatibilite ;
- des champs optionnels supplementaires dans les findings pourront etre normalises plus tard sans bloquer ce child.

## 15_REMAINING_GAP

- le nouveau validateur n'est pas encore branche au workflow existant ;
- aucun artefact legacy embarque n'est stocke dans le repo ;
- la taxonomie canonique des finding codes du rapport source n'est pas encore normalisee.

## 16_TODO

1. Decider explicitement si ce validateur doit etre execute dans la CI plus tard.
2. Ouvrir un child si une future version canonique du rapport doit etre supportee.
3. Ouvrir un child si une taxonomie stricte des `finding.code` devient necessaire.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01
```

Point de reprise concret :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01.md
```
