# Controlled-Write Pilot Report — 2026-05-16

## Metadata

| Champ            | Valeur                                                       |
| ---------------- | ------------------------------------------------------------ |
| GO               | GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_CONTROLLED_WRITE_PILOT_01 |
| Date             | 2026-05-16                                                   |
| Run ID cible     | 20260516_007                                                 |

## Credentials check

| Variable                       | Statut    |
| ------------------------------ | --------- |
| `GOOGLE_SHEETS_CREDENTIALS_JSON` | NON DÉFINI |
| `GOOGLE_SHEETS_SYNC_SHEET_ID`    | NON DÉFINI |

**Le controlled-write Sheets ne peut pas être exécuté** sans ces deux
variables d'environnement.

## Dry-run preview (synthèse)

La ligne prête à écrire contient 22 colonnes :

| Colonne              | Valeur          |
| -------------------- | --------------- |
| run_id               | 20260516_007    |
| date                 | 2026-05-16      |
| signal               | BUY BTCUSDT     |
| verdict              | APPROVED        |
| net_pnl              | 438.0300        |
| tmux_before          | 9               |
| localcms_before_ok   | 4/4             |
| all_ok               | YES             |

## Validation du pipeline

Bien que l'écriture n'ait pas eu lieu (credentials absents), le pipeline
est validé :

- ✅ `sync_daily_session.py --run-id 20260516_007` → dry-run, row preview OK
- ✅ 22 colonnes mappées correctement
- ✅ run_id, TMUX, LocalCMS, P&L cohérents avec le journal source
- ✅ Sync log prêt à recevoir l'entrée

## Étapes pour activer

```bash
export GOOGLE_SHEETS_CREDENTIALS_JSON='{"type":"service_account",...}'
export GOOGLE_SHEETS_SYNC_SHEET_ID="your-sheet-id"
python scripts/sheets/sync_daily_session.py --run-id 20260516_007 --controlled-write
```

## Verdict

```
┌───────────┐
│ DEGRADED  │
└───────────┘
```

Controlled-write non exécuté car credentials Google Sheets non définis.
Le pipeline est prêt et validé en dry-run — seule l'intégration
credentials manque.

## Contraintes respectées

- Controlled-write manuel uniquement ✅ (pas d'écriture automatique)
- Aucune écriture Sheets automatique ✅
- No live trade / No Bitget order ✅
- LocalCMS read-only ✅
