---
doc_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01_02_MERMAID_REPLAY
doc_type: mermaid_replay
repo: opt-trading
project: opt-trading
module: repo_knowledge_graph
go_id: GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01
parent_go: GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01
status: open
lifecycle_stage: rendering
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/01_PRODUCER_DELTA.md
updated_at: 2026-05-07
links:
  - graph_bundle.json
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/BRANCH_STATE.md
---

# 02_MERMAID_REPLAY - GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01

Les vues ci-dessous rejouent les surfaces V1 impactees par l'alignement du Producer.

## 1_REPO_GLOBAL_MAP_V1

Source : `graph_bundle.json`.

```mermaid
flowchart LR
    repo["opt-trading<br/>repo canonique"]
    gov["GOVERNANCE + INDEX"]
    go["GO"]
    doc["DOC"]
    branch["BRANCH"]
    machine["MACHINE"]
    app["APP"]
    producer["PRODUCER"]
    view["VIEW"]
    reprise["RESUME_POINT + TODO"]
    gap["GAP"]
    valid["validation.valid=true"]

    gov -- DOCUMENTS --> repo
    go -- BELONGS_TO --> repo
    doc -- DOCUMENTS --> go
    branch -- HAS_BRANCH --> repo
    machine -- BELONGS_TO --> repo
    app -- BELONGS_TO --> repo
    producer -- PRODUCES --> view
    go -- RESUMES_AT / HAS_TODO --> reprise
    go -- HAS_GAP --> gap
    producer --> valid
```

## 2_GO_ACTIVE_MAP_V1

Source : `graph_bundle.json` + overlay priorite `GO_INDEX.md` / `REPRISE.md`.

```mermaid
flowchart TB
    bundle["Bundle GO statuses<br/>OPEN / ACTIVE / REFERENCE / CLOSED / PASS"]
    p0["P0<br/>GO_TMUX_IDE_OPT_TRADING_CADRAGE_01"]
    p0next["GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01"]
    p1a["P1<br/>GO_OPT_TRADING_RUNTIME_EXCEPTION_FAMILIES_01"]
    p1b["P1<br/>GO_GIT_PROGRESSIVE_MIGRATION_START_13"]
    p1c["P1<br/>GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03"]
    p2["P2<br/>GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01"]

    bundle --> p0
    bundle --> p1a
    bundle --> p1b
    bundle --> p1c
    bundle --> p2
    p0 -- NEXT_GO --> p0next
```

## 3_MACHINE_MAP_V1

Source : `graph_bundle.json`.

```mermaid
flowchart LR
    producer["Repo KG Producer V1"]
    orch["GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01"]
    daily["GO_OPT_TRADING_APPS_CHILD_DAILY_OPERATOR_LOOP_01"]
    cursorgo["GO_OPT_TRADING_CURSOR_AI_OPERATOR_EXPORT_01"]

    fantome["fantome"]
    dblayer["db-layer"]
    cursor["cursor-ai"]

    producer -- RUNS_ON --> fantome
    daily -- RUNS_ON --> fantome
    orch -- RUNS_ON --> dblayer
    cursorgo -- RUNS_ON --> cursor
```

## 4_APPS_MAP_V1

Source : `graph_bundle.json`.

```mermaid
flowchart LR
    repo["opt-trading"]
    clickup["APP ClickUp"]
    repokg["APP Repo KG"]
    airtable["APP Airtable"]
    botpress["APP Botpress"]
    producer["PRODUCER Repo KG Producer V1"]

    go_clickup["GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"]
    go_repo_parent["GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01"]
    go_repo_impl["GO_OPT_TRADING_REPO_KG_PRODUCER_IMPL_01"]
    go_airtable["GO_OPT_TRADING_AIRTABLE_ORCHESTRATION_PARENT_01"]
    go_botpress["GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01"]

    clickup -- BELONGS_TO --> repo
    repokg -- BELONGS_TO --> repo
    airtable -- BELONGS_TO --> repo
    botpress -- BELONGS_TO --> repo

    clickup -- REFERENCES --> go_clickup
    repokg -- REFERENCES --> go_repo_parent
    repokg -- REFERENCES --> go_repo_impl
    repokg -- DEPENDS_ON --> producer
    airtable -- REFERENCES --> go_airtable
    botpress -- REFERENCES --> go_botpress
```

## 5_BRANCH_MAP_V1

Source : `graph_bundle.json` + overlay de classement `BRANCH_STATE.md`.

```mermaid
flowchart TB
    branch1["go/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01"]
    branch2["go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"]
    branch3["go/GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01"]

    go1["GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01"]
    go2["GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"]
    go3["GO_OPENCLAW_DBLAYER_DOCS_SOURCE_CARTOGRAPHY_CHILD_01"]

    branch1 -- REFERENCES --> go1
    branch2 -- REFERENCES --> go2
    branch3 -- REFERENCES --> go3
```

## 6_RISK_GAP_MAP_V1

Source : `graph_bundle.json`.

```mermaid
flowchart LR
    bundle["graph_bundle.json<br/>validation=true"]
    go1["GO_OPT_TRADING_DOC_OPS_CHILD_OPEN_WORK_CONTROL_01"]
    go2["GO_OPT_TRADING_DOC_OPS_PARENT_LOCAL_CONTINUITY_RULE_MATRIX_PATCH_02"]
    gap1["Gap in 90_closeout.md"]
    gap2["Gap in 03_branch_arbitrage_seed.md"]
    gap3["Gap in 90_CLOSEOUT.md"]

    bundle --> go1
    bundle --> go2
    go1 -- HAS_GAP --> gap1
    go1 -- HAS_GAP --> gap2
    go2 -- HAS_GAP --> gap3
```

## 7_REPRISE_MAP_V1

Source : `graph_bundle.json` + ordre de lecture `REPRISE.md`.

```mermaid
flowchart LR
    reprise["docs/index/REPRISE.md"]
    go_tmux["GO_TMUX_IDE_OPT_TRADING_CADRAGE_01"]
    todo_tmux["GO_TMUX_IDE_OPT_TRADING_IMPL_BASE_01"]
    go_parent["GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01"]
    resume_parent["docs/index/inbox/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01.md"]
    go_openclaw["GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01"]
    next_openclaw["GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_01"]

    reprise --> go_tmux
    go_tmux -- HAS_TODO --> todo_tmux
    go_parent -- RESUMES_AT --> resume_parent
    go_openclaw -- NEXT_GO --> next_openclaw
```

## 8_NOTE

`DOC_CANON_MAP_V1` et `MODULE_SURFACE_MAP` ne regressent pas dans ce lot ; le delta utile portait sur apps, runtime, branches, gaps, reprise et statuts GO.

## 17_RESUME_POINT

```text
docs/chantiers/GO_OPT_TRADING_REPO_KG_CHILD_PRODUCER_VIEW_ALIGNMENT_01/90_CLOSEOUT.md
-> relire ensuite graph_bundle.json si un nouveau lot graphique est ouvert
```

## RISKS

- À qualifier.
