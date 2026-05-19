---
doc_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01_CLOSEOUT
doc_type: closeout
repo: opt-trading
project: opt-trading
module: agents
go_id: GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01
status: draft_canonical
lifecycle_stage: draft
topic_keys:
  - opt-trading
  - strict_workers
  - closeout
  - job_packets
surface: chantier
source_kind: canonical
updated_at: 2026-05-19
---

# 90_CLOSEOUT

## Resume

- 8 job packets promus de drafts (40_JOB_PACKET_DRAFTS.md) vers fichiers JSON
- Fichiers places dans scripts/ai/workers/job_packets/
- Chaque packet suit le schema exact valide par _validate_job.py
- Tous les packets en statut DRAFT_ONLY (pas de run externe)

## Fichiers crees

- 8 JSON: scripts/ai/workers/job_packets/GO_STRICT_WORKERS_*_MATRIX_01.json
- 4 docs: docs/chantiers/GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01/*.md

## Etat final

- Branch: go/GO_OPT_TRADING_STRICT_WORKERS_CHILD_JOB_PACKETS_PROMOTION_01
- Base: origin/sot/mainline
- PR: (a creer)
- Status: DRAFT_ONLY / DRY_RUN

## NEXT_GO

(Prochain GO a determiner apres merge)

## Gaps identifiees

1. CHERRY_PICK_INVENTORY: allowed_inputs convertis de commandes git vers file globs
   - Impact: le worker peut lire les fichiers mais les commandes git restent autorisees dans instructions
2. ENDPOINT_AUDIT: allowed_inputs limite a registry + index (URL non representable)
   - Impact: le worker doit fetch l endpoint via curl, autorise par instructions
3. WRITE_GATED: allowed_outputs etendus pour couvrir docs/ reports/ et job_packets/
   - Impact: scope plus large que les autres packets, compense par acceptance stricts
