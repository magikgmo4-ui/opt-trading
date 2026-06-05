---
go_id: GO_OPT_TRADING_LOCALCMS_DOC_OPS_CROSS_REVIEW_01
doc_type: cross_review
repo: opt-trading
status: PASS
created_at: 2026-05-17
scope: doc-only — no mutations
---

# 00_LOCALCMS_CROSS_REVIEW
## GO_OPT_TRADING_LOCALCMS_DOC_OPS_CROSS_REVIEW_01

---

## 1_MASTER_TARGET

```text
Recenser tous les chantiers localcms dans opt-trading par statut.
Identifier les gaps entre opt-trading (producer canonique) et localcms (consumer).
Résultat : rapport doc-only, aucune mutation.
```

---

## 2_INITIAL_PROJECT_DOC

| Champ | Valeur |
| --- | --- |
| Déclencheur | Session 2026-05-17 — post-livraison LocalCMS observation view |
| Repos concernés | `opt-trading` (Linux `/opt/trading`) + `localcms` (`/home/ghost/localcms`) |
| Contrainte | Cross-review complète — les deux repos sont accessibles sur Linux |
| Surface | doc-ops + lecture code source localcms — aucune mutation |

---

## 3_INITIAL_NEED

```text
Après 5 child GOs mergés dans la même session (PRs #522–#528),
avoir une vue consolidée de l'ensemble de la relation localcms
dans opt-trading : chantiers ouverts, fermés, livrables, gaps.
```

---

## 4_MASTER_PROJECT_PLAN

```text
1. Inventaire dirs chantiers *LOCALCMS* (find /opt/trading/docs/chantiers)
2. Lecture GO_INDEX.md + GO_CLOSED_INDEX.md — statuts officiels
3. Lecture git log --oneline | grep localcms — PRs livrées
4. Lecture LOCALCMS_READONLY.md — état external consumer
5. Lecture cadrage_parent — modèle producer/consumer établi
6. Rédaction rapport — tables statut + gaps + next candidates
```

---

## 7_CANONICAL_STATE

### Architecture canonique validée

```
opt-trading  →  producer canonique (runtime, données, gouvernance)
localcms     →  consumer humain (cockpit, continuité projet, docs)
```

**Distinction critique — deux surfaces distinctes partageant le nom "localcms" :**

| Surface | Localisation | Port | Rôle |
| --- | --- | --- | --- |
| `modules/localcms/app/main.py` | opt-trading Linux `/opt/trading` | 8700 | FastAPI db-layer — expose `/metrics/daily` avec bloc observation |
| `main.py` | `/home/ghost/localcms` | 8000 | FastAPI LocalCMS cockpit — M1 shared_explorer, M2 cms_installer, M3 config_store |

Ces deux surfaces ne communiquent pas entre elles en runtime — elles coexistent sous le même nom de marque mais sont des outils distincts.

**Invariant :** logique métier, runtime, secrets, données de trading — jamais migrés dans `/home/ghost/localcms`.

### État /home/ghost/localcms (vérifié 2026-05-17)

```
Baseline : v1.0.0-m3-baseline (commit 515a357)
Branche active : main @ 9ec0824
```

| Module | ID | Tests | Statut |
| --- | --- | --- | --- |
| M1 — shared_explorer | `shared_router` `/api/shared/*` | 23/23 PASS | OPÉRATIONNEL |
| M2 — cms_installer | `installer_router` `/api/installer/*` | — | OPÉRATIONNEL |
| M3 — config_store | `config_router` `/api/config/*` | 11/11 PASS | OPÉRATIONNEL |
| M4 — data-sources.js | `MOD_DATA_SOURCES_DATA · M-3.3` | 52/52 PASS | SÉLECTIONNÉ (non formalisé) |

**Prochain GO localcms :** `GO_LOCALCMS_FULL_TEST_CAMPAIGN_01` (campagne test complète sur `main`)

### État external consumer (opt-trading LOCALCMS_READONLY.md)

```
DOC_ONLY_IMPLEMENTATION_READY
```

- Cadrage et plan documentés dans opt-trading
- GO consumer parent ouvert (`GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`)
- Aucune intégration live entre `/home/ghost/localcms` et `GET /metrics/daily:8700` à ce jour

---

## 13_ESTABLISHED

### Chantiers livrés avec PR merge (PASS)

| GO ID | PR | Livrable | Verdict |
| --- | --- | --- | --- |
| `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | #440 | realign localcms consumer sur db-layer | PASS |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_CENTRAL_UI_MENU_RUNTIME_VIEW_01` | #470 | menu runtime view (64/64 tests) | PASS |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_PIPELINE_WITH_LOCALCMS_VIEW_01` | #472 | E2E dry-run pipeline + LocalCMS view (86 tests) | PASS |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_LOCALCMS_HISTORY_VIEW_01` | #478 | daily session history view | PASS |
| `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` | #492 | WHY localcms TMUX graph integration | PASS (doc) |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_METRICS_DASHBOARD_01` | #509 | /metrics dashboard (42/42 tests) | PASS |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01` | #525 | spec ObservationSummary V1 | PASS (doc) |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01` | #527 | impl `_build_metrics()` — bloc observation | PASS |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_SMOKE_01` | #528 | smoke validation observation view | PASS |

### Chantiers support / reference (PASS)

| GO ID | Nature | Verdict |
| --- | --- | --- |
| `GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01` (localcms contract alignment) | memory bricks — contrat consumer | PASS |
| `GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01` | alignement contrat producer/consumer | PASS |

### Chantiers ouverts (OPEN)

| GO ID | Nature | État |
| --- | --- | --- |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | parent cadrage producer/consumer | OPEN — cadrage posé, implémentation consumer not started |
| `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` | intégration forms compatible localcms | OPEN — doc-only, hypothèse non prouvée |

### Chantiers référencés sous parent (REFERENCE — non exécutés comme GO)

| GO ID | Rôle | Statut |
| --- | --- | --- |
| `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | inventaire UI source | REFERENCE |
| `GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01` | matrice producer/consumer | REFERENCE |
| `GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01` | contrats d'interface | REFERENCE |
| `GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01` | pilote read-only | REFERENCE |

---

## 14_HYPOTHESIS

| Hypothèse | Vérifiée | Résultat |
| --- | --- | --- |
| `/home/ghost/localcms` consomme `GET /metrics/daily:8700` | OUI | FAUX — aucune intégration live |
| `localcms` reflète le schéma `ObservationSummary V1` | OUI | FAUX — schéma inconnu dans localcms |
| `localcms` et `opt-trading/modules/localcms` sont le même outil | OUI | FAUX — deux surfaces distinctes |
| `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` est actionnable | Partiellement | HYPOTHÈSE — non prouvée |
| Les REFERENCE GOs sous parent ont une implémentation | OUI | NON — cadrage seulement |

---

## 15_REMAINING_GAP

### Gap 1 — Aucune intégration live localcms ↔ opt-trading (CONFIRMÉ)

```text
/home/ghost/localcms n'appelle pas GET /metrics/daily:8700.
Les deux repos partagent le nom "localcms" mais opèrent indépendamment.
La relation est documentaire/gouvernance — pas de flux de données en runtime.
```

### Gap 2 — ObservationSummary V1 non reflétée dans localcms

| Livrable producer | opt-trading | /home/ghost/localcms | Delta |
| --- | --- | --- | --- |
| Bloc `observation` dans `/metrics/daily` | OUI — PR #527 | ABSENT | pas de consumer implémenté |
| `ObservationEvent V1` schema | OUI — PR #524 | ABSENT | pas de référence |
| `ObservationSummary` spec | OUI — PR #525 | ABSENT | pas de référence |
| Module observation view | OUI — `_build_metrics()` | ABSENT | pas d'équivalent M-side |

### Gap 3 — Consumer parent non démarré

```text
GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01 est OPEN.
Cadrage posé. Plan : inventaire UI → matrice → contrats → pilote.
Aucun GO enfant consumer exécuté à ce jour.
```

### Pas un gap : localcms côté localcms repo est cohérent avec lui-même

```text
/home/ghost/localcms est à jour : v1.0.0-m3-baseline PASS, M4 sélectionné.
Ses propres GOs (adopt 8/8, shared_explorer 23/23, config_store 11/11) sont PASS.
Prochain GO localcms-side : GO_LOCALCMS_FULL_TEST_CAMPAIGN_01.
```

---

## 16_TODO

```text
[post-seuil Phase 1 uniquement — aucune action pendant observation]

1. Décider si /home/ghost/localcms doit consommer GET /metrics/daily:8700
   → si oui : ouvrir GO_LOCALCMS_OPT_TRADING_METRICS_CONSUMER_01
   → ajouter un module M4/M5 dans localcms qui lit l'endpoint observation
   → aligner sur ObservationSummary V1 spec (PR #525)

2. Fermer GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01
   → décision : soit intégration via module localcms, soit rester DOC_ONLY
   → conditionné à RUNTIME_READINESS_AFTER_OBSERVATION (option D)

3. GO_LOCALCMS_FULL_TEST_CAMPAIGN_01 (localcms-side)
   → lancer depuis /home/ghost/localcms post-seuil
   → indépendant de Phase 1 opt-trading

4. GO_LOCALCMS_FORMS_INTEGRATION_DOC_01
   → à évaluer uniquement si besoin formulaire prouvé post-seuil
```

---

## 17_RESUME_POINT

```text
Cross-review COMPLÈTE — les deux repos sont accessibles et lus.

opt-trading : à jour (PRs #522–#528 mergées, observation Phase 1 active).
localcms    : v1.0.0-m3-baseline PASS, M4 sélectionné, prochaine campagne test.
Intégration live : inexistante — par design à ce stade (DOC_ONLY_IMPLEMENTATION_READY).

Aucune action immédiate requise pendant Phase 1 observation.
Prochain point de décision : ≥2026-05-30 (30 runs + 14 jours).
```

---

## LOCALCMS_CHANTIERS_LIST — inventaire complet

| GO ID | PR | Statut | Type | Livrable |
| --- | --- | --- | --- | --- |
| `GO_OPT_TRADING_UI_LOCALCMS_DB_LAYER_CONSUMER_REALIGNMENT_01` | #440 | PASS | impl+doc | realign consumer sur db-layer |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_CENTRAL_UI_MENU_RUNTIME_VIEW_01` | #470 | PASS | impl | menu runtime — 64/64 tests |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_E2E_DRY_RUN_PIPELINE_WITH_LOCALCMS_VIEW_01` | #472 | PASS | impl | E2E dry-run — 86 tests |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_DAILY_SESSION_LOCALCMS_HISTORY_VIEW_01` | #478 | PASS | impl | session history view |
| `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` | #492 | PASS | doc | WHY TMUX ↔ localcms |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_LOCALCMS_METRICS_DASHBOARD_01` | #509 | PASS | impl | /metrics dashboard — 42/42 tests |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01` | #525 | PASS | doc | spec ObservationSummary V1 |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01` | #527 | PASS | impl | `_build_metrics()` — bloc observation |
| `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_SMOKE_01` | #528 | PASS | smoke | validation observation view |
| `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01` | — | OPEN | parent | cadrage producer/consumer |
| `GO_LOCALCMS_FORMS_INTEGRATION_DOC_01` | — | OPEN | doc | intégration forms |
| `GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01` | — | REFERENCE | ref | inventaire UI source |
| `GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01` | — | REFERENCE | ref | matrice producer/consumer |
| `GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01` | — | REFERENCE | ref | contrats d'interface |
| `GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01` | — | REFERENCE | ref | pilote read-only |

---

## LOCALCMS_VERSUS_OPT_TRADING — état de synchronisation (vérifié 2026-05-17)

| Dimension | opt-trading `/opt/trading` | localcms `/home/ghost/localcms` | Delta |
| --- | --- | --- | --- |
| `/metrics/daily` base (port 8700) | LIVRÉ — PR #509 | ABSENT — non consommé | gap intentionnel (DOC_ONLY) |
| Bloc `observation` | LIVRÉ — PR #527 | ABSENT | pas de module consumer |
| `ObservationEvent V1` schema | LIVRÉ — PR #524 | ABSENT | aucune référence |
| `ObservationSummary` spec | LIVRÉ — PR #525 | ABSENT | aucune référence |
| M1 shared_explorer | hors-scope producer | LIVRÉ — 23/23 PASS | propre à localcms |
| M2 cms_installer | hors-scope producer | LIVRÉ — PASS | propre à localcms |
| M3 config_store | hors-scope producer | LIVRÉ — 11/11 PASS | propre à localcms |
| M4 data-sources | hors-scope producer | SÉLECTIONNÉ — non formalisé | propre à localcms |
| Kill switch + Telegram | LIVRÉ — PR #513 | ABSENT — non pertinent | producer-only |
| Consumer parent cadrage | ÉTABLI (OPEN GO) | non reflété | implémentation non démarrée |
| Campagne test complète | couvert par tests unitaires PR | GO_LOCALCMS_FULL_TEST_CAMPAIGN_01 candidat | localcms-side seulement |

**Conclusion** : les deux repos sont cohérents avec eux-mêmes. Aucune intégration live n'est implémentée — c'est la situation prévue (`DOC_ONLY_IMPLEMENTATION_READY`). L'intégration consumer est le prochain axe de travail, post-seuil Phase 1.

---

## Invariants respectés

- Aucune mutation repo
- Aucun runtime trading
- Aucun SSH
- Aucun trade
- `GO_INDEX.md` non modifié
- `ACTIVE_STREAMS.md` non modifié

## RISKS

- À qualifier.
