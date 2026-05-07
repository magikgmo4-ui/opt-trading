---
doc_id: OPT_TRADING_GUIDE_TRADING_DUAL_STACK_V1_READONLY
doc_type: user_guide_readonly
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md
---

# Guide de lecture - Trading Dual Stack V1 / XAUUSD

> **ATTENTION : ceci est un guide de lecture, pas un guide d'usage live.**
> Ce produit est `DOC_ONLY`. La V1 est close mais sans broker reel, sans ordre reel, sans auto-trading.

## Ce que c'est

Trading Dual Stack V1 est un framework de trading unifie LAB/REALTIME, perimetre XAUUSD borne, visant a imposer la discipline au trader, forcer la validation avant l'autonomie, et produire une journalisation exploitable.

## A quoi ca sert

Il sert de cadre documente pour unifier les environnements LAB et REALTIME autour d'un noyau commun (frame / strategy / execution / analytics).

## Quand le consulter

- pour comprendre le cadre de trading unifie V1 ;
- pour lire la synthese canonique produit ;
- pour consulter les schemas et la configuration V1 etablis.

## Quand ne pas l'utiliser

- comme un produit live-ready (pas de broker connecte) ;
- pour passer des ordres reels ;
- pour du trading automatique sans validation humaine.

## Ce qu'il ne faut pas en deduire

- Ce produit n'est pas `USABLE_NOW`. Il est `DOC_ONLY`.
- La V1 est close mais bornee : LAB operationnel, REALTIME minimal, comparateur operationnel.
- Aucun ordre reel, aucun broker, aucun auto-trading.
- L'extension reelle est conditionnelle (`GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`).

## Prerequis de lecture

- lecture de la synthese canonique : `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md`
- comprehension du perimetre V1 : XAUUSD, America/Montreal, 18h-20h

## Procedure de lecture

1. Lire la synthese canonique produit.
2. Noter le perimetre borne (XAUUSD, horaires, pas de broker).
3. Noter le gap : sans broker reel, sans ordre reel.
4. Noter le NEXT_GO conditionnel : `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`.
5. Ne pas tenter d'usage reel tant que ce GO conditionnel n'est pas ouvert et passe.

## Limites

- sans broker connecte ;
- sans passage d'ordre reel ;
- sans auto-trading ;
- V1 close mais bornee.

## Source canonique

- `docs/governance/TRADING_DUAL_STACK_CANONICAL_PRODUCT_SYNTH_01.md`

## NEXT_GO

`GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` (uniquement si besoin d'extension reelle identifie)
