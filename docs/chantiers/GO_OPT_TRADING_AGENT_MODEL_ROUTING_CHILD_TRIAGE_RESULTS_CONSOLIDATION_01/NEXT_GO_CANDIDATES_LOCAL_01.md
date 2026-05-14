# NEXT_GO_CANDIDATES_LOCAL_01

go_id: GO_OPT_TRADING_AGENT_MODEL_ROUTING_CHILD_TRIAGE_RESULTS_CONSOLIDATION_01
date: 2026-05-14

## Recommandations prochains GO

### 1. PAPER_VALIDATION_GLOBAL_CLOSEOUT — Priorite HAUTE

```text
GO: GO_OPT_TRADING_ADMIN_TRADING_PAPER_VALIDATION_GLOBAL_CLOSEOUT_01
Domaine: trading
Risque: moyen (paper, pas live)
Machine: admin-trading
Justification: closeout en cours, consolidation paper a finaliser
Router vers: 1.5B direct (format structure)
```

### 2. WHY_CONVERGENCE_ARCHITECTURE — Priorite MOYENNE

```text
GO: GO_OPT_TRADING_DOC_OPS_WHY_CONVERGENCE_ARCHITECTURE_01
Domaine: doc-ops
Risque: faible
Machine: fantome ou db-layer
Justification: architecture en cours, 13 documents produits, proche closeout
Router vers: 0.5B agent chain (audit read-only)
```

### 3. OPENCLAW_SANDBOX_SCHEMA — Priorite MOYENNE

```text
GO: GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
Domaine: orchestration
Risque: moyen
Machine: cursor-ai ou fantome
Justification: 11 documents produits, proche closeout child
Router vers: 1.5B direct (format structure)
```

## Regles de routage

```text
- Tous les candidats sont non-trading (paper/doc/orchestration)
- Surface autorisee par adoption gate
- Provider conforme au standard (0.5B agent chain ou 1.5B direct)
- Aucun write sans WRITE_GATED A4
- Aucun secret
```
