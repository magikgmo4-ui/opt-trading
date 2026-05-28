---
doc_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01_DEDUP_AUDIT_PROTOCOL
doc_type: audit_protocol
repo: opt-trading
project: opt-trading
module: code_ops
go_id: GO_CODE_OPS_OPT_TRADING_PARENT_REFACTOR_NORMALIZATION_01
status: open
lifecycle_stage: audit
topic_keys: [dedup, anti_doublon, refactor, code_ops]
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-20
---

# 30_DEDUP_AUDIT_PROTOCOL

## Objectif

Qualifier les doublons avant allègement.

L'anti-doublon doit éviter deux erreurs :

1. supprimer un fichier encore consommé ;
2. fusionner deux variantes qui ont des contrats différents.

## Catégories de doublons

| Catégorie | Définition | Action par défaut |
|---|---|---|
| `EXACT_DUPLICATE` | contenu identique ou quasi identique | consolidation candidate |
| `FUNCTIONAL_DUPLICATE` | même rôle, implémentation différente | audit consommateur |
| `CONTRACT_DUPLICATE` | même entrée/sortie, logique proche | extraction helper possible |
| `WRAPPER_VARIANT` | wrapper spécifique shell/machine | garder si compatibilité justifiée |
| `LEGACY_REPLACED` | ancien outil remplacé par canonique | déprécier puis supprimer plus tard |
| `FALSE_POSITIVE` | nom proche, rôle différent | garder séparé |
| `UNKNOWN` | preuve insuffisante | bloquer décision |

## Signaux de duplication

- noms proches ;
- mêmes arguments CLI ;
- mêmes imports ;
- mêmes sorties JSON ;
- mêmes chemins d'artefacts ;
- mêmes runbooks ;
- mêmes tests copiés ;
- logique répétée dans plusieurs scripts ;
- wrappers Bash/PowerShell non alignés ;
- validateurs proches.

## Méthode de preuve

Chaque doublon suspect doit avoir :

| Preuve | Requis |
|---|---:|
| chemins concernés | oui |
| rôles réels | oui |
| consommateurs | oui |
| différences d'interface | oui |
| tests existants | oui |
| remplacement proposé | si fusion |
| risque | oui |
| décision | oui |

## Matrice de décision

| Cas | Décision |
|---|---|
| Même contenu + même contrat + mêmes consommateurs | fusion candidate |
| Même logique + sorties différentes | extraction helper candidate |
| Même nom + rôle différent | false positive |
| Wrapper OS spécifique | garder séparé mais normaliser contrat |
| Ancien script non consommé + remplaçant testé | deprecate candidate |
| Consommateurs inconnus | blocked |

## Rapport attendu

```text
docs/chantiers/GO_CODE_OPS_OPT_TRADING_CHILD_DEDUP_AUDIT_01/
  00_INITIAL_PROJECT_DOC.md
  10_DUPLICATE_CANDIDATES.md
  20_CONSUMER_MAP.md
  30_DECISION_TABLE.md
  40_SAFE_MERGE_CANDIDATES.md
  50_BLOCKED_OR_RISKY_CASES.md
```

## Format décisionnel

| duplicate_group | files | category | canonical_candidate | evidence | risk | decision | next_go |
|---|---|---|---|---|---|---|---|

## Règles de non-suppression

Suppression interdite si :

- aucun test ne couvre le remplaçant ;
- consommateur inconnu ;
- chemin mentionné dans un runbook ;
- sortie JSON différente ;
- comportement shell différent ;
- dépendance CI possible ;
- fichier utilisé par une machine spécifique.

## Ordre recommandé

1. détecter ;
2. classer ;
3. prouver consommateurs ;
4. choisir canonique ;
5. ajouter test si absent ;
6. déprécier ;
7. supprimer seulement dans un batch ultérieur.

## Invariants

- `DUPLICATE_SUSPECT` ne veut pas dire suppression.
- Un wrapper Windows et un wrapper Bash peuvent être deux variantes légitimes.
- La compatibilité peut justifier la duplication contrôlée.
- Toute suppression doit avoir un commit séparé et réversible.
