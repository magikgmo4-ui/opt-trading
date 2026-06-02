---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01
status: closed
created_at: 2026-05-23
updated_at: 2026-05-23
---

# GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01

## Objectif

Documenter l'acceptance formelle du parent `GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_CONTINUITY_01` après livraison complète PATCH-A1→B2.

Doc-only. Aucun runtime modifié, aucun adapter API Coinglass, aucun send Telegram réel.

## Périmètre

- **IN** : docs acceptance + reprise point + branch state + bundle
- **OUT** : tout code, toute activation runtime, tout index global

## Décisions figées

| Point | Décision |
|---|---|
| Coinglass API | Hors adapter API runtime — permanent |
| Source canonique | `data/vision/coinglass/latest.json` |
| Telegram | Diffusion/summary read-only, pas base de vérité |
| Desk Pro | Consumer read-only via `vision_context_reader.py` |
| Runtime gate | `VISION_BOT_ENABLED=true` requis en staging |
| Staging gate | 3 runs consécutifs PASS avant prod |

## Fichiers créés

| Fichier | Rôle |
|---|---|
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `20_ACCEPTANCE_REPORT.md` | Verdict + bilan tests |
| `90_REPRISE_POINT.md` | Point de reprise pour suite |
| `BRANCH_STATE.md` | État des branches et PRs |
| `docs/index/inbox/...md` | Entrée inbox |
| `bundles/.../` | Bundle transportable |
