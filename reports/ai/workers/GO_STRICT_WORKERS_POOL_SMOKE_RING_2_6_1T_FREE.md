# GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE

job_packet_id: GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE
worker_model: ring-2.6-1t-free
worker_status: VERIFIED_FREE
runner_lock: ACTIVE
patch_draft_guard: ACTIVE
started_at: 2026-05-14

## 13_ESTABLISHED

Smoke READ_INVENTORY sur le modele ring-2.6-1t-free, nouveau dans l'endpoint OpenCode Zen au 2026-05-14 (possible successeur de ling-2.6-flash-free, retire). Scope borne a 3 fichiers. Modele route en A1 (read-only). Runner lock Phase A actif.

## 14_HYPOTHESIS

Le modele ring-2.6-1t-free est un nouveau venu dans l'endpoint. S'il est effectivement le successeur de ling-2.6-flash-free (meme famille de nommage), il devrait offrir des capacites similaires de tri rapide et d'inventaire.

## 15_REMAINING_GAP

- Modele totalement nouveau — aucune reference historique dans le projet.
- Relation exacte avec ling-2.6-flash-free non confirmee (hypothese de succession).
- Pas de test FAST_TRIAGE (second role declare).

## 16_TODO

1. Valider ce smoke -> PASS.
2. Tester trinity-large-preview-free.
3. Consolider dans le rapport de smoke pool.
4. Si PASS global : ajouter aux preferred_workers operationnels.

## FICHIERS_LUS

1. `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md`
2. `scripts/ai/workers/models.registry.json`
3. `scripts/ai/workers/tasks.index.json`

## INVENTAIRE

| Element | Valeur |
|---------|--------|
| ring-2.6-1t-free config_id | `opencode/ring-2.6-1t-free` |
| ring-2.6-1t-free status | VERIFIED_FREE |
| ring-2.6-1t-free autonomy | A1 |
| ring-2.6-1t-free roles | READ_INVENTORY, FAST_TRIAGE |
| ling-2.6-flash-free status | RETIRED_CURRENT_ENDPOINT |
| Note registry | "Possible successeur de ling-2.6-flash-free" |
| Preferred dans tasks.index | READ_INVENTORY, FAST_TRIAGE |

## RISQUES

- Modele free nouveau — peut etre temporaire (cf. hy3-preview-free retire en 3 semaines).
- Succession ling → ring non confirmee officiellement.

## VERDICT_DRAFT_ONLY

DRAFT_ONLY — Smoke READ_INVENTORY ring-2.6-1t-free termine. Modele correctement integre au registry et au task index. Pret pour usage A1 operationnel apres validation globale.
