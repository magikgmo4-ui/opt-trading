---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01
doc_type: data_plane_target
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 30_DB_LAYER_DATA_PLANE_TARGET

---

## Objectif

Définir la cible db-layer comme couche structurée orientée produit.

```text
input → normalization → persistence → query/view → dashboard/export
```

---

## Lecture actuelle — ce que db-layer est aujourd'hui

| Composant | État actuel | Note |
| --- | --- | --- |
| Pipeline OpenClaw dry-run | actif — Phase 1 observation | `DRY_RUN=1 PAPER_MODE=1` |
| Journal runs | `data/journal/daily/*.json` | fichiers non structurés en BDD |
| Métriques LocalCMS | `localhost:8700/metrics/daily` | exposition HTTP locale |
| Google Sheets sync | contrôlé — dry_run / written / blocked | non automatique |
| DB structurée | non initiée | ingestion future documentée dans governance |
| Dashboard opérateur | LocalCMS partial | lecture métriques OK, historique non |

---

## Cible data plane db-layer

### Couche Input

```text
Sources d'événements attendues :
- Pipeline OpenClaw → journal run (run_id, status, pnl, timestamp)
- Sheets sync → état sync externe
- Kill switch / guards → état sécurité
- Telegram → état notification
```

### Couche Normalization

```text
Schéma canonique événement (à formaliser dans un GO dédié) :
- run_id        : string
- session_id    : string
- run_date      : ISO date
- status        : pass | fail | blocked
- pnl_session   : float
- pnl_cumulative: float
- error_type    : string | null
- sheets_status : dry_run | written | blocked | failed
- telegram_sent : bool
- source        : openclaw | manual | systemd
- metadata      : dict
```

Références governance existantes :
- `docs/governance/DB_LAYER_INGESTION_ENGINE_DECISION_01.md`
- `docs/governance/DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md`
- `docs/governance/DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md`
- `docs/governance/DB_LAYER_SHARED_TO_DB_INGESTION_SPEC_01.md`

### Couche Persistence

```text
Options documentées (voir governance/) :
- SQLite local (option retenue dans décisions governance)
- Fichiers JSON journalisés (état actuel)
- Table events + table sessions + table decisions
```

Aucune implémentation dans ce child GO — doc-only.

### Couche Query / View

```text
Vues attendues par les consommateurs :
- vue runs récents (n derniers runs)
- vue métriques agrégées (pass_count, fail_count, pnl_cumulative, win_rate)
- vue état opérateur (kill_switch, paper_mode, dashboard_ready)
- vue historique sessions (par date, par run_id)
```

### Couche Dashboard / Export

```text
Consommateurs identifiés :
- LocalCMS → lecture HTTP via /metrics ou endpoint dédié
- Google Sheets → sync contrôlé (non automatique)
- Opérateur direct → curl / script de reprise
```

---

## Priorité des couches après observation

| Couche | Priorité | Condition |
| --- | --- | --- |
| Input (journal runs) | actif | déjà en place |
| Normalization (schéma canonique) | P1 | ouvrir GO dédié après seuil |
| Persistence (SQLite ou équivalent) | P1 | ouvrir GO dédié après seuil |
| Query/View | P2 | après persistence |
| Dashboard/Export LocalCMS | P2 | après query |
| External sync Sheets | P3 | seulement si besoin explicite |

---

## Ce que db-layer ne doit pas devenir

```text
- Un entrepôt de données live (aucun trade réel, aucune connexion exchange)
- Un service réseau exposé (localhost uniquement pendant observation)
- Un dépendant de Google Sheets (Sheets est un rail externe de contrôle, pas une source de vérité)
- Un doublon de LocalCMS (LocalCMS est le consumer, db-layer est le producteur)
```

---

## Rôle de chaque surface dans le data plane

| Surface | Rôle | Position dans le flux |
| --- | --- | --- |
| OpenClaw | Orchestrateur — exécute les runs, produit les journaux | Input |
| `data/journal/daily/*.json` | Journal intermédiaire non structuré | Input → Normalization |
| db-layer BDD (future) | Persistence structurée des événements normalisés | Normalization → Persistence |
| LocalCMS `/metrics` | Consumer HTTP — exposition opérateur | Query/View → Dashboard |
| Google Sheets | Rail externe de contrôle et d'audit | Export externe (contrôlé) |
| admin-trading | Producteur de signaux trading — source upstream | Input upstream |
| `/shared` | Point de transit inter-machine | Input intermédiaire |
