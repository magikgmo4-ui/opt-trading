---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_ARCHITECTURE_MAP_01
updated_at: 2026-05-28
---

# 40_GAPS_AND_NEXT_GO

## Gaps identifiés

### G01 — tasks.index.json en DRAFT_ONLY

`scripts/ai/workers/tasks.index.json` — schema 0.3-draft, statut `DRAFT_ONLY`.
Aucun registre formel des 30 job_packets ni des 26 workers Python.
**Priorité : HIGH** — bloque le jobs registry.

### G02 — orchestration/ contrat non connecté

`scripts/ai/workers/orchestration/external_apps_orchestration_contract.json` — présent mais
non référencé par les workers opérationnels actuels.
**Priorité : MEDIUM** — à qualifier lors du jobs dedup audit.

### G03 — scripts/ UI desk_pro multiplement patchés

`scripts/apply_desk_pro_*.sh` — 6+ scripts de patch UI séquentiels sans registre.
Possible accumulation de patches dont certains obsolètes.
**Priorité : MEDIUM** — à intégrer dans le jobs dedup audit.

### G04 — gated-pr.yml python-version 3.x (floating)

`.github/workflows/gated-pr.yml` — `python-version: "3.x"` — seul workflow non homogénéisé.
**Priorité : LOW** — batch refactor dédié (hors scope architecture).

### G05 — AI workers sans tests unitaires

26 workers Python dans `scripts/ai/workers/*.py` — aucun test unitaire recensé.
`_validate_job.py` valide les packets JSON mais pas la logique des workers.
**Priorité : MEDIUM** — à couvrir dans un test lock batch.

### G06 — openclaw_operator_bridge rôle non documenté dans CLAUDE.md

`modules/openclaw_operator_bridge/` — présent et opérationnel mais absent de l'architecture CLAUDE.md.
**Priorité : LOW** — doc à mettre à jour.

---

## Décisions de scope pour les child GOs suivants

| Gap | Child GO recommandé |
|---|---|
| G01 tasks.index.json | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01 |
| G02 orchestration contrat | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01 |
| G03 desk_pro patches | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01 |
| G04 gated-pr python-version | batch refactor mineur dédié (hors automation ops) |
| G05 workers sans tests | GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01 ou test lock batch |
| G06 openclaw_operator_bridge | doc patch mineur |

---

## NEXT_GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_REGISTRY_01
```

Objectif : construire `docs/registry/JOBS_REGISTRY.md` en appliquant
le schéma défini dans `20_JOBS_REGISTRY_SPEC.md`.
Scope prioritaire v1 : GHA (7) + job_packets (30) + workers Python clés (26) + OpenClaw scripts.

---

## Verdict

```text
PASS_ARCHITECTURE_MAP_READY

Carte complète : 7 surfaces, 7 flux, 14 gates humains, 6 gaps qualifiés.
Aucune mutation. Lecture seule.
```
