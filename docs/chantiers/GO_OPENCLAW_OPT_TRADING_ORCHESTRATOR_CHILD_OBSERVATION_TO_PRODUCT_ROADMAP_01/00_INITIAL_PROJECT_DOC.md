---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01
doc_type: initial_project_doc
repo: opt-trading
status: open
parent: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01
created_at: 2026-05-17
surface: doc-only
scope: db-layer / observation → product roadmap
---

# 00_INITIAL_PROJECT_DOC
## GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_OBSERVATION_TO_PRODUCT_ROADMAP_01

---

## 1_MASTER_TARGET

```text
Reconnecter db-layer au master product target après consolidation,
pendant l'observation Phase 1 active.

db-layer n'est pas seulement une surface de cleanup.
db-layer est une surface satellite et une couche de soutien produit destinée à devenir :
- couche d'observation structurée
- data plane opérationnel
- journal de runs
- surface de preuve
- source pour LocalCMS / dashboard
- support de décisions runtime futures
- pont entre admin-trading, OpenClaw, Google Sheets, LocalCMS et la gouvernance produit
```

---

## 2_CONTEXTE_ETABLI

| Fait | Valeur |
| --- | --- |
| `GO_DB_LAYER_REPRISE_AUDIT_01` | CLOSED / PASS / 2026-05-17 |
| `BRANCH_STATE.md` | réconcilié post-cleanup |
| Bloc `DB_LAYER` (`MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`) | vue post-cleanup alignée |
| `KEEP_ACTIVE` db-layer | 1 → `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |
| `A_VERIFIER` db-layer | 0 |
| `DROP_MERGED` db-layer | ≈ 45 branches nettoyées |
| Observation Phase 1 | active — 14/30 runs, 2/14 jours (2026-05-17) |
| Branche observation | `go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PHASE1_30_RUN_14_DAY_OBSERVATION_01` |
| Ancre parent | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |

---

## 3_INITIAL_NEED

```text
On a consolidé db-layer. Maintenant il faut savoir ce que cette surface produit
doit devenir, pas seulement quel GO nettoyer ou fermer.
```

Questions à résoudre dans ce child GO :

1. Qu'est-ce que l'observation Phase 1 doit produire comme preuve utile ?
2. Quels signaux doivent alimenter LocalCMS / dashboard ?
3. Quels artefacts doivent devenir historiques persistants ?
4. Quel rôle exact pour Google Sheets : journal externe, sync, archive, ou surface secondaire ?
5. Quel rôle exact pour OpenClaw : orchestrateur quotidien, superviseur, agent executor, ou collecteur ?
6. Quel prochain child GO produit ouvrir après observation ?

---

## 4_LECTURE_PRODUIT_CORRECTE

La matrice maître impose de lire **produit d'abord, parent ensuite, GO local ensuite, support Git ensuite seulement**.

| Niveau | Lecture correcte |
| --- | --- |
| Produit | Desk Pro / Trading Dual Stack / Bot Vision — centres de gravité |
| Famille soutien | `db-layer`, `LocalCMS`, `openclaw / agents / prompt factory`, machines satellites |
| Parent db-layer | `GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01` |
| État actuel | observation + consolidation post-cleanup |
| Git | simple support d'isolement et de preuve |

Interdits :
- lire db-layer comme un chantier de cleanup seulement
- reconstruire la trajectoire produit depuis une branche ou un index opératoire

---

## 5_SCOPE_DE_CE_CHILD_GO

Ce child GO est **doc-only**.

| Axe | Objet |
| --- | --- |
| A — Observation | Définir ce que l'observation doit mesurer et prouver |
| B — Data plane | Cible db-layer comme couche structurée |
| C — LocalCMS view | db-layer comme source pour LocalCMS/dashboard |
| D — External journal | Rôle Google Sheets dans le dispositif |
| E — Runtime readiness | Condition de réouverture runtime après observation |

---

## 6_CONTRAINTES

- Doc-only
- Aucun runtime
- Aucun SSH réel
- Aucun Google Sheets write
- Aucun trade
- Ne pas modifier `GO_INDEX.md` sauf instruction explicite
- Ne pas modifier `ACTIVE_STREAMS.md` sauf décision explicite
- Ne pas créer de cleanup supplémentaire
- Ne pas rouvrir les branches DROP_MERGED

---

## 7_FICHIERS_DE_CE_CHILD_GO

| Fichier | Contenu |
| --- | --- |
| `00_INITIAL_PROJECT_DOC.md` | Ce document — cadrage et contexte |
| `10_MASTER_PRODUCT_TARGET_ALIGNMENT.md` | Alignement db-layer → master product target |
| `20_OBSERVATION_SIGNAL_MAP.md` | Signaux que l'observation doit collecter |
| `30_DB_LAYER_DATA_PLANE_TARGET.md` | Cible data plane db-layer |
| `40_NEXT_CHILD_GO_DECISION.md` | Décision du prochain child GO après observation |
| `90_CLOSEOUT.md` | Closeout de ce child GO |

## RISKS

- À qualifier.
