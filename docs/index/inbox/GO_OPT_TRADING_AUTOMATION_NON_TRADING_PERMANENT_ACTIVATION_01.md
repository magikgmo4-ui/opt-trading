# GO_OPT_TRADING_AUTOMATION_NON_TRADING_PERMANENT_ACTIVATION_01

**Statut** : INBOX — ouvert
**Créé** : 2026-05-23
**Type** : Chantier d'activation permanente limitée
**Parent** : `GO_OPT_TRADING_AUTOMATION_PARENT_NON_TRADING_SCHEDULED_ROLLOUT_01`
**Base** : `sot/mainline` après PR #690 + PR #691

## Description

Activer en réel permanent limité les jobs non-trading déjà prouvés, avec scheduler contrôlé, ledger, kill switch, et exclusions explicites Gmail/Calendar/trading.

## Périmètre

- 13 jobs READ_ONLY autorisés avec timers systemd
- Drive canary en WRITE_GATED manuel seulement
- Activation progressive en 3 phases (J1→J6)
- Gmail, Calendar, trading exclus

## Liens

- `docs/chantiers/GO_OPT_TRADING_AUTOMATION_NON_TRADING_PERMANENT_ACTIVATION_01/`
- Branche : `go/GO_OPT_TRADING_AUTOMATION_NON_TRADING_PERMANENT_ACTIVATION_01`
