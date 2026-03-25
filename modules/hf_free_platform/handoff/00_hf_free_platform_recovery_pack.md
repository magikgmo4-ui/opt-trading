# HF Free Platform Recovery Pack

## State
- Canonical repo: `magikgmo4-ui/opt-trading`
- Base: `sot/mainline`
- HF free module state is already merged in `sot/mainline`
- Portal implementation merged via PR #13 / merge commit `87ae991`
- HF sanity status: PASS
- HF publication réelle confirmée pour `portal_static`, `tools_private` et `public_assets`
- `mcp_public` n'est pas encore publié et reste hors clôture actuelle
- helper fix appliqué sur les scripts de publish pour permettre une review manuelle avec `KEEP_WORKDIR=1`
- publication rehearsal exécutée en mode review manuelle
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
- traiter la publication de `mcp_public`, seule cible HF restante en attente
