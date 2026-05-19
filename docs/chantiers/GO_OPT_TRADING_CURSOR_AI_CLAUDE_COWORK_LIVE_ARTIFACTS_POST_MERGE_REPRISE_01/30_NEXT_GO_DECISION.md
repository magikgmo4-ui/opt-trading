# 30_NEXT_GO_DECISION

## Prochain GO retenu

**`GO_OPT_TRADING_CURSOR_AI_MACHINE_MAP_STALE_LINES_REVIEW_01`**

## Justification

- Les branches ALERT_WEBHOOK_TEMPLATE et PARENT_CLOSEOUT doivent encore etre mergees (P1).
- Mais le merge direct est trivial (les branches sont rebasees, contenu doc-only).
- Le chantier le plus utile maintenant est le nettoyage de la map cursor-ai :
  - Annoter les lignes doc-ops devenues historiques (ACTIVE_GOVERNANCE_CLOSEOUT_REVIEW, CONTINUITY_ALIGNMENT, INDEX_AGGREGATION_BATCH — toutes deja supprimees)
  - Marquer OPEN_WORK_CONTROL comme BLOCKED
  - Marquer les branches merged comme merged
  - Garder les references audit Git comme REFERENCE

## Alternative

Si l'utilisateur prefere finir completement avant de nettoyer :
- `GO_OPT_TRADING_CURSOR_AI_CLAUDE_COWORK_LIVE_ARTIFACTS_POST_MERGE_REPRISE_01` → **PASS** (ce GO)
- Puis merge ALERT_WEBHOOK + PARENT_CLOSEOUT
- Puis cleanup map

## Regle

Rester sur cursor-ai. Ne pas ouvrir admin-trading.
