---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: initial_project_doc
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
created_at: 2026-05-17
surface: doc-only
scope: db-layer / observation event schema canonique
---

# 00_INITIAL_PROJECT_DOC
## GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01

---

## 1_MASTER_TARGET

```text
Définir le schéma canonique des événements d'observation OpenClaw dry-run.

Transformer les entrées de data/journal/daily/*.json en un contrat de données
structuré, persistable, lisible par LocalCMS et exploitable pour les décisions produit.
```

---

## 2_CONTEXTE_ETABLI

| Fait | Valeur |
| --- | --- |
| `GO_DB_LAYER_REPRISE_AUDIT_01` | CLOSED / PASS / 2026-05-17 |
| `PR #522` | MERGED / 2026-05-17 |
| Observation Phase 1 | active — 14/30 runs, 2/14 jours |
| Journaux réels | `data/journal/daily/*.json` — 14 entrées prouvées |
| LocalCMS métriques | `localhost:8700/metrics/daily` — exposition partielle |
| Ingestion BDD | non implémentée — doc-only |
| Parent | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |
| Schéma physique antérieur | `docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md` (Desk Pro path) |

---

## 3_INITIAL_NEED

```text
On observe 14 runs. Mais il n'existe pas encore de schéma canonique qui transforme
ces runs en données structurées utilisables par LocalCMS, un dashboard ou une future BDD.
```

Risque sans ce child GO :

```text
atteindre 30 runs sans savoir quoi en faire structurellement.
```

---

## 4_DISTINCTION_SCHEMAS

Ce child GO porte sur le **schéma d'observation OpenClaw** — distinct du schéma Desk Pro.

| Path | Source | Schéma | État |
| --- | --- | --- | --- |
| **Desk Pro ingestion** | `admin-trading → /shared/desk_pro/latest/ → db-layer` | `run_summary.json`, `portfolio_engine.json` | Documenté dans `docs/governance/DB_LAYER_INGESTION_*` |
| **OpenClaw observation** | `OpenClaw → data/journal/daily/*.json → LocalCMS` | Champs `run_id`, `session_id`, `all_ok`, `steps`, etc. | **Ce child GO** |

Ces deux paths sont complémentaires. Ils ne se substituent pas.

---

## 5_SCOPE

Ce child GO est **doc-only**.

| Axe | Objet |
| --- | --- |
| A — Signal inventory | Inventaire réel des champs dans `data/journal/daily/*.json` |
| B — Canonical schema | Schéma canonique événement d'observation |
| C — Producer/Consumer | Qui produit, qui consomme, comment |
| D — LocalCMS readiness | Ce que LocalCMS peut lire maintenant vs ce qu'il faudrait |
| E — Decision | Quel prochain child GO après ce schéma |

---

## 6_CONTRAINTES

- Doc-only
- Aucun runtime
- Aucun SSH réel
- Aucun Google Sheets write
- Aucun trade
- Ne pas modifier `GO_INDEX.md` sauf instruction explicite
- Ne pas modifier `ACTIVE_STREAMS.md` sauf instruction explicite

---

## 7_FICHIERS

| Fichier | Contenu |
| --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Ce document |
| `10_SIGNAL_INVENTORY.md` | Inventaire réel des champs journal prouvés |
| `20_CANONICAL_OBSERVATION_EVENT_SCHEMA.md` | Schéma canonique événement |
| `30_PRODUCER_CONSUMER_MAPPING.md` | Qui produit, qui consomme, comment |
| `40_LOCALCMS_AND_DASHBOARD_READINESS.md` | LocalCMS actuel vs cible |
| `90_CLOSEOUT.md` | Closeout draft |
