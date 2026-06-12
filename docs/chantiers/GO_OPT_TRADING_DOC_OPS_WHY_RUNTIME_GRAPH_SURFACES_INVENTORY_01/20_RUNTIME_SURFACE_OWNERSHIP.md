# 20_RUNTIME_SURFACE_OWNERSHIP

## 1_MASTER_TARGET

Associer chaque famille de surface runtime a un ownership documentaire et a un niveau de review humaine attendu.

## WHY

Le futur graph devra pouvoir exprimer non seulement les relations techniques, mais aussi qui porte la verite, qui revoit les preuves et ou l'escalade humaine reste obligatoire.

## 7_CANONICAL_STATE

Ownership de travail retenu pour l'inventaire :

| Surface family | Ownership principal | Ownership secondaire | Review humaine attendue |
| --- | --- | --- | --- |
| OpenClaw runtime | OpenClaw runtime security docs | maintainers workflow/doc ops | obligatoire avant toute extension de scope |
| TMUX runtime | orchestration runtime docs | machine/runtime operators | obligatoire sur surfaces critiques et restart semantics |
| LocalCMS | LocalCMS runtime docs | doc ops graph consumers | obligatoire avant alignement consumer/graph |
| Daily journals | daily session governance | runtime observers | obligatoire pour valider les preuves de run |
| Validators | maintainers des validators | doc ops quality owners | obligatoire si verdict ou perimetre change |
| WHY lint | doc ops WHY lint owners | maintainers du validator | obligatoire pour toute nouvelle famille warning |
| Security aggregators | runtime security docs | OpenClaw policy maintainers | obligatoire pour toute promotion de severite |
| Observability artefacts | source surface owner | doc ops synthesis owners | obligatoire pour preuve critique ou ambiguite |

## 8_OWNERSHIP_RULES

- Le proprietaire d'une surface n'est pas automatiquement le proprietaire de tous ses artefacts.
- Une preuve runtime sans review humaine explicite reste insuffisante pour elever une criticite.
- Les surfaces `warning-only` gardent une interpretation humaine obligatoire.
- Les ownerships definis ici sont doc-only et preparatoires au futur graph.

## 12_INVARIANTS

- Aucun ownership defini ici ne cree un droit d'action runtime.
- Aucun ownership defini ici ne remplace la governance existante.
- Aucun ownership defini ici ne supprime les gates humains deja etablis.

## 17_RESUME_POINT

Le prochain GO LocalCMS/TMUX devra transformer ces ownerships en relations lisibles par le graph, sans ajouter de connecteur live.

## RISKS

- À qualifier.
