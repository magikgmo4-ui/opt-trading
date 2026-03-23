# HF Free Platform Recovery Pack

## State
- Canonical repo: `magikgmo4-ui/opt-trading`
- Base: `sot/mainline`
- HF free module state is already merged in `sot/mainline`
- Portal implementation merged via PR #13 / merge commit `87ae991`
- HF sanity status: PASS
- Hugging Face repos are publication targets only.

## Lane order
- foundation
- portal
- publish_bridge
- tools
- mcp
- dataset
- epic merge

## Real merged state
- foundation / portal / publish_bridge / tools / mcp / dataset are already present and merged in `sot/mainline`
- recovery pack and kanban must track the merged state, not reopen completed lanes

## Rules
- do not move canonical truth away from `opt-trading`
- no secrets
- no live trading core on HF
- use lane manifests to preserve branch isolation
- do not present HF publication as fully automated while `modules/hf_free_platform/bin/sync_hf_exports.sh` remains a stub

## Immediate next action
- `GO_HF_PUBLICATION_REHEARSAL_01`
