---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_EVENT_SCHEMA_01
doc_type: producer_consumer_mapping
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 30_PRODUCER_CONSUMER_MAPPING

---

## Flux complet

```text
OpenClaw pipeline
  → data/journal/daily/*.json       (producteur — un fichier par run)
  → [normalization layer future]    (à implémenter)
  → ObservationEvent persisté       (schéma canonique V1)
  → LocalCMS /metrics               (consumer HTTP actuel)
  → dashboard opérateur             (consumer futur)
  → Google Sheets                   (consumer externe optionnel)
```

---

## Producteurs

### OpenClaw pipeline (producteur primaire)

| Attribut | Valeur |
| --- | --- |
| Surface machine | `db-layer` |
| Output | `data/journal/daily/YYYYMMDD_NNN.json` |
| Fréquence | 1 run/jour (scheduler systemd — timer quotidien) |
| Format | JSON structuré — schéma `data/journal/daily/*.json` |
| Mode Phase 1 | `DRY_RUN=1 PAPER_MODE=1` |
| Déclencheur | `systemd` timer — `openclaw-daily.timer` |

Le producteur écrit un fichier brut par run. Il n'écrit pas directement en BDD.

### LocalCMS métriques (producer secondaire — agrégation)

| Attribut | Valeur |
| --- | --- |
| Surface | `LocalCMS` — `localhost:8700` |
| Output | `/metrics/daily` — agrégation HTTP |
| Fréquence | mis à jour à chaque run (si `localcms_ok = true`) |
| Format | JSON agrégé — vue `ObservationSummary` partielle |
| Limite actuelle | `localcms_ok = false` si LocalCMS indisponible au moment du run |

---

## Couche de normalisation (à implémenter — hors scope Phase 1)

```text
Rôle futur :
  - lire data/journal/daily/*.json
  - mapper vers ObservationEvent (cf. 20_CANONICAL_OBSERVATION_EVENT_SCHEMA.md)
  - persister dans BDD (moteur non figé)
  - exposer ObservationSummary à LocalCMS et dashboard
```

Cette couche n'existe pas encore. Ce child GO la documente, ne l'implémente pas.

---

## Consommateurs actuels

### LocalCMS — consommateur HTTP actuel

| Attribut | Valeur |
| --- | --- |
| Surface | `LocalCMS` — `localhost:8700/metrics/daily` |
| Données lues | `total_runs`, `pass_count`, `fail_count`, `win_count`, `loss_count`, `pnl_cumulative`, `win_rate`, `last_run` |
| Limite | lecture partielle — pas toute la surface `ObservationSummary` |
| Dépendance | `localcms_ok = true` dans le journal du run |
| État actuel | exposition partielle — suffisant pour Phase 1 |

### Opérateur direct — consommateur script

| Attribut | Valeur |
| --- | --- |
| Surface | ligne de commande sur `db-layer` |
| Commandes | `curl localhost:8700/metrics/daily`, `ls data/journal/daily/`, scripts de reprise |
| Usage | reprise rapide, diagnostic, revue de run |

---

## Consommateurs futurs

### Dashboard opérateur (futur — après LocalCMS observation view)

```text
Child GO associé :
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
```

Ce consumer lit l'`ObservationSummary` et l'affiche en vue opérateur structurée.

### Google Sheets (futur — optionnel)

```text
Child GO associé (si besoin prouvé) :
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_EXTERNAL_JOURNAL_SYNC_DECISION_01
```

Usage possible : audit trail externe, archivage, partage.
Ne pas ouvrir par défaut — uniquement si besoin explicite.

---

## Règles de flux

```text
1. Le producteur écrit data/journal/daily/*.json — ne pas le modifier.
2. La normalisation lit sans modifier les fichiers source.
3. LocalCMS est le consumer UI principal — ne pas le court-circuiter.
4. Google Sheets est un rail externe optionnel — contrôlé et manuel en Phase 1.
5. Aucun consumer ne doit dépendre du format interne des journaux bruts
   une fois le schéma canonique en place.
```

---

## Séparation des paths Desk Pro et OpenClaw

| Path | Producteur | Format source | Consumer | Schéma |
| --- | --- | --- | --- | --- |
| **Desk Pro ingestion** | `admin-trading` | `/shared/desk_pro/latest/run_summary.json` | `db-layer` BDD future | `DB_LAYER_INGESTION_SCHEMA_MAPPING_01.md` |
| **OpenClaw observation** | `openclaw pipeline` | `data/journal/daily/*.json` | `LocalCMS` + dashboard futur | `20_CANONICAL_OBSERVATION_EVENT_SCHEMA.md` (ce GO) |

Ces deux paths coexistent. Ils alimentent deux vues complémentaires de `db-layer`.
