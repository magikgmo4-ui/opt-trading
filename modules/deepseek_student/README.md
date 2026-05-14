# MODULE DEEPSEEK STUDENT (INCOMPLET)

⚠️ **ATTENTION : CE MODULE N'EST PAS LA SOURCE DE VÉRITÉ RUNTIME ACTUELLE.**

## ÉTAT DU RUNTIME (2026-03-12)
La logique active de la machine `student` (IA, Reporting, Logs) se trouve actuellement dans :
👉 **`scripts/student/`** (à la racine du repo)

Le workspace canonique cible est désormais :
👉 **`student/scripts/`** (PR #340, audit DEEPSEEK impl_01)

Ce module (`modules/deepseek_student/`) est une structure standard en attente de migration/consolidation.
Il ne contient **PAS** les scripts de production (`daily-ai-report`, etc.).

## CONSIGNES DE MAINTENANT
1. **NE PAS DÉPLOYER** ce module en pensant remplacer l'existant.
2. **NE PAS SUPPRIMER** le dossier `scripts/student/` tant que les callers (post_change.sh, deepseek_hub) n'ont pas été vérifiés.
3. Pour toute intervention sur le reporting IA, voir `scripts/student/` (legacy) ou `student/scripts/` (canonique) selon la machine.
4. Voir `student/scripts/MIGRATION_STATUS.md` pour l'état de la migration.

## Statut de famille
- `deepseek_student` reste une cible de transition / consolidation
- il n'est pas la verite runtime actuelle
- le candidat module unifie le plus avance est `deepseek_hub`
- `deepseek_response` et `deepseek_thinking` restent des satellites de compatibilite
