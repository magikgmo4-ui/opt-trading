---
doc_id: HEADLESS_CLOSEOUT_01_LIMITS
doc_type: limits_backlog
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CHILD_BOT_VISION_HEADLESS_CLOSEOUT_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-04
---

# 60_LIMITS_AND_BACKLOG

## Limites

| Limite | Impact | Mitigation |
| --- | --- | --- |
| Playwright/Chromium dependency | ~500 MB disk, npm required | Accepte |
| 10 min interval minimal | Pas de capture en temps reel | Suffisant pour analyse H1 |
| Web page dependency | Si TradingView change layout → OCR degrade | Observer |
| OCR quality variable | .md/.txt peuvent etre peu lisibles | bot_vision_step2 (OpenAI Vision) en fallback |
| Single URL profile | Un seul dashboard capture | Ajouter plus de profils si besoin |
| Stabilitе long terme non observee | Chromium memory leak possible | systemd oneshot limite l'impact |

## Backlog

| GO | Priorite | Description |
| --- | --- | --- |
| STABILITY_WINDOW_01 | P2 | Observer stabilite sur 24-48h |
| DASHBOARD_MONITORING | P3 | Dashboard sante timers/captures |
| WEBHOOK_RUNTIME_REVIEW_01 | P2 | Audit webhook runtime |
| DESK_PRO_SHARED_REFRESH_01 | P3 | Rafraichir /shared/desk_pro/latest/ |
| PROFILES_EXPANSION | P3 | Ajouter plus de profils de capture |
| ADMIN_TRADING_PARENT_CLOSEOUT | P3 | Closeout parent machine admin-trading |
