---
doc_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01_LOCALCMS
doc_type: ui_gap_plan
repo: opt-trading
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_SYSTEM_MASTER_PLAN_01
status: open
updated_at: 2026-05-16
---

# 08_LOCALCMS_CENTRAL_UI_GAP_PLAN

## Objet

Définir LocalCMS comme UI centrale de gouvernance/lecture du système.
Distinguer LocalCMS (système/gouvernance) de Desk Pro (trading opérationnel).
Lister les gaps actuels et les vues à produire.

---

## SÉPARATION FONDAMENTALE

```text
DESK PRO  = UI trading active
  → Positions, P&L, snapshots, bot_vision, pipeline décision en cours
  → Machine: admin-trading
  → Audience: opérateur trading (actions directes)

LOCAL CMS = UI centrale système / gouvernance / état / orchestration
  → État runtime, workers, sessions TMUX, apps, GO roadmap, healthchecks
  → Machine: db-layer (consumer)
  → Audience: opérateur système (lecture / supervision)
```

---

## ÉTAT ACTUEL LOCALCMS

```text
STATUT: REALIGNMENT DONE (2026-05-14)
LIEN: GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 OUVERT
CAPACITÉ ACTUELLE:
  → structure consumer présente
  → lecture données opt-trading (db-layer)
  → cockpit système absent
CAPACITÉ MANQUANTE:
  → aucune vue sur runtime OpenClaw
  → aucune vue sur TMUX
  → aucune vue sur workers stricts
  → aucune vue sur apps externes
  → aucune vue sur performance / datasheet
  → aucune vue sur GO roadmap
  → aucune vue sur healthchecks
```

---

## VUES À PRODUIRE — CATALOGUE

### VUE 1 — État Runtime OpenClaw

```text
NOM: openclaw-runtime-status
SOURCE: gateway_openclaw /health (ws://127.0.0.1:18789)
        openclaw_operator_bridge /health (à créer)
AFFICHAGE:
  → gateway: LIVE / DOWN + timestamp dernière réponse
  → bridge: IMPL / MISSING + version
  → builder: disponible / occupé
  → dernier appel builder (timestamp + durée)
REFRESH: toutes les 30s
PRÉREQ: operator_bridge implémenté (GO-01)
```

### VUE 2 — TMUX Sessions

```text
NOM: tmux-sessions-map
SOURCE: tmux list-sessions (via reseau_ssh ou health endpoint)
AFFICHAGE:
  → liste sessions (nom, état, nb panes)
  → par session: panes actifs, process owner, timestamp start
  → sessions manquantes (celles définies dans spine mais absentes)
REFRESH: toutes les 60s
PRÉREQ: GO_OPENCLAW_OPT_TRADING_TMUX_RUNTIME_SPINE_01 (sessions canoniques)
```

### VUE 3 — Workers Stricts (état + rôle)

```text
NOM: strict-workers-board
SOURCE: endpoint health de chaque worker (à créer par worker)
AFFICHAGE:
  → tableau: worker | rôle | état | dernière activité
  → pour chaque worker : input attendu, output produit, erreurs récentes
  → pipeline complet : signal → proposition → validation → trade → résultat → learning
REFRESH: toutes les 30s
PRÉREQ: workers existants (GO-03 signal_router minimum)
```

### VUE 4 — Apps Externes (état connexion)

```text
NOM: apps-connectors-status
SOURCES:
  → Telegram: last message sent + bot status
  → Airtable: last write + table counts
  → ClickUp: last task sync
  → Botpress: bot status
  → TradingView: last webhook received (via signal_router)
  → Google Sheets: last write
AFFICHAGE:
  → tableau: app | connecté | dernière activité | erreur
REFRESH: toutes les 5 min
PRÉREQ: notification_dispatcher + signal_router + datasheet_writer
```

### VUE 5 — Datasheet Performance (P&L)

```text
NOM: datasheet-pnl-central
SOURCE: Google Sheets API (read) + Airtable API (read)
AFFICHAGE:
  → P&L du jour (total)
  → trades du jour (count, gagnants, perdants)
  → P&L hebdo / mensuel
  → derniers 10 trades (résumé)
REFRESH: toutes les 5 min
PRÉREQ: datasheet_writer opérationnel (GO-09)
```

### VUE 6 — KG Repo (Knowledge Graph)

```text
NOM: kg-repo-explorer
SOURCE: memory_bricks (learning store) + graph repo
AFFICHAGE:
  → nœuds principaux du KG
  → liens entre modules/surfaces
  → dernières entrées learning_feeder
REFRESH: à la demande (coûteux)
PRÉREQ: learning_feeder opérationnel (GO-10)
NOTE: vue différée — dépend du pipeline complet
```

### VUE 7 — GO Roadmap Cockpit

```text
NOM: go-roadmap-cockpit
SOURCE: docs/chantiers/ (scan statique) + ClickUp API (tâches)
AFFICHAGE:
  → GO ouverts / fermés par domaine
  → séquence bloquante (Gantt simplifié)
  → prochains GO à ouvrir
  → progression phase 1/2/3/4/5/6
REFRESH: toutes les heures
PRÉREQ: task_tracker opérationnel (ou lecture doc statique)
```

### VUE 8 — Healthchecks Centralisés

```text
NOM: health-aggregator
SOURCE: health endpoint de chaque surface opérationnelle
AFFICHAGE:
  → matrice: surface | machine | statut | latence | dernière vérif
  → alerte si surface DOWN > seuil configurable
  → résumé global: N surfaces OK / M KO
REFRESH: toutes les 30s
NOTIFICATION: → Telegram si surface critique DOWN
PRÉREQ: health module + notification_dispatcher
```

---

## ARCHITECTURE LOCALCMS CONSUMER

```text
PATTERN: LocalCMS est un consumer READ-ONLY.
Il ne modifie jamais les données de production.
Il lit via APIs / health endpoints / fichiers partagés.

FLUX:
  sources (gateway, workers, apps) → APIs / endpoints
  → LocalCMS consumer (db-layer) → vues HTML/JSON
  → opérateur (lecture navigateur)

PRINCIPE:
  Desk Pro → ÉCRITURE TRADE (admin-trading)
  LocalCMS → LECTURE ÉTAT SYSTÈME (db-layer)
  Jamais d'inversion.
```

---

## ORDRE DE PRODUCTION DES VUES

```text
PHASE A — Dès GO-02 TMUX spine:
  VUE 2 — TMUX Sessions (lecture sessions actives)
  VUE 8 — Healthchecks Centralisés (surfaces connues)

PHASE B — Dès GO-01 operator_bridge:
  VUE 1 — État Runtime OpenClaw

PHASE C — Dès GO-03 signal_router:
  VUE 3 — Workers Stricts (signal_router en premier)
  VUE 4 — Apps Externes (TradingView connecté)

PHASE D — Dès GO-04 notification_dispatcher + GO-09 datasheet:
  VUE 4 — Apps Externes (Telegram + Sheets + Airtable)
  VUE 5 — Datasheet Performance

PHASE E — Pipeline complet:
  VUE 6 — KG Repo
  VUE 7 — GO Roadmap Cockpit
```

---

## GO REQUIS

```text
GO_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_UI_CENTRAL_GAP_BRIDGE_01
  SCOPE: produire les vues A + B (TMUX + OpenClaw runtime)
  PRÉREQ: GO-01 (bridge) + GO-02 (TMUX spine)
  LIVRABLE: LocalCMS avec vues 1 + 2 + 8 opérationnelles
  MACHINE: db-layer

SUBSEQUENT: produire vues 3-7 au fil des GO pipeline (workers + datasheet + learning)
```

---

## DISTINCTION FINALE

| Aspect | LocalCMS | Desk Pro |
| --- | --- | --- |
| Rôle | Gouvernance / lecture système | Trading opérationnel |
| Machine | db-layer | admin-trading |
| Audience | Opérateur système | Opérateur trading |
| Écriture | JAMAIS (read-only) | Oui (trade actions) |
| Données | État, healthchecks, roadmap, KG | Positions, P&L, snapshots |
| Refresh | Polling / batch | Temps réel |
| Relation | Complémentaire | Complémentaire |
