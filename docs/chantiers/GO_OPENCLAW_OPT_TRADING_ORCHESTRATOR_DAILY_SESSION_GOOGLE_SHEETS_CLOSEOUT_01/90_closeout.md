# Google Sheets Controlled Sync — Closeout Final

## Résultat global

```
GOOGLE_SHEETS_CONTROLLED_SYNC_CYCLE = PASS
```

## PRs du cycle

| PR    | GO                                                                           | État   | Résultat               |
| ----- | ---------------------------------------------------------------------------- | ------ | ---------------------- |
| #480  | DAILY_SESSION_GOOGLE_SHEETS_CONTROLLED_SYNC_01                               | MERGED | script + schema créés  |
| #495  | GOOGLE_SHEETS_CONTROLLED_WRITE_PILOT_01                                      | MERGED | DEGRADED (JSON bloqué) |
| #496  | GOOGLE_SHEETS_CREDENTIALS_SETUP_AND_CONTROLLED_WRITE_RETRY_01                | MERGED | plan retry posé        |
| #497  | GOOGLE_SHEETS_CONTROLLED_WRITE_EXECUTION_01                                  | MERGED | BLOCKED (policy)       |
| #499  | GOOGLE_SHEETS_CREDENTIALS_EXTERNAL_SETUP_01                                  | MERGED | ADC identifié          |
| #501  | GOOGLE_SHEETS_ADC_AUTH_FALLBACK_01                                           | MERGED | ADC = PASS             |
| #504  | GOOGLE_SHEETS_GSPREAD_DEPENDENCY_FIX_01                                      | MERGED | deps figées            |

## État final ADC

```
Méthode  : Application Default Credentials (ADC)
Commande : gcloud auth application-default login \
             --scopes=https://www.googleapis.com/auth/spreadsheets
Status   : PASS
Raison   : iam.disableServiceAccountKeyCreation bloque JSON key — ADC est le seul path
```

## État final dépendances

```
gspread      = 6.2.1  (requirements.txt — PR #504)
google-auth  = 2.53.0 (requirements.txt — PR #504)
```

## Preuve controlled-write

```
run_id              = 20260516_013
date                = 2026-05-16
signal              = BUY BTCUSDT
verdict             = APPROVED
outcome             = win
net_pnl             = 438.03
mode                = controlled_write
status              = synced
row appended        = YES (Google Sheets sheet1)
GOOGLE_SHEETS_SYNC_SHEET_ID = SET (env, non commité)
```

## Setup machine (reproductibilité)

```bash
# 1. Auth ADC — une fois par machine/utilisateur
gcloud auth application-default login \
  --scopes=https://www.googleapis.com/auth/spreadsheets

# 2. Env var — session ou .env (non commité)
export GOOGLE_SHEETS_SYNC_SHEET_ID="<sheet_id>"

# 3. Dry-run (aucun prérequis)
python scripts/sheets/sync_daily_session.py --latest

# 4. Controlled-write (ADC + SHEET_ID requis)
python scripts/sheets/sync_daily_session.py --latest --controlled-write
```

## Invariants sécurité

| Invariant                         | État      |
| --------------------------------- | --------- |
| Aucun secret dans le repo         | PASS      |
| Aucun secret dans les logs        | PASS      |
| `SHEET_ID` hors repo (env)        | PASS      |
| Controlled-write manuel seulement | PASS      |
| No live trade                     | PASS      |
| No Bitget order                   | PASS      |
| LocalCMS read-only                | PASS      |

## Observabilité daily session — état complet

| Composant            | État         |
| -------------------- | ------------ |
| systemd              | opérationnel |
| TMUX sessions        | opérationnel |
| LocalCMS             | opérationnel |
| Journal daily JSON   | opérationnel |
| Google Sheets sync   | opérationnel |

## Prochaines options

- **Observation** : accumuler les `run_id` dans Sheets sur plusieurs sessions
- **Dashboard** : lire le Sheets en lecture seule pour agréger les métriques
- **Multi-signal** : étendre le sync à d'autres signaux (SELL, paper multi-ticker)
- **Paper-mode élargi** : activer le paper-mode sur plusieurs assets en parallèle
