# 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Ouvrir `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01` pour cadrer un `ide.yml` minimal controle pour `admin-trading`.

## WHY

Le GO precedent `GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01` est ferme apres merge PR #515.

Son verdict etait :

```text
PASS_TRIAL / IDE_YML_ALLOW_NEXT_GO
```

Ce GO transforme cette autorisation en draft statique de configuration, sans installation durable et sans lancement de session complete.

## 3_INITIAL_NEED

- Deriver les exigences depuis le trial pinne `tmux-ide@1.3.1`.
- Proposer un `ide.yml` minimal pour `admin-trading`.
- Valider statiquement le YAML et le schema attendu par `tmux-ide@1.3.1`.
- Decider si un essai de session controlee peut etre ouvert dans un GO suivant.

## 5_GO_SCOPE

Ce GO couvre :

- documentation du besoin minimal ;
- modele `ide.yml` propose dans le dossier chantier ;
- validation statique hors lancement de session ;
- decision de gate.

Ce GO ne couvre pas :

- creation d'un `ide.yml` actif a la racine du repo ;
- installation globale de `tmux-ide` ;
- `tmux-ide init`, `detect --write`, `config set` ou mutation automatique ;
- lancement de session runtime ;
- modification des index globaux.

## 7_CANONICAL_STATE

| Element | Etat |
| --- | --- |
| P0 actif | `GO_TMUX_IDE_OPT_TRADING_CADRAGE_01` |
| Machine cible | `admin-trading` |
| Topologie | `cursor-ai -> SSH -> admin-trading` |
| Trial pinne | `PASS_TRIAL` |
| Package retenu | `tmux-ide@1.3.1` via `npx -y` |
| Gate precedente | `IDE_YML_ALLOW_NEXT_GO` |
| Installation durable | interdite |
| Session complete | interdite dans ce GO |

## 8_VALIDATED_PLAN

1. Repartir de `origin/sot/mainline` apres merge PR #515.
2. Lire `MACHINE_WORK_SPLIT`, `ACTIVE_STREAMS` et les gates du GO pinned trial.
3. Proposer un `ide.yml` minimal en documentation.
4. Valider le draft avec `tmux-ide@1.3.1 validate --json` dans un repertoire temporaire.
5. Documenter la gate avant toute session reelle.

## 12_INVARIANTS

- Aucun `npm install -g`.
- Aucun `apt install`.
- Aucun `ide.yml` actif cree dans le repo.
- Aucun lancement de session tmux-ide.
- Aucun index global modifie.
- Aucun melange avec OpenClaw, Student/Ollama, db-layer ou fantome.

## 17_RESUME_POINT

```text
REPRISE:
GO ouvert dans C:\wideyml.
PR #515 mergée.
Pinned trial ferme en PASS_TRIAL / IDE_YML_ALLOW_NEXT_GO.

NEXT:
relire 20_IDE_YML_MINIMAL_DRAFT.md puis 30_STATIC_VALIDATION.md avant toute decision de session.
```

## 18_VERDICT

```text
WIP / IDE_YML_MINIMAL_CONFIG_OPENED
```

## RISKS

- À qualifier.
