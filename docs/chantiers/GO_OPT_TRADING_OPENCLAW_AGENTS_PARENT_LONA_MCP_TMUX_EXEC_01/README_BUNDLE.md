# IDE BUNDLE — GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01

## Objet

Bundle autonome pour appliquer dans `opt-trading` le chantier parent :

```text
OpenClaw + MCP + LONA Trading Assistant + tmux + opt-trading
```

## Branche cible

```bash
git checkout go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
```

## Mode d'application

1. Lire `README_BUNDLE.md`
2. Lire `prompts/GO_PROMPT_01_APPLY_DOCS.md`
3. Appliquer uniquement la documentation d'abord
4. Lancer le smoke sandbox seulement après revue
5. Ne jamais brancher secrets ou live trading dans cette passe

## Contenu

```text
docs/chantiers/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01/
├── 00_PARENT_CHECKPOINT.md
├── 01_SESSION_DOCUMENTATION_INTEGRALE.md
├── 02_RESEARCH_NOTES.md
├── 03_EXECUTION_PLAN_REAL.md
├── 04_SECURITY_GUARDS.md
├── 05_TMUX_COCKPIT_PLAN.md
├── 06_BRANCH_STATE.md
├── 07_GAP_INDEXATION.md
├── prompts/
│   ├── GO_PROMPT_01_APPLY_DOCS.md
│   ├── GO_PROMPT_02_SANDBOX_SMOKE.md
│   └── GO_PROMPT_03_CLOSEOUT.md
├── scripts/
│   └── tmux_openclaw_lona_lab.sh
└── schemas/
    └── strategy_candidate.schema.json

modules/openclaw_lona_lab/
├── README.md
├── config/
│   └── mcp.example.json
├── docs/
│   └── EXECUTION_CONTRACT.md
├── schemas/
│   └── lona_backtest_report.schema.json
└── scripts/
    ├── import_lona_report.py
    └── compare_strategy_candidate.py
```

## Invariants

- LONA = strategy lab / backtest, pas executor live.
- OpenClaw = orchestrateur agent, pas détenteur de secrets.
- MCP = bus outil, à confiner.
- tmux = cockpit opérateur.
- opt-trading = autorité finale.
- risk_engine = passage obligatoire.

## Point de reprise

```text
branche: go/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01
chantier: docs/chantiers/GO_OPT_TRADING_OPENCLAW_AGENTS_PARENT_LONA_MCP_TMUX_EXEC_01/
next_go: GO_OPT_TRADING_OPENCLAW_AGENTS_CHILD_SANDBOX_SMOKE_01
```
