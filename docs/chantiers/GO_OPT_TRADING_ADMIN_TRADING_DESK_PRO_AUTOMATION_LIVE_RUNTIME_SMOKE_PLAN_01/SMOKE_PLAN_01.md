---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_PLAN_01
doc_type: smoke_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_LIVE_RUNTIME_SMOKE_PLAN_01
status: active
lifecycle_stage: cadrage
surface: chantier
source_kind: canonical
updated_at: 2026-05-13
---

# SMOKE_PLAN_01 - Desk Pro Automation Live Runtime Smoke Plan

## 1_INITIAL_NEED

Valider le Desk Pro dry-run enrichi en conditions live simulées, sans jamais exposer de trade réel, webhook réel, Telegram réel, ou secret.

## 4_MASTER_PROJECT_PLAN linkage

Dépend de:
- PR #303 (Desk Pro Automation dry-run/timer sequence)
- PR #325 (Desk Pro Artifact Output sequence)
- PR #347 (Desk Pro Input Enrichment sequence)

## 6_FINAL_TARGET

Planifier un GO `EXECUTION_GATED_01` capable de:
1. Exécuter le service systemd desk_pro_dry_run.service avec les trois inputs réels
2. Lire les artefacts générés
3. Confirmer que les safety flags restent true
4. Aucun side effect runtime interdit

## 7_CANONICAL_STATE

- `sot/mainline` @ `50df15c`
- PR #303, #325, #347 merged
- Timer installed, enabled, active/waiting
- Tests: 84/84 PASS
- Artifacts under `/opt/trading/runtime/desk_pro_dry_run/` (gitignored)
- Three inputs ready: signal_event, visual_context, desk_snapshot

## 8_VALIDATED_PLAN

1. Pas de smoke live direct dans ce GO (docs only)
2. Préparer la matrice de smoke

## 12_INVARIANTS

- Ne pas exécuter de live runtime réel
- Ne pas déclencher d'ordre réel
- Ne pas exposer ni copier de secret
- Ne pas modifier les index globaux
- Ne pas modifier les fichiers systemd installés
- Ne pas start/stop le timer ou le service
- Ne pas envoyer Telegram
- Ne pas déclencher webhook

## Préconditions runtime

| Précondition | État |
| --- | --- |
| Timer installé | OK |
| Timer enabled | OK |
| Timer actif | OK |
| Service static | OK |
| Three inputs ready | OK |
| Safety gates in code | Verified (no_trade, no_telegram, no_webhook, no_systemd) |
| Artifact path writable | OK |
| Tests 84/84 | OK |

## Garde-fous live

- `no_trade=true` DOIT rester `true` dans toute la durée du smoke
- `no_telegram=true` DOIT rester `true`
- `no_webhook=true` DOIT rester `true`
- `no_systemd=true` DOIT rester `true`
- Aucun appel réseau sortant vers un service externe
- Aucune écriture hors `/opt/trading/runtime/desk_pro_dry_run/`
- Aucune lecture de `.env`
- Arrêt immédiat si un safety flag passe à `false`

## Matrice PASS / WARN / FAIL

| Condition | Verdict |
| --- | --- |
| sortie `0/SUCCESS` | PASS |
| `errors=[]` | PASS |
| safety flags tous `true` | PASS |
| trois inputs présents | PASS |
| artefact `latest.json` produit | PASS |
| `warnings` non bloquantes | WARN |
| `errors` non vides | FAIL (bloquant) |
| safety flag `false` | FAIL (critique, arrêt immédiat) |
| artefact manquant | FAIL |
| sortie non-zero | FAIL |

## Smoke cases (mode observation/simulation)

1. **Timer start gated** — `systemctl start desk_pro_dry_run.timer`, observer le prochain cycle naturel, vérifier artefacts
2. **Artifact output check** — lire `latest.json`, confirmer status/safety/inputs
3. **Signal event enrichment** — injecter signal_event via `DESK_PRO_DRY_RUN_SIGNAL_EVENT_PATH`
4. **Visual context enrichment** — injecter visual_context via `DESK_PRO_DRY_RUN_VISUAL_CONTEXT_PATH`
5. **Desk snapshot enrichment** — confirmer que snapshot réel est chargé
6. **Fallback behavior** — retirer les inputs, confirmer fallback WARN attendu

## Actions interdites

- `systemctl start desk_pro_dry_run.service`
- `systemctl stop desk_pro_dry_run.timer` pendant un run
- Modification des unit files systemd
- Modification de `/etc/systemd/system/`
- Écriture de secrets dans les artefacts
- Telegram / webhook / trade
- `enable`, `disable`, `daemon-reload`

## Critères d'ouverture du GO d'exécution

- Ce plan est validé (review/doc PASS)
- Tests 84/84 toujours verts
- Safety gates à jour dans `modules/webhook/paper_guards.py`
- Timer actif et enabled
- Pas de run en cours
