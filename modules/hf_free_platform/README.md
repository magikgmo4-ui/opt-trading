# hf_free_platform

Module de publication Hugging Face free-first, concu comme cible de diffusion et non comme source de verite canonique.

## Role
- preparer des surfaces HF publiques ou privees legeres
- porter des assets de publication, scripts de bridge et discipline de lane
- maintenir la separation entre canon Git et cibles de publication Hugging Face

## Contenu
- `spec/` : spec et scope (`00_hf_free_platform_spec_v1.md`, `01_hf_free_platform_scope_v1.md`)
- `handoff/` : pack de reprise
- `kanban/` : suivi du lot HF
- `spaces/` : starters `portal_static`, `tools_private`, `mcp_public`
- `datasets/public_assets/` : assets dataset publics
- `bin/` : scripts `publish_hf_dataset.sh`, `publish_hf_space.sh`, `sync_hf_exports.sh`
- `scripts/hf_free_platform_cmd.sh`, `hf_free_platform_menu.sh`, `sanity_check_hf_free_platform.sh`

## Integration
- le canon reste dans le repo `opt-trading`
- les repos Hugging Face sont des cibles de publication seulement
- hors scope :
  - secrets
  - coeur live trading
  - backend stateful de production

## Statut
- actif
- verticale de publication et de distribution, pas surface runtime trading

## Notes de consolidation
- a garder separe des modules de trading et d'execution
- a traiter comme verticale specialisee avec ses propres lanes de livraison
