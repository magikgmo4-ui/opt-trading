# Journal d'observation — Phase 1 (≥30 runs, ≥14 jours)

## État au démarrage du GO — 2026-05-17

### Métriques LocalCMS `/metrics`

| Métrique          | Valeur        |
| ----------------- | ------------- |
| `total_runs`      | 14            |
| `pass_count`      | 14            |
| `fail_count`      | 0             |
| `win_count`       | 14            |
| `loss_count`      | 0             |
| `breakeven_count` | 0             |
| `pnl_cumulative`  | +6132.42      |
| `win_rate`        | 1.0 (100%)    |
| `last_run`        | 20260517_001  |

### Sheets sync

| Statut   | Count |
| -------- | ----- |
| dry_run  | 6     |
| written  | 1     |
| blocked  | 2     |
| failed   | 0     |

### Prérequis Phase 1

| Critère              | Valeur actuel | Seuil | Gap   | État     |
| -------------------- | ------------- | ----- | ----- | -------- |
| Runs sans fail       | 14            | ≥ 30  | -16   | EN COURS |
| Jours observation    | 2             | ≥ 14  | -12   | EN COURS |
| Kill switch testé    | OUI           | OUI   | —     | PASS     |
| Telegram testé       | OUI           | OUI   | —     | PASS     |

**Éligibilité multi-signal : NON** (≥30 runs et ≥14 jours non atteints)

---

## Grille de suivi (à compléter)

| Date       | Runs total | Fail | P&L cumulé | Jours obs | Anomalies | Verdict     |
| ---------- | ---------- | ---- | ---------- | --------- | --------- | ----------- |
| 2026-05-16 | 13         | 0    | +5694.39   | 1         | none      | EN COURS    |
| 2026-05-17 | 14         | 0    | +6132.42   | 2         | none      | EN COURS    |
| 2026-05-18 | —          | —    | —          | 3         | —         | —           |
| 2026-05-19 | —          | —    | —          | 4         | —         | —           |
| 2026-05-20 | —          | —    | —          | 5         | —         | —           |
| 2026-05-21 | —          | —    | —          | 6         | —         | —           |
| 2026-05-22 | —          | —    | —          | 7         | —         | —           |
| 2026-05-23 | —          | —    | —          | 8         | —         | —           |
| 2026-05-24 | —          | —    | —          | 9         | —         | —           |
| 2026-05-25 | —          | —    | —          | 10        | —         | —           |
| 2026-05-26 | —          | —    | —          | 11        | —         | —           |
| 2026-05-27 | —          | —    | —          | 12        | —         | —           |
| 2026-05-28 | —          | —    | —          | 13        | —         | —           |
| 2026-05-29 | —          | —    | —          | 14        | —         | —           |
| 2026-05-30 | —          | —    | —          | 15        | —         | ÉLIGIBLE ? |

---

## Sources de données

```bash
# Métriques agrégées
curl http://localhost:8700/metrics/daily | python3 -m json.tool

# Nombre de runs
ls data/journal/daily/*.json | wc -l

# Dernier run
ls data/journal/daily/*.json | sort | tail -1

# Fails
python3 -c "
import json; from pathlib import Path
entries = [json.loads(f.read_text()) for f in Path('data/journal/daily').glob('*.json')]
fails = [e for e in entries if not e.get('all_ok')]
print(f'fails={len(fails)}/{len(entries)}')
"
```

---

## Critères de verdict d'éligibilité

```
ELIGIBLE = total_runs >= 30 AND fail_count == 0 AND jours_observation >= 14

BLOQUE si :
  - fail_count > 0 → investigation requise avant continuation
  - anomalie systemd → GO dédié
  - timer désactivé → relancer et reset compteur jours si interruption > 24h
```

---

## Anomalies connues

| ID  | Date       | Description | Résolution |
| --- | ---------- | ----------- | ---------- |
| 001 | 2026-05-16 | systemd StartLimitBurst rate-limiting (tests rapides) | Désactivé dans service file |

Aucune anomalie en conditions normales (timer quotidien espacé de 24h).

## RISKS

- À qualifier.
