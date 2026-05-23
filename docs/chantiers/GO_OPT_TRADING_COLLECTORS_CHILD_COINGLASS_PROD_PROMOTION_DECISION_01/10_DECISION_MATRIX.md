---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PROD_PROMOTION_DECISION_01
doc_type: decision_matrix
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 10_DECISION_MATRIX

---

## 1_ÉTAT_INFRA_ADMIN_TRADING

| Composant | État | Notes |
|---|---|---|
| `bot-vision-headless-capture.timer` | actif | capture Node.js périodique |
| `bot_vision_step2_send.timer` | actif | diffusion résultats |
| `bot_vision_step2_prune.timer` | actif | nettoyage daily |
| `venv` Python | présent | playwright + openai installés (#728) |
| `scripts/run_vision_capture.py` | présent | syncé depuis sot/mainline |
| `modules/vision/coinglass/` | présent | syncé depuis sot/mainline |
| `OPENAI_API_KEY` | `secrets/openai.env` local | non dans .env permanent |
| `tv-perf.service` (port 8010) | actif | Desk Pro — redémarré après #728 |

---

## 2_CRITÈRES_DE_COMPARAISON

| Critère | Poids | A — Timer dédié | B — Intégration historique | C — Manuel |
|---|---|---|---|---|
| Fraîcheur donnée Desk Pro | ★★★★★ | continu automatique | continu via hook | manuelle seulement |
| Risque infra | ★★★★ | faible (timer isolé) | moyen (couplage JS+Python) | nul |
| Complexité maintenance | ★★★ | 1 timer de plus | facteur 1 (réutilise) | zéro |
| Droits requis | ★★★ | root systemd | root systemd | aucun root |
| OPENAI_API_KEY secure | ★★★★ | EnvironmentFile dédié | EnvironmentFile dédié | export manuel |
| Indépendance pipeline historique | ★★★★ | totale | couplée | totale |
| Time-to-activate | ★★★ | ~30 min (service + timer) | ~1h (intégration + test) | immédiat |
| Réversibilité | ★★★★ | `systemctl disable` | à démêler | N/A |

---

## 3_ANALYSE_PAR_OPTION

### Option A — Timer systemd dédié (recommandée)

```text
Fichiers à créer sur admin-trading :

/etc/systemd/system/bot-vision-coinglass-capture.service
  [Unit]
  Description=Coinglass Vision headless capture
  After=network.target

  [Service]
  Type=oneshot
  WorkingDirectory=/opt/trading
  EnvironmentFile=/opt/trading/secrets/coinglass.env
  ExecStart=/opt/trading/venv/bin/python scripts/run_vision_capture.py
  User=ghost

/etc/systemd/system/bot-vision-coinglass-capture.timer
  [Unit]
  Description=Coinglass Vision — toutes les heures
  Requires=bot-vision-coinglass-capture.service

  [Timer]
  OnCalendar=hourly
  Persistent=true

  [Install]
  WantedBy=timers.target

secrets/coinglass.env (chmod 600) :
  VISION_BOT_ENABLED=true
  VISION_AI_PROVIDER=openai
  OPENAI_API_KEY=<valeur de secrets/openai.env>

Activation :
  sudo systemctl daemon-reload
  sudo systemctl enable --now bot-vision-coinglass-capture.timer

Monitoring :
  sudo systemctl status bot-vision-coinglass-capture.timer
  journalctl -u bot-vision-coinglass-capture.service -f
```

### Option B — Intégration pipeline historique

```text
Risque : bot-vision-headless-capture.timer utilise Node.js + capture_headless.js.
Brancher run_vision_capture.py dans ce flow crée une dépendance JS→Python fragile.
vision_inbox / vision_processed ne sont pas utilisés par la voie Coinglass.
Verdict : déconseillé — complexité sans gain réel.
```

### Option C — Manuel

```text
Acceptable si Desk Pro n'est consulté qu'à la demande.
Donnée périmée entre les runs : age_hours augmente sans refresh automatique.
/desk/vision retourne stale si screenshot_ts > 4h.
Verdict : acceptable en période de test, insuffisant pour usage opérationnel continu.
```

---

## 4_PRÉ-REQUIS_OPTION_A

```text
1. OPENAI_API_KEY stable (actuellement secrets/openai.env — OK pour EnvironmentFile)
2. Droits sudo pour créer les fichiers systemd et recharger daemon
3. Playwright + openai installés dans /opt/trading/venv (OK depuis #728)
4. Vérifier que ghost peut exécuter le script (User=ghost dans service)
5. Créer secrets/coinglass.env séparé de secrets/openai.env pour scope clair
```
