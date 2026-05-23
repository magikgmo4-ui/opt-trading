---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01_REPRISE
doc_type: reprise_point
repo: opt-trading
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
status: active
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 90_REPRISE_POINT

## État figé au 2026-05-23

### Livré et mergé

| PR | Patch | Mergé |
|---|---|---|
| #712 | A1 — schema dataclass | oui |
| #713 | A2 — parser mock + fixtures | oui |
| #714 | A3 — Desk Pro consumer | oui |
| #716 | B1 — headless runtime gated | oui |
| #717 | B2 — Telegram summary | oui |

### Branche active

```
go/GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_BOT_VISION_HEADLESS_ACCEPTANCE_01
```
Cible : `sot/mainline`

### Prochains choix produit (non engagés)

```
A. Activation capture headless planifiée en staging
   → wirer un caller (cron/scheduler) qui appelle runner.run_capture()
   → VISION_BOT_ENABLED=true sur machine staging
   → valider 3 runs PASS consécutifs

B. Telegram sender réel via caller séparé
   → créer un script/service qui appelle:
       msg = load_and_format()
       send_telegram_html(msg, source="coinglass_vision")
   → déclenché après chaque run_capture réussi

C. Desk Pro UI panel vision_context.coinglass.v1
   → ajouter section dédiée dans le template Desk Pro
   → afficher detections avec confidence bar
```

### Contraintes pour toute reprise

- Coinglass API : jamais wired → NOT_PROVEN_RUNTIME_ADAPTER permanent
- Telegram : jamais source de vérité, jamais en write path
- Desk Pro : jamais writer
- Runtime : toujours gated `VISION_BOT_ENABLED`
- Tests requis avant tout merge

## Commandes de reprise rapide

```bash
git switch sot/mainline && git pull
python3 -m pytest modules/vision/ tests/test_desk_pro_vision_context_reader.py -q
# → 53 tests PASS attendus
```
