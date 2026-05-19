# Start

## Contexte de reprise

- reprise sur la branche existante `go/GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
- base canonique de comparaison : `origin/sot/mainline`
- le parent est repris apres le child `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01`
- le child `6572ae8` a produit un `FAIL` controle, sans installation ni modification runtime

## Relation avec le child FAIL controle

- le child a prouve `student` joignable en SSH
- le child a prouve `Ollama 0.17.0` actif localement sur `127.0.0.1:11434`
- le child a prouve au moins `deepseek-r1:1.5b`
- le child a aussi prouve que `OpenClaw` est absent sur `student`

## Objectif de ce lot

- reprendre proprement le parent `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01`
- appliquer la methode `COMMIT_TRANSFER_INVENTORY`
- canoniser le rattachement `student -> Local Ollama`
- figer la frontiere `OpenClaw lab differe` sans toucher `db-layer`

## Invariants de ce lot

- aucun runtime modifie
- aucune installation
- aucun changement `OpenClaw` principal sur `db-layer`
- aucun changement `admin-trading`
- aucun secret expose
