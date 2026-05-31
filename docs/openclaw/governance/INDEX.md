---
doc_id: OPENCLAW_GOVERNANCE_INDEX
doc_type: governance_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw/governance — Governance & Targets

## Documents canoniques

| Document | Path | Status | Updated |
| --- | --- | --- | --- |
| OpenClaw Target Canon | `docs/product_targets/OPENCLAW_TARGET_CANON.md` | validated | 2026-04-23 |
| Project Card OpenClaw | `docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md` | validated | 2026-04-23 |

## Synthèse TARGET_CANON

```
doc_id: OPT_TRADING_OPENCLAW_TARGET_CANON
status: validated / lifecycle_stage: reprise
```

**Position produit OpenClaw :**

```
OpenClaw = labo Linux cloisonné sur db-layer
role     = couche expérimentale / provider LLM
isolation = utilisateur dédié, environnement isolé
règles   = intégration sous contrôle strict
           non exposé directement aux flux critiques
           pas de bypass PR/GitHub Actions
```

**Hiérarchie documentaire :**

```
MATRICE_DOC_OPS_MASTER_MATRIX_01.md      ← souverain
  └─> MATRICE_GOUVERNANTE_V2.md
  └─> PRODUCT_CONTINUITY_HIERARCHY_01.md
        └─> OPENCLAW_TARGET_CANON.md     ← annexe produit, non souveraine
```

TARGET_CANON ne remplace pas la matrice ni les arbitrages de frontière `openclaw` / `opt-trading`.
Toujours lire la matrice souveraine avant d'utiliser TARGET_CANON comme base de décision.

## Synthèse PROJECT_CARD_OPENCLAW_01

```
doc_id: OPT_TRADING_PROJECT_CARD_OPENCLAW_01
status: validated / date: 2026-04-14
```

**But final retenu :**

```
OpenClaw = cockpit opérateur local sur db-layer
focus    = installation, configuration, gateway, reprise opérateur
```

**Rôle de la fiche :**

Fiche compacte de reprise — agrège en un seul point :
- but final retenu
- plan validé
- état établi
- non établi
- point de reprise

Ne remplace pas les docs module par module ni les notes d'évidence.

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
Retour vers ChatGPT = encore à formaliser (GAP 3 actif)
```

## Vérification

```bash
head -80 docs/product_targets/OPENCLAW_TARGET_CANON.md
head -80 docs/ot/project_cards/PROJECT_CARD_OPENCLAW_01.md
```
