# GO_OPT_TRADING_UI_PRODUCTIZATION_MAPPING_AND_KANBAN_01
# 00_INITIAL_PROJECT_DOC

Generated: 2026-05-19

## Objectif

Valider l'existant UI par recherche exhaustive code/docs, produire un mapping complet des surfaces,
identifier les gaps produit, et structurer le Kanban vers une UI "produit fini" validée visuellement
et humainement.

## Périmètre

| Surface | Port | Rôle |
|---------|------|------|
| localcms | 8000 | viewer/navigation/docs — indépendant de opt-trading |
| Desk Pro | 8010 | UI opérationnelle FastAPI — centre runtime |
| Alert pipeline | 8010 | notification Telegram / webhook / JSONL |
| Runtime supervision | n/a | boot/recovery/watchdog scripts |

## Contraintes

- Audit read-only d'abord.
- Aucun secret dans Git.
- Aucun push direct sur `sot/mainline` si code modifié.
- Aucun reset/clean destructif.
- Ne pas fusionner localcms et Desk Pro.
- Ne pas casser les tests existants (172/172 PASS au démarrage).
- Bundle ZIP sans secrets, .env, logs sensibles.

## Invariants hérités

- localcms et Desk Pro = deux surfaces séparées, rôles distincts.
- Telegram natif ≠ webhook générique (ne pas confondre).
- Watchdog sans auto-restart tant que non explicitement décidé.
- `/desk/health` retourne toujours `ok: true` (hardcodé) — ne mesure pas la santé applicative réelle.
- `webhook_activity:fail` en local = attendu sans signal TradingView entrant — pas d'ALERT.

## Découverte critique

**localcms tourne sur port 8000** — même port que le webhook server.
Les deux processus sont **mutuellement exclusifs** sur la même machine.
Quand localcms tourne, le webhook server est arrêté et `/desk/status` montre `webhook:fail`.

## Baseline au démarrage

- Branche : `sot/mainline` à `ea3d447d`
- Tests : 172/172 PASS
- Secrets : `secrets/` non tracké (correct)
- `/desk/status/enhanced` : **n'existe pas** (référencé dans bundle mais absent du code)
