---
doc_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01_CLOSEOUT_ISOLATION
doc_type: chantier_closeout
repo: opt-trading
project: opt-trading
module: reseau_ssh
go_id: GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01
status: open
lifecycle_stage: closeout_isolation_publication
topic_keys:
  - opt-trading
  - reseau_ssh
  - isolation
  - publication
  - closeout
surface: docs
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_TARGET_DECISION_01/03_decisions.md
---

# GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01 - Closeout isolation publication

## Etat de depart retenu

Le cadrage `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01` a ete produit comme lot doc-only pour preparer un futur GO physique, sans application machine.

Etat documentaire de reference :

- cible finale unique retenue : `modules/reseau_ssh_step2`
- contrat operateur final vise : alias courts `menu-reseau_ssh`, `cmd-reseau_ssh`, `sanity-reseau_ssh`
- `NO_GO_PHYSICAL` maintenu
- le cadrage publie ne vaut pas execution physique

## Probleme de bornage initial sur `sot/mainline`

L'arbitrage Git sur `sot/mainline` a montre deux commits locaux en avance sur `origin/sot/mainline` :

- `6a75b13 docs: add reseau ssh runtime compat retirement cadrage`
- `a885f0b docs: anchor canonical GO naming rule and initial project token source`

Conclusion :

- un push direct de `sot/mainline` aurait publie les deux commits ensemble
- le lot `reseau_ssh` n'etait donc pas publiable en lot borne sur `sot/mainline`

## Decision d'arbitrage

Statut retenu pour `a885f0b` :

`HOLD_SEPARATE`

Motif :

- `a885f0b` porte un lot documentaire de gouvernance globale
- ce lot est hors perimetre `reseau_ssh`
- il ne devait pas etre embarque avec le cadrage `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01`

## Strategie d'isolation appliquee

Strategie retenue et executee :

1. partir de `origin/sot/mainline`
2. creer une branche dediee
3. y isoler seulement le commit `6a75b13`
4. verifier le diff contre `origin/sot/mainline`
5. publier uniquement la branche isolee

Cette strategie a ete appliquee sans :

- nouveau patch runtime
- changement de perimetre
- modification de contenu du lot publie
- push de `sot/mainline`

## Branche creee

Branche d'isolation et de publication :

`codex/reseau-ssh-runtime-compat-retirement-01-isolate`

## Commit publie

Le commit present sur la branche isolee et publie est :

`8749e30 docs: add reseau ssh runtime compat retirement cadrage`

Il correspond a l'isolation du seul lot `reseau_ssh` porte par :

- `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md`

## Preuve de bornage du diff

Preuve Git retenue contre `origin/sot/mainline` :

```text
git log --oneline origin/sot/mainline..HEAD
8749e30 docs: add reseau ssh runtime compat retirement cadrage
```

```text
git diff --stat origin/sot/mainline..HEAD
docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md | 336 insertions
1 file changed, 336 insertions(+)
```

Conclusion de bornage :

- un seul commit en avance
- un seul fichier dans le diff
- seul `00_cadrage.md` est publie dans cette sequence

## Rappel de garde-fou

La publication sur branche isolee n'est pas une application physique.

Elle ne vaut pas :

- retrait effectif
- renommage
- repointage
- changement runtime
- changement symlink
- changement alias
- changement lie a `fantome`

Le verdict directeur reste :

- `PASS documentaire`
- `NO_GO_PHYSICAL` maintenu

## Verdict final

`PASS_CLOSEOUT_ISOLATION`

La sequence d'isolation et de publication bornee du cadrage `GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01` est close cote documentaire.

## Point de reprise

Etat de reprise retenu :

- branche source publiee : `origin/codex/reseau-ssh-runtime-compat-retirement-01-isolate`
- base de comparaison : `origin/sot/mainline`
- commit publie : `8749e30 docs: add reseau ssh runtime compat retirement cadrage`
- diff publie : seul `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_RUNTIME_COMPAT_RETIREMENT_01/00_cadrage.md`

Suite admissible :

- relire le cadrage publie
- ouvrir separement tout travail de PR ou de fusion documentaire si requis
- ne pas confondre cette publication bornee avec un feu vert de migration physique

## RISKS

- À qualifier.
