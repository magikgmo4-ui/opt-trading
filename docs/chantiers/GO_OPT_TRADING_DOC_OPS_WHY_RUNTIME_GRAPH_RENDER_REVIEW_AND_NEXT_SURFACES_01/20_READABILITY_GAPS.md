# 20_READABILITY_GAPS

## 1_MASTER_TARGET

Identifier les gaps de lisibilite du rendu Markdown v0 avant toute extension fonctionnelle.

## WHY

Un graph minimal peut etre correct mais difficile a lire. Avant d'ajouter des nodes, du traversal ou une vue LocalCMS, il faut verifier que le rendu actuel explique deja clairement les relations centrales.

## 7_CANONICAL_STATE

Gaps prioritaires :

| Gap | Impact | Priorite |
| --- | --- | --- |
| Labels Mermaid longs | les edges sont exactes mais peu scannables | HIGH |
| Absence de legende visuelle | les types de nodes et de relations ne sont pas expliques dans le rendu | HIGH |
| Provenance non locale au graph | la provenance existe en table, mais pas au niveau node/edge rendu | MEDIUM |
| Pas de separation lecture/runtime/source | LocalCMS, TMUX et Daily Journal sont differents, mais le graph ne code pas assez cette difference | MEDIUM |
| Pas de verdict de prochaine action | l'artefact render ne dit pas quelle evolution est bloquee ou ouverte | MEDIUM |

## 8_READABILITY_REQUIREMENTS

Le prochain raffinement de rendu devrait ajouter :

- labels courts pour les edges ;
- table de correspondance `label court -> relation JSON` ;
- legende des types `read-only surface`, `runtime session surface`, `source mapping` ;
- orientation explicite des fleches ;
- mention claire que le JSON reste source de verite ;
- trace de provenance par node et edge dans une table plus proche du render.

## 9_NON_REQUIREMENTS

Ces gaps ne demandent pas encore :

- une modification du JSON ;
- une vue HTML ;
- un dashboard ;
- une integration LocalCMS ;
- un traversal interactif ;
- un moteur de layout complet.

## 10_REVIEW_NOTES

Le rendu actuel est assez petit pour etre auditable, mais il ne porte pas encore assez de pedagogie pour servir de base a une surface de navigation. L'etape suivante la plus sobre est donc de raffiner le rendu Markdown lui-meme.

## 12_INVARIANTS

- Ne pas enrichir les donnees pour corriger un probleme de presentation.
- Ne pas ouvrir un dashboard pour corriger des labels trop longs.
- Ne pas ajouter une surface nouvelle tant que le rendu minimal n'est pas lisible.

## 17_RESUME_POINT

Le gap dominant est la lisibilite du render, pas la profondeur du JSON.
