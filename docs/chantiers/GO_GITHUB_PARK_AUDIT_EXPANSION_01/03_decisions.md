# GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01 — 03_decisions

## Besoin initial

Lever la contradiction sur `Llm-wiki-minimal` concernant le statut “trunk inspecté” avant toute décision stabilisée.

## ETABLI

- `github_repo_inventory_full.md` et `github_repo_inventory_full.json` indiquent `trunk_inspected=False` pour `Llm-wiki-minimal`.
- `github_repo_inventory_from_zips_v2.md` et `github_park_file_role_cartography_01.md` indiquent `Llm-wiki-minimal` couvert via ZIP (34 fichiers) et donc trunk inspecté dans ce run.

## HYPOTHESE

- les artefacts secondaires proviennent de runs distincts (set de ZIP différent), d’où des champs “trunk inspecté” divergents sans que cela implique une contradiction canonique.

## CONTRADICTION

- contradiction apparente : `Llm-wiki-minimal` trunk inspecté = oui/non selon le support.

## Décision opératoire sur \"trunk inspecté\"

- décision : le champ “trunk inspecté” est défini comme un fait **scopé à un run d’inventaire**.
- règle : un support secondaire ne peut être interprété qu’à l’intérieur de son run (inputs ZIP réellement utilisés).
- conséquence : la divergence `full` vs `from_zips` ne constitue pas une contradiction bloquante si le scope est explicité.

## Impact sur `Llm-wiki-minimal`

- `full.(md/json)` : trunk non inspecté dans ce run, donc aucune garantie sur le contenu trunk.
- `from_zips_v2` + `file_role_cartography` : trunk inspecté dans ce run, contenu trunk disponible pour cartographie.
- résultat : contradiction levée par requalification de scope ; `Llm-wiki-minimal` peut rester lane `KEEP_PRECONSOLIDATION` sans décision supplémentaire à ce stade.

## TODO

- si besoin de rejouer/valider le run “from_zips” sur la machine courante : retrouver/fournir le ZIP trunk de `Llm-wiki-minimal` et rerun l’inventaire.
- si besoin de stabiliser un inventaire unique : régénérer un seul support secondaire “full” cohérent (sans le promouvoir en canon), puis archiver l’ancien.

## REPRISE

- continuer `GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01` en gardant la distinction scope/run des supports secondaires.
- point de reprise : [02_journal_technique.md](file:///C:/Users/ghost/opt-trading/docs/chantiers/GO_GITHUB_PARK_AUDIT_EXPANSION_01/02_journal_technique.md)

## Verdict PASS / OPEN / FAIL

PASS
