---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: closeout
repo: opt-trading
status: draft
created_at: 2026-05-17
verdict: DRAFT — à valider après lecture opérateur
---

# 90_CLOSEOUT

---

## Statut

```text
DRAFT — ce child GO est documenté mais pas encore fermé.
La fermeture intervient après validation opérateur.
```

---

## Objectif atteint

```text
Définir le schéma canonique V1 des événements d'observation OpenClaw dry-run.
Inventorier les champs réels du journal.
Documenter le mapping producteur/consommateur.
Évaluer la readiness LocalCMS.
```

---

## Livrables produits

| Fichier | Contenu | Statut |
| --- | --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Cadrage et contexte | DONE |
| `10_SIGNAL_INVENTORY.md` | Inventaire réel des champs journal | DONE |
| `20_CANONICAL_OBSERVATION_EVENT_SCHEMA.md` | Schéma canonique V1 — `ObservationEvent` + `ObservationSummary` | DONE |
| `30_PRODUCER_CONSUMER_MAPPING.md` | OpenClaw → journal → LocalCMS → dashboard | DONE |
| `40_LOCALCMS_AND_DASHBOARD_READINESS.md` | LocalCMS actuel vs cible — gaps identifiés | DONE |
| `90_CLOSEOUT.md` | Ce document | DRAFT |

---

## Schéma canonique V1 — résumé

### `ObservationEvent` (par run)

Champs clés : `run_id` (PK), `session_id`, `run_date`, `started_at`, `status` (PASS/FAIL),
`dry_run`, `paper_mode`, `outcome`, `pnl_net`, `localcms_ok`, `closeout_required`, `ingested_at`.

### `ObservationSummary` (agrégé)

Champs clés : `total_runs`, `pass_count`, `fail_count`, `pnl_cumulative`, `win_rate`,
`days_elapsed`, `runs_to_threshold`, `days_to_threshold`, `eligible`.

---

## Décision sur le prochain child GO

| Option | Verdict |
| --- | --- |
| A — WAIT_MORE_OBSERVATION | Recevable si aucune urgence |
| **B — LOCALCMS_OBSERVATION_VIEW** | **Recommandé — consumer le plus immédiat** |
| C — RUNTIME_READINESS | Attendre seuil Phase 1 |
| D — EXTERNAL_JOURNAL_SYNC | Seulement si besoin prouvé |

```text
DECISION_RECOMMANDEE : B — LOCALCMS_OBSERVATION_VIEW
```

Le schéma canonique V1 étant posé, le prochain child naturel est d'exposer
`ObservationSummary` complet dans LocalCMS (seuils, éligibilité, alertes).

Child GO suivant recommandé :
```text
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
```

---

## Invariants post-closeout

- Le schéma V1 est un contrat documentaire — pas encore implémenté en BDD
- L'observation Phase 1 continue sans dépendance à ce schéma
- Aucune implémentation runtime dans ce child GO
- `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` reste l'ancre principale

---

## Verdict

```text
À compléter par l'opérateur :
[ ] PASS — schéma documenté, child GO peut être fermé
[ ] HOLD — attendre validation avant fermeture
[ ] AMEND — des corrections sont requises avant fermeture
```

## RISKS

- À qualifier.
