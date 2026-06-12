---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: localcms_dashboard_readiness
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 40_LOCALCMS_AND_DASHBOARD_READINESS

---

## Objectif

Évaluer ce que LocalCMS expose aujourd'hui vs ce qu'il faudrait pour une vue
opérateur complète basée sur le schéma canonique `ObservationEvent`.

---

## LocalCMS actuel — ce qu'il expose

Source : `localhost:8700/metrics/daily` — données réelles au 2026-05-17.

| Champ exposé | Valeur | Présent dans `ObservationSummary` V1 |
| --- | --- | --- |
| `total_runs` | 14 | oui |
| `pass_count` | 14 | oui |
| `fail_count` | 0 | oui |
| `win_count` | 14 | oui |
| `loss_count` | 0 | oui |
| `breakeven_count` | 0 | oui |
| `pnl_cumulative` | +6132.42 | oui |
| `win_rate` | 1.0 | oui |
| `last_run` | `20260517_001` | oui |

---

## Champs manquants dans LocalCMS actuel

Ces champs sont dans l'`ObservationSummary` V1 mais pas encore exposés par LocalCMS.

| Champ | Valeur calculable | Source |
| --- | --- | --- |
| `observation_start` | `2026-05-16` | min(run_date) des journaux |
| `days_elapsed` | `2` | (today - observation_start).days |
| `runs_to_threshold` | `16` | 30 - 14 |
| `days_to_threshold` | `12` | 14 - 2 |
| `eligible` | `false` | seuils non atteints |
| `last_run_date` | `2026-05-17` | max(run_date) |
| `session_id` | par run | `data/journal/daily/YYYYMMDD_NNN.json` |
| `closeout_required_count` | `0` | count(closeout_required=true) |

---

## Gap LocalCMS — résumé

```text
LocalCMS actuel expose les métriques run agrégées (pass/fail/win/pnl).
Il n'expose pas encore :
- les seuils Phase 1 et l'éligibilité
- le nombre de jours d'observation
- les gaps aux seuils
- les alertes closeout_required
```

---

## Niveau de readiness actuel

| Surface | Readiness | Note |
| --- | --- | --- |
| Métriques agrégées de base | PASS | total_runs, pass_count, pnl_cumulative, win_rate exposés |
| Éligibilité Phase 1 | GAP | runs_to_threshold, days_to_threshold, eligible absents |
| Alertes opérateur | GAP | closeout_required non exposé |
| Vue par run | GAP | pas de liste de runs individuels |
| Vue session | GAP | session_id par run non exposé |

---

## Ce que le prochain child GO LocalCMS view doit apporter

```text
Child GO recommandé :
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
```

Ce child doit documenter l'extension de LocalCMS pour exposer :

1. `ObservationSummary` complet (avec seuils et éligibilité)
2. Vue liste de runs (derniers N runs avec status, pnl, date)
3. Alertes closeout_required actives
4. Indicateur d'éligibilité Phase 1

---

## Ce que le schéma canonique rend possible

Avec `ObservationEvent` V1 en place comme contrat de données, les consommateurs
peuvent être écrits sans dépendance au format brut des journaux.

| Consommateur | Ce qui devient possible |
| --- | --- |
| LocalCMS | endpoint `/metrics/observation` basé sur `ObservationSummary` |
| Dashboard | vue runs récents, graphe P&L, indicateur éligibilité |
| Google Sheets | sync optionnel `ObservationEvent` par run |
| BDD future | ingestion `ObservationEvent` → persistence requêtable |
| Governance | preuve de stabilité structurée — non inertielle |

---

## Décision sur la priorité LocalCMS vs BDD

```text
Ordre recommandé :
1. Valider le schéma canonique V1 (ce child GO)
2. Ouvrir LocalCMS observation view (child B)
3. Ouvrir BDD persistence seulement si LocalCMS seul ne suffit pas

Raison : LocalCMS est le consumer le plus immédiat.
La BDD est utile pour l'historique long terme, pas pour Phase 1.
```

---

## Ce qui ne bloque pas Phase 1

```text
Phase 1 peut continuer sans BDD ni extension LocalCMS.
Les journaux bruts sont consultables.
LocalCMS expose les métriques essentielles.
L'observation est valide même sans schéma canonique implémenté.
```

Ce child GO pose la fondation documentaire — il ne bloque pas l'observation.

## RISKS

- À qualifier.
