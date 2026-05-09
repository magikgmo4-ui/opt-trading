---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-09
topic_keys:
  - openclaw
  - runtime_security
  - policy_schema
  - skill_policy
  - yaml
  - warning_only
  - audit
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01

## 1_MASTER_TARGET

Transformer la matrice Markdown de permissions runtime OpenClaw en schema policy exploitable, encore sans execution runtime.

Le livrable doit fournir une structure canonique suffisamment stable pour devenir ensuite un fichier machine-readable de type `skill_policy.yaml`, tout en restant dans un scope documentation-only.

## 3_INITIAL_NEED

Le child precedent `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01` a defini :

- les niveaux L0 a L8 ;
- les surfaces runtime ;
- le croisement permissions x surfaces ;
- la politique warning-only ;
- les confirmations humaines ;
- les logs d'audit ;
- les conditions de promotion vers execution.

Besoin actuel : convertir cette logique en schema policy reutilisable par les futurs skills, routers, workers et superviseurs OpenClaw.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child source :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```

Child courant :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
```

Branche :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
```

Scope : documentation uniquement.

## 6_FINAL_TARGET

**FINAL_TARGET : produire le schema canonique `skill_policy.yaml` pour OpenClaw runtime security, definissant les champs obligatoires, les types, les valeurs autorisees, les defaults securises, les contraintes d'audit, les confirmations humaines, les interdits et les conditions de promotion, sans encore creer de policy runtime executable.**

## WHY

Ce child existe pour eviter que la matrice de permissions reste seulement lisible par un humain.

Le but est de preparer un contrat policy stable que les composants OpenClaw pourront utiliser plus tard sans ambiguite : skill registry, router, supervisor, workers, checks statiques et validations warning-only.

Sans schema, chaque skill pourrait interpreter les permissions differemment. Le schema force une lecture commune : meme niveaux, memes surfaces, memes confirmations, memes logs, memes interdits.

## 7_CANONICAL_STATE

Etat valide au demarrage :

- PR parent #288 mergee ;
- PR permission matrix #289 mergee ;
- parent disponible dans `docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/` ;
- matrice de permissions disponible ;
- branche child dediee creee ;
- scope doc-only ;
- aucun runtime a modifier ;
- aucun index global a modifier.

## 8_VALIDATED_PLAN

Etapes validees :

1. Reprendre depuis la matrice de permissions.
2. Definir un schema policy YAML canonique.
3. Definir les enums obligatoires.
4. Definir les champs requis.
5. Definir les defaults securises.
6. Definir les contraintes par niveau.
7. Definir les contraintes par surface.
8. Definir les regles d'audit.
9. Definir les regles de confirmation humaine.
10. Definir les validations warning-only.
11. Ne pas produire encore de runtime executable.

## 9_SELECTED_SOLUTION

Solution retenue : schema YAML declaratif.

Le schema cible ne doit pas executer. Il doit seulement decrire :

- l'identite d'un skill ;
- ses surfaces autorisees ;
- son niveau maximal par defaut ;
- ses actions permises ;
- ses actions interdites ;
- ses confirmations requises ;
- ses logs d'audit ;
- ses conditions de promotion ;
- ses limites secrets / filesystem / network / Git / services / trading runtime.

## 10_SELECTED_SETUP

Document child unique :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
```

Fichier cible futur, non cree dans ce child :

```text
configs/openclaw/security/skill_policy.schema.yaml
```

## 11_KEY_DECISIONS

- Le schema est declaratif.
- Le schema n'est pas encore runtime.
- Les defaults sont securises.
- `READ_ONLY`, `ANALYZE`, `PLAN` et `PROPOSE_PATCH` sont les modes par defaut les moins risques.
- Toute mutation L4+ doit declarer audit et confirmation.
- Toute action L5+ doit etre bloquee sans confirmation stricte.
- Toute action L8 reste interdite par defaut.
- Les secrets sont metadata-only ou block-values.

## 12_INVARIANTS

- Documentation-only.
- Aucun runtime.
- Aucun auto-fix.
- Aucun service.
- Aucun secret.
- Aucun index global.
- Warning-only par defaut pour validation statique.
- Une policy valide ne donne pas automatiquement droit a execution.
- La promotion vers execution exige un GO dedie ulterieur.

## 13_ESTABLISHED

- La matrice L0-L8 existe.
- Les surfaces runtime sont definies.
- Les conditions de confirmation humaine sont definies.
- Les logs d'audit minimaux sont definis.
- Le schema policy est la suite logique.

## 14_HYPOTHESIS

A valider ensuite :

- emplacement canonique exact du schema YAML ;
- nom final du fichier `skill_policy.schema.yaml` ;
- compatibilite avec un futur skill registry ;
- compatibilite avec OpenClaw gateway ;
- compatibilite avec wrappers module existants ;
- format JSON Schema possible en derive ;
- validation CI warning-only possible.

## Schema policy cible

Nom cible propose :

```text
skill_policy.yaml
```

Schema logique :

```yaml
policy_version: "0.1"
policy_id: "OPENCLAW_RUNTIME_SECURITY_POLICY"
status: "draft"
default_mode: "READ_ONLY"
warning_only_default: true
runtime_execution_enabled: false

skill:
  id: "string_required"
  name: "string_required"
  owner_go: "GO_ID_required"
  module_path: "string_optional"
  machine_scope:
    - "admin-trading"
    - "db-layer"
    - "student"
    - "cursor-ai"
    - "fantome"

permissions:
  max_default_level: "L0"
  allowed_levels:
    - "L0"
    - "L1"
    - "L2"
    - "L3"
  blocked_levels:
    - "L5"
    - "L6"
    - "L7"
    - "L8"

surfaces:
  docs:
    max_level: "L4"
    requires_go: true
    audit_required_from: "L4"
  repo_code:
    max_level: "L3"
    propose_only: true
    write_requires_confirmation: true
  git:
    max_level: "L3"
    mutation_requires_confirmation: true
    force_operations_blocked_default: true
  services:
    max_level: "L2"
    execution_blocked_default: true
  telegram:
    max_level: "L2"
    send_requires_confirmation: true
  workers:
    max_level: "L2"
    autonomous_execution_enabled: false
  filesystem:
    max_level: "L3"
    delete_blocked_default: true
  network:
    max_level: "L2"
    outbound_requires_confirmation: true
  secrets:
    max_level: "L0"
    values_read_blocked: true
    metadata_only: true
  machine_ops:
    max_level: "L2"
    install_reboot_permission_change_blocked_default: true
  trading_runtime:
    max_level: "L2"
    order_execution_blocked_default: true

confirmation:
  required_from_level: "L5"
  strict_required_from_level: "L6"
  fields_required:
    - "go_id"
    - "surface"
    - "action"
    - "exact_command_or_patch"
    - "expected_effect"
    - "rollback_or_mitigation"
    - "post_action_evidence"

audit:
  required_from_level: "L4"
  fields_required:
    - "timestamp"
    - "go_id"
    - "machine_or_surface"
    - "actor_or_agent"
    - "permission_level"
    - "action_requested"
    - "files_or_services_touched"
    - "result"
    - "resume_link"

promotion:
  requires:
    - "explicit_go"
    - "known_surface"
    - "known_permission_level"
    - "risk_qualified"
    - "confirmation_if_required"
    - "audit_defined"
    - "rollback_if_applicable"
    - "no_secret_exposure"
    - "no_parent_invariant_violation"

validation:
  mode: "warning_only"
  can_fail_ci: false
  can_autofix: false
```

## Enums obligatoires

### `permission_level`

```text
L0_READ_ONLY
L1_ANALYZE
L2_PLAN
L3_PROPOSE_PATCH
L4_WRITE_DOC
L5_WRITE_CODE
L6_EXECUTE_SAFE
L7_EXECUTE_RISKY
L8_DESTRUCTIVE
```

### `surface`

```text
DOCS
REPO_CODE
GIT
SERVICES
TELEGRAM
WORKERS
FILESYSTEM
NETWORK
SECRETS
MACHINE_OPS
TRADING_RUNTIME
```

### `confirmation_mode`

```text
NONE
GO_EXPLICIT
HUMAN_CONFIRM
HUMAN_CONFIRM_STRICT
BLOCK_DEFAULT
BLOCK_ALWAYS
```

### `audit_mode`

```text
NONE
RECOMMENDED
REQUIRED
REQUIRED_STRICT
```

### `validation_mode`

```text
WARNING_ONLY
BLOCKING_STATIC
RUNTIME_GATED
```

## Regles de validation statique warning-only

Une validation statique peut emettre des warnings si :

- un skill n'a pas de `owner_go` ;
- un skill declare L4+ sans audit ;
- un skill declare L5+ sans confirmation ;
- une surface `secrets` autorise autre chose que metadata-only ;
- une surface `git` autorise mutation sans confirmation ;
- une surface `trading_runtime` autorise order execution ;
- `runtime_execution_enabled` vaut `true` dans une phase non validee.

La validation statique ne doit pas :

- modifier les policies ;
- appliquer des auto-fix ;
- bloquer la CI par defaut ;
- lancer un worker ;
- executer une commande.

## Contraintes minimales par niveau

| Niveau | Audit | Confirmation | Execution | Default |
| --- | --- | --- | --- | --- |
| L0 | recommande | non | oui lecture | autorise |
| L1 | recommande | non | oui analyse | autorise |
| L2 | recommande | non | plan seulement | autorise |
| L3 | requis si patch | parfois | propose only | autorise borne |
| L4 | requis | GO ou confirm | docs seulement | borne |
| L5 | requis | stricte | code/config | bloque defaut |
| L6 | requis | stricte | commande safe | bloque defaut |
| L7 | requis strict | stricte | risque renforce | bloque defaut |
| L8 | requis strict | explicite + GO dedie | destructif | interdit defaut |

## 15_REMAINING_GAP

Restant apres ce child :

- creer le fichier schema YAML reel ;
- ajouter une policy sample warning-only ;
- ajouter un validateur statique non bloquant ;
- definir les messages de warning ;
- definir le rattachement au futur skill registry ;
- definir la strategie CI sans blocage ;
- definir une premiere policy pour un skill documentaire non destructif.

## 16_TODO

Suite logique :

1. Reviewer ce schema documentaire.
2. Merge PR du child.
3. Ouvrir le child `POLICY_YAML_DRAFT_01`.
4. Creer le fichier YAML reel, encore non connecte au runtime.
5. Ajouter une policy sample read-only.
6. Ajouter uniquement une validation statique warning-only dans un child ulterieur.

## 17_RESUME_POINT

Reprendre ici :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01.md
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01
```

Objectif prochain : creer le premier fichier YAML de policy, encore sans execution runtime et sans validation bloquante.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_POLICY_SCHEMA
- OPENCLAW_SKILL_POLICY_YAML
- OPENCLAW_RUNTIME_SECURITY
- OPENCLAW_WARNING_ONLY_VALIDATION
- OPENCLAW_NO_RUNTIME_EXECUTION

Blocs a extraire :

- `Schema policy cible`
- `Enums obligatoires`
- `Regles de validation statique warning-only`
- `Contraintes minimales par niveau`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01` transforme la matrice de permissions OpenClaw en schema policy YAML cible.
- Le schema reste declaratif et non runtime.
- `runtime_execution_enabled: false` et `warning_only_default: true` sont les defaults securises.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_YAML_DRAFT_01`.
