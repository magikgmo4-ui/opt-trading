---
doc_id: OPT_TRADING_GUIDE_REPO_KG
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md
  - docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md
  - graph_bundle.json
  - producer_repo_kg_v1.py
---

# Guide utilisateur - Repo KG

## Ce que c'est

Repo KG est une projection read-only du repo `opt-trading` sous forme de graphe reconstruisible.

## A quoi ca sert

Il sert a naviguer rapidement entre GO, docs, modules, branches, gaps et resume points sans perdre la logique repo-first.

## Quand l'utiliser

- quand un lot touche beaucoup de docs ou de branches ;
- quand il faut voir les dependances entre surfaces ;
- quand il faut retrouver vite un gap ou un point de reprise.

## Quand ne pas l'utiliser

- comme source canonique autonome ;
- comme decision finale sans relire le closeout repo ;
- comme consumer graphique produit fini deja stabilise.

## Prerequis

- acces au repo ;
- acces a `graph_bundle.json` ;
- lecture des closeouts Repo KG pour comprendre la forme du bundle.

## Commandes / acces

- Bundle : `graph_bundle.json`
- Producer : `producer_repo_kg_v1.py`
- Vues de reference : `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md`

## Procedure simple

1. Partir du GO ou de la surface a comprendre.
2. Lire `graph_bundle.json` via les vues de reference ou les replays Mermaid.
3. Verifier les liens utiles : `APP`, `RUNS_ON`, `HAS_GAP`, `RESUMES_AT`, branche -> GO.
4. Revenir au closeout ou a `GO_INDEX.md` pour confirmer le sens operatoire final.

## Verification PASS

- `validation.valid=true` est prouve par le closeout courant ;
- la projection expose les surfaces utiles aux vues V1 ;
- un GO, un gap et un resume point peuvent etre retrouves sans ambiguite ;
- le lecteur revient bien au repo pour la preuve finale.

## Limites

- le bundle reste une projection ;
- pas de consumer graphique externe fini sur cette couche ;
- la lecture produit / usage reel doit encore etre maintenue explicitement.

## Depannage

- Si la projection semble incoherente, relire le closeout Repo KG le plus recent.
- Si une relation manque, verifier d'abord si elle est absente du repo ou seulement de la projection.
- Si la priorite operatoire n'est pas claire, `GO_INDEX.md` et les closeouts passent avant le graphe.

## Source canonique

- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01/10_EXECUTION_SUMMARY.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01/09_graph_views_v1.md`

## NEXT_GO

`GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01`

## RISKS

- À qualifier.
