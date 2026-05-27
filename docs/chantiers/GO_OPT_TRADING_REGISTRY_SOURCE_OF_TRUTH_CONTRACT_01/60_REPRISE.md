---
go_id: GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
doc_type: REPRISE
repo: opt-trading
project: opt-trading
status: OPEN
updated_at: 2026-05-26
---

# 60_REPRISE

## Summary

- `registry/*.yaml` est confirme comme verite centrale prioritaire.
- les readers specialises restent proprietaires de la lecture par registre.
- `registry_router` est confirme comme facade de navigation seulement.
- les exports JSON, seeds locaux et copies verticales sont classes derives ou fallbacks, jamais autorite centrale.
- le contrat recommande d'ajouter centralement `legacy` et `transitional` dans un GO d'implementation ulterieur.
- `machine_target` primaire est conserve, mais `any` est restreint et un raffinement cross-machine est recommande.

## Files created

- `docs/chantiers/GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01/00_INITIAL_PROJECT_DOC.md`
- `10_REGISTRY_SOURCE_MAP.md`
- `20_FALLBACK_AND_DERIVED_VIEWS_CONTRACT.md`
- `30_STATUS_AND_MACHINE_TARGET_MODEL.md`
- `40_DIVERGENCE_RULES.md`
- `50_NEXT_IMPL_GO_LIST.md`
- `60_REPRISE.md`

## Diff summary

- formalise la priorite des registres centraux sur toutes les copies locales
- borne strictement les fallbacks locaux a des usages de bootstrap ou degrade read-only
- pose un vocabulaire minimal pour `status` et une regle plus stricte pour `machine_target`
- prepare les GOs d'implementation `source-of-truth`, `deepseek_student`, et `machine_target`

## Verification useful

```bash
rg -n "source centrale|fallback|legacy|transitional|machine_target|deepseek_student" docs/chantiers/GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
git status --short --branch
git diff -- docs/chantiers/GO_OPT_TRADING_REGISTRY_SOURCE_OF_TRUTH_CONTRACT_01
```

## Verdict

`PASS`
