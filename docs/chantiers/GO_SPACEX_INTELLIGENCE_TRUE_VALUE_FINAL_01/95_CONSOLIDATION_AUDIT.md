# 95_CONSOLIDATION_AUDIT

## Sources reviewed

- GO_STOCK_TRUE_VALUE_ENGINE_01 docs patch bundle.
- GO_STOCK_TRUE_VALUE_ENGINE_01 bundles 02 → 08.
- spacex_intelligence_bundle_final.
- SPACEX_FINAL_CANONICAL_01_BUNDLE.
- SPACEX_MASTER_PROJECT_V5_BUNDLE.

A full machine-readable input manifest is included in:

```text
legacy_source_manifests/source_bundles_manifest.json
legacy_source_manifests/source_files_inventory.json
```

## KEEP

### From SpaceX bundles

- monitor-only invariant.
- SPCX Tier 0 priority.
- Starlink / Starship / xAI / NASA / FAA / FCC / DoD catalyst model.
- IPO tracking architecture.
- data flow raw → normalized → scored → Data Center/UI/reports.
- setup catalog: ORB, VWAP reclaim, FVG reclaim, IPO price flush/reclaim.
- Data Center latest view concept.

### From True Value bundles

- fundamental_score.
- valuation_score.
- flow_score.
- surprise_score.
- hype_score.
- risk_score.
- confidence_score.
- score 0-100 convention.
- fixture-only test discipline.
- Data Center contract prep.

## MERGE

- `catalyst_score` and `ecosystem_score` merge with `surprise_score` and `flow_score`.
- SpaceX watchlists merge with CORE_AI / CORE_SEMI / CORE_SPACE.
- SpaceX output contracts merge with Stock True Value output contracts.

## REMOVE / ARCHIVE

- standalone future of `GO_STOCK_TRUE_VALUE_ENGINE_01`.
- repeated bundle-level IDE instructions.
- placeholder Bundle 08 patch.
- duplicate score docs from Bundle 02/03 once absorbed.

## UPGRADE

Bundle 08 CLI is upgraded here from placeholder into a functional fixture-only generator.

## Final decision

The canonical continuation is:

```text
GO_SPACEX_INTELLIGENCE_TRUE_VALUE_FINAL_01
```

not a separate Bundle #9 under Stock True Value.
