# 50_RUNTIME_SURFACE_OBSERVABILITY

## 1_MASTER_TARGET

Definir les preuves d'observabilite minimales a retenir pour chaque famille de surface runtime inventoriee.

## WHY

Le futur WHY/runtime graph devra distinguer une surface reelle, une preuve de son etat et un overlay de warning sans transformer un artefact d'observation en source runtime active.

## 7_CANONICAL_STATE

Cadre d'observabilite retenu :

| Surface family | Preuves prioritaires | Signal attendu | Limite explicite |
| --- | --- | --- | --- |
| TMUX runtime | sessions documentees, snapshots, machine placement, traces de restart | etat de la spine et des sessions runtime | aucune action live ou commande runtime |
| LocalCMS | vues read-only, menus, domaines, captures ou traces de lecture | exposition read-only des surfaces runtime | aucun connecteur live ou pilotage |
| Daily journals | `run_id`, chronologie, snapshots, references croisées | preuve de run et de contexte temporel | aucune inference hors du run documente |
| OpenClaw runtime | workflow warning-only, artifact JSON, review d'artefact | preuve d'overlay runtime/security | aucun mode bloquant ni runtime execute |
| Validators | spec, tests cites, scans, perimetre de lecture | cohérence statique des docs et schemas | aucune autorite runtime |
| WHY lint | scans, zero-finding ou findings bornes, warning model | qualite documentaire et warnings | aucun gate bloquant |
| Security aggregators | rapports agreges, lineage d'artefact, statuts warning-only | synthese de signaux de conformite | aucune escalation automatique |
| Observability artefacts | JSON, logs, reports, snapshots | trace lisible par humain et future projection graph | aucune promotion en surface active |

## 8_OBSERVABILITY_RULES

- Une preuve doit conserver sa provenance explicite.
- Une preuve de lecture ne vaut pas preuve de controle.
- Une absence de preuve fraiche doit rester visible comme limite d'observabilite.
- Les artefacts agreges doivent rester relies a leur surface source.

## 12_INVARIANTS

- Aucune preuve definie ici n'autorise un runtime live.
- Aucune preuve definie ici n'autorise un connecteur actif.
- Aucune preuve definie ici ne remplace la review humaine sur surface critique.

## 17_RESUME_POINT

Le prochain GO LocalCMS/TMUX devra reutiliser ce cadre pour mapper les lectures read-only, les snapshots et les preuves de spine sans melanger observation et orchestration.
