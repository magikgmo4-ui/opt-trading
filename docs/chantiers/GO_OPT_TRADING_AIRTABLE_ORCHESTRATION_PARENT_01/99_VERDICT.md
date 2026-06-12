---
doc_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01_VERDICT
doc_type: verdict
repo: opt-trading
branch: go/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
go_id: GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01
status: verdict
lifecycle_stage: decision
updated_at: 2026-05-06
links:
  - docs/chantiers/GO_OPT_TRADING_APPS_PARENT_VALIDATED_PLAN_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/01_RESEARCH_SYNTHESIS.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/02_INTEGRATION_ARCHITECTURE.md
  - docs/chantiers/GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01/04_PRODUCT_FINISH_PLAN.md
---

# VERDICT — Airtable dans la stack opt-trading

## Contexte

- Plan apps valide: ClickUp → Repo KG → Airtable → Botpress
- ClickUp PASS, Repo KG PASS (parent + Producer)
- Airtable = 3e phase apps

## Comparaison Airtable vs alternatives

| Surface | Airtable | Google Sheets | DB layer | LocalCMS |
| --- | --- | --- | --- | --- |
| Journal trading | Bon (tables relationnelles) | Limite (feuilles) | Lourd (setup) | Non adapte |
| Backtests visuels | OK (interfaces) | OK (charts) | Lourd (BI tool) | Non |
| Signaux / alerts | OK (API entree) | Limite | Bon (temps reel) | Non |
| Validation humaine | Excellent (review UI) | OK | Nul (pas d'UI) | Non |
| Dashboard operateur | Bon (views) | OK | Lourd | Non |
| Export sortie | CSV/JSON (bon) | CSV (bon) | Direct (bon) | N/A |
| Volume max | 500K rows/table | 10M cells | Illimite | Limite |
| Risque vendor lock | Haut | Moyen | Faible | Nul |
| Cout | Gratuit → $20/mois | Gratuit | Setup temps | Gratuit |
| API entree | REST OK | Sheets API | SQL direct | YAML local |
| Integration repo | Bridge via API | Bridge via API | Connexion directe | Fichiers locaux |

## Conclusion

- **Google Sheets**: trop fragile pour suivi structure, pas de relations, pas d'API rich
- **DB layer**: ideal pour historique/backtest massif, mais pas de cockpit UI
- **LocalCMS**: doc YAML uniquement, pas pour data trading
- **Airtable**: meilleur compromis cockpit data leger avec UI, API, relations, exports

## Verdict

**GO_LIMITED** — Airtable est utilise pour:

1. **Journal trading**: tables `/trades`, `/signals`, `/backtests` — structure legere exportable
2. **Validation humaine**: review des signaux avant/après execution
3. **Dashboard operateur**: vues rapides statut GO, positions, alerts
4. **Bridge optionnel**: module `airtable_bridge` non bloquant

**Airtable NE devient PAS**:
- Source canonique (repo reste la preuve)
- Moteur trading live (pas de tick data)
- DB massive (max 500K rows, export CSV/JSON comme sortie reguliere)
- Remplacement de Google Sheets/DB layer pour leurs usages propres

## MVP minimal propose

### Tables Airtable V1

| Table | Description | Champs cles |
| --- | --- | --- |
| `Trades` | Journal trades | date, pair, direction, entry, exit, pnl, status, review_url |
| `Signals` | Signaux recus | timestamp, source, symbol, signal, confidence, reviewed_by |
| `Backtests` | Resultats tests | strategy, period, sharpe, drawdown, trades_count, verdict |
| `GO_Status` | Miroir GO cockpit | go_id, status, machine, branch, next_go, updated_at |

### Flux

```
TradingView/Telegram → webhook → opt-trading → airtable_bridge → Airtable
                                             → Google Sheets (reporting)
                                             → DB layer (historique)
```

### Strategie de sortie

- Export quotidien CSV/JSON depuis Airtable → commit ou stockage local
- Les donnees Airtable sont reconstruisibles depuis le repo
- Si volume > limite: migration vers DB layer avec historique preserve

## Prochain GO

Si GO_LIMITED accepte:

```text
GO_OPT_TRADING_AIRTABLE_BRIDGE_CHILD_01
```

Implementation du module `airtable_bridge` (client API, config non commitee, cmd/menu/sanity).

## RISKS

- À qualifier.
