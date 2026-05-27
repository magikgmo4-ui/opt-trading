# Bundle — GO_OPT_TRADING_ORCHESTRATOR_CHILD_TRADE_EXECUTOR_V1_01

## Contents

- `modules/trade_executor/` — module complet (code + 28 tests + convention files)
- `docs/chantiers/.../00_INITIAL_PROJECT_DOC.md` — initial project doc

## Artifacts

| File | Description |
|------|-------------|
| `patches/trade_executor_v1.patch` | Patch canonique (diff sot/mainline) |
| `trade_executor_v1.tar.gz` | Bundle tarball |
| `trade_executor_v1.zip` | Zip transportable |

## Usage

```bash
# Apply patch
git am patches/trade_executor_v1.patch

# Extract bundle
tar xzf trade_executor_v1.tar.gz

# Extract zip
unzip trade_executor_v1.zip -d /tmp/trade_executor
```
