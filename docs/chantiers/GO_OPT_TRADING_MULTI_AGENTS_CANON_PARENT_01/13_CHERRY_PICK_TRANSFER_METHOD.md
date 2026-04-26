---
doc_id: OPT_TRADING_MULTI_AGENTS_CHERRY_PICK_TRANSFER_METHOD_01
doc_type: cherry_pick_transfer_method
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: method
created_at: 2026-04-26
updated_at: 2026-04-26
topic_keys:
  - opt-trading
  - multi_agents
  - git
  - cherry_pick
  - branch_sync
  - transfer
  - agent_procedure
  - ide_procedure
  - governance
search_tags:
  - surface:chantier
  - doc_role:cherry_pick_transfer_method
  - git:cherry_pick
  - transfer:selective
  - agent_procedure:required
  - ide_procedure:required
  - governance:multi_agents_doctrine
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "BUNDLE_IDE_CHERRY_PICK_TRANSFER_METHOD.txt"
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/02_AGENT_SKILL_PROVIDER_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/CHERRY_PICK_INVENTORY_TEMPLATE.md
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BUNDLE_IDE_CHERRY_PICK_TRANSFER_METHOD.txt
---

# 13_CHERRY_PICK_TRANSFER_METHOD — Multi-agents / IDE / Git transfer

## 1. Objet

Canoniser la méthode `cherry-pick inventory` comme procédure de travail transverse pour les branches agents / IDE / multi-machines.

Cette méthode sert à préparer le transfert sélectif de commits depuis une branche source vers une branche cible, sans fusionner toute la branche et sans reconstruire l'inventaire à la fin du chantier.

## 2. Verdict intégré

La méthode cherry-pick doit faire partie des méthodes de travail, mais pas seulement comme astuce Git.

Elle doit être traitée comme une procédure conjointe entre :

| Couche | Rôle |
|---|---|
| Matrice gouvernante | fixe la règle durable |
| Matrice multi-agents | dit quels agents doivent produire l'inventaire |
| Procédures IDE / agents | impose l'inventaire pendant l'exécution |
| Git workflow | fournit les commandes reproductibles |
| Continuité parent | garde le point de reprise et les commits transférables |
| Indexation / inbox | trace les lots prêts à être repris ou agrégés |

Le chantier `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` est la bonne surface pour préparer cette méthode, car son objectif est déjà d'aligner agents, skills, providers, prompts, bundles, index, naming, frontmatter et search tags dans la matrice gouvernante et opérationnelle.

## 3. Définition canonique

```text
Cherry-pick inventory = Git transfer method / prepared selection layer
```

Ce n'est pas :

- un agent ;
- un skill autonome ;
- un provider ;
- une gouvernance ;
- un orchestrateur ;
- un closeout ;
- un index global.

C'est une méthode de transfert Git sélectif que les agents, IDE et opérateurs doivent alimenter pendant le travail.

## 4. Place dans la matrice agents / skills / providers

À relier à `02_AGENT_SKILL_PROVIDER_MATRIX.md` comme couche transverse :

| Surface | Type canonique | Rôle valide | Entrée | Sortie | Limite |
|---|---|---|---|---|---|
| `CHERRY_PICK_INVENTORY.md` | Git transfer method | préparer la reprise sélective de commits | branche source + base + commits | commande cherry-pick prête + validations | ne remplace pas closeout, index global ou décision de merge |

La séparation canonique reste :

```text
Doctrine != Agent != Skill != Provider != Orchestrateur != Deployer != Prompt Generator != Bridge
```

Ajout de lecture :

```text
Cherry-pick inventory != Agent != Skill != Provider != Orchestrateur
```

## 5. Place dans la doctrine frontmatter / naming / search tags

Doc type recommandé :

```yaml
doc_type: cherry_pick_inventory
```

Topic keys recommandés :

```yaml
topic_keys:
  - git
  - cherry_pick
  - transfer
  - branch_sync
  - multi_agents
```

Search tags recommandés :

```yaml
search_tags:
  - git:cherry_pick
  - transfer:selective
  - doc_role:cherry_pick_inventory
  - agent_procedure:required
  - ide_procedure:required
```

Surface recommandée par chantier :

```text
docs/chantiers/<GO_ID>/CHERRY_PICK_INVENTORY.md
```

Surface template pour ce parent :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/CHERRY_PICK_INVENTORY_TEMPLATE.md
```

## 6. Phase à ajouter au plan opérationnel

Phase recommandée :

```text
Phase H — Cherry-pick readiness / transfert sélectif Git
```

Critères :

- chaque branche agent/IDE doit pouvoir produire un inventaire ;
- chaque commit transférable doit être listé ;
- chaque commit doit avoir rôle, dépendance, fichiers touchés, statut ;
- les exclusions doivent être documentées ;
- la commande `git cherry-pick ...` doit être prête ;
- une variante `git cherry-pick -n ...` doit être prévue pour les cas partiels ;
- le test sur branche temporaire doit être obligatoire avant propagation.

## 7. Méthode proposée

### Nouveau fichier canonique recommandé

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/13_CHERRY_PICK_TRANSFER_METHOD.md
```

Contenu attendu :

```md
# 13_CHERRY_PICK_TRANSFER_METHOD

## Objet
Méthode de préparation cherry-pick pour branches agents / IDE / multi-machines.

## Principe
Tout travail produit par Codex, Claude, Trae, OpenClaw ou autre agent/IDE doit pouvoir être transféré sélectivement par commit propre.

## Fichier obligatoire par chantier
CHERRY_PICK_INVENTORY.md

## Champs obligatoires
- branche source
- branche cible
- base commit
- commits à reprendre
- ordre
- rôle
- dépendances
- fichiers touchés
- exclusions
- risques de conflit
- commande prête
- validation après pick
- statut PASS/FAIL

## Commandes minimales
git log --oneline <base>..HEAD
git diff --name-status <base>..HEAD
git show --name-status --oneline <sha>
git cherry-pick <sha1> <sha2>
git cherry-pick -n <sha1> <sha2>
```

## 8. Structure d'inventaire standard

Fichier standard :

```text
docs/chantiers/<GO_ID>/CHERRY_PICK_INVENTORY.md
```

Template :

```md
# CHERRY_PICK_INVENTORY — <GO_ID>

## Branche source
<source_branch>

## Branche cible prévue
sot/mainline

## Base observée
<base_sha>

## Commits à reprendre

| Ordre | SHA | Message | Rôle | Dépendance | Statut |
|---|---|---|---|---|---|
| 01 | <sha> | <message> | doc / impl / test / fix | aucune | prêt |
| 02 | <sha> | <message> | impl | 01 | prêt |

## Fichiers touchés

git diff --name-status <base>..HEAD

## Exclusions

- logs
- caches
- secrets
- fichiers runtime
- données locales
- artefacts temporaires

## Commande cherry-pick prête

git cherry-pick <sha1> <sha2> <sha3>

## Variante sans commit automatique

git cherry-pick -n <sha1> <sha2>

## Validation après transfert

git status --short --branch
git diff --stat origin/sot/mainline..HEAD
git log --oneline -10

## Verdict

- PASS :
- FAIL :
- Gap restant :
```

## 9. Invariants à ajouter aux procédures agents / IDE

1. Un agent qui produit plusieurs commits doit produire un inventaire cherry-pick.
2. Un travail multi-agent ne doit pas dépendre uniquement du nom de branche.
3. Les commits transférables doivent être petits, nommés, ordonnés et testables.
4. Le cherry-pick doit être testé sur une branche temporaire avant intégration.
5. `cherry-pick -n` est la méthode recommandée si les commits mélangent trop de surfaces.
6. Aucun cherry-pick ne doit importer secrets, logs, caches ou fichiers runtime.
7. Un inventaire cherry-pick n'est pas un closeout ; il complète le closeout.
8. Un inventaire cherry-pick n'est pas un index global ; il reste local au chantier.

## 10. Gap réel

Aucune surface existante dédiée à `CHERRY_PICK_INVENTORY` ou `cherry-pick` n'a été trouvée lors de la recherche initiale dans le repo.

Gap concret :

```text
La doctrine multi-agents existe, mais la procédure Git de transfert sélectif par cherry-pick n'est pas encore canonisée.
```

## 11. Patch recommandé

Avant de patcher localement, réaligner la branche si nécessaire :

```bash
git fetch origin
git checkout go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
git pull --rebase origin sot/mainline
```

Créer ou maintenir :

```text
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/13_CHERRY_PICK_TRANSFER_METHOD.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/CHERRY_PICK_INVENTORY_TEMPLATE.md
docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/BUNDLE_IDE_CHERRY_PICK_TRANSFER_METHOD.txt
```

Commit proposé :

```bash
git add docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/
git commit -m "docs: add cherry-pick transfer method to multi-agents canon"
git push
```

Si un push forcé devient nécessaire :

```bash
git push --force-with-lease
```

## 12. GO_PROMPT intégré

```text
GO_OPT_TRADING_MULTI_AGENTS_CHERRY_PICK_TRANSFER_METHOD_01

Mission :
Sur la branche go/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01, ajouter une méthode canonique de préparation cherry-pick pour agents / IDE / branches multi-machines.

Contraintes :
- Doc-only.
- Aucune mutation runtime.
- Aucun patch OpenClaw runtime.
- Ne pas modifier les gros index globaux directement.
- Garder la continuité locale dans docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/.
- Utiliser la doctrine existante : matrice multi-agents, frontmatter/search_tags/naming, operational integration plan.
- Si réalignement requis, utiliser git pull --rebase.
- Si push forcé requis, utiliser git push --force-with-lease.

À faire :
1. Vérifier état Git :
   - git fetch origin
   - git status --short --branch
   - git branch -vv
2. Réaligner la branche sur origin/sot/mainline si nécessaire.
3. Créer :
   - 13_CHERRY_PICK_TRANSFER_METHOD.md
   - CHERRY_PICK_INVENTORY_TEMPLATE.md
4. Mettre à jour :
   - 02_AGENT_SKILL_PROVIDER_MATRIX.md
   - 03_FRONTMATTER_SEARCH_TAGS_NAMING_DOCTRINE.md
   - 05_OPERATIONAL_MATRIX_INTEGRATION_PLAN.md
   - PARENT_STATE.md
   - NEXT.md
5. Ajouter un bloc clair :
   - Cherry-pick inventory = méthode de transfert Git sélectif.
   - Obligatoire pour travaux agents/IDE multi-commits.
   - Non agent, non skill, non provider, non orchestrateur.
6. Produire un closeout court :
   - fichiers touchés ;
   - diff synthétique ;
   - validations Git ;
   - statut PASS/FAIL ;
   - point de reprise.
```

## 13. Point de reprise

Reprise recommandée : utiliser le bundle IDE `BUNDLE_IDE_CHERRY_PICK_TRANSFER_METHOD.txt` pour patcher ou consolider cette méthode localement si une passe IDE est requise.

Statut courant : méthode documentée sur la branche parent, sans mutation runtime.
