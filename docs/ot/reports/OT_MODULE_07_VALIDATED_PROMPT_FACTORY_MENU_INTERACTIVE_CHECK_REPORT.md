# OT-MODULE-07 — VALIDATED_PROMPT_FACTORY (MENU INTERACTIVE CHECK) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Wrapper global `menu-validated_prompt_factory` résout correctement sur Linux cible (`admin-trading`) vers `modules/validated_prompt_factory/menu.sh`.
- Test interactif “pur TTY” non automatisable proprement (pas de `expect` sur la cible).
- Test contrôlé prouvé via injection stdin (sélections `0` puis `5 -> list-modes -> 0`) avec neutralisation de `clear` pour capturer des sorties lisibles.

## 2. ENVIRONNEMENT RÉEL
- Hostname : `admin-trading`
- User : `ghost`
- Shell : `/bin/bash`
- Repo : `/opt/trading`

## 3. RÉSOLUTION DU WRAPPER MENU
- `menu-validated_prompt_factory` : `/usr/local/bin/menu-validated_prompt_factory`
- Cible : `/opt/trading/modules/validated_prompt_factory/menu.sh`
- Cohérence : hash `sha256` identique entre la cible du symlink et `menu.sh`.

## 4. MÉTHODE DE TEST UTILISÉE
### ÉTABLI
- `expect` absent sur la cible (`EXPECT_MISSING`), donc pas d’automatisation TTY robuste.
- Méthode retenue (contrôlée, non-ambiguë) :
  - exécuter le menu en lui fournissant une séquence d’entrées via stdin (`printf`),
  - neutraliser `clear` (cosmétique) via fonction bash exportée,
  - retirer les séquences ANSI pour logs (`sed`).

### À CONFIRMER
- Test manuel opérateur en vrai TTY (SSH interactif) : possible, mais non prouvé ici.

## 5. VERDICT
**PASS (preuve contrôlée)** : le menu s’affiche et exécute un parcours simple (`List Modes`) sur Linux cible.

## 6. POINT DE REPRISE EXACT
> **GO_OT_SESSION_OPENING_DRILL_01**

