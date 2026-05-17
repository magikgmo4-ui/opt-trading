---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01
doc_type: product_alignment
repo: opt-trading
status: open
created_at: 2026-05-17
source: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
---

# 10_MASTER_PRODUCT_TARGET_ALIGNMENT

---

## Centres de gravité produit (matrice maître)

| Produit | Intention | Gap restant db-layer |
| --- | --- | --- |
| **Desk Pro** | Cockpit paper trading multi-machine, relâchable et gouverné | L'ingestion réelle côté `db-layer` n'est pas encore faite ; le flux `admin-trading → /shared → db-layer` est documenté mais non exécuté |
| **Trading Dual Stack V1** | Framework trading unique — LAB + REALTIME borné à observation | V1 close ; pas de nouvelle phase justifiée à ce stade ; db-layer n'est pas sollicité directement |
| **Bot Vision** | Pipeline vision cross-platform → artefacts Desk Pro exploitables | Cible finale cross-platform à revalider ; db-layer hors scope direct |

---

## Familles de soutien — rôle db-layer

| Famille soutien | Rôle db-layer | Statut |
| --- | --- | --- |
| `LocalCMS` | Consumer UI des données db-layer — lecture état, métriques, runs | Candidat produit — à cadrer |
| `openclaw / agents / prompt factory` | Orchestrateur principal — exécute, observe, journalise les runs | Actif — Phase 1 observation en cours |
| `satellites machines` | db-layer est un satellite machine — couche d'observation et de persistence | KEEP_ACTIVE — `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |

---

## Position db-layer dans la lecture globale

```text
db-layer est lue comme :
  1. satellite machine (couche d'observation et de persistence)
  2. famille de soutien via openclaw / agents
  3. source future pour LocalCMS / dashboard
  4. surface de preuve pour les décisions produit Desk Pro
```

db-layer n'est pas :
- un centre de gravité produit
- un chantier de cleanup seulement
- un substitut à la matrice produit

---

## Trajectoire produit correcte

```text
cleanup terminé + observation active
→ observation → data plane → dashboard/LocalCMS → decision gates → next runtime/product child
```

| Étape | Description | État |
| --- | --- | --- |
| Cleanup | Branches nettoyées, BRANCH_STATE réconcilié | CLOSED/PASS |
| Observation Phase 1 | ≥30 runs, ≥14 jours — dry-run quotidien | EN COURS (14/30 runs, 2/14 jours) |
| Data plane | Couche structurée événements → persistence → query | À définir |
| LocalCMS view | Exposition état db-layer vers dashboard opérateur | Candidat |
| Decision gate | Éligibilité multi-signal après seuils Phase 1 | Bloqué jusqu'au seuil |
| Next runtime child | Ouverture seulement après seuils atteints | Bloqué |

---

## Rattachement canonique de ce child GO

Ce child GO se rattache à :

1. **Centre de gravité Desk Pro** (via flux `admin-trading → /shared → db-layer → LocalCMS`)
2. **Famille de soutien `openclaw / agents / prompt factory`** (via Phase 1 observation orchestrée par OpenClaw)
3. **Famille de soutien `LocalCMS`** (via exposition future de l'état db-layer)
4. **Parent direct** : `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01`

---

## Surfaces documentées liées

| Surface | Rôle | Lien |
| --- | --- | --- |
| `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | Parent machine canonique db-layer | `docs/chantiers/GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01/` |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` | Ancre principale OpenClaw/db-layer | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/REPRISE_DB_LAYER_20260505.md` |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01` | GO observation Phase 1 actif | `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01/00_GO_MASTER.md` |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | Parent UI/LocalCMS consumer | `docs/chantiers/GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01/01_cadrage_parent.md` |
| `DB_LAYER_INGESTION_*` | Décisions d'ingestion db-layer | `docs/governance/DB_LAYER_INGESTION_*.md` |
