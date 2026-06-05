---
doc_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01
status: open
lifecycle_stage: decision_doc_only
topic_keys:
  - opt-trading
  - reseau_ssh
  - target_decision
  - decisions
  - no_go_physical
surface: docs
source_kind: canonical
updated_at: 2026-04-20
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/02_journal_technique.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_UNIFIED_MODULE_CADRAGE_01/00_cadrage.md
  - docs/status/reseau_ssh_canonique.md
---

# GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01 - Decisions

## Verdict du GO

Verdict documentaire :

`PASS_DOC_ONLY`

Garde-fou maintenu :

`NO_GO_PHYSICAL`

Ce GO ne realise aucune action runtime et ne donne aucun feu vert d'execution machine.

## Decision 1 - cible finale unique

La cible finale unique de la famille `reseau_ssh` est :

`modules/reseau_ssh_step2`

Decision :
- `modules/reseau_ssh_step2` est la cible de convergence future
- `modules/reseau_ssh_step1b` n'est pas cible finale
- `modules/reseau_ssh` n'est pas cible finale
- aucune nouvelle cible unifiee n'est creee par ce GO

## Decision 2 - runtime final vise

Le runtime final vise repose sur les alias courts stables :
- `menu-reseau_ssh`
- `cmd-reseau_ssh`
- `sanity-reseau_ssh`

Decision :
- les alias courts restent le contrat operateur stable
- l'implementation cible future est `modules/reseau_ssh_step2`
- les alias `*_reseau_ssh_step2` ne deviennent pas le contrat final
- `scripts/reseau_ssh/` reste canon operateur actuel jusqu'a migration physique separee

## Decision 3 - statuts finals des surfaces

| Surface | Statut final decide | Condition |
| --- | --- | --- |
| `modules/reseau_ssh_step2` | cible module unique finale | validation dans GO physique separe |
| `modules/reseau_ssh_step1b` | legacy gele / archive possible | retrait interdit avant convergence prouvee |
| `scripts/reseau_ssh/` | canon actuel puis compat/archive apres migration | maintien obligatoire pour rollback initial |
| wrappers racine | candidate-retire-later | retrait differe seulement apres preuve d'absence de callers |
| alias courts | interface operateur finale | conservation obligatoire |
| alias `*_reseau_ssh_step2` | compat transitoire | retrait ou gel seulement apres stabilite machine par machine |

## Decision 4 - mapping actuel vers final

| Actuel | Final | Decision |
| --- | --- | --- |
| `/usr/local/bin/menu-reseau_ssh` | alias court stable vers cible future `step2` | conserver le nom, repointage seulement en GO physique |
| `/usr/local/bin/cmd-reseau_ssh` | alias court stable vers cible future `step2` | conserver le nom, repointage seulement en GO physique |
| `/usr/local/bin/sanity-reseau_ssh` | alias court stable vers cible future `step2` | conserver le nom, repointage seulement en GO physique |
| `/usr/local/bin/*_reseau_ssh_step2` | compat temporaire | conserver pendant transition, retrait differe |
| `/opt/trading/scripts/reseau_ssh/` | compat/archive apres migration | conserver intact pendant la premiere phase physique |
| `/opt/trading/modules/reseau_ssh_step2/` | cible finale | valider comme implementation finale future |
| `/opt/trading/scripts/reseau_ssh_cmd.sh` | retrait differe possible | ne pas retirer sans preuve et rollback |
| `/opt/trading/scripts/reseau_ssh_menu.sh` | retrait differe possible | ne pas retirer sans preuve et rollback |
| `modules/reseau_ssh_step1b` | legacy gele | ne pas retirer dans la migration initiale |

## Decision 5 - rollback obligatoire avant futur GO physique

Le futur GO physique devra contenir avant toute mutation :
- inventaire machine par machine
- snapshot des alias courts
- snapshot des alias `*_reseau_ssh_step2` quand presents
- cibles `readlink -f` avant changement
- copie ou hash des wrappers racine
- commandes de restauration
- critere d'abandon en cas de smoke KO

Rollback minimal decide :
- restaurer les alias courts vers `scripts/reseau_ssh/`
- conserver `scripts/reseau_ssh/` intact
- conserver les wrappers racine
- conserver `modules/reseau_ssh_step1b`
- annuler toute promotion de `modules/reseau_ssh_step2` si validation KO

## Decision 6 - smoke tests obligatoires

Smoke tests minimaux par machine :
- `command -v menu-reseau_ssh`
- `command -v cmd-reseau_ssh`
- `command -v sanity-reseau_ssh`
- `readlink -f /usr/local/bin/menu-reseau_ssh`
- `readlink -f /usr/local/bin/cmd-reseau_ssh`
- `readlink -f /usr/local/bin/sanity-reseau_ssh`
- `sanity-reseau_ssh`
- `cmd-reseau_ssh sanity`
- test menu non destructif
- verification de presence de `scripts/reseau_ssh/`

Compat `step2` quand presente :
- `command -v menu-reseau_ssh_step2`
- `command -v cmd-reseau_ssh_step2`
- `command -v sanity-reseau_ssh_step2`
- `sanity-reseau_ssh_step2`

## Decision 7 - criteres de retrait differe

Les retraits restent interdits tant que tous les criteres suivants ne sont pas satisfaits :
- alias courts stables sur cible finale pendant une periode definie
- absence de callers actifs des wrappers racine prouvee
- `step1b` classe historique seulement
- rollback teste
- etat final documente par machine
- accord explicite du parent `GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03`

Retraits differes :
- wrappers racine
- alias `*_reseau_ssh_step2`
- surfaces `step1b`
- surfaces `modules/reseau_ssh`

## Decision 8 - futur GO physique separe

Le futur GO physique separe reste :

`GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

Ce futur GO devra etre ouvert separement. Il ne peut pas etre deduit de ce GO doc-only.

## Cloture documentaire attendue

Ce GO peut etre clos en PASS documentaire si les decisions ci-dessus sont acceptees.

La cloture documentaire ne change pas l'etat runtime.

`NO_GO_PHYSICAL` reste applicable jusqu'a ouverture et validation d'un GO physique separe.

## RISKS

- À qualifier.
