---
doc_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: stock_space_ai_crosswalk
go_id: GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01
machine: student
status: active
lifecycle_stage: opening
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-14
links:
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01/10_branch_crosswalk.md
  - docs/chantiers/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01/20_resume_point.md
---

# GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01

## 1_MASTER_TARGET

Faire du recroisement des deux branches stocks le prochain chantier documentaire execute sur `student`.

Branches sources :
- `go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01`
- `go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01`

## 3_INITIAL_NEED

L'utilisateur a corrige le cadrage : `student` n'est pas reouvert pour un runtime Student/Ollama.

`student` devient la machine documentaire qui doit :
- comparer les deux branches ;
- extraire leur structure canonique ;
- decider ce qui reste dans `watchlist` ;
- decider ce qui reste dans `market-structure` ;
- integrer `LUNR` proprement ;
- preparer le prochain patch / PR minimal.

## 4_MASTER_PROJECT_PLAN

1. Relire le parent `watchlist` comme couche dataset / scoring / suivi ticker-first.
2. Relire le parent `market-structure` comme couche these sectorielle top-down centree sur `SpaceX`.
3. Isoler les actifs partages et les actifs specifiques.
4. Stabiliser la frontiere canonique entre `dataset public` et `these sectorielle`.
5. Integrer `LUNR` dans la these `market-structure` sans casser le role dataset de `watchlist`.
6. Statuer sur `FLY` : these sectorielle oui, watchlist seulement si une integration ticker cotee devient explicite.
7. Produire une matrice de recroisement et un plan de patch minimal par branche source.

## 6_FINAL_TARGET

Livrer un paquet documentaire de consolidation qui permet de decider proprement :
- ce qui reste `AI_SPACE_WATCHLIST` ;
- ce qui reste `STOCK_SPACE_AI_MARKET_STRUCTURE` ;
- comment traiter `RKLB`, `ASTS`, `PL`, `LUNR`, `FLY`, `AMD` et `NVDA` ;
- dans quel ordre ouvrir les prochains patchs / PR.

## 7_CANONICAL_STATE

- `student` est un operateur documentaire sur ce chantier.
- Aucun runtime Student/Ollama n'est reouvert.
- Le chantier reste doc-only.
- Le but n'est pas de fusionner les deux branches, mais de preparer leur harmonisation.

## 12_INVARIANTS

- Chantier documentaire uniquement.
- Aucun runtime `student` / `ollama`.
- Aucun broker.
- Aucun signal achat / vente.
- Aucun merge direct des deux branches sans revue.
- Ne pas toucher aux index globaux sans instruction explicite.

## RISKS

- À qualifier.
