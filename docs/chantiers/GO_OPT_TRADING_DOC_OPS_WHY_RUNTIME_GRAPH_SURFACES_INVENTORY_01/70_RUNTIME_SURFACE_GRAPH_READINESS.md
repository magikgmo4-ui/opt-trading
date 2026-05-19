# 70_RUNTIME_SURFACE_GRAPH_READINESS

## 1_MASTER_TARGET

Evaluer le niveau de preparation graph de chaque famille de surface runtime avant l'ouverture des GOs d'integration et de mapping.

## WHY

Le nouvel ordre post-OpenClaw impose de savoir quelles surfaces sont deja assez stables pour etre mappees dans le graph et lesquelles doivent encore rester au stade d'inventaire borne.

## 7_CANONICAL_STATE

Readiness de travail retenue :

| Surface family | Readiness actuelle | Motif principal | Prochain traitement |
| --- | --- | --- | --- |
| TMUX runtime | READY_FOR_INTEGRATION | spine et surfaces critiques deja structurantes | `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` |
| LocalCMS | READY_FOR_INTEGRATION | consumer read-only deja pertinent pour le graph | `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` |
| Daily journals | READY_FOR_MAPPING | run trace utile mais depend des relations runtime | `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` |
| OpenClaw runtime | READY_FOR_OVERLAY_CONTEXT | warnings et artifacts disponibles comme contexte | integration apres surfaces centrales |
| Validators | SUPPORTING_ENABLER | borne documentaire et statique, pas source graph centrale | support seulement |
| WHY lint | SUPPORTING_ENABLER | zero-finding recent et role d'enabler | overlay differe apres inventory et integration |
| Security aggregators | READY_FOR_OVERLAY_CONTEXT | signaux warning-only machine-readable disponibles | integration apres surfaces centrales |
| Observability artefacts | DEPENDENT_ON_SOURCE_MAPPING | valeur forte mais depend de la surface source mappee | utiliser apres integration source |

## 8_READINESS_RULES

- `READY_FOR_INTEGRATION` ne vaut pas autorisation d'export JSON immediat.
- `SUPPORTING_ENABLER` signifie support du chantier, pas priorite produit numero 1.
- `READY_FOR_OVERLAY_CONTEXT` signifie que le signal existe mais ne doit pas preceder les surfaces centrales.
- `DEPENDENT_ON_SOURCE_MAPPING` impose de mapper la surface source avant l'artefact.

## 12_INVARIANTS

- Aucun statut de readiness n'autorise un runtime live.
- Aucun statut de readiness n'autorise un dashboard live.
- Aucun statut de readiness n'autorise un traversal autonome.

## 17_RESUME_POINT

La readiness publiee ici verrouille l'ordre suivant : integration LocalCMS/TMUX d'abord, mapping daily journal ensuite, export JSON reel seulement apres ces deux etapes.
