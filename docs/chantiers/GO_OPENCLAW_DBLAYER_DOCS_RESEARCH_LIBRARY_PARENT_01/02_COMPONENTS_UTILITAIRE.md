---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01_COMPONENTS
doc_type: component_analysis
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
updated_at: 2026-05-06
---

# 02_COMPONENTS_UTILITAIRE — OpenClaw Modules

Chaque module OpenClaw scanne pour son utilitaire reel (cmd.sh, menu.sh, sanity, README).

| Module | cmd | menu | sanity | README | Role |
| --- | --- | --- | --- | --- | --- |
| configure_openclaw | ✓ | ✓ | ✓ | ✓ | Configuration |
| doctor_openclaw | ✓ | ✓ | ✓ | ✓ | Diagnostic |
| evidence_openclaw | ✓ | ✓ | ✓ | — | Traces |
| gateway_openclaw | ✓ | ✓ | ✓ | ✓ | Gateway tmux |
| install_module_openclaw | ✓ | ✓ | ✓ | ✓ | Installation |
| menu_openclaw | ✓ | ✓ | ✓ | ✓ | Menu interactif |
| model_provider_openclaw | ✓ | ✓ | ✓ | ✓ | Provider LLM |
| openclaw_config_modulaire | ✓ | ✓ | ✓ | ✓ | Config modulaire |
| tradingview_observer_openclaw | — | — | — | — | Observer TV |

## Differentiateurs

| Module | Specifique OpenClaw | Generique |
| --- | --- | --- |
| gateway_openclaw | Pilotage tmux gateway | — |
| doctor_openclaw | Health check gateway | — |
| model_provider_openclaw | Provider policy, alignment | — |
| evidence_openclaw | Traces execution | — |
| menu_openclaw | Menu navigation | Wrapper standard |
| configure_openclaw | Config | Config generique |
| install_module_openclaw | Installation | Installation generique |
| openclaw_config_modulaire | Modules | Config generique |
| tradingview_observer_openclaw | — | Non implemente |

## Recommandation

- 5 modules specifiques OpenClaw (gateway, doctor, model_provider, evidence, tradingview)
- 4 modules wrappers generiques (menu, configure, install, config_modulaire)
- tradingview_observer_openclaw: coquille vide, a evaluer
