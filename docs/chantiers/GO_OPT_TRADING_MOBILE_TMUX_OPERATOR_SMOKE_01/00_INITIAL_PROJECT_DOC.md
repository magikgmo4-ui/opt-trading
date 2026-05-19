# GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` |
| Objet | Smoke tests mobile SSH/tmux operator — validation sans device physique en CI + checklist manuelle Termius/Termux |
| Parent | `GO_OPT_TRADING_RUNTIME_ORCHESTRATOR_TMUX_FLEET_MOBILE_DEPLOY_01` (PR #618) |
| Déclencheur | GAP-03 : Tests mobile réel non effectués — dispositif physique requis |
| Branche | `go/GO_OPT_TRADING_MOBILE_TMUX_OPERATOR_SMOKE_01` |

## Stratégie

Les tests mobile réels (SSH depuis Termius/Termux vers db-layer) nécessitent un device Android physique — non testable en CI. Ce GO crée :

1. **Smoke tests CI** — valident la logique sans SSH réel ni device
2. **Script simulation** — reproduit le comportement mobile en local
3. **Checklist humaine** — matrice de validation à exécuter sur device réel

## État initial (après audit)

| Zone | Statut |
|---|---|
| `docs/chantiers/.../40_MOBILE_OPERATOR_ACCESS.md` (parent) | ✅ Runbook mobile complet |
| `modules/openclaw_tmux_operator/scripts/cmd.sh` (`attach-hint`) | ✅ Commande mobile clé |
| `modules/openclaw_tmux_operator/scripts/health_aggregate.py` | ✅ Dry-run utilisable depuis mobile |
| Script smoke mobile | ❌ Gap — à créer |
| Tests Python mobile | ❌ Gap — à créer |
| Checklist validation humaine device | ❌ Gap — à créer |

## Machines cibles mobile

| Machine | Sessions prioritaires |
|---|---|
| db-layer | openclaw-core, fleet-status |
| admin-trading | desk-pro, screeners |
