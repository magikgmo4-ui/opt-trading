---
doc_id: OPT_TRADING_GUIDE_OPENCLAW_RUNTIME
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/product_targets/OPENCLAW_TARGET_CANON.md
  - docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/
  - docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/
---

# Guide utilisateur - OpenClaw Runtime

## Ce que c'est

OpenClaw Runtime est la couche d'orchestration IA qui expose une gateway, des agents, et une supervision au-dessus des surfaces trading.

## A quoi ca sert

Il sert a orchestrer les appels IA via gateway OpenClaw, configurer les modules, superviser le runtime et preparer le deploiement d'agents.

## Quand l'utiliser

- pour installer et configurer les modules OpenClaw ;
- pour superviser la gateway via TMUX ;
- pour consulter la cartographie documentaire OpenClaw (77 sources) ;
- pour preparer les GOs agents et orchestration.

## Quand ne pas l'utiliser

- comme un runtime complet et fige (les agents ne sont pas deployes) ;
- pour du trading automatique sans validation humaine ;
- comme source canonique (le repo prime).

## Prerequis

- modules OpenClaw installes : gateway, configure, install, doctor, evidence, model_provider, menu ;
- acces au repo et aux closeouts de cartographie ;
- connaissance des 77 sources documentaires (cartographie parent).

## Commandes / acces

- Gateway : `modules/gateway_openclaw/`
- Configuration : `modules/configure_openclaw/`
- Installation : `modules/install_module_openclaw/`
- Diagnostic : `modules/doctor_openclaw/`
- Preuves : `modules/evidence_openclaw/`
- Supervision TMUX : `docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/`
- Cartographie : `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md`

## Procedure simple

1. Installer les modules OpenClaw necessaires.
2. Configurer la gateway et verifier son etat.
3. Superviser le runtime via TMUX.
4. Consulter la cartographie pour identifier le prochain GO OpenClaw utile.
5. Preparer le deploiement d'agents si le GO est ouvert.

## Verification PASS

- les modules OpenClaw sont installes et operationnels ;
- la gateway repond ;
- la supervision TMUX est active ;
- la cartographie documentaire est accessible.

## Limites

- l'orchestration runtime est en construction ;
- les agents ne sont pas deployes ;
- la synthese runtime unifiee est absente ;
- ne pas confondre avec OpenClaw Docs Library (cartographie documentaire, `DOC_ONLY`).

## Depannage

- Si la gateway ne repond pas : utiliser `doctor_openclaw`.
- Si un module manque : utiliser `install_module_openclaw`.
- Si la supervision TMUX est absente : ouvrir le GO de supervision dedie.

## Source canonique

- `docs/product_targets/OPENCLAW_TARGET_CANON.md`
- `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`
- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/`

## NEXT_GO

`GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`
