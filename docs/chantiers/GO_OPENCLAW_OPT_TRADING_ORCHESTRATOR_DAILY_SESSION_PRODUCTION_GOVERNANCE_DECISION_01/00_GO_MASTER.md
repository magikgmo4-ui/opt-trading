---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_PRODUCTION_GOVERNANCE_DECISION_01
doc_type: go_master
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
depends_on:
  - PR #490  (3-run systemd steady-state review — merged)
created_at: 2026-05-16
---

# GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_PRODUCTION_GOVERNANCE_DECISION_01

## Objectif

Prendre une décision de gouvernance sur la prochaine phase après
validation du steady-state systemd dry-run.

## Contexte établi

- 3 runs systemd dry-run consécutifs : PASS (PR #490)
- TMUX 9 sessions stable, LocalCMS 4/4 stable
- Google Sheets sync dry-run stable
- P&L paper reproductible (+438.03/run)
- Rollback verified
- Aucun trade live, aucun Bitget order, aucune écriture Sheets auto

## Options

### A. Continuer dry-run systemd 7 jours

Installer le timer systemd et laisser tourner 7 jours en dry-run.
Observer les runs quotidiens automatiques, collecter les métriques
de fiabilité (uptime, succès/échec, latence).

| Avantages | Risques |
|-----------|---------|
| Validation longue durée | Aucun (déjà validé en 3 runs) |
| Détection de potentiels drift temporel | Consomme ~0.2s/jour CPU |
| Confirme la robustesse cron/systemd | |

### B. Activer controlled-write Sheets manuel uniquement

Ajouter `--controlled-write` à la sync Sheets pour les runs
quotidiens, mais déclenché manuellement (pas automatique).
Nécessite de configurer `GOOGLE_SHEETS_CREDENTIALS_JSON` et
`GOOGLE_SHEETS_SYNC_SHEET_ID` dans l'environnement.

| Avantages | Risques |
|-----------|---------|
| Remplit le sheet de métriques réelles | Exposition credentials Google |
| Permet validation end-to-end Sheets | Données paper dans un sheet "prod" |
| Utile pour reporting visuel | |

### C. Élargir paper-mode avec nouveaux signaux

Ajouter des signaux additionnels au pipeline dry-run (ex: ETHUSDT,
SOLUSDT) et vérifier que le scheduler/journal/Sheets gère
correctement des run_ids multiples par jour.

| Avantages | Risques |
|-----------|---------|
| Test multi-signal | Changement de code (hors scope GO actuel) |
| Valide la montée en charge | Nécessite un nouveau GO |
| Plus représentatif de la prod | |

### D. Préparer mais ne pas activer live trading

Analyser ce qui manque pour passer du paper dry-run au live
(API keys, risk management, sauvegarde, alerting, audit trail).
Documenter les gaps sans les combler.

| Avantages | Risques |
|-----------|---------|
| Vision claire du chemin vers live | Aucun (documentation seule) |
| Planification budgétaire possible | |
| Décision repoussée | |

## Recommandation

**Option A** : continuer dry-run systemd 7 jours.

Raison : le dry-run est validé, stable, reproductible. Avant d'activer
controlled-write Sheets (B), d'élargir les signaux (C), ou de préparer
le live (D), une semaine d'observation en conditions réelles (timer
systemd quotidien) confirmera l'absence de drift temporel, de fuite
mémoire, ou de dégradation lente.

Les options B, C, D peuvent être initiées en parallèle ou séquentiellement
après la semaine d'observation.

## Échéance

Décision à prendre et acter dans ce GO (PR merge).

## Contraintes

- Pas de live trade sans décision explicite
- Pas de write automatique Sheets
- No Bitget order
- Conserver rollback
- Doc-only (sauf décision d'implémentation)
