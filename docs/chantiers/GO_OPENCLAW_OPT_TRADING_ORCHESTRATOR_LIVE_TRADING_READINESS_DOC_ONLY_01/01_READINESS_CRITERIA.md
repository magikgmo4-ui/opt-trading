# Critères de readiness — dry-run → paper élargi → live

## Phase 0 — Baseline (ACTUELLE — PASS)

État courant validé :

| Critère                        | État   |
| ------------------------------ | ------ |
| Timer systemd quotidien actif  | PASS   |
| TMUX 9 sessions stables        | PASS   |
| LocalCMS 4/4 endpoints         | PASS   |
| Journal JSON/CSV opérationnel  | PASS   |
| Google Sheets sync (ADC)       | PASS   |
| Metrics dashboard `/metrics`   | PASS   |
| 13 runs dry-run — 0 fail       | PASS   |
| P&L paper cumulé = +5694.39    | PASS   |
| Win rate = 100% (paper)        | PASS   |

---

## Phase 1 — Paper élargi (PROCHAINE ÉTAPE)

**Prérequis d'entrée :**

- [ ] ≥ 30 runs dry-run sans anomalie (actuellement 13)
- [ ] Cohérence validée sur ≥ 14 jours calendaires
- [ ] Métriques LocalCMS `/metrics` consultées chaque semaine
- [ ] Validation gate : 0 faux positif APPROVED sur signal incohérent
- [ ] Kill switch testé manuellement : `TRADING_KILL_SWITCH=1` → bloc confirmé
- [ ] Telegram alerting fonctionnel sur signal APPROVED
- [ ] Risk engine : sizing vérifié (FULL=1%, HALF=0.5%, MICRO=0.25%)
- [ ] Rollback systemd testé : `sudo systemctl disable --now daily-session.timer`

**Actions paper élargi :**
- Étendre à 2-3 tickers (ETHUSDT, SOLUSDT) en paper-mode
- Toujours `DRY_RUN=1 PAPER_MODE=1`
- Pas d'ordre Bitget

---

## Phase 2 — Live trading (FUTURE — décision séparée requise)

**Prérequis d'entrée (non exhaustif) :**

- [ ] ≥ 30 runs paper élargi sans anomalie sur ≥ 2 tickers
- [ ] Risk engine validé en conditions réelles (latence, slippage)
- [ ] API Bitget configurée hors repo — clés dans secrets manager ou env sécurisé
- [ ] Kill switch hardware testé : arrêt total < 5s
- [ ] Telegram alerting en production testé end-to-end
- [ ] Taille de position initiale : MICRO uniquement (0.25% account)
- [ ] Plafond journalier défini et implémenté (ex. max 3 ordres/jour)
- [ ] Pertes max journalières définies et bloquantes (ex. -2% → halt)
- [ ] Audit trail complet : chaque ordre logué avec timestamp, signal, confidence
- [ ] Approbation explicite dans un GO dédié (GO_LIVE_ACTIVATION_*)
- [ ] Décision documentée et commitée avant exécution

**Décision live = GO séparé obligatoire.**
Le présent GO ne constitue pas une autorisation de passage live.

---

## Critères minimaux N jours / N runs

| Phase               | N runs min | N jours min | Tickers min |
| ------------------- | ---------- | ----------- | ----------- |
| Paper élargi        | 30         | 14          | 1           |
| Live MICRO          | 30 paper   | 30          | 2           |
| Live FULL sizing    | 30 live ok | 30          | 2           |
