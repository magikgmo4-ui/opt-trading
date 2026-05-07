---
doc_id: OPT_TRADING_GUIDE_BOTPRESS_ADAPTER_SIMULATED
doc_type: user_guide
repo: opt-trading
status: reference
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md
  - docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md
  - docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md
  - adapter_botpress_openclaw.py
  - smoke_adapter.py
---

# Guide utilisateur - Botpress Adapter simulated

## Ce que c'est

Cette surface couvre le flux Botpress -> adapter -> reponse dans un cadre simule et borne par une safety gate.

## A quoi ca sert

Elle sert a valider le routage conversationnel, les reponses structurees et le blocage des intents interdits sans ouvrir un usage reel complet.

## Quand l'utiliser

- pour relire ou rejouer le flux simule ;
- pour verifier que la safety gate bloque bien `execute_trade` ;
- pour preparer le futur GO Telegram reel.

## Quand ne pas l'utiliser

- comme bot live pret pour production ;
- pour du webhook reel non cadre ;
- pour du trading reel ;
- pour pousser Git ou modifier la prod.

## Prerequis

- lecture des closeouts Botpress ;
- acces a `adapter_botpress_openclaw.py` et `smoke_adapter.py` ;
- comprehension que l'etat porte est `SIMULATED_PASS`.

## Commandes / acces

- Adapter : `adapter_botpress_openclaw.py`
- Smoke : `smoke_adapter.py`
- Closeouts : voir les liens ci-dessus

## Procedure simple

1. Lire le parent Botpress pour comprendre le role final vise.
2. Verifier que l'usage recherche reste dans le cadre simule.
3. Rejouer ou relire le smoke de l'adapter et le smoke Telegram E2E simule.
4. Verifier qu'un intent interdit reste bloque par la safety gate.
5. Conclure uniquement sur la simulation, jamais sur un usage live.

## Verification PASS

- adapter prouve par closeout PASS ;
- smoke adapter prouve ;
- smoke Telegram E2E simule prouve ;
- intent `execute_trade` bloque ;
- aucun secret et aucun trade reel.

## Limites

- Telegram reel absent ;
- webhook reel absent ;
- credentials reel absents ;
- pas de promotion au-dessus de `SIMULATED_PASS` sans nouvelle preuve.

## Depannage

- Si un intent semble passer hors cadre, relire d'abord la safety gate.
- Si une demande suppose du live, le bon resultat est le refus ou le report.
- Si la simulation diverge du role final, ouvrir un GO dedie au reel plutot que de forcer l'Atlas.

## Source canonique

- `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md`
- `docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md`

## NEXT_GO

`GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`
