---
doc_id: BUNDLE_CURSOR_AI_OPERATOR_REPRISE_PACKET_01
doc_type: bundle/reprise_packet
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_reprise
links:
  - docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/40_OPERATOR_REPRISE_PACKET.md
  - bundles/ACTIVE_WORKFLOW.md
---

# CURSOR_AI_OPERATOR_REPRISE_PACKET

Point de reprise rapide operateur cursor-ai.

## Reprise

```bash
git fetch origin --prune && git checkout sot/mainline && git pull --rebase origin sot/mainline
git log --oneline -1  # attendu : 03fe829 ou descendant
```

## Lecture prioritaire

1. `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` → bloc CURSOR_AI
2. `bundles/claude-artifacts/PROMPT_TEMPLATES.md` → prompts standard
3. `bundles/OPERATOR_FLOW.md` → flux de creation bundle
4. `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/40_OPERATOR_REPRISE_PACKET.md` → packet complet

## Etat

- [x] Claude artifacts operator pack : integre
- [x] Bundles : workflow actif
- [x] Pre-admin gate spec : integree
- [x] alert_webhook : ACTIVE_CONTINUITY
- [x] admin-trading : ferme
- [x] Runtime : non modifie

## A ne jamais faire

- Modifier runtime (hors docs/, bundles/)
- Committer secrets, .env, tokens
- Ouvrir admin-trading sans "chantier pour admin-trading"
- Fermer alert_webhook ou Bundles produit
