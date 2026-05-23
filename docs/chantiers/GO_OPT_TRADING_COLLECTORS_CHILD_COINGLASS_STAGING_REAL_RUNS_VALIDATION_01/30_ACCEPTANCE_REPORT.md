---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_STAGING_REAL_RUNS_VALIDATION_01
doc_type: acceptance_report
repo: opt-trading
status: accepted
created_at: 2026-05-23
---

# 30_ACCEPTANCE_REPORT

---

## VERDICT

```text
PASS_STAGING_REAL

Date : 2026-05-23
Opérateur : magikgmo4
Machine : admin-trading
```

---

## CRITÈRES_PASS

| Critère | Résultat | Détail |
|---|---|---|
| 3 runs capturés | PASS | 10:39:16Z, 10:40:19Z, 10:41:12Z |
| ≥ 1 detection/run (conf ≥ 0.60) | PASS | 5 détections/run, confidence=1.00 |
| extracted_value non-null sur ≥ 1 detection/run | PASS | toutes non-null |
| latest.json présent et valide | PASS | `vision_context.coinglass.v1` |
| events.jsonl contient 3 entrées qualifiées | PASS | 4 lignes total (1 ancien + 3 nouveaux) |
| --validate --required 3 exit 0 | PASS | `PASS — 3/3 consecutive runs OK` |
| /desk/vision ok=true | PASS | age_hours=0.036, 5 detections |
| /desk/ui panel "Coinglass Vision" visible | PASS | `<summary>Coinglass Vision</summary>` |

---

## OBSERVATIONS

```text
- Playwright + anti-bot (PR #728) requis : /LiquidationData → /liquidations + user-agent réel
- Chromium headless contourné grâce à --disable-blink-features=AutomationControlled
- OpenAI Vision (gpt-4o-mini) : confidence=1.00 sur 5 métriques — qualité OCR excellente
- Métriques extraites : liquidations_long, liquidations_short, long_short_ratio,
  open_interest, liquidation_heatmap_level
- Service tv-perf.service (port 8010) redémarré pour charger le code à jour (#728)
- Telegram non testé (--send) : hors scope staging validation
```

---

## PROCHAINE_ÉTAPE

```text
Stack prête pour évaluation de promotion prod.
Pré-requis prod identifiés :
  - Timer systemd dédié (bot-vision-coinglass-capture.timer) ou intégration timer existant
  - OPENAI_API_KEY dans .env admin-trading (actuellement dans secrets/openai.env local)
  - Décision REUSE/BRIDGE/KEEP_DEDICATED pour pipeline bot_vision historique
  - GO dédié à la promotion prod si planifiée

Ce GO est CLOSED : PASS_STAGING_REAL.
```
