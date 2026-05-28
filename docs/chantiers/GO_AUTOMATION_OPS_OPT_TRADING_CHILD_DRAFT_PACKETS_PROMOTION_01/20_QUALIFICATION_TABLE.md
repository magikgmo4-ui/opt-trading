---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01_QUALIFICATION
doc_type: qualification_table
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_DRAFT_PACKETS_PROMOTION_01
status: GATE_HUMAIN_REQUIS
created_at: 2026-05-28
---

# 20_QUALIFICATION_TABLE

## 1_TABLE_COMPLÈTE

| # | Packet | Famille | Verdict | Raison | Registry change |
|---|--------|---------|---------|--------|-----------------|
| 1 | `GO_STRICT_WORKERS_READONLY_SMOKE_01` | A | **promote_candidate** | Workers VERIFIED, inputs existent, go_id actif | status: DRAFT_ONLY → candidate |
| 2 | `GO_STRICT_WORKERS_POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE` | B | **promote_candidate** | Worker `deepseek-v4-flash-free` VERIFIED_FREE | status: DRAFT_ONLY → candidate |
| 3 | `GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE` | B | **deprecate** | Worker `ring-2.6-1t-free` RETIRED_CURRENT_ENDPOINT | status: DRAFT_ONLY → deprecated |
| 4 | `GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE` | B | **deprecate** | Worker `trinity-large-preview-free` RETIRED_CURRENT_ENDPOINT | status: DRAFT_ONLY → deprecated |
| 5–12 | `GO_STRICT_WORKERS_*_MATRIX_01` (8) | C | **pending_parent** | Parent `POOL_EXTENSION` status=cadrage — pas fermé | aucune (bloquer en DRAFT_ONLY) |
| 13 | `GO_STRICT_WORKERS_PATCH_DRAFT_IMPL_01` | D | **pending_parent** | Parent `RUNTIME_LOCK` status=cadrage — pas fermé | aucune |
| 14–20 | `GO_OPT_TRADING_DOC_OPS_*` (7) | E | **pending_parent** | Parent `DOC_OPS_PATCH_ZIP` status=draft_canonical — pas fermé | aucune |

## 2_DÉTAIL_PROMOTIONS

### promote_candidate — 2 packets

**#1 GO_STRICT_WORKERS_READONLY_SMOKE_01**
- Workers valides : qwen3.5-plus, minimax-m2.5, kimi-k2.5, big-pickle, gpt-5-nano — tous VERIFIED
- Inputs référencés existants dans `docs/agents/strict_workers/`
- go_id parent actif
- Changement dans packet : `"status": "DRAFT_ONLY"` → `"status": "candidate"`

**#2 GO_STRICT_WORKERS_POOL_SMOKE_DEEPSEEK_V4_FLASH_FREE**
- Worker assigné `deepseek-v4-flash-free` : VERIFIED_FREE dans models.registry
- Inputs valides
- Changement dans packet : `"status": "DRAFT_ONLY"` → `"status": "candidate"`

### deprecate — 2 packets

**#3 GO_STRICT_WORKERS_POOL_SMOKE_RING_2_6_1T_FREE**
- Worker `ring-2.6-1t-free` : RETIRED_CURRENT_ENDPOINT — endpoint non disponible
- Changement dans packet : `"status": "DRAFT_ONLY"` → `"status": "deprecated"`

**#4 GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE**
- Worker `trinity-large-preview-free` : RETIRED_CURRENT_ENDPOINT — endpoint non disponible
- Changement dans packet : `"status": "DRAFT_ONLY"` → `"status": "deprecated"`

### pending_parent — 16 packets

Aucune modification. Ces packets restent DRAFT_ONLY jusqu'à fermeture de leur parent :
- Famille C (8) : attendent `GO_OPT_TRADING_STRICT_WORKERS_CHILD_WORKER_POOL_EXTENSION_01`
- Famille D (1) : attend `GO_OPT_TRADING_STRICT_WORKERS_CHILD_RUNTIME_LOCK_AND_E2E_01`
- Famille E (7) : attendent `GO_OPT_TRADING_DOC_OPS_CHILD_PATCH_ZIP_EXECUTION_FORMAT_V2_01`

## 3_REGISTRY_UPDATES_REQUIS

Après gate humain, dans `docs/registry/JOBS_REGISTRY.md` Section 3 :

| job_id registry | Changement |
|-----------------|-----------|
| `jp_strict_readonly_smoke` | status: `DRAFT_ONLY` → `candidate` |
| `jp_strict_pool_smoke_deepseek` | status: `DRAFT_ONLY` → `candidate` (entrée à créer si absente) |
| `jp_strict_pool_smoke_ring` | status: `DRAFT_ONLY` → `deprecated` |
| `jp_strict_pool_smoke_trinity` | status: `DRAFT_ONLY` → `deprecated` |
| `jp_strict_pool_smoke_*` note générale | ajouter note : ring/trinity RETIRED — voir models.registry |

## 4_GATE_HUMAIN

```
STATUS : VALIDÉ_OPÉRATEUR — 2026-05-28
```

| # | Action | Décision |
|---|--------|----------|
| P1 | Promouvoir `READONLY_SMOKE` → candidate | **OUI** — appliqué |
| P2 | Promouvoir `POOL_SMOKE_DEEPSEEK` → candidate | **OUI** — appliqué |
| P3 | Déprécier `POOL_SMOKE_RING` + `POOL_SMOKE_TRINITY` | **OUI** — appliqué |
| P4 | 16 packets `pending_parent` sans modification | **OUI** — confirmé |

Note P3 : RING avait `worker_assigned: deepseek-v4-flash-free` (pas ring-2.6-1t-free) — nom trompeur.
TRINITY avait `worker_assigned: nemotron-3-super-free` — nom trompeur. Dépréciations justifiées par incohérence nom/contenu.
