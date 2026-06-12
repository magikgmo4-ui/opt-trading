---
doc_id: OPT_TRADING_GUIDE_TRADING_DUAL_STACK_V1_READONLY
doc_type: reprise_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md
---

# Guide de reprise - Trading Dual Stack V1 / XAUUSD

> **Sous-type :** `DOC_ONLY_INITIAL_PROJECT`
> Document initial de cadre produit. La V1 est close mais bornee. L'extension reelle est conditionnelle.

## 1_MASTER_TARGET

Framework trading unifie LAB/REALTIME avec broker connecte, perimetre XAUUSD, ordres papier puis reel controle.

## FINAL_TARGET

Framework LAB/REALTIME operationnel avec broker, ordres et validation humaine systematique.

## CURRENT_STATE

`DOC_ONLY` -- `DOC_ONLY_INITIAL_PROJECT`. V1 close mais bornee : schemas/config etablis, LAB operationnel, REALTIME minimal, comparateur operationnel. Sans broker reel, sans ordre reel, sans auto-trading.

## USAGE_ALLOWED_NOW

- Lire la synthese canonique produit.
- Exploiter le LAB pour backtest.
- Observer en REALTIME (sans ordre).
- Preparer le terrain pour l'extension reelle.

## USAGE_FORBIDDEN_NOW

- Passer des ordres reels.
- Connecter un broker sans validation.
- Auto-trading.

## IMPLEMENTATION_PATH

1. Identifier le besoin d'extension reelle.
2. Ouvrir `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`.
3. Connecter un broker.
4. Valider les ordres papier.
5. Passage progressif au reel controle.

## CONTINUITY_STATE

En attente -- extension conditionnelle, pas de GO actif.

## MACHINE / SURFACE

`admin-trading` (LAB, REALTIME).

## REPRISE_POINT

```text
docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md
```

## TODO

1. Identifier le besoin d'extension reelle.
2. Ouvrir le GO conditionnel si besoin confirme.
3. Preparer l'architecture broker.

## REMAINING_GAP

Sans broker connecte, sans passage d'ordre reel, sans auto-trading. V1 close mais bornee.

## NEXT_GO

`GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` (uniquement si besoin d'extension reelle identifie).

## PROMOTION_CONDITIONS

`DOC_ONLY` -> `USABLE_LIMITED` quand :
- GO d'extension reelle ouvert et en cours.

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- broker connecte,
- ordres papier valides,
- closeout pose.

## Ce que c'est

Framework de trading unifie LAB/REALTIME, perimetre XAUUSD borne, discipline avant autonomie.

## A quoi ca sert

Cadre documente pour unifier LAB et REALTIME autour d'un noyau commun.

## Quand le consulter

- Pour comprendre le cadre de trading unifie V1.
- Pour lire la synthese canonique produit.
- Pour consulter les schemas et config V1.

## Quand ne pas l'utiliser

- Comme produit live-ready (pas de broker).
- Pour passer des ordres reels.
- Pour du trading automatique.

## Prerequis de lecture

- `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md`
- Perimetre V1 : XAUUSD, America/Montreal, 18h-20h.

## Procedure de lecture

1. Lire la synthese canonique produit.
2. Noter le perimetre borne (XAUUSD, horaires, pas de broker).
3. Noter le NEXT_GO conditionnel.
4. Ne pas tenter d'usage reel sans GO dedie.

## Limites

- Sans broker connecte.
- Sans passage d'ordre reel.
- Sans auto-trading.
- V1 close mais bornee.

## Source canonique

- `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md`

## RISKS

- À qualifier.
