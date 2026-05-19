# 10 — Checklist validation humaine device

À exécuter depuis un device Android (Termius ou Termux) connecté au réseau de prod.

## Pré-requis

- [ ] Clé SSH mobile chargée dans Termius / Termux (pas de mot de passe en clair)
- [ ] Accès réseau db-layer et admin-trading confirmé (VPN si requis)
- [ ] Aucun secret mobile affiché à l'écran

## Bloc 1 — Connexion db-layer

| # | Commande | Résultat attendu | PASS/FAIL |
|---|---|---|---|
| 1.1 | `ssh db-layer` | Shell opérationnel | |
| 1.2 | `hostname` | `db-layer` | |
| 1.3 | `tmux ls` | Liste des sessions (openclaw-core, fleet-status au minimum) | |
| 1.4 | `tmux attach -t openclaw-core` | Attachement session | |
| 1.5 | `Ctrl+b d` (détacher) | Retour shell, session toujours active | |
| 1.6 | `tmux attach -t fleet-status` | Attachement session | |
| 1.7 | `Ctrl+b d` | Retour shell | |

## Bloc 2 — Connexion admin-trading

| # | Commande | Résultat attendu | PASS/FAIL |
|---|---|---|---|
| 2.1 | `ssh admin-trading` | Shell opérationnel | |
| 2.2 | `tmux ls` | Sessions desk-pro, screeners présentes | |
| 2.3 | `tmux attach -t desk-pro` | Attachement session | |
| 2.4 | `Ctrl+b d` | Retour shell | |
| 2.5 | `tmux attach -t screeners` | Attachement session | |
| 2.6 | `Ctrl+b d` | Retour shell | |

## Bloc 3 — Commandes read-only depuis mobile

| # | Commande | Résultat attendu | PASS/FAIL |
|---|---|---|---|
| 3.1 | `cd /opt/trading && python3 modules/runtime_health/fleet_orchestrator.py --dry-run` | JSON fleet_status WARN/PASS | |
| 3.2 | `bash modules/openclaw_tmux_operator/scripts/cmd.sh health-aggregate --dry-run` | JSON aggregat machines | |
| 3.3 | `bash modules/openclaw_tmux_operator/scripts/cmd.sh session-logs openclaw-core 20` | Dernières 20 lignes log | |
| 3.4 | `bash modules/openclaw_tmux_operator/scripts/cmd.sh health-all` | Sessions tmux listées | |

## Bloc 4 — Interdits vérifiés

| # | Vérification | PASS/FAIL |
|---|---|---|
| 4.1 | Aucun `.env` affiché | |
| 4.2 | Aucun `git push` exécuté | |
| 4.3 | Aucun `trade_executor` / `kil_v1` touché | |
| 4.4 | Aucun write tmux (send-keys, new-session) | |

## Score PASS

Objectif : 20/20 items PASS pour valider GAP-03.
