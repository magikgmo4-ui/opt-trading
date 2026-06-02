---
doc_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01_INITIAL
doc_type: initial_project_doc
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
status: open
opened_at: 2026-06-01
---

# GO_OPENCLAW_DBLAYER_WORKERS_CHILD_JOBS_ACTIVATION_PRIORITY_01

## 1_MASTER_TARGET

Produire une matrice d'activation priorisée des 114 jobs non-trading,
scorée sur 5 axes (priorité, cadence, utilité, pertinence, efficacité),
pour décider lesquels activer en premier via OpenClaw dispatcher ou GHA.

## 2_CONTEXT

- `GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01` : toutes
  les 9 phases exécutées (101 PASS, 13 WARN, 0 FAIL). Chaque job a une
  smoke PASS ou dry-run PASS. Pas encore activés en production récurrente.
- `GO_OPENCLAW_DBLAYER_WORKERS_CHILD_STRICT_DISPATCHER_01` : dispatcher
  déterministe opérationnel (PR #1043, PR #1044).
- `GO_OPENCLAW_DBLAYER_WORKERS_CHILD_BRIDGE_DISPATCH_01` : OperatorBridge
  câblé au dispatcher (PR #1045 — 18/18 tests PASS, prod smoke PASS).
- Maintenant que le dispatcher existe, on peut activer des jobs via
  `BridgeRequest(action="dispatch", parameters={"packet_id": ...})`.

## 3_SCOPE

Sources analysées :
- `docs/chantiers/GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01/10_NON_TRADING_JOBS_REGISTER.md` — 114 jobs A-I
- `docs/registry/JOBS_REGISTRY.md` — ~86 jobs (JOBS_REGISTRY_V1)

## 4_LIVRABLES

1. `10_ACTIVATION_MATRIX.md` — matrice scorée avec verdict par job
   - Score priorité (P1–P5)
   - Cadence réelle recommandée
   - Vecteur d'activation (dispatcher / GHA / script direct / manual / bloqué)
   - Verdict : `NOW` / `NEXT` / `LATER` / `MANUAL_ONLY` / `BLOCKED`
   - Lot 1 (<= 15 jobs) : activation immédiate recommandée
   - Lot 2 (<= 20 jobs) : activation suivante (semaine suivante)
   - Lot 3 : planifiés mais pas urgents

## 5_CONSTRAINTS

```
✓ Aucun LLM dans la boucle de dispatch
✓ dry_run=True pour tout write-gated non approuvé
✓ gate_approved=False par défaut
✓ Les apps externes (Airtable, ClickUp, Botpress…) restent BLOCKED
  tant que le bridge contract n'est pas prouvé en live
✓ Pas de modification de code dans ce chantier — analyse uniquement
```

## 6_SUCCESS_CRITERIA

```
✓ Matrice complète couvrant 114 jobs
✓ Lot 1 identifié avec <= 15 jobs, tous vecteurs "dispatcher" ou "gha"
✓ Chaque job du Lot 1 a un script/packet existant et validé
✓ Verdict BLOCKED justifié (dépendance externe non prouvée)
```
