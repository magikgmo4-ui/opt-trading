# 40_GRAPH_INTEGRATION_READINESS

## 1_MASTER_TARGET

Evaluer si l'integration documentaire `LocalCMS + TMUX` est suffisamment posee pour ouvrir la suite vers le mapping journal et le premier render graph reel local.

## WHY

Ce GO doit fermer proprement la phase d'integration centrale sans rebasculer trop tot vers un export JSON, ni sauter l'etape qui relie les runs et snapshots reels au modele deja pose.

## 7_CANONICAL_STATE

Readiness retenue :

| Axe | Etat | Motif |
| --- | --- | --- |
| role `LocalCMS` | READY | consumer read-only borne et distinct de l'orchestration |
| role `TMUX` | READY | spine runtime/session decrite comme source primaire observable |
| linkage model | READY | edges canoniques `HOSTS_OR_EXPOSES`, `PROVES`, `READS_OR_SUMMARIZES`, `GOVERNS` poses |
| preuves minimales | READY_WITH_HUMAN_GATES | preuves attendues identifiees mais restent sous review humaine |
| render graph reel local | NOT_YET | manque encore le mapping journal des `run_id`, snapshots et chronologies |

## 8_DECISION

Decision retenue :

1. Clore cette ouverture comme integration documentaire centrale `LocalCMS/TMUX`.
2. Ouvrir ensuite `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01`.
3. Ne considerer le premier render graph reel local qu'apres stabilisation du mapping journal.

Lecture de sequence :

```text
GO_OPT_TRADING_DOC_OPS_WHY_LOCALCMS_TMUX_GRAPH_INTEGRATION_01
-> GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01
-> GO_OPT_TRADING_DOC_OPS_WHY_RUNTIME_GRAPH_JSON_EXPORT_REAL_01
```

## 12_INVARIANTS

- Ne pas rouvrir l'inventory precedent sans finding explicite.
- Ne pas ouvrir directement un render graph reel local depuis ce GO.
- Ne pas modifier runtime, validator, CI ou index globaux.

## 17_RESUME_POINT

Le point de reprise verrouille reste `GO_OPT_TRADING_DOC_OPS_WHY_DAILY_JOURNAL_GRAPH_EXPORT_MAPPING_01`, comme derniere etape documentaire avant la premiere projection graph reelle locale.

## 18_VERDICT

```text
WIP / DOC_ONLY_LOCALCMS_TMUX_READINESS_PUBLISHED
```
