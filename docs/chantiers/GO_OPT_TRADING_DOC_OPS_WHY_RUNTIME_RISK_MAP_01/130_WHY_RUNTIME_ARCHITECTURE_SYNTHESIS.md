# 130_WHY_RUNTIME_ARCHITECTURE_SYNTHESIS

## Objectif

Synthétiser l'architecture WHY runtime produite par ce chantier.

## Synthese

Le chantier établit une couche de gouvernance runtime reliant:
- criticite R0-R5,
- invariants runtime,
- gates humaines,
- observabilite,
- reprise,
- dependances multi-machine,
- limites d'autonomie IA.

## Architecture retenue

| Couche | Role |
| --- | --- |
| R0-R5 | classifier la criticite |
| Runtime surfaces map | identifier les surfaces |
| Dependencies map | identifier les dependances |
| Failure modes | identifier les ruptures |
| Invariants map | bloquer les derives |
| Gates map | controler l'execution |
| Recovery paths | permettre la reprise |
| Observability requirements | prouver l'etat reel |
| Autonomy limits | limiter les actions IA/runtime |

## Pourquoi cette architecture existe

Le repo contient des surfaces qui peuvent affecter:
- l'observation,
- l'orchestration,
- les signaux trading,
- les chaines multi-machine.

Une IA ou un operateur ne doit pas traiter toutes les surfaces avec le meme niveau de liberte.

## Resultat attendu

Les futurs GO critiques peuvent maintenant reprendre cette base pour:
- choisir une classe R0-R5,
- documenter leurs invariants,
- imposer des gates,
- documenter les failure modes,
- definir les exigences de review humaine.

## Invariant final

Aucune surface R4/R5 ne devrait etre modifiee sans WHY explicite, preuves runtime, reprise et review humaine.
