---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: reprise_point
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 90_REPRISE_POINT

---

## ÉTAT_INITIAL

GO ouvert le 2026-05-23. Aucun run staging réel effectué.

Stack complète mergée sur sot/mainline :
- Playwright BrowserFn : `modules/vision/coinglass/playwright_capture.py`
- Runner + writer : `modules/vision/coinglass/runner.py`
- AI extraction : `modules/vision/coinglass/ai_extraction.py` (provider=openai)
- Staging validator : `modules/vision/coinglass/staging_validator.py`
- CLI : `scripts/run_vision_capture.py`
- Telegram sender : `modules/vision/coinglass/telegram_sender.py`
- Desk Pro panel : `modules/desk_pro/service/vision_panel.py` + `GET /desk/vision`

---

## RUNS_EFFECTUÉS

```yaml
runs_effectués: 1
runs_pass: 0
runs_fail: 1
dernier_run: "2026-05-23T10:26:57Z"
validate_ok: false
desk_pro_ok: ~
```

---

## BLOCAGES_RENCONTRÉS

### BLOCAGE_1 — URL obsolète + bot detection (2026-05-23)

```text
Symptôme :
  Run 1 → screenshot 10KB → 404 Not Found nginx
  AI extraction : 0 detections (page vide)

Cause 1 — URL obsolète :
  modules/vision/coinglass/headless_capture.py hardcode :
    COINGLASS_LIQUIDATIONS_URL = "https://www.coinglass.com/LiquidationData"
  Coinglass a déplacé cette page :
    301 → https://www.coinglass.com/liquidations
  Curl (-L) confirme HTTP/2 200 sur /liquidations.

Cause 2 — Bot detection CloudFront :
  Playwright (headless Chromium) reçoit 404 après le redirect.
  curl avec ou sans User-Agent reçoit HTTP 200.
  CloudFront détecte le headless browser et sert une page 404.

Impact :
  Abort criterion met : Playwright ne peut pas charger coinglass.com.

Fix requis :
  1. Mettre à jour COINGLASS_LIQUIDATIONS_URL → /liquidations dans headless_capture.py
  2. Ajouter args anti-détection dans playwright_capture.py (--disable-blink-features=AutomationControlled, user-agent réel)
  3. Valider que la page charge correctement avant relancer les 3 runs
```

---

## PROCHAINE_ACTION

```text
1. Merger patch URL + anti-bot Playwright (child GO ou PR standalone)
2. Vérifier capture test isolé : python -c "from modules.vision.coinglass.playwright_capture import ..."
3. Relancer les 3 runs staging selon 10_RUNBOOK_STAGING.md
4. Remplir 20_RUN_EVIDENCE.md au fil des runs
5. Remplir 30_ACCEPTANCE_REPORT.md après --validate PASS
```
