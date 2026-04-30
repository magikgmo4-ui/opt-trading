---
doc_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01_MACHINE_MAP
doc_type: machine_map
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_DOC_OPS_CHILD_POST_MATRIX_REMAINING_PARENT_ARBITRATION_01
status: open
lifecycle_stage: arbitration
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-04-29
links:
  - docs/index/GO_INDEX.md
  - docs/index/GO_PARENT_THREAD_MAP.md
  - docs/index/ACTIVE_STREAMS.md
---

# 20_MACHINE_WORKSTREAM_MAP

## Regle retenue

Maintenir idealement `1` chantier principal ouvert par machine.
Les surfaces projet, runtime et methode restent secondaires et ne doivent pas absorber le principal machine.

## Carte machine -> chantier principal recommande

| Machine | Role retenu | Chantier principal recommande | Chantiers secondaires ou differes | Arbitrage |
| --- | --- | --- | --- | --- |
| `db-layer` | machine runtime/app actuelle ; hote reel courant | `GO_OPT_TRADING_MACHINE_DB_LAYER_PARENT_01` | `GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01`, `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`, `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | priorite post-arbitrage |
| `admin-trading` | machine trading reelle ; webhook / desk / bots / runtime trading | `GO_OPT_TRADING_MACHINE_ADMIN_TRADING_PARENT_01` | `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`, futur review runtime admin-trading | differe jusqu'a clarification `db-layer` + OpenClaw runtime + SSH |
| `cursor-ai` | orchestration multi-agents / IDE / Git / Claude / ChatGPT | `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01`, `GO_GIT_PROGRESSIVE_MIGRATION_START_13`, `GO_OPT_TRADING_BUNDLES_REPO_STORAGE_PARENT_01` | principal prioritaire pour le poste multi-agents |
| `fantome` | cible AI Team / strict workers | `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` | `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` | `strict workers` ne doit pas rester isole |
| `student` | machine lab / differee | `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` | bundle `GO_OPT_TRADING_LOCAL_OLLAMA_CHILD_STUDENT_OPENCLAW_LAB_QUALIFICATION_01` via le parent bundles | ne pas ouvrir avant `db-layer`, SSH, OpenClaw runtime et `cursor-ai` |
| `reseau_ssh` | transverse multi-machine | `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03` | `GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01` | validation physique avant tests multi-machine finaux |

## Notes de rattachement

### db-layer

- `db-layer` reste le principal machine prioritaire.
- `LocalCMS` y est consomme comme surface projet, pas comme principal machine.
- `OpenClaw` y est installe comme runtime reel courant, mais son parent reste `GO_TMUX_OPENCODE_OPENCLAW_RUNTIME_01`.

### admin-trading

- `admin-trading` n'est pas abandonne.
- Son ouverture maintenant melangerait SSH, runtime OpenClaw, services trading et surfaces operateur.
- La bonne reprise vient apres clarification `db-layer` / OpenClaw runtime / `reseau_ssh`.

### cursor-ai

- Le principal reste `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01`.
- `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` reste une surface de methode utile, mais pas le principal machine.

### fantome

- Le principal reste `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01`.
- `GO_OPT_TRADING_STRICT_WORKERS_PARENT_01` a une preuve de closeout draft only sur sa branche dediee ; il doit etre consolide sous ce principal plutot que rouvert seul.

### student

- `GO_OPT_TRADING_LOCAL_OLLAMA_PARENT_01` est le meilleur candidat prouve pour `student`.
- Le sujet reste lab-only, non production, et differe.

### reseau_ssh

- `reseau_ssh` n'est pas une machine supplementaire.
- C'est la gate transverse qui doit rester claire avant de relancer `admin-trading` ou `student`.
