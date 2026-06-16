# GO_VOICE_OPERATOR_COMMAND_CONTRACTS_AUDIT_01 — Initial Project Doc

## Objectif

Faire passer Voice Operator de "ca repond" a "ca repond utilement".
Auditer toutes les commandes /voice, definir les sorties attendues, les sources de donnees, les gaps, et corriger les commandes qui fallback ou repondent pauvrement.

## Contexte

Apres P0-P3 routing/TTS fixes:
- rapport marche -> market_view
- resume spcx -> spcx_full
- TTS rate 0.88 pitch 0.95
- TTS parle rich.spoken_text

## Regles

- Monitor-only — aucun broker/order/execution
- Pas de LLM dans le routing (keyword-based)
- Chaque commande doit retourner: intent, ok, one_line, rich (spoken_text + cards + badges), freshness, source, missing[], next_action[]
- missing[] = informations attendues mais absentes — pour distinguer donnees absentes vs reponse pauvre

## Critères PASS

- chaque bouton /voice retourne un intent non-unknown
- aucune commande attendue ne tombe sur /read/system par fallback
- chaque reponse a one_line, rich.spoken_text, cards
- chaque reponse indique missing[] si info absente
- TTS parle spoken_text
- monitor-only maintenu
