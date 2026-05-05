# 00_START — GO_OPT_TRADING_CURSOR_AI_MACHINE_WORK_SPLIT_ANTI_CONFLICT_01

## Reprise Git

- **Date**: 2026-05-05
- **Base**: `origin/sot/mainline`
- **Branche**: `go/GO_OPT_TRADING_CURSOR_AI_MACHINE_WORK_SPLIT_ANTI_CONFLICT_01`
- **Statut working tree**: clean

## Objectif

Attacher la map machine anti-conflit a la continuite existante proche de `BRANCH_STATE` / `BRANCH_PROJECT_MAP` / matrice.

## Besoin initial

Operer depuis plusieurs machines (cursor-ai, admin-trading, db-layer, student, fantome) sans collisions Git en offrant une vue de routage par machine directement interrogeable.

## Plan

1. Creer la fiche index dediee `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
2. Creer l'entree inbox atomique
3. Rattacher a `BRANCH_STATE`, `BRANCH_PROJECT_MAP` et a la matrice
4. Ajouter une ligne courte dans `BRANCH_PROJECT_MAP.md` sans gros remaniement

## Invariants

- Ne pas transformer une branche en chantier actif sans preuve
- Ne pas modifier runtime
- Ne pas promouvoir automatiquement une branche dans `GO_INDEX`
- Une branche Git ne prouve pas seule un chantier actif

## Regle de routage

Quand l'utilisateur demande "chantiers pour <machine>", la reponse doit ressortir le bloc machine correspondant depuis `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.
