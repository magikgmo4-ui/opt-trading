---
doc_id: OPENCLAW_GOVERNANCE_INDEX
doc_type: governance_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw/governance — Governance & Targets (2 docs)

Source : `01_SOURCE_CARTOGRAPHY.md` CLASS 4.

## Documents canoniques

| Document | Path | Rôle |
| --- | --- | --- |
| OpenClaw Target Canon | `docs/product_targets/OPENCLAW_TARGET_CANON.md` | Cible produit canonique OpenClaw |
| Project Card OpenClaw | `docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md` | Fiche projet OpenClaw |

## Règles de gouvernance établies

```
OpenClaw ne contourne pas GitHub Actions.
Pas de direct push / reset hard / auto-merge.
Force push seulement avec --force-with-lease si nécessaire.
PR gated obligatoire pour tout changement durable.
OpenClaw orchestre — il n'exécute pas sans gate humain.
```

## Principes d'orchestration

```
ChatGPT  = couche conversationnelle / gouvernance
OpenClaw = couche orchestration / opérateur
IDE / agents / jobs = surfaces d'exécution
Retour vers ChatGPT = encore à formaliser (GAP 3)
```

## Vérification

```bash
cat docs/product_targets/OPENCLAW_TARGET_CANON.md | head -40
cat docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md | head -40
```
