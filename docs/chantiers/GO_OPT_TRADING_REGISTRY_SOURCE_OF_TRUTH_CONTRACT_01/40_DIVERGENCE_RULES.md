---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: DIVERGENCE_RULES
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 40_DIVERGENCE_RULES

## Canonical divergence rule

Si fallback local != registry centrale, la registry centrale gagne.

## Expected handling by class

### 1. Reader can read central registry

- utiliser la valeur centrale
- ignorer la copie locale
- emettre un warning seulement si la divergence est encore visible pour l'operateur

### 2. Reader cannot read central registry, but a documented fallback exists

- basculer en mode degrade read-only
- marquer la source comme fallback/non canonique
- interdire toute interpretation comme ecriture autoritaire

### 3. Central registry missing or invalid and no documented fallback exists

- fail fast
- considerer l'etat comme `BLOCKED_WITH_REASON`

## Divergence workflow

1. constater la divergence
2. classer la copie locale comme derivee ou fallback
3. corriger ensuite la copie locale ou la regeneration, pas la verite centrale a l'aveugle
4. ouvrir un GO d'implementation si la divergence revele un manque de modele

## Special case: `deepseek_student`

Le cas n'est pas une divergence de donnees entre deux registries.

C'est un trou de modelisation central volontaire.

La resolution doit passer par un GO dedie de statut/placement, pas par une reinjection opportuniste dans un fallback local.
