---
doc_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01_CALLERS_AUDIT
doc_type: callers_audit
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01
status: draft_for_review
lifecycle_stage: audit
topic_keys:
  - opt-trading
  - modules
  - deepseek
  - callers
surface: modules
source_kind: canonical_draft
updated_at: 2026-05-25
links:
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_FAMILY_CONSOLIDATION_01/10_FAMILY_INVENTORY.md
---

# 20_CALLERS_AUDIT

## Callers et preuves directes

| Surface | Caller / preuve | Lecture |
| --- | --- | --- |
| `deepseek_hub` | `opt_trading_menu.json` status `impl`; `student/scripts/MIGRATION_STATUS.md`; `scripts/student/LEGACY.md` | hub expose et reference de convergence |
| `deepseek_response` | `opt_trading_menu.json` status `impl`; `student/scripts/MIGRATION_STATUS.md`; `deepseek_hub` patches | composant encore appele |
| `deepseek_thinking` | `opt_trading_menu.json` status `impl`; `student/scripts/MIGRATION_STATUS.md`; `deepseek_hub` patches | composant encore appele |
| `deepseek_student` | `docs/product/guides/DEEPSEEK_STUDENT.md`; `student/scripts/MIGRATION_STATUS.md`; `deepseek_hub` roadmap calls | surface limitee encore referencee |

## Documentation structurante amont

Les documents suivants convergent :

- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01/04_CONSOLIDATION_ROADMAP.md`
  - `deepseek_hub` produit canonique
  - `deepseek_response` et `deepseek_thinking` a conserver comme sous-surfaces
  - `deepseek_student` a archiver / fermer
- `modules/deepseek_student/README.md`
  - surface non runtime canonique
- `modules/deepseek_hub/README.md`
  - hub le plus avance, sans remplacer encore toute la verite runtime

## Lecture callers

- `deepseek_hub` est le seul point de convergence explicitement promu
- `deepseek_response` et `deepseek_thinking` gardent des callers reels via patches, wrappers et menu
- `deepseek_student` reste appele dans les guides et certaines migrations, mais comme surface de transition, pas comme owner actuel
