---
doc_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
doc_type: chantier_child_spec
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
chantier_parent: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: child_opening
surface: docs/chantiers
source_kind: canonical_child
updated_at: 2026-05-09
topic_keys:
  - openclaw
  - runtime_security
  - permission_matrix
  - skill_permissions
  - warning_only
  - audit
  - why
links:
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
---

# GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01

## 1_MASTER_TARGET

Produire la matrice concrete des permissions runtime OpenClaw pour `opt-trading`.

La matrice doit transformer le principe general de securite runtime en regles operatoires utilisables par les futurs skills, workers, agents, routers et superviseurs.

## 3_INITIAL_NEED

Le parent `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` a etabli que l'orchestration OpenClaw doit etre explicable, tracable, bornee et non destructive par defaut.

Besoin du child : definir concretement qui peut faire quoi, sur quelle surface, avec quelle confirmation, quelle journalisation, quelle limite et quelle condition de promotion.

## 5_GO_PLAN

Parent :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

Child :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```

Branche :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```

Scope initial : documentation uniquement.

## 6_FINAL_TARGET

**FINAL_TARGET : produire une matrice concrete des permissions runtime OpenClaw pour `opt-trading`, couvrant les niveaux d'action, les surfaces d'execution, les permissions par defaut, les confirmations humaines requises, les logs d'audit, les interdits par defaut, la politique warning-only et les conditions de promotion vers execution.**

## WHY

Ce child existe pour transformer le principe de securite runtime en regles operatoires concretes.

Le parent dit pourquoi securiser.

Ce child dit :

- qui peut faire quoi ;
- ou l'action peut etre appliquee ;
- comment elle doit etre tracee ;
- quand l'humain doit confirmer ;
- quelles actions restent seulement proposees ;
- quelles actions sont interdites par defaut ;
- quelles conditions permettent une promotion vers execution.

Sans cette matrice, OpenClaw risque de confondre capacite technique et permission operationnelle.

## 7_CANONICAL_STATE

Etat valide au demarrage :

- PR parent `#288` mergee ;
- parent disponible dans `docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/` ;
- branche child dediee creee ;
- scope child doc-only ;
- aucune modification runtime autorisee ;
- aucune modification d'index global autorisee ;
- matrice de permissions requise avant implementation.

## 8_VALIDATED_PLAN

Etapes validees :

1. Ouvrir le child depuis le parent merge.
2. Creer ce document dans le dossier du parent.
3. Definir les niveaux d'action.
4. Definir les surfaces d'application.
5. Croiser niveaux x surfaces.
6. Marquer les confirmations humaines.
7. Marquer les besoins d'audit.
8. Marquer les interdits par defaut.
9. Definir les conditions de promotion vers execution.
10. Garder le chantier documentation-only.

## 9_SELECTED_SOLUTION

Solution retenue : matrice par niveaux d'action et surfaces runtime.

Axes :

- niveau de permission ;
- surface cible ;
- autorisation par defaut ;
- confirmation humaine ;
- log d'audit ;
- mode warning-only ;
- interdits ;
- condition de promotion.

## 10_SELECTED_SETUP

Document child unique :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
```

Support Git :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```

## 11_KEY_DECISIONS

- La lecture seule est le defaut.
- Les audits et lints non valides restent warning-only.
- Les patchs peuvent etre proposes avant d'etre appliques.
- L'ecriture doc est moins risquee que l'ecriture code, mais reste bornee.
- L'ecriture code/runtime exige confirmation stricte.
- Les actions services, reseau, Git push, install et system ops sont a risque renforce.
- Les actions destructives sont interdites par defaut.
- Les secrets sont hors perimetre d'exposition.
- Chaque execution future doit produire une trace.

## 12_INVARIANTS

- Read-only par defaut.
- Warning-only par defaut pour lint / audit / analyse non validee.
- Aucun auto-fix sans GO explicite.
- Aucune action destructive sans confirmation humaine explicite et scope valide.
- Aucun secret dans les prompts, logs, specs ou outputs.
- Toute action runtime doit etre liee a un GO, une surface, un niveau de permission et une trace.
- Les index globaux ne sont pas modifies automatiquement.
- Une capacite technique n'est pas une permission operationnelle.

## 13_ESTABLISHED

- Le parent runtime security est merge.
- La matrice de permissions est le premier child logique.
- La phase reste documentaire.
- Les niveaux d'action doivent etre explicites.
- Les surfaces doivent etre explicites.

## 14_HYPOTHESIS

A valider ensuite :

- format YAML ou Markdown machine-readable pour la matrice ;
- integration avec un futur skill registry ;
- liaison aux wrappers `cmd.sh`, `menu.sh`, `sanity_check.sh` ;
- liaison aux services systemd ;
- liaison au gateway OpenClaw ;
- liaison a Telegram comme control plane ;
- audit log central ou local par machine.

## Matrice des niveaux d'action

| Niveau | Nom | Description | Permission par defaut | Confirmation humaine | Audit log | Warning-only |
| --- | --- | --- | --- | --- | --- | --- |
| L0 | READ_ONLY | Lire, lister, inspecter, resumer | Autorise | Non | Recommande | Non requis |
| L1 | ANALYZE | Analyser, detecter, scorer, comparer | Autorise si non destructif | Non | Recommande | Oui par defaut si lint/audit |
| L2 | PLAN | Proposer un plan ou sequence d'actions | Autorise | Non | Recommande | Oui |
| L3 | PROPOSE_PATCH | Produire patch/diff sans appliquer | Autorise avec trace | Non sauf surface sensible | Oui | Oui |
| L4 | WRITE_DOC | Ecrire documentation bornee | Autorise si GO explicite | Oui ou GO explicite | Oui | Non |
| L5 | WRITE_CODE | Modifier code, config runtime ou scripts | Bloque par defaut | Oui strict | Oui obligatoire | Non |
| L6 | EXECUTE_SAFE | Executer commande non destructive | Bloque par defaut | Oui | Oui obligatoire | Non |
| L7 | EXECUTE_RISKY | Service, reseau, Git push, install, system ops | Bloque par defaut | Oui renforce | Oui obligatoire | Non |
| L8 | DESTRUCTIVE | Delete, reset, force, purge, prod action irreversible | Interdit par defaut | Oui explicite + GO dedie | Oui obligatoire | Non |

## Matrice des surfaces runtime

| Surface | Exemples | Niveau max par defaut | Regle |
| --- | --- | --- | --- |
| DOCS | `docs/`, specs, closeouts, inbox | L4 | Ecriture autorisee seulement avec GO ou instruction explicite |
| REPO_CODE | `modules/`, scripts, app code | L3 | Patch propose par defaut ; application exige L5 |
| GIT | branch, commit, push, merge, force-with-lease | L3 | Toute mutation Git exige confirmation ou instruction explicite |
| SERVICES | systemd, tmux, daemons, ports | L2 | Execution bloquee tant que non cadre en GO dedie |
| TELEGRAM | bots, chat control, notifications | L2 | Observation / plan seulement par defaut |
| WORKERS | collectors, analyzers, schedulers | L2 | Pas d'execution autonome sans policy runtime |
| FILESYSTEM | paths, shared folders, generated files | L3 | Lecture ok ; ecriture bornee ; delete interdit par defaut |
| NETWORK | downloads, APIs, outbound calls | L2 | Analyse et plan ; execution exige confirmation |
| SECRETS | tokens, env secrets, credentials | L0 | Ne jamais exposer ; lecture de valeur interdite |
| MACHINE_OPS | installs, permissions, packages, reboot | L2 | Plan seulement par defaut |
| TRADING_RUNTIME | orders, paper/live trade actions, broker calls | L2 | Aucune action ordre sans GO dedie et garde-fous explicites |

## Croisement permissions x surfaces

| Surface | L0 | L1 | L2 | L3 | L4 | L5 | L6 | L7 | L8 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| DOCS | OK | OK | OK | OK | GO/CONFIRM | BLOCK | BLOCK | BLOCK | BLOCK |
| REPO_CODE | OK | OK | OK | OK | BLOCK | CONFIRM_STRICT | BLOCK | BLOCK | BLOCK |
| GIT | OK | OK | OK | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| SERVICES | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| TELEGRAM | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| WORKERS | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| FILESYSTEM | OK | OK | OK | PROPOSE_ONLY | CONFIRM | CONFIRM_STRICT | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| NETWORK | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| SECRETS | METADATA_ONLY | BLOCK_VALUES | PLAN_REDACTION_ONLY | BLOCK | BLOCK | BLOCK | BLOCK | BLOCK | BLOCK |
| MACHINE_OPS | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | CONFIRM_STRICT | CONFIRM_STRICT | BLOCK_DEFAULT |
| TRADING_RUNTIME | OK | OK | PLAN_ONLY | PROPOSE_ONLY | BLOCK | BLOCK | BLOCK_DEFAULT | BLOCK_DEFAULT | BLOCK_DEFAULT |

Legend :

- `OK` : autorise dans le perimetre courant.
- `GO/CONFIRM` : GO explicite ou confirmation humaine.
- `CONFIRM` : confirmation humaine requise.
- `CONFIRM_STRICT` : confirmation humaine explicite + contexte + surface + commande exacte.
- `PROPOSE_ONLY` : produire seulement un plan, patch ou diff.
- `PLAN_ONLY` : aucun patch, seulement plan.
- `METADATA_ONLY` : metadata sans valeur secrete.
- `BLOCK` : interdit dans ce child.
- `BLOCK_DEFAULT` : interdit par defaut, ne peut etre rouvert que par GO dedie.

## Politique warning-only

Warning-only obligatoire pour :

- lint documentaire non valide ;
- audit repo exploratoire ;
- detection d'incoherences ;
- scoring de risque ;
- recherche de secrets sans lecture des valeurs ;
- analyse de chemins ;
- analyse de services ;
- analyse de permissions.

Un warning-only ne doit pas :

- modifier un fichier ;
- appliquer un auto-fix ;
- redemarrer un service ;
- pousser du Git ;
- supprimer un artefact ;
- exposer un secret.

## Confirmation humaine minimale

Pour toute action L5 ou plus, la confirmation doit contenir :

- GO concerne ;
- surface cible ;
- action exacte ;
- commande ou patch exact si applicable ;
- effet attendu ;
- rollback ou mitigation si applicable ;
- preuve post-action attendue.

## Audit log minimal

Toute action L4+ doit produire une trace avec :

- timestamp ;
- GO ;
- machine ou surface ;
- action demandee ;
- acteur ou agent ;
- niveau de permission ;
- fichiers ou services touches ;
- resultat ;
- preuve ou lien de reprise.

## Conditions de promotion vers execution

Une action peut passer de proposition a execution seulement si :

1. un GO explicite couvre l'action ;
2. la surface est identifiee ;
3. le niveau de permission est connu ;
4. le risque est qualifie ;
5. la confirmation humaine est presente si requise ;
6. la trace d'audit est definie ;
7. le rollback ou la mitigation est defini quand applicable ;
8. aucun secret n'est expose ;
9. aucun invariant parent n'est viole.

## 15_REMAINING_GAP

Restant a faire apres cette matrice :

- convertir la matrice en format machine-readable ;
- definir un schema `skill_policy.yaml` ;
- definir les permissions par skill concret ;
- definir une policy par machine ;
- definir les logs d'audit reels ;
- definir les tests de non-destruction ;
- definir le lien avec un futur skill registry.

## 16_TODO

Suite logique :

1. Reviewer cette matrice.
2. Fermer ou merge le child doc.
3. Ouvrir un child dedie au format machine-readable.
4. Produire une premiere policy YAML warning-only.
5. Tester uniquement la validation statique, sans execution runtime.

## 17_RESUME_POINT

Reprendre ici :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01.md
```

Prochain GO logique :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01
```

Objectif prochain : transformer cette matrice Markdown en schema policy exploitable, encore sans execution runtime.

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_PERMISSION_MATRIX
- OPENCLAW_RUNTIME_SECURITY
- OPENCLAW_WARNING_ONLY
- OPENCLAW_AUDIT_LOG
- OPENCLAW_HUMAN_CONFIRMATION
- OPENCLAW_BLOCK_DEFAULT

Blocs a extraire :

- `Matrice des niveaux d'action`
- `Matrice des surfaces runtime`
- `Croisement permissions x surfaces`
- `Politique warning-only`
- `Conditions de promotion vers execution`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- Le child `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01` definit les niveaux L0 a L8 de permissions runtime OpenClaw.
- La lecture seule, le warning-only et la proposition sans execution sont les defauts securises.
- Les actions destructives restent bloquees par defaut.
- Toute execution L5+ exige confirmation humaine, trace d'audit et GO explicite.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_POLICY_SCHEMA_01`.
