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
OPTION RETENUE : [ A / B / C ]

Date : ~
Opérateur : ~
Justification : ~
```

---

## PROCHAINE_ÉTAPE

```text
Si A — Timer dédié :
→ Créer bot-vision-coinglass-capture.service + .timer sur admin-trading
→ Créer secrets/coinglass.env avec VISION_BOT_ENABLED + VISION_AI_PROVIDER + OPENAI_API_KEY
→ sudo systemctl daemon-reload && systemctl enable --now bot-vision-coinglass-capture.timer
→ Vérifier premier run automatique via journalctl

Si B — Intégration historique :
→ Ouvrir GO dédié (hors scope de ce GO)

Si C — Manuel :
→ Documenter la cadence manuelle dans le runbook opérationnel
→ Fermer ce GO PASS_DECISION_C
```
