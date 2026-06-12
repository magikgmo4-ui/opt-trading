# 30_NEXT_SURFACE_CANDIDATES

## 1_MASTER_TARGET

Comparer les prochaines surfaces candidates apres review du premier rendu local borne.

## WHY

La suite doit rester sequentielle. Chaque candidate doit etre acceptee seulement si elle repond a un gap documente sans ouvrir un risque disproportionne.

## 7_CANONICAL_STATE

Candidates demandees :

| Candidate | Statut | Raison |
| --- | --- | --- |
| render readability refinement | RECOMMENDED_NEXT | repond directement aux gaps de labels, legende, orientation et provenance visible |
| JSON enrichment | DEFERRED | utile plus tard, mais premature tant que les limites sont surtout presentationnelles |
| LocalCMS graph view integration | DEFERRED | necessite un render plus stable avant integration de vue |
| graph traversal / navigation | BLOCKED_FOR_NOW | aucun besoin de traversal tant que le graph contient 3 nodes et 3 edges |
| dashboard prototype | BLOCKED | les gates dashboard/runtime restent non satisfaits |

## 8_CANDIDATE_DETAILS

### render readability refinement

Objectif possible :

```text
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_RENDER_READABILITY_REFINEMENT_01
```

Scope recommande :

- produire une version Markdown v1 du rendu ;
- garder la meme source JSON ;
- ajouter labels courts, legende, table edge/provenance et orientation explicite ;
- ne pas modifier le JSON ;
- ne pas creer de dashboard.

### JSON enrichment

Scope futur possible :

- ajouter des champs de rendu seulement si le refinement prouve qu'ils manquent vraiment ;
- garder `runtime_state_live`, overlays et traversal hors JSON tant que non decides.

### LocalCMS graph view integration

Scope futur possible :

- integration uniquement apres stabilisation du render statique ;
- commencer par contrat de vue read-only, pas par implementation live.

### graph traversal / navigation

Scope futur possible :

- traversal uniquement quand le graph depasse le stade 3 nodes / 3 edges ;
- garder la navigation humaine et non decisionnelle.

### dashboard prototype

Scope futur possible :

- seulement apres render stable, JSON enrichi si necessaire, gates explicites, et decision separee ;
- aucune boucle live, mutation runtime ou CI automatique.

## 12_INVARIANTS

- Une candidate bloquee ne devient pas active sans GO dedie.
- Une candidate deferred ne doit pas etre melangee au refinement.
- Le dashboard reste hors sequence immediate.

## 17_RESUME_POINT

La prochaine surface canonique recommandee est un refinement de lisibilite du rendu, pas un enrichissement data ou une integration runtime.

## RISKS

- À qualifier.
