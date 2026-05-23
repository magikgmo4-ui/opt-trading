---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: run_evidence
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 20_RUN_EVIDENCE

Remplir pendant les 3 runs staging réels.

---

## RUN_1

```yaml
timestamp_run: ~
screenshot_ts: ~
freshness_state: ~
detections_count: ~
detections:
  - detected_metric_type: ~
    extracted_value: ~
    unit: ~
    confidence: ~
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_~.png
  normalized: data/vision/coinglass/normalized/vision_~.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne N)
run_pass: ~   # true / false
run_fail_reason: ~
```

---

## RUN_2

```yaml
timestamp_run: ~
screenshot_ts: ~
freshness_state: ~
detections_count: ~
detections:
  - detected_metric_type: ~
    extracted_value: ~
    unit: ~
    confidence: ~
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_~.png
  normalized: data/vision/coinglass/normalized/vision_~.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne N)
run_pass: ~
run_fail_reason: ~
```

---

## RUN_3

```yaml
timestamp_run: ~
screenshot_ts: ~
freshness_state: ~
detections_count: ~
detections:
  - detected_metric_type: ~
    extracted_value: ~
    unit: ~
    confidence: ~
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_~.png
  normalized: data/vision/coinglass/normalized/vision_~.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne N)
run_pass: ~
run_fail_reason: ~
```

---

## VALIDATE_OUTPUT

```text
Commande :
VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate --required 3

Sortie :
[à coller ici]

Exit code : ~
```

---

## DESK_PRO_CHECK

```text
curl http://127.0.0.1:8010/desk/vision
[à coller la réponse JSON]

ok: ~
age_hours: ~
```

---

## TELEGRAM_CHECK (si --send utilisé)

```text
Message reçu : oui / non
Timestamp : ~
```
