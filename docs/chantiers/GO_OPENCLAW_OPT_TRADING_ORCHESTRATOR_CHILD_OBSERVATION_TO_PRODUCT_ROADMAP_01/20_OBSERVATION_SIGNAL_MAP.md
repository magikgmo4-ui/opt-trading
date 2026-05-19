---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01
doc_type: signal_map
repo: opt-trading
status: open
created_at: 2026-05-17
source: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01
---

# 20_OBSERVATION_SIGNAL_MAP

---

## Objectif

Définir ce que l'observation Phase 1 doit produire comme preuve utile.

L'observation n'est pas un simple compteur de runs.
C'est une surface de collecte structurée qui alimente les décisions produit.

---

## État actuel de l'observation (2026-05-17)

| Critère | Valeur actuelle | Seuil | Gap | État |
| --- | --- | --- | --- | --- |
| Runs sans fail | 14 | ≥ 30 | -16 | EN COURS |
| Jours observation | 2 | ≥ 14 | -12 | EN COURS |
| Kill switch testé | OUI | OUI | — | PASS |
| Telegram testé | OUI | OUI | — | PASS |
| P&L cumulé | +6132.42 | — | — | mesurable |
| Fail count | 0 | 0 | — | PASS |

**Éligibilité multi-signal : NON** (seuils non atteints)

Source : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01/01_OBSERVATION_LOG.md`

---

## Signaux à collecter pendant l'observation

### Signaux run / session

| Signal | Description | Source | Présent |
| --- | --- | --- | --- |
| `run_id` | Identifiant unique du run | `data/journal/daily/*.json` | oui |
| `session_id` | Identifiant session OpenClaw | logs OpenClaw | à vérifier |
| `status` | pass / fail / blocked | `all_ok` flag | oui |
| `run_date` | Date ISO du run | filename | oui |
| `pnl_session` | P&L du run courant | journal entry | oui |
| `pnl_cumulative` | P&L cumulé depuis observation start | métriques LocalCMS | oui |

### Signaux erreur / anomalie

| Signal | Description | Source | Présent |
| --- | --- | --- | --- |
| `error_type` | Type d'erreur si fail | logs | à vérifier |
| `error_source` | Module source (OpenClaw, réseau, exchange) | logs | à vérifier |
| `latency_ms` | Latence d'exécution | timer run | à vérifier |
| `recovery_action` | Action de reprise si anomalie | manuel / runbook | partiel |

### Signaux sync externe

| Signal | Description | Source | Présent |
| --- | --- | --- | --- |
| `sheets_status` | dry_run / written / blocked / failed | Sheets sync log | oui |
| `sheets_count` | Nombre de lignes envoyées | Sheets sync log | oui |
| `telegram_sent` | Notification envoyée (oui/non) | Telegram log | oui |

### Signaux état opérateur

| Signal | Description | Source | Présent |
| --- | --- | --- | --- |
| `kill_switch_state` | armé / désarmé | `/api/paper/guards` ou équivalent | oui (testé) |
| `paper_mode_active` | `DRY_RUN=1 PAPER_MODE=1` | config | oui |
| `dashboard_readiness` | LocalCMS accessible et cohérent | `curl localhost:8700/metrics` | oui |

### Signaux décision produit

| Signal | Description | Utilité |
| --- | --- | --- |
| `runs_to_threshold` | Écart au seuil 30 runs | gate décision |
| `days_to_threshold` | Écart au seuil 14 jours | gate décision |
| `consecutive_pass` | Séquence sans fail | confiance stabilité |
| `anomaly_count` | Nombre d'anomalies journalisées | risque reprise |
| `operator_decision_pending` | Décision opérateur requise (oui/non) | alerte gouvernance |

---

## Ce que l'observation doit prouver

```text
1. Stabilité du pipeline dry-run sur 30 runs et 14 jours calendaires
2. Absence de fail non résolu
3. Kill switch opérationnel
4. Telegram opérationnel
5. LocalCMS lit et expose correctement les métriques
6. Google Sheets sync contrôlé (dry_run / written / blocked tracés)
7. Pas de dérive de configuration (DRY_RUN, PAPER_MODE)
8. Capacité de reprise machine sans perte de context
```

---

## Ce que l'observation ne prouve pas

```text
- La qualité des signaux trading (hors scope Phase 1)
- La performance réelle (dry-run uniquement)
- La robustesse en conditions live (aucun trade réel)
- La complétude du data plane (à construire après observation)
```

---

## Décision d'éligibilité

```text
ELIGIBLE = runs >= 30 AND fail_count == 0 AND jours_observation >= 14

BLOQUE si :
  - fail_count > 0 → investigation requise avant continuation
  - anomalie systemd non résolue → GO dédié
  - timer désactivé → relancer et reset compteur jours si interruption > 24h
```

Prochaine revue recommandée : **2026-05-24** (20 runs ou 7 jours atteints — whichever comes first).
