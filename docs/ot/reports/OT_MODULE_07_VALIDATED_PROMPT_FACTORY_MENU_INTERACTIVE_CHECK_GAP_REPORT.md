# OT-MODULE-07 — VALIDATED_PROMPT_FACTORY (MENU INTERACTIVE CHECK) — GAP REPORT

Date (America/Montreal) : 2026-03-14

## ÉCARTS PROUVÉS BLOQUANTS
- Néant.

## RÉSERVES (NON BLOQUANTES)
- `expect` absent sur la cible Linux : pas de preuve “TTY interactive” automatisée.
- Le menu utilise `clear` (cosmétique) : capture de logs plus difficile sans neutralisation lors d’un test non-interactif.

## HORS PÉRIMÈTRE
- Redesign du menu.
- Ajout de dépendances (expect).

