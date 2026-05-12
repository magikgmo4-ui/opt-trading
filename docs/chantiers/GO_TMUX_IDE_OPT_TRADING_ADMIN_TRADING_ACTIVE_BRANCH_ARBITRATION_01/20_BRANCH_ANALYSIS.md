---
doc_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01_20_BRANCH_ANALYSIS
doc_type: chantier/analysis
repo: opt-trading
machine: cursor-ai + admin-trading
go_id: GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01
status: active
scope: doc-only
analyzed_at: 2026-05-12
links:
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/10_SOURCE_STATE.md
  - docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_ACTIVE_BRANCH_ARBITRATION_01/30_ARBITRATION_OPTIONS.md
---

# 20_BRANCH_ANALYSIS

## Topologie retenue

```text
origin/sot/mainline @ c28b9bd2
merge-base         @ 6373d455
output branch      @ 1a52bb0
observe branch     @ eadc6f5
```

La branche active `OBSERVE_01` est une surcouche d'un commit sur `OUTPUT_01`.

## Comptage exact des ecarts

Comparaison active vs branche parente :

```text
origin/go/...ARTIFACT_OUTPUT_01...go/...ARTIFACT_OBSERVE_01 = 0 / 1
```

Interpretation :

- `OUTPUT_01` n'a aucun commit absent de `OBSERVE_01`
- `OBSERVE_01` a exactement un commit supplementaire : `eadc6f5`

Comparaison active vs base canonique courante :

```text
origin/sot/mainline...go/...ARTIFACT_OBSERVE_01 = 13 / 2
```

Interpretation :

- `sot/mainline` a avance de `13` commits depuis le merge-base `6373d455`
- la branche active porte `2` commits non merges sur `sot/mainline`

Commits uniques de la branche active :

```text
eadc6f5 docs: record admin-trading desk pro artifact observation
1a52bb0 feat: add admin-trading desk pro dry-run artifact output
```

## Statut PR

Lectures GitHub executees le `2026-05-12` :

```bash
gh pr list --state all --head go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01
gh pr list --state all --head go/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OUTPUT_01
```

Resultat :

- aucune PR pour `...ARTIFACT_OBSERVE_01`
- aucune PR pour `...ARTIFACT_OUTPUT_01`

## Surface fonctionnelle du travail non merge

Le commit `1a52bb0` n'est pas doc-only. Il contient :

- `.gitignore`
- `modules/desk_pro/desk_pro_dry_run.sh`
- `modules/desk_pro/dry_run.py`
- `tests/test_desk_pro_artifact_output.py`
- documentation de closeout associee

Le commit `eadc6f5` ajoute le closeout d'observation :

- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_ARTIFACT_OBSERVE_01/90_CLOSEOUT.md`

Conclusion :

- la branche active contient du travail utile
- ce travail n'est pas merge sur `sot/mainline`
- ce travail n'est pas seulement local : il est preserve sur `origin`

## Risque de conflit apparent

Comparaison des chemins modifies depuis le merge-base :

- `origin/sot/mainline` a surtout avance sur des surfaces `docs/`, `modules/perf/`, `modules/collector_binance_spot/`
- la branche desk-pro modifie `modules/desk_pro/`, `tests/`, `.gitignore` et ses propres docs de chantier

Recouvrement de chemins detecte : aucun.

Conclusion :

- risque de conflit Git apparent faible au niveau des chemins
- merge non tente dans ce GO
- la recommandation "ouvrir PR puis merger avant reprise tmux-ide" est defendable sans action destructive
