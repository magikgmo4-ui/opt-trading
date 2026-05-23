---
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_PROD_PROMOTION_DECISION_01
doc_type: acceptance_report
repo: opt-trading
status: open
created_at: 2026-05-23
---

# 20_ACCEPTANCE_REPORT

À remplir après décision.

---

## VERDICT

```text
OPTION RETENUE : A — Timer systemd dédié

Date : 2026-05-23
Opérateur : magikgmo4
Justification :
  - Stack staging PASS (3/3 runs, conf=1.00) → promotion justifiée
  - Timer dédié isolé du pipeline historique (Node.js non couplé)
  - Réversible : systemctl disable suffit
  - OPENAI_API_KEY via EnvironmentFile dédié (jamais dans le code)
```

---

## DÉPLOIEMENT_OPTION_A

```text
Machine : admin-trading
Date : 2026-05-23

Fichiers créés :
  /etc/systemd/system/bot-vision-coinglass-capture.service
  /etc/systemd/system/bot-vision-coinglass-capture.timer
  /opt/trading/secrets/coinglass.env (chmod 600)

Commandes exécutées :
  sudo systemctl daemon-reload
  sudo systemctl enable --now bot-vision-coinglass-capture.timer

Vérification :
  systemctl status bot-vision-coinglass-capture.timer → active (waiting)
  Premier run automatique : à vérifier via journalctl
```

---

## PROCHAINE_ÉTAPE

```text
→ Surveiller les premiers runs automatiques :
  journalctl -u bot-vision-coinglass-capture.service -f

→ Vérifier que /desk/vision reste frais (age_hours < 1h) après chaque run horaire

→ Si problème : sudo systemctl disable bot-vision-coinglass-capture.timer

GO CLOSED : PASS_DECISION_A
```
