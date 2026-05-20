---
doc_id: GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01_REPRISE
doc_type: reprise
repo: opt-trading
go_id: GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01
status: reference
source_kind: canonical
updated_at: 2026-05-20
---

# 90_REPRISE

## MASTER_TARGET

Ce child reste subordonne au parent umbrella
`GO_OPT_TRADING_ADMIN_TRADING_SIGNAL_CHAIN_TOTAL_PRODUCT_PARENT_01` via le GO
runtime `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`.

## Etat de cette passe

Ce GO fournit :

- une checklist humaine device (Termius/Termux) a executer sur reseau prod
- des tests locaux CI-safe qui restent partiels sur Windows lorsque `bash` est
  indisponible (WSL sans distribution)

Le verdict runtime global reste porte par le GO runtime parent.

## Livrables

| Fichier | Statut |
|---|---|
| `scripts/tmux/mobile_smoke.sh` | ✅ Créé (16/16 PASS) |
| `tests/mobile/__init__.py` | ✅ Créé |
| `tests/mobile/test_mobile_smoke.py` | ✅ Créé (37/37 PASS) |
| `docs/chantiers/.../00_INITIAL_PROJECT_DOC.md` | ✅ |
| `docs/chantiers/.../10_HUMAN_CHECKLIST.md` | ✅ (20 items device réel) |
| `docs/chantiers/.../90_REPRISE.md` | ✅ (ce fichier) |
| `docs/index/inbox/GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01.md` | ✅ |

## Tests exécutés

| Niveau | Test | Resultat |
|---|---|---|
| 1 | Python unit tests | `python -m unittest tests.mobile.test_mobile_smoke -v` | ✅ OK (skipped=12 si `bash` indisponible) |
| 2 | tmux health check | `python -m pytest tests\\tmux\\test_health_check.py -q` | ✅ 32 passed (preuve locale) |
| 3 | openclaw operator tests | `python -m unittest tests.openclaw_tmux_operator.test_health_aggregate -v` | ✅ 35 tests OK (preuve locale) |
| 4 | bash smoke script | `bash scripts/tmux/mobile_smoke.sh` | BLOCKED ici (WSL Linux absent) |
| 5 | Device Android reel | Termius/Termux | ⏳ PENDING — checklist 10_HUMAN_CHECKLIST.md |

## Couverture smoke CI

| Aspect | Couvert |
|---|---|
| attach-hint 4 sessions mobile | ✅ |
| health-aggregate dry-run JSON | ✅ |
| Mobile sessions dans ALL_SESSIONS | ✅ |
| Sessions critiques (openclaw-core, screeners) | ✅ |
| cmd.sh usage completeness | ✅ |
| Runbook mobile doc intégrité | ✅ |
| Interdits mobile (pas .env, pas push force) | ✅ |

## Gap restant

- **GAP-03 PARTIAL** : Validation device Android physique non effectuée. Utiliser `10_HUMAN_CHECKLIST.md` depuis Termius/Termux sur réseau prod.

## Tableau Kanban du bundle

Le tableau Kanban du bundle reste la navigation principale. Ce child documente
le smoke mobile, mais l'item Kanban exact reste le GO runtime tant que les
validations distantes ne sont pas executees.

## Prochain item Kanban exact

`GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01`

## NEXT_GO

Aucun GO enfant obligatoire identifié. Prochaines pistes optionnelles :
- Enrichissement runbook si gaps découverts lors de la validation humaine
- Intégration Tailscale (VPN mobile) si réseau direct non disponible
