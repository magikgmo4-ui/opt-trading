---
doc_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01_SIGNALS
doc_type: cockpit_page
go_id: GO_LOCALCMS_AUTOMATION_COCKPIT_01
status: draft
---

# 70_SIGNALS.md

## Page: Signals

URL: `/cockpit/automation/signals`

### Derniers signaux

| ID | Source | Symbol | Direction | Confiance | Cross | Bloqué |
|---|---|---|---|---|---|---|
| a54e8d18 | tradingview | BTCUSD | buy | 0.82 | confirmed | YES |
| 3ca73386 | collector | SOLUSD | buy | 0.75 | pending | NO |

### Stats

```text
Signaux aujourd'hui : 12
Confirmés : 8 (66.7%)
Rejetés : 3 (25.0%)
Ordres bloqués : 8 (100% des confirmés)
Win rate simulé : N/A (pas assez de données)
```

### Actions

```text
[BUTTON: VIEW ORDER]  →  Voir l'ordre dry-run simulé (lecture seule)
[BUTTON: REFRESH]     →  Recharger les signaux
```

### Intégration

- Alimenté par le journal G10 (`data/signals/journal/YYYY-MM-DD.jsonl`)
- Stats via `signal_stats.py`
