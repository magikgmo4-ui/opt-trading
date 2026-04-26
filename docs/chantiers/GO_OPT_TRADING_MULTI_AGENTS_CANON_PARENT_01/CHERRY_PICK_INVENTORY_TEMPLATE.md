---
doc_id: OPT_TRADING_MULTI_AGENTS_CHERRY_PICK_INVENTORY_TEMPLATE_01
doc_type: cherry_pick_inventory_template
repo: opt-trading
project: opt-trading
module: multi_agents
go_id: GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01
status: open
lifecycle_stage: template
created_at: 2026-04-26
updated_at: 2026-04-26
topic_keys:
  - opt-trading
  - multi_agents
  - git
  - cherry_pick
  - branch_sync
  - transfer
  - template
search_tags:
  - surface:chantier
  - doc_role:cherry_pick_inventory_template
  - git:cherry_pick
  - transfer:selective
  - template:agent_ide
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "13_CHERRY_PICK_TRANSFER_METHOD.md"
links:
  - docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/13_CHERRY_PICK_TRANSFER_METHOD.md
---

# CHERRY_PICK_INVENTORY_TEMPLATE — <GO_ID>

## Objet

Template standard pour préparer un transfert sélectif Git par `cherry-pick`.

À copier dans chaque chantier concerné sous :

```text
docs/chantiers/<GO_ID>/CHERRY_PICK_INVENTORY.md
```

## 1. Identité du chantier

| Champ | Valeur |
|---|---|
| GO_ID | `<GO_ID>` |
| Owner logique | `<agent / IDE / humain / machine>` |
| Type de chantier | `<doc-only / impl / test / refactor / mixed>` |
| Branche source | `<source_branch>` |
| Branche cible prévue | `sot/mainline` |
| Base observée | `<base_sha>` |
| Date | `<YYYY-MM-DD>` |
| Statut | `<draft / ready / tested / blocked / applied>` |

## 2. Intention de transfert

Décrire en 3 à 8 lignes ce qui doit être repris et pourquoi.

```text
<résumé court du transfert>
```

## 3. Commits à reprendre

| Ordre | SHA | Message | Rôle | Dépendance | Statut | Note |
|---|---|---|---|---|---|---|
| 01 | `<sha>` | `<message>` | `<doc / impl / test / fix>` | aucune | `<ready>` | `<note>` |
| 02 | `<sha>` | `<message>` | `<doc / impl / test / fix>` | 01 | `<ready>` | `<note>` |

## 4. Commits exclus

| SHA | Message | Raison exclusion |
|---|---|---|
| `<sha>` | `<message>` | `<logs / secrets / local-only / mixed / superseded>` |

## 5. Fichiers touchés par la branche

Commande source :

```bash
git diff --name-status <base_sha>..HEAD
```

Résultat attendu :

```text
<coller la sortie réelle ici>
```

## 6. Fichiers touchés par commit

Commande source :

```bash
git show --name-status --oneline <sha>
```

Résultat par commit :

```text
<sha> <message>
M path/to/file
A path/to/file
```

## 7. Exclusions obligatoires

Ne pas importer par cherry-pick :

- secrets ;
- `.env` ;
- logs ;
- caches ;
- artefacts temporaires ;
- fichiers runtime locaux ;
- données générées ;
- fichiers spécifiques machine non documentés.

## 8. Risques de conflit

| Surface | Risque | Mitigation |
|---|---|---|
| `<path>` | `<low / medium / high>` | `<action>` |

## 9. Commande cherry-pick prête

```bash
git fetch origin
git checkout <target_branch>
git pull --rebase
git checkout -b test/cherry-pick-<GO_ID>
git cherry-pick <sha1> <sha2> <sha3>
```

## 10. Variante sans commit automatique

À utiliser si les commits mélangent plusieurs surfaces ou si une sélection partielle est nécessaire.

```bash
git fetch origin
git checkout <target_branch>
git pull --rebase
git checkout -b test/cherry-pick-<GO_ID>
git cherry-pick -n <sha1> <sha2>
git status --short
git diff --stat
git add -p
git commit -m "<message>"
```

## 11. Validation après transfert

```bash
git status --short --branch
git log --oneline -10
git diff --stat origin/sot/mainline..HEAD
```

Ajouter les tests spécifiques du chantier :

```bash
<commande test / smoke / sanity>
```

## 12. Verdict

| Critère | Statut | Note |
|---|---|---|
| Cherry-pick appliqué | `<PASS/FAIL>` |  |
| Conflits résolus | `<PASS/FAIL/NA>` |  |
| Exclusions respectées | `<PASS/FAIL>` |  |
| Tests exécutés | `<PASS/FAIL>` |  |
| Diff borné | `<PASS/FAIL>` |  |
| Prêt pour PR / intégration | `<PASS/FAIL>` |  |

## 13. Point de reprise

```text
<état exact où reprendre>
```

## 14. Notes opérateur

```text
<notes libres, uniquement si utiles>
```
