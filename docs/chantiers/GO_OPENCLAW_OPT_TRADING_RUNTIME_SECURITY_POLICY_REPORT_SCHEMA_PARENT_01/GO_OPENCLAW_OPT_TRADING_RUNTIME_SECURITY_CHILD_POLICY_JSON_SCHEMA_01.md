---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
doc_type: chantier_child_closeout
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-16
topic_keys:
  - openclaw
  - runtime_security
  - policy_report
  - json_schema
  - warning_only
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_ARTIFACT_REVIEW_01.md
  - tools/openclaw/validate_skill_policy_static.py
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01

## 1_MASTER_TARGET

Definir le schema canonique du rapport JSON OpenClaw policy warning-only pour que les artefacts futurs soient comparables, validables et exploitables sans activer de runtime ni transformer la validation en gate bloquant.

## 3_INITIAL_NEED

Le rapport JSON existe deja et a ete prouve en execution reelle via l'artefact `openclaw-skill-policy-report.json` du run `25956668749`.

Le besoin courant est de transformer cette sortie reelle en contrat concret : champs requis, types, invariants, exemples valides, exemples invalides, compatibilite et versioning.

Sans schema canonique, deux consommateurs peuvent lire le meme rapport de facon differente ou accepter des variantes silencieusement incompatibles.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
```

But du child :

- definir les champs minimaux obligatoires ;
- definir `schema_version` ;
- fixer les types et invariants ;
- definir les regles de compatibilite et de versioning ;
- lier le schema au rapport reel `openclaw-skill-policy-report.json` ;
- rester doc/schema-only.

## 6_FINAL_TARGET

**FINAL_TARGET : produire le schema canonique du rapport JSON OpenClaw policy warning-only, couvrant `schema_version`, les champs requis, les types, les invariants, les exemples valides et invalides, les regles de compatibilite, les regles de versioning et le lien avec l'artefact reel de reference.**

## WHY

Ce child existe pour que les rapports JSON futurs soient comparables, validables et exploitables sans transformer la validation en runtime ou en blocage CI.

Le schema doit stabiliser l'interface machine-readable du rapport, pas ajouter de nouvelle execution ni changer le comportement warning-only etabli.

## 7_CANONICAL_STATE

Etat valide :

- parent `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01` ouvert ;
- `OPENCLAW_RUNTIME_SECURITY_POLICY_CHAIN: REAL_ARTIFACT_CONFIRMED` ;
- `OPENCLAW_RUNTIME_SECURITY_PARENT_STATUS: WARNING_ONLY_CONFIRMED` ;
- preuve reelle disponible via le run `25956668749` ;
- artefact reel disponible : `openclaw-skill-policy-report` ;
- rapport reel observe :

```json
{
  "findings": [],
  "findings_count": 0,
  "mode": "WARNING_ONLY",
  "mutation": "DISABLED",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "runtime_execution": "DISABLED",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR"
}
```

- scope doc/schema-only ;
- aucun runtime a modifier ;
- aucun workflow a modifier ;
- aucun validateur a modifier ;
- aucune policy YAML a modifier ;
- aucun index global a modifier.

## 8_VALIDATED_PLAN

- Partir de l'artefact reel comme baseline.
- Definir le schema canonique cible pour les futurs rapports.
- Marquer les champs minimaux obligatoires.
- Definir les contraintes `WARNING_ONLY`, `DISABLED`, cardinalites et coherence interne.
- Definir les regles de compatibilite ascendante et de versioning.
- Donner des exemples valides et invalides.
- Ne pas modifier le generateur du rapport dans ce child.

## 9_SELECTED_SOLUTION

Solution retenue : schema documentaire canonique versionne en `1.0`.

Nuance de depart : l'artefact reel confirme est une baseline non versionnee. Le schema canonique cible ajoute `schema_version` comme champ requis pour les futurs rapports conformes au contrat versionne.

Schema canonique cible `1.0` :

| Champ | Requis | Type | Contrainte |
| --- | --- | --- | --- |
| `schema_version` | oui | `string` | valeur `1.0` pour la premiere version canonique |
| `validator` | oui | `string` | valeur attendue `OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR` |
| `policy_path` | oui | `string` | chemin relatif non vide |
| `mode` | oui | `string` | doit etre `WARNING_ONLY` |
| `runtime_execution` | oui | `string` | doit etre `DISABLED` |
| `mutation` | oui | `string` | doit etre `DISABLED` |
| `findings_count` | oui | `integer` | entier >= `0`, coherent avec `len(findings)` |
| `findings` | oui | `array` | liste de findings, vide autorise |

Schema canonique d'un finding en `1.0` :

| Champ | Requis | Type | Contrainte |
| --- | --- | --- | --- |
| `level` | oui | `string` | niveau semantique du finding ; valeur initiale recommandee `WARNING` |
| `code` | oui | `string` | identifiant stable et non vide |
| `message` | oui | `string` | message humain non vide |

Regles structurelles :

- `findings` doit toujours etre une liste ;
- `findings_count` doit toujours etre egal au nombre d'elements de `findings` ;
- si `findings_count` vaut `0`, `findings` doit pouvoir etre `[]` ;
- si `findings_count` est strictement positif, chaque element de `findings` doit respecter le schema finding `1.0` ;
- le rapport reste purement statique et descriptif ;
- aucun champ ne doit suggerer une execution runtime, une mutation ou un auto-fix.

Exemple valide minimal `1.0` :

```json
{
  "schema_version": "1.0",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 0,
  "findings": []
}
```

Exemple valide `1.0` avec finding :

```json
{
  "schema_version": "1.0",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 1,
  "findings": [
    {
      "level": "WARNING",
      "code": "SKILL_POLICY_PATH_SCOPE_WARNING",
      "message": "path scope should be narrowed"
    }
  ]
}
```

Exemples invalides :

Exemple invalide 1, `schema_version` absent :

```json
{
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 0,
  "findings": []
}
```

Exemple invalide 2, `findings_count` incoherent :

```json
{
  "schema_version": "1.0",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 2,
  "findings": []
}
```

Exemple invalide 3, mode non conforme :

```json
{
  "schema_version": "1.0",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "STRICT",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 0,
  "findings": []
}
```

Exemple invalide 4, finding incomplet :

```json
{
  "schema_version": "1.0",
  "validator": "OPENCLAW_SKILL_POLICY_STATIC_VALIDATOR",
  "policy_path": "configs/openclaw/security/skill_policy.yaml",
  "mode": "WARNING_ONLY",
  "runtime_execution": "DISABLED",
  "mutation": "DISABLED",
  "findings_count": 1,
  "findings": [
    {
      "level": "WARNING",
      "message": "missing stable code"
    }
  ]
}
```

Regles de compatibilite :

- un consommateur `1.x` doit exiger tous les champs requis de `1.0` ;
- un consommateur `1.x` doit pouvoir ignorer des champs additionnels documentes tant qu'ils ne changent pas la semantique des champs requis ;
- un producteur ne doit pas supprimer ni renommer un champ requis dans la meme version majeure ;
- un rapport sans `schema_version` est traite comme artefact legacy pre-schema, utile comme baseline historique mais non conforme au contrat versionne `1.0`.

Regles de versioning :

- `1.0` introduit le premier contrat canonique versionne ;
- increment mineur `1.x` pour ajouts backward-compatible, par exemple champs optionnels documentes ;
- increment majeur `2.0` pour changements cassants, par exemple suppression, renommage ou changement de type d'un champ requis ;
- la semantique `WARNING_ONLY`, `runtime_execution: DISABLED` et `mutation: DISABLED` ne doit pas changer par simple increment mineur.

## 11_KEY_DECISIONS

- Deriver le schema du rapport reel observe plutot que d'un schema theorique completement abstrait.
- Introduire `schema_version` dans le contrat cible sans pretendre qu'il est deja present dans l'artefact legacy observe.
- Garder le schema minimal et centre sur les champs deja etablis.
- Exiger `level`, `code` et `message` pour chaque finding non vide.
- Garder le contrat semantique strictement warning-only.

## 12_INVARIANTS

- `mode` doit rester `WARNING_ONLY` ;
- `runtime_execution` doit rester `DISABLED` ;
- `mutation` doit rester `DISABLED` ;
- `findings_count` doit etre coherent avec `len(findings)` ;
- `findings` doit etre une liste ;
- chaque finding doit contenir `level`, `code`, `message` ;
- aucun champ ne doit introduire runtime, auto-fix ou mutation ;
- aucun workflow, validateur, policy YAML, runtime, service, secret ou index global n'est modifie par ce child.

## 13_ESTABLISHED

Etat etabli a partir des preuves reelles et du parent :

- le rapport JSON warning-only existe deja ;
- l'artefact reel de reference est `openclaw-skill-policy-report.json` ;
- le run reel de reference est `25956668749` ;
- les champs reels deja observes sont `validator`, `policy_path`, `mode`, `runtime_execution`, `mutation`, `findings_count`, `findings` ;
- l'artefact observe a `findings_count: 0` et `findings: []` ;
- le present child fixe le schema canonique cible en ajoutant `schema_version` pour la suite versionnee.

## 14_HYPOTHESIS

Hypotheses a valider ensuite :

- certains findings futurs auront besoin de champs optionnels supplementaires comme `path`, `line`, `column` ou `hint` ;
- un formalisme plus strict de type JSON Schema pourra etre utile dans un child ulterieur ;
- un dashboard, un registry ou un collector pourra exiger des garanties supplementaires sur les enums de `level` et la stabilite des `code` ;
- un echantillonnage multi-samples sera utile pour couvrir des findings non nuls.

## 15_REMAINING_GAP

- le schema est defini documentalement, pas encore materialise dans un fichier formel machine-readable ;
- `schema_version` n'est pas encore present dans l'artefact legacy reel observe ;
- les champs optionnels possibles des findings ne sont pas encore normalises ;
- la liste canonique des codes de findings n'est pas encore definie ;
- aucun validateur de schema distinct n'existe encore.

## 16_TODO

Suite logique :

1. Revoir et accepter ce contrat canonique minimal.
2. Ouvrir un child si un fichier de schema machine-readable devient necessaire.
3. Ouvrir un child si une taxonomie canonique des finding codes devient necessaire.
4. Ouvrir un child si des exemples multi-samples doivent etre documentes.

## 17_RESUME_POINT

Reprendre ici :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01
```

Point de reprise concret :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_POLICY_REPORT_SCHEMA_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_JSON_SCHEMA_01.md
```
