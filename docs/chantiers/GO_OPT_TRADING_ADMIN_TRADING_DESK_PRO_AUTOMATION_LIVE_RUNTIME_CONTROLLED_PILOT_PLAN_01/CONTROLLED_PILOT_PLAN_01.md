---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_PLAN_01
doc_type: controlled_pilot_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_CONTROLLED_PILOT_PLAN_01
status: active
updated_at: 2026-05-13
---

# CONTROLLED_PILOT_PLAN_01

## 1_INITIAL_NEED

Transformer le smoke PASS en plan pilote contrôlé pour monitorer le Desk Pro dry-run enrichi en conditions runtime réelles, sans augmenter le risque.

## 4_MASTER_PROJECT_PLAN linkage

Dépend de:
- PR #303 (Desk Pro Automation dry-run/timer sequence)
- PR #325 (Desk Pro Artifact Output sequence)
- PR #347 (Desk Pro Input Enrichment sequence)
- PR #349 (Live Runtime Smoke Plan)
- PR #350 (Live Runtime Smoke Execution — PASS 6/6)

## 6_FINAL_TARGET

Planifier un GO `EXECUTION_GATED_01` capable de:
1. Exécuter le pilote contrôlé avec monitoring actif
2. Collecter métriques d'observation
3. Respecter les limites et seuils d'arrêt
4. Rollback immédiat si seuil critique atteint

## 7_CANONICAL_STATE

- `sot/mainline` @ `260f044`
- PR #303, #325, #347, #349, #350 merged
- Timer installed, enabled, active/waiting
- Tests: 84/84 PASS
- Smoke execution: PASS 6/6
- Safety flags: true throughout

## 8_VALIDATED_PLAN

1. Docs-only dans ce GO
2. Définir périmètre, limites, seuils, rollback

## 12_INVARIANTS

- Ne pas exécuter le pilote dans ce GO
- Ne pas déclencher d'ordre réel
- Ne pas exposer ni copier de secret
- Ne pas modifier les index globaux
- Ne pas modifier les fichiers systemd installés
- Ne pas start/stop le timer ou le service
- Ne pas envoyer Telegram
- Ne pas déclencher webhook

## Périmètre pilote

- Observation du timer systemd actif
- Collecte des artefacts latest.json, latest.md, history.jsonl
- Surveillance des safety flags (no_trade, no_telegram, no_webhook, no_systemd)
- Aucune interaction avec le trading réel
- Aucune injection de signal externe
- Aucune modification de configuration live

## Préconditions

| Condition | État |
| --- | --- |
| Timer installed | OK |
| Timer enabled | OK |
| Timer active | OK |
| Service static | OK |
| Three inputs ready | OK |
| Safety gates in code | Verified |
| Artifact path writable | OK |
| Tests 84/84 | OK |
| Smoke execution PASS | OK |
| Rollback documented | OK |

## Garde-fous runtime

- `no_trade=true` DOIT rester `true`
- `no_telegram=true` DOIT rester `true`
- `no_webhook=true` DOIT rester `true`
- `no_systemd=true` DOIT rester `true`
- Arrêt immédiat si un safety flag passe à `false`

## Limites quantitatives

| Métrique | Limite | Action si dépassée |
| --- | --- | --- |
| `errors` non vides | 0 | WARN, STOP si critique |
| safety flag `false` | 0 | STOP immédiat |
| Exécutions consécutives FAIL | 3 | STOP, investigation |
| Artefact manquant | 0 | STOP |
| Sortie non-zero | 0 | STOP |

## Seuils STOP / WARN / FAIL

| Seuil | Déclencheur | Action |
| --- | --- | --- |
| STOP | safety flag false, errors critiques, artefact manquant | Rollback immédiat |
| WARN | warnings non bloquants, execution FAIL isolée | Observation renforcée |
| PASS | Tout OK | Continuer monitoring |

## Rollback

- `sudo systemctl disable --now desk_pro_dry_run.timer`
- `sudo rm -f /etc/systemd/system/desk_pro_dry_run.service`
- `sudo rm -f /etc/systemd/system/desk_pro_dry_run.timer`
- `sudo systemctl daemon-reload`
- `sudo systemctl reset-failed desk_pro_dry_run.service desk_pro_dry_run.timer`

## Métriques d'observation

- `exit_code` par exécution
- `status` (PASS/WARN/FAIL)
- `errors` count
- safety flags
- inputs presence
- artifact size
- history.jsonl line count
- Temps entre triggers

## Actions interdites

- `systemctl start desk_pro_dry_run.service`
- Modification des unit files systemd
- Écriture de secrets
- Telegram / webhook / trade
- Modification des garde-fous

## RISKS

- À qualifier.
