# Audit des surfaces — avant passage live

## 1. trade_executor

**Fichier :** `modules/trade_executor/app/executor.py`

**État actuel :**
- Utilise `PaperAdapter` exclusivement — aucune intégration Bitget live
- Guard ligne ~89 : n'exécute que si `verdict == "APPROVED"`
- `dry_run=True` → `status="dry_run"` (aucun fill réel)
- `dry_run=False` + `paper_mode=True` → `status="filled"` simulé (PaperAdapter)

**À auditer avant live :**
- [ ] Implémenter `BitgetAdapter` (ou équivalent) pour ordres réels
- [ ] Vérifier que `PaperAdapter` est le default et que le switch vers live nécessite config explicite
- [ ] Rate limiting : protéger contre rafale d'ordres (max N/min)
- [ ] Retry logic : que se passe-t-il si l'API Bitget timeout ?
- [ ] Fill partiel : le résultat tracker gère-t-il les fills partiels ?
- [ ] Slippage : l'écart fill_price vs signal_price est-il loggué ?

---

## 2. validation_gate

**Fichier :** `modules/validation_gate/app/gate.py`
**Risk check :** `modules/validation_gate/app/risk_check.py`
**Operator gate :** `modules/validation_gate/app/operator_gate.py`

**Garde-fous actuels :**
- `TRADING_KILL_SWITCH` → bloc immédiat (`kill_switch_active`)
- `HOLD` / `SKIP` → BLOCK automatique
- `confidence < 0.6` (`GATE_MIN_CONFIDENCE`) → BLOCK
- `confidence ∈ [0.6, 0.8)` → CAUTION (approbation opérateur requise)
- `confidence ≥ 0.8` (`GATE_HIGH_CONFIDENCE`) → ALLOW
- Operator gate : polling fichier `/data/gate_approvals/{request_id}.json`

**À auditer avant live :**
- [ ] Operator gate : le timeout est-il correctement défini ? (risque de stuck)
- [ ] Seuil `GATE_MIN_CONFIDENCE` : valider que 0.6 est correct pour live
- [ ] CAUTION : en live, qui approuve ? Telegram → action humaine ?
- [ ] Confirmer que kill switch coupe immédiatement les ordres en vol

---

## 3. risk_engine

**Fichier :** `modules/risk_engine/app/risk_engine.py`

**Paramètres actuels :**
```
min_confidence_allow  = 0.6
high_confidence       = 0.8
base_risk_pct         = 1.0%  (FULL)
HALF                  = 0.5%
MICRO                 = 0.25%
NONE                  = 0%
```

**À auditer avant live :**
- [ ] `base_risk_pct=1.0%` sur quel montant ? (capital total ou capital alloué ?)
- [ ] Plafond absolu par ordre (ex. max $500 quoi qu'il arrive)
- [ ] Plafond journalier total (ex. max 3% du capital par jour)
- [ ] Corrélation de positions : si BTC long + ETH long → risk cumulé ?
- [ ] Perte max déclenchant halt automatique

---

## 4. kill switch / emergency stop

**Kill switch dur :** `TRADING_KILL_SWITCH=1` — `risk_check.py:21`
- Coupe la validation gate → aucun ordre passé

**Kill switch soft :** `POST /api/kill-switch` — `webhook_server.py`
- Positionne `TRADE_ALLOWED=false`

**Telegram sur kill :** `NotificationDispatcher` — `gate.py:63`

**À auditer avant live :**
- [ ] Tester `TRADING_KILL_SWITCH=1` en dry-run : confirmer bloc total
- [ ] Documenter la procédure d'urgence (runbook 1 page)
- [ ] Vérifier que le soft-stop est accessible sans accès serveur (Telegram command ?)
- [ ] Temps de réaction : de la décision à l'arrêt effectif < 5s

---

## 5. TMUX sessions

**Sessions critiques :** `openclaw-core`, `screeners`, `strict-workers`

**À auditer avant live :**
- [ ] `strict-workers` : DRY_RUN=1 forcé — confirmer que le flag est dans le script de démarrage
- [ ] Restart automatique après crash : systemd / supervisor configuré ?
- [ ] Alerting si session critique tombe (Telegram ou LocalCMS alert)
- [ ] Runbook restart par session

---

## 6. LocalCMS monitoring

**Endpoints utiles :**
- `/runtime/tmux` — état sessions
- `/metrics` — agrégats journal
- `/journal` — historique runs

**À auditer avant live :**
- [ ] Auto-refresh 30s suffisant ? (actuel : 30s dans `/ui`)
- [ ] Alerting proactif si `fail_count > 0` (push Telegram ?)
- [ ] Ajouter `exec_status` dans `/metrics` pour distinguer dry_run vs live

---

## 7. Telegram alerting

**Module :** `shared/telegram_notify.py`
**Dispatcher :** `modules/notification_dispatcher/app/dispatcher.py`

**Env vars requises :**
```
TELEGRAM_BOT_TOKEN  (ou TELEGRAM_TOKEN)
TELEGRAM_CHAT_ID
```

**À auditer avant live :**
- [ ] Tester end-to-end : signal → gate APPROVED → Telegram reçu
- [ ] Tester kill switch → Telegram reçu
- [ ] Dry-run mode : confirmer `{"ok": True, "dry_run": True}` sans envoi réel
- [ ] Dédoublonnage : si 2 workers envoient le même event → 1 seul message ?

---

## 8. API Bitget / secrets

**État actuel :** aucune clé configurée, aucune intégration live.

**À configurer avant live (hors repo) :**
- Clés API Bitget dans secrets manager ou env sécurisé (jamais dans le repo)
- Scope minimal : trade only (pas de withdrawal)
- IP whitelist si supporté par Bitget
- Clés testnet d'abord — valider le flow complet sur testnet

**Invariant :** `NO_SECRETS_IN_REPO = toujours vrai`
