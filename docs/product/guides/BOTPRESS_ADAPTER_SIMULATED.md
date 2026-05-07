---
doc_id: OPT_TRADING_GUIDE_BOTPRESS_ADAPTER_SIMULATED
doc_type: implementation_guide
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

# Guide d'implementation - Botpress Adapter

> **Sous-type :** `SIMULATED_ONLY_IMPLEMENTATION_READY`
> Smokes passes en simulation (12/12 E2E, 13/13 adapter). Safety gate active. Le passage au reel Telegram est la prochaine etape.

## 1_MASTER_TARGET

Operateur conversationnel borne avec Botpress, Telegram reel, webhook reel et safety gate.

## FINAL_TARGET

Routeur conversationnel controle : Telegram -> Botpress -> OpenClaw Gateway -> surfaces trading -> retour Telegram, avec journalisation structuree.

## CURRENT_STATE

`SIMULATED_ONLY` -- `SIMULATED_ONLY_IMPLEMENTATION_READY`. Parent, spec, adapter et smoke E2E passes en simulation. Adapter 13/13 smoke, E2E 12/12. Safety gate active (execute_trade bloque). Telegram reel absent, webhook reel absent.

## USAGE_ALLOWED_NOW

- Relire ou rejouer le flux simule.
- Verifier que la safety gate bloque `execute_trade`.
- Preparer le GO Telegram reel.

## USAGE_FORBIDDEN_NOW

- Bot live pret pour production.
- Webhook reel non cadre.
- Trading reel.
- Push Git ou modification prod automatique.

## IMPLEMENTATION_PATH

1. Ouvrir `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`.
2. Setup Telegram bot (credentials hors repo).
3. Configurer webhook -> Botpress.
4. Configurer Botpress -> adapter HTTP reel.
5. Smoke production controle.
6. Closeout reel.

## CONTINUITY_STATE

En attente d'implementation reelle -- `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01` est le prochain GO.

## MACHINE / SURFACE

`admin-trading` (Botpress, adapter).

## REPRISE_POINT

```text
docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md
docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md
```

## TODO

1. Ouvrir `GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`.
2. Obtenir les credentials Telegram (hors repo).
3. Configurer le webhook reel.
4. Smoke production controle.
5. Closeout reel.

## REMAINING_GAP

Telegram reel, webhook reel, credentials et smoke production controle.

## NEXT_GO

`GO_TRADING_BOTPRESS_TELEGRAM_REAL_INTEGRATION_01`

## PROMOTION_CONDITIONS

`SIMULATED_ONLY` -> `USABLE_LIMITED` quand :
- Telegram reel connecte,
- webhook reel operationnel,
- smoke production controle passe.

`USABLE_LIMITED` -> `USABLE_NOW` quand :
- closeout reel pose.

## Ce que c'est

Flux Botpress -> adapter -> reponse dans un cadre simule et borne par une safety gate.

## A quoi ca sert

Valider le routage conversationnel, les reponses structurees et le blocage des intents interdits.

## Quand l'utiliser

- Relire ou rejouer le flux simule.
- Verifier le blocage de `execute_trade`.
- Preparer le futur GO Telegram reel.

## Quand ne pas l'utiliser

- Comme bot live pret pour production.
- Pour du webhook reel non cadre.
- Pour du trading reel.
- Pour pousser Git ou modifier la prod.

## Prerequis

- Lecture des closeouts Botpress.
- Acces a `adapter_botpress_openclaw.py` et `smoke_adapter.py`.
- Comprehension que l'etat porte est `SIMULATED_PASS`.

## Commandes / acces

- Adapter : `adapter_botpress_openclaw.py`
- Smoke : `smoke_adapter.py`

## Procedure simple

1. Lire le parent Botpress.
2. Verifier que l'usage reste dans le cadre simule.
3. Rejouer ou relire le smoke.
4. Verifier qu'un intent interdit reste bloque.
5. Conclure uniquement sur la simulation.

## Verification PASS

- Adapter prouve par closeout PASS.
- Smoke adapter prouve.
- Smoke Telegram E2E simule prouve (12/12).
- Intent `execute_trade` bloque.
- Aucun secret, aucun trade reel.

## Limites

- Telegram reel absent.
- Webhook reel absent.
- Credentials reel absents.
- Pas de promotion au-dessus de `SIMULATED_PASS` sans nouvelle preuve.

## Depannage

- Intent hors cadre : relire la safety gate.
- Demande live : refus ou report.
- Simulation diverge du role final : ouvrir GO reel dedie.

## Source canonique

- `docs/chantiers/GO_TRADING_PIPELINE_BOTPRESS_OPERATOR_PARENT_01/README.md`
- `docs/chantiers/GO_TRADING_BOTPRESS_OPENCLAW_ADAPTER_IMPL_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_TRADING_BOTPRESS_TELEGRAM_SMOKE_E2E_01/90_CLOSEOUT.md`
