# 60_RUNTIME_SURFACE_HUMAN_REVIEW_GATES

## 1_MASTER_TARGET

Identifier les gates de review humaine qui restent obligatoires avant toute projection graph plus structuree des surfaces runtime inventoriees.

## WHY

Le graphe futur doit rester audit-oriented et read-only. Il a donc besoin de gates humains explicites la ou les preuves sont partielles, les surfaces critiques ou les overlays warning-only.

## 7_CANONICAL_STATE

Gates de review humaine retenus :

| Surface family | Gate humain minimal | Declencheur principal | Sortie attendue |
| --- | --- | --- | --- |
| TMUX runtime | validation de criticite et de placement | spine critique, restart semantics, machine hosting | classification de surface et risques confirms |
| LocalCMS | validation consumer/read-only | ambiguite entre lecture et orchestration | role graph confirme sans connecteur live |
| Daily journals | validation de run de reference | run incomplet, preuve partielle, snapshots ambigus | preuve de run retenue ou exclue |
| OpenClaw runtime | validation warning-only | extension de scope, changement de severite, artifact atypique | interpretation humaine du signal |
| Validators | validation de perimetre | nouveau schema, nouvelle regle, nouvelle tolerance | borne de lecture reconfirme |
| WHY lint | validation de warning family | nouveau finding, nouvelle famille, nouveau bruit | warning retenu, ignore ou reporte |
| Security aggregators | validation d'overlay | severite percue plus haute, conflit de signaux | statut overlay confirme |
| Observability artefacts | validation de preuve unique | artefact seul sans corroboration | confiance documentaire explicitee |

## 8_GATE_RULES

- Une surface `warning-only` garde toujours une interpretation humaine.
- Une surface critique ne peut pas etre promue dans le futur graph sans gate humain explicite.
- Une preuve unique doit etre revue avant d'etre traitee comme reference canonique.
- Un consumer read-only ambigu doit etre tranche avant toute integration graph.

## 12_INVARIANTS

- Aucun gate defini ici n'est automatise par CI.
- Aucun gate defini ici ne modifie runtime, validator ou docs hors scope.
- Aucun gate defini ici ne supprime les limites `warning-only` ou `read-only`.

## 17_RESUME_POINT

Le prochain GO d'integration LocalCMS/TMUX devra exposer ces gates comme prerequis de lisibilite graph, pas comme mecanismes d'automatisation.

## RISKS

- À qualifier.
