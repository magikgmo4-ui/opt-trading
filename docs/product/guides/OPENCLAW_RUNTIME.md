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

# Guide - OpenClaw Runtime

## 1_MASTER_TARGET

Runtime d'orchestration IA complet avec gateway, agents, supervision et synthese unifiee.

## FINAL_TARGET

Orchestration IA controlee au-dessus des surfaces trading, avec gateway operationnelle, agents deployes et supervision TMUX.

## CURRENT_STATE

`USABLE_LIMITED` -- Modules installables et gateway operationnels. TMUX supervision runtime en cours. Agents non deployes. Synthese unifiee absente. Cartographie documentaire (77 sources) disponible.

## USAGE_ALLOWED_NOW

- Installer et configurer les modules OpenClaw.
- Superviser la gateway via TMUX.
- Consulter la cartographie documentaire (77 sources).
- Preparer le deploiement d'agents.

## USAGE_FORBIDDEN_NOW

- Traiter comme un runtime complet et fige.
- Trading automatique sans validation humaine.

## IMPLEMENTATION_PATH

1. Terminer la supervision TMUX.
2. Deployer les agents.
3. Produire une synthese runtime unifiee.
4. Closeout runtime.

## CONTINUITY_STATE

Actif -- `GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01` en cours.

## MACHINE / SURFACE

`db-layer` (gateway, orchestration).

## REPRISE_POINT

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01/
docs/product_targets/OPENCLAW_TARGET_CANON.md
```

## TODO

1. Terminer TMUX supervision.
2. Deployer agents.
3. Synthese runtime.

## REMAINING_GAP

Orchestration runtime en construction, agents non deployes, synthese unifiee absente.

## NEXT_GO

`GO_OPENCLAW_OPT_TRADING_CHILD_GATEWAY_SUPERVISION_TMUX_RUNTIME_01`

## PROMOTION_CONDITIONS

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- agents deployes,
- synthese runtime unifiee produite,
- closeout runtime pose.

## Ce que c'est

Couche d'orchestration IA (gateway, agents, supervision) au-dessus des surfaces trading.

## A quoi ca sert

Orchestrer les appels IA, configurer les modules, superviser le runtime, preparer le deploiement d'agents.

## Quand l'utiliser

- Installer et configurer les modules OpenClaw.
- Superviser la gateway via TMUX.
- Consulter la cartographie documentaire.

## Quand ne pas l'utiliser

- Comme un runtime complet et fige.
- Pour du trading automatique sans validation humaine.

## Prerequis

- Modules OpenClaw installes : gateway, configure, install, doctor, evidence, model_provider, menu.
- Connaissance de la cartographie (77 sources).

## Commandes / acces

- Gateway : `modules/gateway_openclaw/`
- Configuration : `modules/configure_openclaw/`
- Installation : `modules/install_module_openclaw/`
- Diagnostic : `modules/doctor_openclaw/`
- Preuves : `modules/evidence_openclaw/`
- Cartographie : `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md`

## Procedure simple

1. Installer les modules OpenClaw.
2. Configurer la gateway, verifier son etat.
3. Superviser le runtime via TMUX.
4. Consulter la cartographie.
5. Preparer le deploiement d'agents.

## Verification PASS

- Modules OpenClaw installes et operationnels.
- Gateway repond.
- Supervision TMUX active.
- Cartographie documentaire accessible.

## Limites

- Orchestration runtime en construction.
- Agents non deployes.
- Synthese unifiee absente.
- Ne pas confondre avec OpenClaw Docs Library (cartographie, `DOC_ONLY`).

## Depannage

- Gateway ne repond pas : `doctor_openclaw`.
- Module manquant : `install_module_openclaw`.
- Supervision TMUX absente : ouvrir le GO de supervision dedie.

## Source canonique

- `docs/product_targets/OPENCLAW_TARGET_CANON.md`
- `docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/`
- `docs/chantiers/GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_PARENT_01/`

## RISKS

- À qualifier.
