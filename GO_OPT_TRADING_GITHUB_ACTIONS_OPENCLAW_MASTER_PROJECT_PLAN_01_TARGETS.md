# TARGETS — GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01

## 1_MASTER_TARGET

`github_actions_openclaw`

## 6_FINAL_TARGET

Ouvrir un master project plan pour :

- inventorier GitHub Actions ;
- créer le registre jobs/actions ;
- dédupliquer avec les jobs non-trading ;
- préparer les conditions de test ;
- reporter l'orchestration OpenClaw à un child GO.

## BUNDLE_TARGET

`opening_bundle_registry_inventory_dedup`

## TRANSPORT_MODE

`bundle_patch_zip`

## Application

Appliquer le patch à la racine du repo sur une branche dédiée :

```bash
git switch sot/mainline
git fetch --prune origin
git pull --ff-only origin sot/mainline
git switch -c go/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01
git apply bundles/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01/GO_OPT_TRADING_GITHUB_ACTIONS_OPENCLAW_MASTER_PROJECT_PLAN_01.patch
git diff --check
python - <<'PY'
import yaml, pathlib
for p in [
    'docs/registries/GITHUB_ACTIONS_WORKFLOWS_INVENTORY_01.yml',
    'docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml',
]:
    yaml.safe_load(pathlib.Path(p).read_text())
print('PASS yaml')
PY
```
