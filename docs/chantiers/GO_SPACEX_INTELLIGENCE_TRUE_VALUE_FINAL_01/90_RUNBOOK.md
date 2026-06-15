# 90_RUNBOOK

## Apply

```bash
cd /opt/trading
git checkout sot/mainline
git pull --rebase
git checkout -b go/spacex-intelligence-true-value-final-01
git apply --check patches/GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01.patch
git apply patches/GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01.patch
```

## Validate

```bash
python -m py_compile modules/stock_true_value/models.py modules/stock_true_value/scoring_engine.py modules/stock_true_value/cli.py
python -m pytest tests/stock_true_value -q
python -m modules.stock_true_value.cli --fixture-only
python -m json.tool outputs/stock_true_value/latest/scores.json >/dev/null
```

## Commit

```bash
git status
git add docs/chantiers/GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01
git add docs/index/inbox/GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01.md
git add configs/stock_true_value configs/ipo/spacex_true_value_final.yaml
git add schemas/stock_true_value schemas/ipo/spacex_true_value_final.v1.schema.json
git add modules/stock_true_value fixtures/stock_true_value tests/stock_true_value
git commit -m "feat(spacex): consolidate true value intelligence layer"
```

## Push

```bash
git push -u origin go/spacex-intelligence-true-value-final-01
```
