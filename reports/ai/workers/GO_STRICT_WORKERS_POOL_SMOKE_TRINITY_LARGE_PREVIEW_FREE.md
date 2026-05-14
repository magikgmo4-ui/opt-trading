# GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE

job_packet_id: GO_STRICT_WORKERS_POOL_SMOKE_TRINITY_LARGE_PREVIEW_FREE
worker_model: trinity-large-preview-free
worker_status: VERIFIED_FREE
runner_lock: ACTIVE
patch_draft_guard: ACTIVE
started_at: 2026-05-14

## 13_ESTABLISHED

Smoke READ_INVENTORY sur le modele trinity-large-preview-free, nouveau dans l'endpoint OpenCode Zen. Scope borne a 3 fichiers. Modele route en A1 (read-only), usage conservatif (READ_INVENTORY uniquement). Runner lock Phase A actif.

## 14_HYPOTHESIS

Le modele trinity-large-preview-free est un modele "large" en preview gratuite. L'usage conservatif A1 avec READ_INVENTORY uniquement est approprie tant que les capacites reelles ne sont pas validees. Si le modele demontre des capacites de raisonnement, il pourrait etre promu a A2 (DOC_DRAFT, PATCH_DRAFT) apres validation supplementaire.

## 15_REMAINING_GAP

- Modele "large preview" — pas de documentation sur les cas d'usage optimaux.
- Usage restreint a READ_INVENTORY (A1) par prudence.
- Aucun test DOC_DRAFT ni PATCH_DRAFT.
- Quotas utilisateur non documentes pour ce modele.

## 16_TODO

1. Valider ce smoke -> PASS.
2. Consolider les 3 smokes dans le rapport global.
3. Si comportement READ_INVENTORY satisfaisant : envisager test DOC_DRAFT en GO separe.
4. Documenter les quotas si disponibles.

## FICHIERS_LUS

1. `docs/agents/strict_workers/STRICT_WORKERS_AUTONOMIE_ETROITE_01.md`
2. `scripts/ai/workers/models.registry.json`
3. `scripts/ai/workers/tasks.index.json`

## INVENTAIRE

| Element | Valeur |
|---------|--------|
| trinity-large-preview-free config_id | `opencode/trinity-large-preview-free` |
| trinity-large-preview-free status | VERIFIED_FREE |
| trinity-large-preview-free autonomy | A1 |
| trinity-large-preview-free roles | READ_INVENTORY |
| Usage | conservatif — A1 uniquement |
| Note registry | "Usage conservatif A1 uniquement" |

## RISQUES

- Modele "large" inconnu — comportement non previsible sans test reel.
- Preview = peut etre retire ou modifie sans preavis.
- Restriction volontaire a READ_INVENTORY tant que non valide.

## VERDICT_DRAFT_ONLY

DRAFT_ONLY — Smoke READ_INVENTORY trinity-large-preview-free termine. Modele correctement integre au registry (A1, READ_INVENTORY uniquement). Pret pour usage operationnel conservatif apres validation globale.
