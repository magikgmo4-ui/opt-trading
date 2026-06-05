---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: signal_inventory
repo: opt-trading
status: open
created_at: 2026-05-17
source_prouvee: data/journal/daily/20260517_001.json
---

# 10_SIGNAL_INVENTORY

Inventaire réel des champs présents dans `data/journal/daily/*.json`.

Source prouvée : `20260517_001.json` — dernier run connu au 2026-05-17.

---

## Champs top-level du journal

| Champ | Type | Exemple | Rôle |
| --- | --- | --- | --- |
| `run_id` | string | `"20260517_001"` | Identifiant unique du run — clé primaire naturelle |
| `session_id` | UUID string | `"ec10dc06-..."` | Identifiant session OpenClaw — tracé par run |
| `journal_type` | string | `"daily_session"` | Type de journal — actuellement fixe |
| `pipeline` | string | `"E2E dry-run..."` | Description texte du pipeline |
| `controlled_write` | bool | `false` | Écriture Sheets contrôlée — activée ou non |
| `dry_run` | bool | `true` | Mode dry-run — `true` en Phase 1 |
| `paper_mode` | bool | `true` | Mode paper — `true` en Phase 1 |
| `started_at` | ISO timestamp | `"2026-05-17T04:03:47.562Z"` | Début du run |
| `completed_at` | ISO timestamp | `"2026-05-17T04:03:47.849Z"` | Fin du run |
| `duration_s` | float | `0.3` | Durée totale du run (secondes) |
| `pipeline_duration_s` | float | `0.284` | Durée pipeline strict (secondes) |
| `all_ok` | bool | `true` | Statut global du run — `true` = PASS |
| `validation_verdict` | string | `"APPROVED"` | Verdict de la validation gate |
| `trade_executor_status` | string | `"dry_run"` | Statut de l'executor — `dry_run` / `paper` / `live` |
| `result_tracker_outcome` | string | `"win"` | Résultat du tracker — `win` / `loss` / `breakeven` |
| `pnl_paper` | object | `{"net_pnl": 438.03, "outcome": "win"}` | P&L papier du run |
| `signal_source` | string/object | — | Source du signal trading |
| `proposition_summary` | object | — | Résumé de la proposition |
| `datasheet_writer` | object | — | Résultat écriture datasheet |
| `learning_feeder` | object | — | Résultat learning feeder |
| `localcms` | object | — | Résultat mise à jour LocalCMS |
| `localcms_ok` | bool | `false` | LocalCMS mis à jour avec succès — `false` si indisponible |
| `localcms_before` | object | — | État LocalCMS avant run |
| `localcms_after` | object | — | État LocalCMS après run |
| `tmux_before` | object | — | État tmux avant run |
| `tmux_after` | object | — | État tmux après run |
| `closeout_required` | bool | `false` | Closeout requis — `true` si anomalie bloquante |
| `closeout_acknowledged` | bool | `false` | Closeout acquitté par l'opérateur |

---

## Structure `steps` (7 étapes de pipeline)

| Étape | Rôle | Champs résultat observés |
| --- | --- | --- |
| `1_signal_router` | Routage du signal trading | `signal_id`, `ticker`, `side`, `price`, `strategy_id`, `tf`, `tp`, `sl` |
| `2_proposition_engine` | Moteur de proposition | `request_id`, `action`, `size_pct`, `entry`, `confidence`, `rationale`, `status` |
| `3_validation_gate` | Gate de validation | résultat validation, verdict |
| `4_trade_executor` | Exécuteur (dry_run) | `status: dry_run` en Phase 1 |
| `5_result_tracker` | Tracker résultat | `outcome: win/loss/breakeven`, P&L |
| `6_datasheet_writer` | Écriture datasheet | résultat écriture |
| `7_learning_feeder` | Alimentation learning | résultat feeder |

---

## Structure `pnl_paper`

| Champ | Type | Exemple |
| --- | --- | --- |
| `net_pnl` | float | `438.03` |
| `outcome` | string | `"win"` |

---

## Champs clés pour l'observation (signaux prioritaires)

Ces champs sont suffisants pour qualifier un run comme PASS/FAIL et alimenter un dashboard :

| Champ | Priorité observation | Note |
| --- | --- | --- |
| `run_id` | P0 — clé primaire | format `YYYYMMDD_NNN` |
| `all_ok` | P0 — statut run | `true` = PASS |
| `started_at` | P0 — timestamp | ISO UTC |
| `pnl_paper.net_pnl` | P1 — P&L session | float |
| `result_tracker_outcome` | P1 — win/loss | string |
| `dry_run` + `paper_mode` | P1 — mode guard | `true/true` en Phase 1 |
| `localcms_ok` | P1 — santé LocalCMS | bool |
| `closeout_required` | P1 — anomalie bloquante | bool |
| `session_id` | P2 — traçabilité session | UUID |
| `validation_verdict` | P2 — gate | APPROVED / REJECTED |
| `trade_executor_status` | P2 — mode executor | `dry_run` / `paper` |
| `duration_s` | P2 — latence | float |

---

## Champs non retenus pour le schéma canonique d'observation

Ces champs sont trop granulaires pour l'observation de premier niveau. Ils appartiennent au détail de run, consultable dans le fichier brut.

| Champ | Raison |
| --- | --- |
| `steps` (détail complet) | Granularité step — consulter le fichier brut |
| `tmux_before/after` | État tmux — monitoring local, pas produit |
| `learning_feeder` | Détail interne pipeline |
| `signal_source` (complet) | Trop granulaire pour l'observation agrégée |
| `engines_context` | Détail moteur probabilité — niveau step |

## RISKS

- À qualifier.
