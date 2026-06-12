# OT-MODULE-06 — VALIDATED_PROMPT_FACTORY (OPERATOR RUNBOOK) — REPORT

Date (America/Montreal) : 2026-03-14

## 1. RÉSUMÉ EXÉCUTIF
- Runbook opérateur minimal stabilisé, aligné avec les wrappers globaux validés (`cmd-validated_prompt_factory`, `sanity-validated_prompt_factory`).
- Support canonique retenu : `modules/validated_prompt_factory/README.md` (évite la multiplication documentaire).
- Runbook focalisé : quand utiliser / quand ne pas utiliser, parcours nominal, cas standard (max 3), outputs, erreurs attendues.

## 2. ÉTAT RÉEL ÉTABLI (POST MODULE_05)
- Wrappers locaux validés sur Linux cible.
- Wrappers globaux `/usr/local/bin/*validated_prompt_factory*` validés sur Linux cible (cmd + sanity).
- `menu` : résout correctement mais reste interactif (preuve non-interactive non pertinente).

## 3. SUPPORT CANONIQUE RETENU
- Canon : `modules/validated_prompt_factory/README.md`
- Motif : doc unique, courte, exploitable par opérateur, sans nouveau fichier runbook redondant.

## 4. RUNBOOK FINAL (BLOC AJOUTÉ / MODIFIÉ)
Voir `README.md` section : “Runbook opérateur (canonique, minimal)” + “Erreurs attendues / lecture rapide”.

## 5. KANBAN
- OT-MODULE-06 ajouté en CLOSE (PASS).
- Point de reprise basculé : GO_OT_MODULE_07_VALIDATED_PROMPT_FACTORY_MENU_INTERACTIVE_CHECK.

## 6. POINT DE REPRISE EXACT
> **GO_OT_MODULE_07_VALIDATED_PROMPT_FACTORY_MENU_INTERACTIVE_CHECK**


## RISKS

- À qualifier.
