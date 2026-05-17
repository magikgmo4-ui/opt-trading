# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01` pour executer une premiere session `tmux-ide` controlee sur `admin-trading`.

## WHY

PR #516 a ferme le GO `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01`.

Le gate amont est :

```text
PASS_STATIC_VALIDATE / ALLOW_CONTROLLED_SESSION_TRIAL
```

Ce GO consomme cette autorisation de facon bornee : creation temporaire d'un `ide.yml`, lancement controle, observation, fermeture, suppression du fichier temporaire.

## 3_INITIAL_NEED

- Confirmer la baseline pre-session.
- Lancer `tmux-ide@1.3.1` via `npx -y`, sans installation globale.
- Observer la session et les panes.
- Stopper la session.
- Supprimer le `ide.yml` temporaire.
- Documenter la decision de gate.

## 5_GO_SCOPE

Ce GO couvre :

- session `tmux-ide` controlee sur `admin-trading` ;
- `ide.yml` temporaire dans `/opt/trading/ide.yml` ;
- `validate`, launch, `status`, `inspect`, `stop` ;
- verification post-cleanup.

Ce GO ne couvre pas :

- installation globale ;
- session permanente ;
- mutation systeme ;
- dashboard ;
- extension a `db-layer`, `student`, `fantome` ou OpenClaw ;
- modification des index globaux.

## 7_CANONICAL_STATE

| Element | Etat |
| --- | --- |
| PR #516 | `MERGED` |
| Merge #516 | `64cd81df` |
| GO amont | `CLOSED_FINAL` |
| Gate amont | `ALLOW_CONTROLLED_SESSION_TRIAL` |
| Worktree local | `C:\wtmuxsess` |
| Branche | `go/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_CONTROLLED_SESSION_TRIAL_01` |
| Cible | `admin-trading:/opt/trading` |
| Package | `tmux-ide@1.3.1` via `npx -y` |

## 8_VALIDATED_PLAN

1. Verifier PR #516 mergee dans `origin/sot/mainline`.
2. Ouvrir un worktree court depuis `origin/sot/mainline`.
3. Relire `MACHINE_WORK_SPLIT`, `ACTIVE_STREAMS`, `40_GATE_DECISION.md` et `90_CLOSEOUT.md` du GO amont.
4. Confirmer absence de session et absence de `ide.yml`.
5. Creer temporairement `/opt/trading/ide.yml`.
6. Executer `validate`, launch, `status`, `inspect`, `stop`.
7. Supprimer `/opt/trading/ide.yml`.
8. Documenter les resultats.

## 12_INVARIANTS

- Aucun `npm install -g`.
- Aucun `apt install`.
- Aucun `ide.yml` durable.
- Aucune session persistante.
- Aucun index global modifie.
- Aucun melange avec chaines `CLOSED_FINAL`.

## 17_RESUME_POINT

```text
REPRISE:
GO session controlee ouvert dans C:\wtmuxsess.
Session controlee executee et stoppee.

NEXT:
relire 30_SESSION_RESULTS.md et 40_GATE_DECISION.md avant publication.
```

## 18_VERDICT

```text
WIP / CONTROLLED_SESSION_TRIAL_OPENED
```
