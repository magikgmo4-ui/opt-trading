HF FREE PLATFORM — MASTER KANBAN FINAL
======================================

Status legend
- TODO
- IN_PROGRESS
- CLOSE

M-0 Cadrage / guardrails — CLOSE
- repo canonique = opt-trading
- repo canonique réel = magikgmo4-ui/opt-trading
- hf = delivery/runtime/tooling only
- pas de secrets / pas de cœur stateful sur hf free

M-1 Foundation lane — CLOSE
Goal
- bootstrap module and operator skeleton
Close criteria
- module tree exists
- spec/scope/kanban/recovery exist
- cmd/menu/sanity exist
- lane mergée dans `sot/mainline`

M-2 Portal lane — CLOSE
Goal
- add portal_static starter
Close criteria
- starter exists
- readme exists
- portail mergé dans `sot/mainline` via PR #13 / merge commit `87ae991`

M-3 Publish bridge lane — CLOSE
Goal
- add publish bridge scripts
Close criteria
- scripts exist
- dry-run instructions exist
- lane mergée dans `sot/mainline`

M-4 Tools lane — CLOSE
Goal
- add private tools starter
Close criteria
- starter exists
- safe sample tool exists
- lane mergée dans `sot/mainline`

M-5 MCP lane — CLOSE
Goal
- add public mcp starter
Close criteria
- starter exists
- guardrails documented
- lane mergée dans `sot/mainline`

M-6 Dataset lane — CLOSE
Goal
- add public assets starter
Close criteria
- dataset starter exists
- example exists
- lane mergée dans `sot/mainline`

M-7 Epic merge — CLOSE
Goal
- merge accepted lanes into epic branch
Close criteria
- module HF mergé dans `sot/mainline`
- sanity HF = PASS
- foundations / portal / publish_bridge / tools / mcp / dataset déjà présentes et mergées

M-8 HF publication rehearsal — TODO
Goal
- create target hf repos and dry-run publication payloads
Close criteria
- repo names confirmed
- no secrets leakage
- publication checklist ready
- `sync_hf_exports.sh` reste un stub, donc la publication HF ne doit pas être présentée comme fully automated

Next real mission
- `GO_HF_PUBLICATION_REHEARSAL_01`
