---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: data_center
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01
parent_go_id: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
status: open
lifecycle_stage: planning
surface: docs/chantiers
source_kind: canonical
created_at: 2026-06-05
updated_at: 2026-06-05
GO_STRUCTURAL_ROLE: GO_CHILD_ATTACHED_TO_PARENT
PF_ID: PF_DATA_CENTER
MASTER_PROJECT_PLAN_ID: MPP_DATA_CENTER_NORMALIZED_REGISTRY
PARENT_GO_ID: GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01
BUNDLE_TARGET: PRO_DESK_EXISTING_COVERAGE_AUDIT_V1
NEXT_ATTACH_TARGET: null
NEXT_GO: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_DATA_INVENTORY_CANONICAL_01
TRANSPORT_MODE: patch_only
6_FINAL_TARGET: Cartographier l'existant reel producers / consumers / contracts / views / readers / legacy paths avant d'ajouter source_score.v1 ou best_value_resolver.v1.
topic_keys:
  - opt-trading
  - data_center
  - deskpro
  - pro_desk
  - coverage_audit
  - existing_surfaces
links:
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/00_INITIAL_PROJECT_DOC.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/20_EXISTING_SURFACES_TO_REUSE.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/40_ROADMAP_AND_NEXT_GO.md
  - docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/20_TARGET_INPUT_CLASSES.md
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01/00_INITIAL_PROJECT_DOC.md
  - modules/data_center/registry/producers.json
  - modules/data_center/registry/consumers.json
  - modules/desk_pro/service/market_metrics_reader.py
  - modules/desk_pro/service/spot_snapshot_reader.py
  - modules/desk_pro/service/vision_analysis_reader.py
  - modules/desk_pro/service/vision_context_reader.py
  - modules/desk_pro/service/telegram_claim_reader.py
  - modules/desk_pro/service/vision_panel.py
  - modules/desk_pro/service/aggregator.py
  - modules/desk_pro/service/scoring.py
---

# GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01

## Objet

Cartographier l'existant reel Data Center / DeskPro avant toute extension : producers, consumers, contracts, views, readers, legacy paths, puis produire une matrix de gaps preliminaires alignee sur P0-P21.

## 1_MASTER_TARGET

*(herite du parent)* Construire une couche `PF_DATA_CENTER` pro-grade capable de couvrir les donnees utilisees par des desks professionnels reels, sans doubler DeskPro.

Objectif immediat de ce child : auditer l'existant avant d'ajouter `source_score.v1` ou `best_value_resolver.v1`.

## 3_INITIAL_NEED

L'utilisateur a demande :

```text
Auditer l'existant reel producers / consumers / contracts / views / readers / legacy paths avant d'ajouter source_score.v1 ou best_value_resolver.v1.
```

## 4_MASTER_PROJECT_PLAN

1. Lire les registres Data Center (`producers.json`, `consumers.json`).
2. Lire les readers DeskPro et leurs paths (DC view vs legacy).
3. Lire les docs de reference (DeskPro input expansion, view migration).
4. Documenter les producers existants avec leur contract, path et etat.
5. Documenter les consumers existants avec leur contract, path, migration status.
6. Documenter les contracts existants et leur couverture P0-P21.
7. Documenter les views existantes et les paths de lecture effectifs.
8. Produire la gap matrix preliminaire vs inventaire P0-P21 du parent.

## 6_FINAL_TARGET

```text
PRO_DESK_EXISTING_COVERAGE_AUDIT_V1
```

Livrables :

```text
10_EXISTING_DATA_CENTER_SURFACES.md      ← producers + registres + contracts actifs
20_EXISTING_DESKPRO_CONSUMERS.md         ← consumers + paths effectifs + migration status
30_EXISTING_PRODUCERS_AND_CONTRACTS.md   ← mapping producer → contract → path
40_EXISTING_VIEWS_AND_PATHS.md           ← vues DC existantes + paths legacy
50_PRELIMINARY_GAPS.md                   ← gaps vs P0-P21 (parent inventory plan)
```

## 7_CANONICAL_STATE

Etat canonique a respecter (herite du parent) :

```text
data/data_center/<family>/<producer_id>/ = ecriture producteur / audit
data/data_center/views/<contract_class>/ = lecture consommateur
data/data_center/_registry/ = status / registry / health
```

DeskPro reste consumer. Data Center reste ingestion/resolution.

## 8_VALIDATED_PLAN

Roadmap child :

1. Ouvrir `10_EXISTING_DATA_CENTER_SURFACES.md` — inventaire producers, registry, contracts.
2. Ouvrir `20_EXISTING_DESKPRO_CONSUMERS.md` — consumers, paths effectifs, migration.
3. Ouvrir `30_EXISTING_PRODUCERS_AND_CONTRACTS.md` — mapping producer/contract/path.
4. Ouvrir `40_EXISTING_VIEWS_AND_PATHS.md` — vues + paths legacy.
5. Ouvrir `50_PRELIMINARY_GAPS.md` — gap matrix vs P0-P21.

## 9_SELECTED_SOLUTION

Audit doc-only. Pas de runtime modifie. Lecture des registres existants, des readers existants, des paths effectifs. Production d'une matrix de gaps basee sur l'inventaire P0-P21 du parent et les observations reelles.

## 10_SELECTED_SETUP

```text
registres       → modules/data_center/registry/*.json
readers DeskPro → modules/desk_pro/service/*.py
views DC        → data/data_center/views/
legacy paths    → data/deskpro/inputs/
docs ref        → docs/chantiers/GO_DESKPRO_INPUT_EXPANSION_01/
                → docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_DESKPRO_VIEW_MIGRATION_01/
```

## 11_KEY_DECISIONS

- Audit = doc-only, aucun runtime modifie.
- Les readers sont inspectes pour leur path par defaut (DC view vs legacy).
- Un consumer enregistre avec `read_path` vers une view DC est considere migre.
- Un consumer enregistre avec `read_path` vers `data/deskpro/inputs/` est legacy ou en attente de migration.
- Une view absente de `data/data_center/views/<contract_class>/` est un gap d'infrastructure.
- Un producer avec `last_write: null` est un producer jamais execute.
- La gap matrix reference les categories P0-P21 du parent (docs/chantiers/GO_OPT_TRADING_DATA_CENTER_PARENT_PRO_DESK_DATA_COVERAGE_01/10_PRO_DESK_DATA_INVENTORY_PLAN.md).

## 12_INVARIANTS

Herites du parent :

- Ne pas doubler DeskPro.
- Ne pas ingerer dans DeskPro.
- Ne pas faire lire DeskPro dans les producers raw.
- Ne pas creer de reader fantome.
- Ne pas fusionner les categories P0-P21.
- Ne pas traiter deux sources comme equivalentes sans score.
- Ne pas publier une best value sans `resolver_decision`.
- Ne pas modifier runtime dans ce parent.
- Ne pas modifier les index globaux sans consigne explicite.

Specifiques a ce child :

- Aucun appel API, DB, Telegram.
- Aucune modification de code.
- Les audits ne creent pas de nouveaux fichiers en dehors de `docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01/`.
- Les observations sont factuelles (basées sur les fichiers lus, pas sur des suppositions).

## 15_REMAINING_GAP

- `pair_market_snapshot` view directory non creee (consumer registered, view missing).
- Vision context readers non migres vers DC views (3 readers legacy).
- `vision_analysis_reader.py` lit un path legacy, pas une DC view.
- `telegram_claim_reader.py` lit un path legacy.
- Tous les producers ont `last_write: null`.
- P0-P21 : couverture partielle (P1, P4, P9, P10, P11, P14, P17 uniquement).
- Aucun source_score.v1, source_evidence.v1, canonical_value.v1, resolver_decision.v1.
- Pas de schema de scoring source.

## 16_TODO

Produire les 5 livrables du child dans l'ordre.

## 17_RESUME_POINT

Reprendre ici : child ouvert, branche `go/GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_EXISTING_COVERAGE_AUDIT_01`. Prochaine action = produire `10_EXISTING_DATA_CENTER_SURFACES.md`.
