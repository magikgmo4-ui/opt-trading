# Checklists opérationnelles — avant passage live

Ces checklists doivent être complétées et commitées dans un GO dédié
avant toute activation live. Elles ne valident pas le passage live elles-mêmes :
seul un GO_LIVE_ACTIVATION_* avec approbation explicite le fait.

---

## Checklist A — Risk engine

```
[ ] base_risk_pct vérifié sur capital alloué (pas capital total)
[ ] Plafond absolu par ordre défini et configuré (ex. max $500)
[ ] Plafond journalier défini et bloquant (ex. max $1500/jour)
[ ] Perte max journalière déclenchant halt (ex. -2% → stop)
[ ] Sizing MICRO (0.25%) configuré pour les premiers ordres live
[ ] Corrélation multi-actif documentée (BTC + ETH = risk cumulé ?)
[ ] risk_engine testé sur signal réel avec PAPER_MODE=0, DRY_RUN=0
```

---

## Checklist B — Validation gate / Kill switch

```
[ ] TRADING_KILL_SWITCH=1 testé — bloc confirmé dans les logs
[ ] Soft-stop POST /api/kill-switch testé — TRADE_ALLOWED=false confirmé
[ ] Operator gate timeout configuré (éviter stuck sur CAUTION)
[ ] Seuil GATE_MIN_CONFIDENCE=0.6 validé pour live (réviser ?)
[ ] CAUTION flow documenté : qui approuve ? via Telegram ?
[ ] Kill switch accessible sans accès SSH (Telegram command ?)
[ ] Temps arrêt mesuré < 5s (de décision à bloc effectif)
[ ] Runbook emergency stop rédigé (1 page, accessible offline)
```

---

## Checklist C — API Bitget / secrets

```
[ ] Clés API Bitget créées hors repo (secrets manager / env sécurisé)
[ ] Scope clés : trade-only, NO withdrawal
[ ] IP whitelist configurée si supportée
[ ] Clés testnet créées et testées d'abord
[ ] BitgetAdapter implémenté et testé sur testnet
[ ] Fill simulé vs fill réel : écart loggué (slippage tracking)
[ ] Rate limit Bitget API documenté et respecté
[ ] BITGET_API_KEY / BITGET_SECRET jamais dans le repo ni dans les logs
```

---

## Checklist D — Monitoring et alerting

```
[ ] Telegram end-to-end : signal → APPROVED → message reçu
[ ] Telegram kill switch → message reçu
[ ] TMUX session critique DOWN → alerte (Telegram ou LocalCMS)
[ ] LocalCMS /metrics : fail_count > 0 → visible immédiatement
[ ] Journal daily JSON : chaque ordre live loggué avec timestamp + fill_price
[ ] Sync Sheets controlled-write : un row par session live
[ ] Runbook on-call rédigé (1 page) : que faire si alerte à 3h du matin
```

---

## Checklist E — Rollback et continuité

```
[ ] Rollback systemd testé : sudo systemctl disable --now daily-session.timer
[ ] PaperAdapter restaurable en < 2 minutes (config seule, pas de code)
[ ] TRADING_KILL_SWITCH documenté dans /etc/environment ou équivalent
[ ] Backup journal daily avant premier run live (snapshot data/)
[ ] Procedure de rollback en cas de fill erroné documentée
[ ] Contact Bitget support enregistré (numéro, email, chat)
```

---

## Checklist F — Critères d'observation pré-live

```
[ ] ≥ 30 runs dry-run sans fail_count (actuellement 13)
[ ] ≥ 14 jours calendaires d'observation stable
[ ] ≥ 30 runs paper élargi (2-3 tickers) sans fail
[ ] P&L paper cumulé positif sur ≥ 30 runs
[ ] Win rate paper ≥ 50% sur ≥ 30 runs
[ ] 0 faux positif APPROVED sur signal incohérent
[ ] Kill switch testé manuellement ≥ 1 fois
[ ] Telegram alerting testé end-to-end ≥ 1 fois
```

---

## Template décision finale (à compléter dans GO_LIVE_ACTIVATION_*)

```
DATE_DECISION         :
OPERATEUR             :
N_RUNS_DRY_RUN        :
N_RUNS_PAPER          :
WIN_RATE_PAPER        :
PNL_CUMULE_PAPER      :
KILL_SWITCH_TESTE     : OUI/NON
TELEGRAM_TESTE        : OUI/NON
BITGET_TESTNET_PASSE  : OUI/NON
CAPITAL_ALLOUE        :
TAILLE_MAX_ORDRE      :
PERTE_MAX_JOURNALIERE :
APPROBATION_EXPLICITE : OUI/NON
```

Sans ce template complété et committé dans un GO_LIVE_ACTIVATION_*, aucun
ordre live ne doit être passé.

## RISKS

- À qualifier.
