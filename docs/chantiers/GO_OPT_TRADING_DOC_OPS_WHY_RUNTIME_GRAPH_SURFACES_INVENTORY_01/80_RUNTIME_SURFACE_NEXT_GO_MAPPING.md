# 80_RUNTIME_SURFACE_NEXT_GO_MAPPING

## 1_MASTER_TARGET

Verrouiller le point de reprise et mapper chaque famille de surface vers le prochain GO pertinent apres l'inventaire post-OpenClaw.

## WHY

L'inventaire n'est utile que s'il ferme explicitement le debat sur l'ordre immediat et evite un retour premature vers `export JSON graph reel`.

## 7_CANONICAL_STATE

Mapping des suites retenues :

| Surface family | GO suivant pertinent | Raison |
| --- | --- | --- |
| TMUX runtime | `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` | surface centrale de la spine runtime a relier au consumer |
| LocalCMS | `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01` | consumer read-only a aligner avec les vues runtime |
| Daily journals | `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01` | mapping des runs, snapshots et chronologies apres integration centrale |
| OpenClaw runtime | `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` plus tard | contexte d'overlay utile une fois les sources centrales stabilisees |
| Validators | aucun GO dedicace immediat | enabler transversal, pas chantier prioritaire |
| WHY lint | `GO_OPT_TRADING_DOC_OPS_WHY_GRAPH_WARNINGS_OVERLAY_01` plus tard | overlay differe apres inventory, integration et mapping |
| Security aggregators | `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01` plus tard | warning overlay a brancher sur un modele source deja etabli |
| Observability artefacts | depend du GO de leur surface source | une preuve ne precede pas la source qu'elle decrit |

## 8_DECISION

Decision de reprise verrouillee :

1. `GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01`
2. `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01`
3. `GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01`

Puis seulement :

4. `GO_OPT_TRADING_DOC_OPS_WHY_GRAPH_WARNINGS_OVERLAY_01`
5. governance dashboard prototype
6. traversal runtime reel

## 12_INVARIANTS

- Ne pas rouvrir un GO `export JSON graph reel` avant l'integration LocalCMS/TMUX.
- Ne pas prioriser l'overlay WHY lint avant les surfaces runtime centrales.
- Ne pas introduire de connecteur live, runtime, CI ou index global depuis ce chantier.

## 17_RESUME_POINT

```text
LOCKED_NEXT_GO:
GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01

FOLLOWED_BY:
GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01
GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
```

## 18_VERDICT

```text
PASS / DOC_ONLY_SURFACES_INVENTORY_SEQUENCE_LOCKED
```

## RISKS

- À qualifier.
