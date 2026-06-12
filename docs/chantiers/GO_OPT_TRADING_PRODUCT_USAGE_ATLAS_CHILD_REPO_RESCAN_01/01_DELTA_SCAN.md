---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01_DELTA_SCAN
doc_type: delta_scan
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_RESCAN_01
parent_go: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-18
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_REPO_INVENTORY_01/02_CLASSIFICATION_MATRIX.md
  - docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md
  - docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md
---

# 01_DELTA_SCAN - Reevaluation post-2026-05-07

## Regle

Le rescan ne promeut que les surfaces dont la preuve posterieure au `2026-05-07` change reellement la lecture produit.

## Tableau de decision

| Surface | Etat avant rescan | Preuve nouvelle relue | Decision |
| --- | --- | --- | --- |
| Deepseek Student | `KEEP_CANDIDATE` hors Atlas, lecture `USABLE_LIMITED` seulement dans l'inventaire | `docs/student_deepseek_runbook.md`, `docs/status/deepseek_student_canonique.md`, `docs/chantiers/GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_IMPL_03/90_CLOSEOUT.md`, `docs/chantiers/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01/90_CLOSEOUT.md` | **ADD_TO_ATLAS** en `USABLE_LIMITED`, avec limites fortes et sans guide live nouveau |
| Bot Vision | Dans l'Atlas en `USABLE_LIMITED`, mais `NEXT_GO` ancien et preuve partielle | `docs/chantiers/GO_OPT_TRADING_VISION_RUNTIME_CONSOLIDATION_IMPL_01/90_CLOSEOUT.md` | **REFRESH_ATLAS_ENTRY** sans changer le bucket |
| derivatives_collector | Dans l'Atlas en `USABLE_LIMITED`, mais `NEXT_GO` encore pointe vers un GO deja ferme | `docs/chantiers/GO_COLLECTORS_BASELINE_INVENTORY_01/90_CLOSEOUT.md`, `docs/chantiers/GO_COLLECTORS_SELECTIVE_RUNTIME_EXTRACTION_DECISION_01/90_CLOSEOUT.md` | **REFRESH_ATLAS_ENTRY** sans changer le bucket |
| PERF runtime / perf_engine | Hors Atlas | Consolidation + restructuration + sync runtime plus nets qu'avant, mais lecture encore trop technique et multi-composants pour une entree produit propre dans ce lot | **KEEP_OUT_FOR_NOW** |

## Notes de prudence

- `Deepseek Student` reste `USABLE_LIMITED`, pas `USABLE_NOW`.
- `Deepseek Student` ne devient pas une surface de decision autonome ni un produit trading.
- `PERF` reste hors Atlas tant qu'une couche produit lisible n'est pas mieux bornee.
- Aucun changement n'est applique a `Airtable`, `Botpress`, `BTC COIN-M` ou `OpenClaw Docs Library` dans ce lot.

## RISKS

- À qualifier.
