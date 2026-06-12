---
doc_id: GO_SPACEX_V2_DESK_TELEGRAM_SHEETS_EXPORT_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
go_id: GO_SPACEX_V2_DESK_TELEGRAM_SHEETS_EXPORT_01
parent_go: GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01
status: draft
lifecycle_stage: impl
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-12
links:
  - docs/chantiers/GO_SPACEX_V2_LIVE_PIPELINE_INTEGRATION_01/00_INITIAL_PROJECT_DOC.md
  - modules/spcx_v2/paper_logger.py
  - modules/ipo_tracking/reports.py
  - modules/ipo_tracking/telegram_dispatcher.py
  - modules/ipo_tracking/sheets_consumer.py
  - shared/telegram_notify.py
  - modules/desk_pro/
---

# GO_SPACEX_V2_DESK_TELEGRAM_SHEETS_EXPORT_01

## [6_FINAL_TARGET]

Exporter les résultats du paper_logger SPCX V2 vers les surfaces de sortie :
Desk Pro (JSON panel), Telegram (alertes A+), Google Sheets (journal), et rapport quotidien (stats par grade/setup).

---

## [7_CANONICAL_STATE] — Files

```text
modules/spcx_v2/export_desk.py         # Desk Pro JSON endpoint
modules/spcx_v2/export_telegram.py     # Telegram A+ alerts + EOD summary
modules/spcx_v2/export_sheets.py       # Google Sheets append
modules/spcx_v2/daily_summary.py       # daily summary aggregator + markdown
scripts/ipo/spacex_export_daily_v2.sh  # wrapper for daily export cycle
tests/test_spcx_v2_export.py
docs/chantiers/GO_SPACEX_V2_DESK_TELEGRAM_SHEETS_EXPORT_01/
├── 00_INITIAL_PROJECT_DOC.md
└── FILE_SCOPE.txt
```

---

## [5_GO_PLAN]

### export_desk.py
- `get_desk_status() -> dict` — setups actifs, derniers candidats, stats summary
- `get_desk_candidates(limit=20) -> list[dict]` — dernières détections
- `get_desk_stats() -> dict` — stats aggrégées par grade + setup_type
- Sortie JSON compatible Desk Pro (`/desk/spcx_v2/`)

### export_telegram.py
- `send_a_plus_alerts() -> int` — envoie les alertes pour tous les candidats A+ non encore notifiés
- `send_eod_summary() -> str` — résumé de session
- Format compact : `[A+] SPCX IPO_ORB_15M | TR78 LQ72 RS38 SM70 CT65`
- Utilise `shared/telegram_notify.py` existant
- Évite les doublons via `candidate_id` déjà notifiés

### export_sheets.py
- `export_to_sheets() -> int` — exporte tous les candidats A+/A non encore envoyés
- Format : ts, symbol, setup_type, grade, entry_zone, invalidation, scores, reason_codes
- Utilise `modules/google_sheets_global_schema/` ou `modules/ipo_tracking/sheets_consumer.py`
- Mode `--dry-run` pour test sans écriture

### daily_summary.py
- `generate_daily_summary(date_str=None) -> dict` — stats du jour
- `write_daily_markdown() -> Path` — rapport markdown dans `reports/ipo/spacex/spcx_v2_daily_*.md`
- Contenu : setups détectés, classés, résultats, score buckets
- Appelé depuis le script daily_wrapper

### spacex_export_daily_v2.sh
- Appelle `daily_summary.py`
- Appelle `export_telegram.send_eod_summary()`
- Appelle `export_sheets.export_to_sheets()`

---

## [11_KEY_DECISIONS]

- Telegram: SEULEMENT A+ notifié en temps réel
- Sheets: A+ et A exportés
- Desk: tout visible (y compris B et rejets pour debug)
- Éviter les doublons : chaque export tracke les candidats déjà envoyés
- Aucune modification des modules ipo_tracking/ existants
- Paper-only (mention explicite dans les messages Telegram)

---

## [12_INVARIANTS]

1. PAPER ONLY — mention obligatoire dans chaque message Telegram et ligne Sheets
2. PAS DE DOUBLON — tracking par candidate_id
3. ZÉRO SECRET — token Telegram / creds Sheets via .env
4. TOUT EST LOGGÉ — même les rejets visibles dans le Desk
5. NEUTRALITÉ — aucun conseil d'achat/vente, uniquement détection et stats

---

## [17_RESUME_POINT]

```text
Export des résultats SPCX V2 vers Desk (JSON panel), Telegram (A+ alerts + EOD), 
Sheets (A+/A journal), et rapport markdown quotidien.
Pas de doublons, paper-only, tracking par candidate_id.
```
