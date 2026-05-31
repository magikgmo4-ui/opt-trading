---
doc_id: OPENCLAW_MODULES_INDEX
doc_type: modules_index
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
updated_at: 2026-05-30
---

# docs/openclaw/modules — Index des modules runtime

9 modules sous `modules/` dont le nom contient "openclaw".

## Table

| Module | Path | Rôle | Fiche |
| --- | --- | --- | --- |
| configure_openclaw | `modules/configure_openclaw/` | Configuration runtime OpenClaw | [configure_openclaw.md](configure_openclaw.md) |
| doctor_openclaw | `modules/doctor_openclaw/` | Diagnostic et health check | [doctor_openclaw.md](doctor_openclaw.md) |
| evidence_openclaw | `modules/evidence_openclaw/` | Preuves et traces d'exécution | [evidence_openclaw.md](evidence_openclaw.md) |
| gateway_openclaw | `modules/gateway_openclaw/` | Pilotage tmux gateway | [gateway_openclaw.md](gateway_openclaw.md) |
| install_module_openclaw | `modules/install_module_openclaw/` | Installation de modules | [install_module_openclaw.md](install_module_openclaw.md) |
| menu_openclaw | `modules/menu_openclaw/` | Menu opérateur interactif | [menu_openclaw.md](menu_openclaw.md) |
| model_provider_openclaw | `modules/model_provider_openclaw/` | Provider LLM, policy, alignment | [model_provider_openclaw.md](model_provider_openclaw.md) |
| openclaw_config_modulaire | `modules/openclaw_config_modulaire/` | Configuration modulaire (`~/.openclaw/config.d/`) | [openclaw_config_modulaire.md](openclaw_config_modulaire.md) |
| tradingview_observer_openclaw | `modules/tradingview_observer_openclaw/` | Observer TradingView | [tradingview_observer_openclaw.md](tradingview_observer_openclaw.md) |

## Convention modules

Chaque module expose :

```
scripts/cmd.sh          — CLI entry point
scripts/menu.sh         — menu interactif
scripts/sanity_check.sh — validation installation
scripts/install_shortcuts.sh — wrappers /usr/local/bin
```

## Statut fiches

| Fiche | Statut |
| --- | --- |
| configure_openclaw.md | produit |
| doctor_openclaw.md | produit |
| evidence_openclaw.md | produit |
| gateway_openclaw.md | produit |
| install_module_openclaw.md | produit |
| menu_openclaw.md | produit |
| model_provider_openclaw.md | produit |
| openclaw_config_modulaire.md | produit |
| tradingview_observer_openclaw.md | produit |
