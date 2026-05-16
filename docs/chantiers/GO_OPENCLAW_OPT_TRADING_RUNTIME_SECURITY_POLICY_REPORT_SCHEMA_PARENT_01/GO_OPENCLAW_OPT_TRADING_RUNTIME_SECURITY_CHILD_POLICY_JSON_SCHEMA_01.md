---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CANONICAL_RESTORE_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
status: draft
lifecycle_stage: child_spec
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_report
  - json_schema
  - validator
  - ci
  - warning_only
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_VALIDATOR_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CI_WIRING_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_CLOSEOUT_01.md
  - tools/openclaw/validate_policy_json_report_schema.py
  - tools/openclaw/validate_skill_policy_static.py
  - tests/openclaw/test_validate_policy_json_report_schema.py
  - .github/workflows/openclaw-skill-policy-warning-only.yml
  - https://github.com/magikgmo4-ui/opt-trading/pull/466
  - https://github.com/magikgmo4-ui/opt-trading/pull/469
  - https://github.com/magikgmo4-ui/opt-trading/pull/473
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01

## 1_MASTER_TARGET

Restaurer et canoniser le document de contrat `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01` au chemin reference par les children OpenClaw policy report schema, sans changer le comportement deja merge du validateur, du workflow CI warning-only ou du closeout parent.

## 3_INITIAL_NEED

La chaine OpenClaw policy report JSON schema est fermee fonctionnellement depuis les merges du validateur, du wiring CI et du closeout parent.

Le gap restant est documentaire : le fichier canonique de contrat schema-only attendu par les children n'etait pas present sur `sot/mainline` au chemin reference, alors meme que le validateur et ses tests materialisent deja ce contrat dans le code.

Il faut donc restaurer un document de reference unique qui :

- fixe `schema_version: "1.0"` comme cible canonique ;
- reconnait l'absence de `schema_version` comme `legacy_baseline` acceptee ;
- aligne le contrat documentaire sur le validateur deja merge ;
- ne modifie ni runtime, ni workflow, ni code, ni index globaux.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Child canonique restaure :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
```

Branche :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CANONICAL_RESTORE_01
```

Plan valide :

- recreer le fichier canonique au chemin reference par les children ;
- decrire le contrat schema-only du rapport JSON source produit par `validate_skill_policy_static.py` ;
- aligner les champs requis, invariants et regles de compatibilite sur `validate_policy_json_report_schema.py` et ses tests ;
- garder `WARNING_ONLY`, `runtime_execution: DISABLED`, `mutation: DISABLED` et `--strict-exit` opt-in seulement ;
- rester strictement doc-only, sans modifier runtime, workflow, validateurs, tests, policy YAML, services, secrets ou index globaux.

## 6_FINAL_TARGET

**FINAL_TARGET : restaurer un contrat documentaire canonique unique pour le rapport JSON OpenClaw policy, defini comme schema-only warning-only compatible avec la baseline legacy non versionnee et avec `schema_version: "1.0"`, sans changer aucun comportement deja merge.**

## WHY

Ce child existe pour supprimer l'ambiguite documentaire laissee par le closeout parent : le contrat est deja implemente et teste, mais son document canonique manque au chemin annonce.

Sans ce fichier, les children deja merges pointent vers une cible absente. Restaurer ce document stabilise la reference contractuelle avant toute suite logique, notamment avant une eventuelle commande globale agregatrice.

## 7_CANONICAL_STATE

Etat canonique a figer :

- le rapport source attendu est le JSON produit par `tools/openclaw/validate_skill_policy_static.py` ;
- l'absence de `schema_version` est acceptee comme `legacy_baseline` ;
- `schema_version: "1.0"` est la cible canonique versionnee ;
- toute autre version de schema est classee `unsupported_schema_version` ;
- les champs requis du rapport source sont `validator`, `policy_path`, `mode`, `runtime_execution`, `mutation`, `findings_count`, `findings` ;
- `validator` cible cote rapport source est `OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR` ;
- `mode` doit rester `WARNING_ONLY` ;
- `runtime_execution` doit rester `DISABLED` ;
- `mutation` doit rester `DISABLED` ;
- `findings` doit etre une liste ;
- `findings_count` doit etre un entier >= 0 et rester coherent avec `len(findings)` ;
- chaque finding doit contenir `level`, `code`, `message` comme chaines non vides ;
- le contrat reste warning-only ;
- aucun runtime n'est execute ;
- aucune mutation de fichier n'est autorisee ;
- `--strict-exit` peut exister dans le validateur de schema, mais reste opt-in et non active par defaut ni dans le workflow.

## 8_VALIDATED_PLAN

- Partir du comportement deja merge et non de speculations futures.
- Faire du document restaure la source canonique de lecture pour les children deja fusionnes.
- Decrire explicitement les deux contrats acceptes : `legacy_baseline` et `schema_1_0`.
- Formaliser la regle de rejet semantique des versions non supportees sans changer le validateur.
- Limiter ce GO a un seul fichier documentaire pour conserver un diff minimal et sans impact d'execution.

## 9_SELECTED_SOLUTION

Solution retenue : restaurer le fichier `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md` comme document spec canonique schema-only, derive du comportement deja etabli par le validateur, les tests et le workflow warning-only.

Le document ne re-implemente rien dans le code. Il capture simplement le contrat deja observe comme reference stable pour les lecteurs humains, les children lies et les futurs GOs.

## 11_KEY_DECISIONS

- Utiliser `schema_version: "1.0"` comme seule version canonique supportee actuellement.
- Accepter l'absence de `schema_version` comme `legacy_baseline` compatible.
- Classer toute autre version dans `unsupported_schema_version`.
- Garder les champs requis limites a `validator`, `policy_path`, `mode`, `runtime_execution`, `mutation`, `findings_count`, `findings`.
- Exiger `level`, `code`, `message` sur chaque finding.
- Garder le contrat strictement warning-only et sans mutation.
- Laisser `--strict-exit` en option explicite du validateur de schema seulement, sans activation par defaut.
- Ne toucher ni au validateur principal, ni au validateur de schema, ni au workflow.

## 12_INVARIANTS

- Scope doc-only.
- Un seul fichier ajoute au chemin manque.
- Aucun runtime OpenClaw n'est execute.
- Aucun workflow GitHub Actions n'est modifie.
- `tools/openclaw/validate_policy_json_report_schema.py` n'est pas modifie.
- `tools/openclaw/validate_skill_policy_static.py` n'est pas modifie.
- Aucun test n'est modifie.
- Aucune policy YAML n'est modifiee.
- Aucun service ou secret n'est ajoute, lu ou change.
- Aucun index global n'est modifie.
- `mode == WARNING_ONLY`.
- `runtime_execution == DISABLED`.
- `mutation == DISABLED`.

## 13_ESTABLISHED

Etabli avant cette restauration :

```text
PR #466
STATUS: MERGED
MERGE_COMMIT: 2ca0b58f26860e6abf610989124f9e80606b8d1e
ROLE: schema validator warning-only

PR #469
STATUS: MERGED
MERGE_COMMIT: 87483d45211c82b878367103087a8bba4efb047d
ROLE: CI warning-only wiring

PR #473
STATUS: MERGED
MERGE_COMMIT: df737ea51f6d4614b08f6eb37561eca9aa214cd5
ROLE: parent closeout documenting the missing canonical file gap
```

Etabli par les surfaces repo deja presentes :

- `tools/openclaw/validate_policy_json_report_schema.py` code deja les contrats `legacy_baseline`, `schema_1_0` et `unsupported_schema_version` ;
- `tests/openclaw/test_validate_policy_json_report_schema.py` prouve l'acceptation du legacy non versionne et de `schema_version: "1.0"` ;
- `.github/workflows/openclaw-skill-policy-warning-only.yml` execute deja le validateur de schema sans `--strict-exit` ;
- le closeout parent a confirme que le gap restant etait l'absence de ce fichier canonique.

## 14_HYPOTHESIS

- une future version `1.x` ou `2.0` pourra exiger un GO separe ;
- une taxonomie plus stricte des `finding.code` pourra etre normalisee plus tard ;
- une commande globale agregatrice pourra etre introduite une fois le contrat documentaire stabilise ;
- un mode blocking avec `--strict-exit` devra rester un GO distinct s'il est etudie.

## 15_REMAINING_GAP

- le contrat documentaire est restaure, mais aucune version canonique au-dela de `1.0` n'est definie ;
- la taxonomie stricte des `finding.code` du rapport source reste ouverte ;
- aucune commande globale agregatrice n'est encore definie ;
- le mode blocking n'est toujours pas active, par decision.

## 16_TODO

1. Ne pas rouvrir cette restauration sauf si le contrat `1.0` doit evoluer.
2. Ouvrir un GO separe si une version `1.x` ou `2.0` doit etre supportee.
3. Ouvrir un GO separe si une taxonomie stricte des `finding.code` devient necessaire.
4. Ouvrir un GO separe si une commande globale agregatrice de validation doit etre ajoutee.
5. Ouvrir un GO separe si `--strict-exit` doit devenir bloquant en CI.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_CANONICAL_RESTORE_01
```

Etat de reprise :

```text
OPENCLAW_POLICY_REPORT_SCHEMA_CHAIN_01: CLOSED_WITH_CANONICAL_SCHEMA_DOC
JSON_SCHEMA_01: RESTORED_DOC_ONLY
VALIDATOR: MERGED via PR #466
CI_WIRING: MERGED via PR #469
PARENT_CLOSEOUT: MERGED via PR #473
NEXT_LOGICAL_GO: OPTIONAL_GLOBAL_VALIDATION_AGGREGATOR
```
