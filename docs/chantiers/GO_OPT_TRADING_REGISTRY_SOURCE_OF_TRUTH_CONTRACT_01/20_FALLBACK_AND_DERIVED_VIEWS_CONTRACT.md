---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: FALLBACK_AND_DERIVED_VIEWS_CONTRACT
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 20_FALLBACK_AND_DERIVED_VIEWS_CONTRACT

## Vues derivees

Sont considerees vues derivees:

- exports JSON produits depuis les readers (`modules_registry_reader/output/modules_registry.json`, `machines_registry_reader/output/machines_registry.json`, et equivalents)
- copies locales specialisees a un sous-domaine comme `modules/install_module_openclaw/app/modules_registry.json`
- toute vue UI, CLI, Markdown, JSON ou menu regeneree a partir des registries centrales

## Fallbacks locaux autorises

Un fallback local n'est autorise que si toutes les conditions suivantes sont reunies:

1. le fallback est explicitement documente comme non canonique
2. il sert au bootstrap, au seed initial, a la compatibilite locale, ou au read-only degrade
3. il ne pousse jamais d'ecriture de retour vers une registry centrale
4. il est borne a une surface precise, pas reutilise comme verite transverse

## Fallbacks deja toleres

- `modules/ui_registry_msi/config/ui_registry_seed.json`
Cause: bootstrap local si `registry/ui_surfaces_registry.yaml` est absent ou illisible.

## Fallbacks non toleres comme norme

- une copie locale qui diverge durablement de la registry centrale
- un JSON export `output/` consomme comme reference canonique transverse
- une registry embarquee dans un module vertical si une source centrale equivalente existe deja

## Contract boundary

Le fallback local est une exception de disponibilite, pas un second mode normal de gouvernance.
