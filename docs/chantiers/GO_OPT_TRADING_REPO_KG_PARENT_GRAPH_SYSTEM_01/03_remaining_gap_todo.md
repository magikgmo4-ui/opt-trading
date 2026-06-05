# 15_REMAINING_GAP

- Définir schéma exact des nodes (GO, docs, modules, branches, machines, décisions)
- Définir edges standards (depends_on, part_of, documents, runs_on, produces)
- Choisir format final JSON / JSONL / graph DB compatible
- Définir périmètre scan initial (docs uniquement vs repo complet)
- Définir méthode d'extraction Git (branches, commits, liens)
- Définir validation automatique du graph
- Définir stratégie d'évolution incrémentale du graph

# 16_TODO

## GO_01 — Cadrage Producer détaillé
- définir input exact (repo, docs, index)
- définir output JSON normalisé
- définir règles de mapping docs → nodes

## GO_02 — Cadrage Consumer
- définir comment ACE KG consomme le bundle
- définir vues minimales (GO graph, doc graph, module graph)

## GO_03 — Prototype Producer
- créer script lecture seule
- générer premier graph_bundle.json

## GO_04 — Validation
- vérifier cohérence nodes/edges
- vérifier absence de données sensibles

## GO_05 — Visualisation
- produire vues exploitables
- tester navigation multi-angle

## GO_06 — Closeout
- documenter usage
- produire SESSION_REPRISE
- valider PASS

## RISKS

- À qualifier.
