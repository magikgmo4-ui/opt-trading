---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: run_evidence
repo: opt-trading
status: pass
created_at: 2026-05-23
---

# 20_RUN_EVIDENCE

---

## RUN_1

```yaml
timestamp_run: "2026-05-23T10:39:16Z"
screenshot_ts: "2026-05-23T10:39:16Z"
freshness_state: fresh
detections_count: 5
detections:
  - detected_metric_type: liquidations_long
    extracted_value: 869.02
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidations_short
    extracted_value: 71.84
    unit: USD
    confidence: 1.00
  - detected_metric_type: long_short_ratio
    extracted_value: 90.99
    unit: "%"
    confidence: 1.00
  - detected_metric_type: open_interest
    extracted_value: 126069243.0
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidation_heatmap_level
    extracted_value: 1.56
    unit: M
    confidence: 1.00
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_20260523_103916.png (260879 bytes)
  normalized: data/vision/coinglass/normalized/vision_20260523_103916.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne 2)
run_pass: true
run_fail_reason: ~
```

---

## RUN_2

```yaml
timestamp_run: "2026-05-23T10:40:19Z"
screenshot_ts: "2026-05-23T10:40:19Z"
freshness_state: fresh
detections_count: 5
detections:
  - detected_metric_type: liquidations_long
    extracted_value: 869.03
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidations_short
    extracted_value: 71.80
    unit: USD
    confidence: 1.00
  - detected_metric_type: long_short_ratio
    extracted_value: 90.99
    unit: "%"
    confidence: 1.00
  - detected_metric_type: open_interest
    extracted_value: 126071099856.0
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidation_heatmap_level
    extracted_value: 1.56
    unit: M
    confidence: 1.00
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_20260523_104019.png (264681 bytes)
  normalized: data/vision/coinglass/normalized/vision_20260523_104019.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne 3)
run_pass: true
run_fail_reason: ~
```

---

## RUN_3

```yaml
timestamp_run: "2026-05-23T10:41:12Z"
screenshot_ts: "2026-05-23T10:41:12Z"
freshness_state: fresh
detections_count: 5
detections:
  - detected_metric_type: liquidations_long
    extracted_value: 869.03
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidations_short
    extracted_value: 71.77
    unit: USD
    confidence: 1.00
  - detected_metric_type: long_short_ratio
    extracted_value: 90.99
    unit: "%"
    confidence: 1.00
  - detected_metric_type: open_interest
    extracted_value: 126037910.715
    unit: USD
    confidence: 1.00
  - detected_metric_type: liquidation_heatmap_level
    extracted_value: 1.56
    unit: M
    confidence: 1.00
fichiers_produits:
  raw: data/vision/coinglass/raw/screenshot_20260523_104112.png (249708 bytes)
  normalized: data/vision/coinglass/normalized/vision_20260523_104112.json
  latest: data/vision/coinglass/latest.json
  events: data/vision/coinglass/events.jsonl (ligne 4)
run_pass: true
run_fail_reason: ~
```

---

## VALIDATE_OUTPUT

```text
Commande :
VISION_BOT_ENABLED=true python scripts/run_vision_capture.py --validate --required 3

Sortie :
[validate] PASS — 3/3 consecutive runs OK
  2026-05-23T10:39:16Z  PASS  5 qualifying detections
  2026-05-23T10:40:19Z  PASS  5 qualifying detections
  2026-05-23T10:41:12Z  PASS  5 qualifying detections

Exit code : 0
```

---

## DESK_PRO_CHECK

```text
curl http://127.0.0.1:8010/desk/vision

ok: true
age_hours: 0.036 (≈ 2 minutes après run 3)
detections: 5
freshness: fresh

/desk/ui contient : <summary>Coinglass Vision</summary>
```

---

## TELEGRAM_CHECK

```text
--send non utilisé pour les runs de validation.
Telegram = confirmation read-only, non requis pour PASS staging.
```

---

## NOTE_BLOCAGE_RESOLU

```text
Run 0 (avant patch) : 404 nginx CloudFront — URL /LiquidationData obsolète.
Fix PR #728 : URL /liquidations + Playwright anti-bot (user-agent + --disable-blink-features).
Runs 1-3 exécutés après merge #728.
```
