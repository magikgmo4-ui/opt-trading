# 40_GATE_DECISION

## 1_MASTER_TARGET

Decider si le draft minimal autorise un essai de session controlee dans un GO suivant.

## 7_CANONICAL_STATE

Elements etablis :

- PR #515 mergée ;
- pinned trial `tmux-ide@1.3.1` : `PASS_TRIAL` ;
- gate precedente : `IDE_YML_ALLOW_NEXT_GO` ;
- draft `ide.yml` minimal documente ;
- validation statique : `PASS_STATIC_VALIDATE` ;
- aucun `ide.yml` actif cree ;
- aucune session lancee.

## 8_GATE_VERDICT

```text
ALLOW_CONTROLLED_SESSION_TRIAL
```

Motif :

- le package pinne a deja passe `--version` et `--help` sur `admin-trading` ;
- le draft minimal valide avec `tmux-ide@1.3.1 validate --json` ;
- les commandes du draft sont non destructives ;
- aucune installation globale n'est requise ;
- la session reelle reste separee dans un GO suivant.

## 9_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_CONTROLLED_SESSION_TRIAL_01
```

Objectif recommande :

- creer temporairement ou explicitement l'`ide.yml` minimal dans un emplacement controle ;
- lancer uniquement un essai de session borne ;
- inspecter `tmux-ide status` / `inspect` ;
- stopper proprement la session si le trial le demande ;
- documenter les resultats sans installation durable.

## 10_NOT_ALLOWED_BY_THIS_GATE

Cette gate n'autorise pas :

- installation globale ;
- mutation systeme ;
- lancement permanent ;
- ajout d'un dashboard ;
- extension a `db-layer`, `student`, `fantome` ou OpenClaw ;
- modification des index globaux sans GO dedie.

## 12_INVARIANTS

- `ALLOW_CONTROLLED_SESSION_TRIAL` ne vaut pas runtime permanent.
- `PASS_STATIC_VALIDATE` ne vaut pas usage operateur stabilise.
- Toute session doit rester bornee, inspectable et reversible.

## 17_RESUME_POINT

```text
REPRISE:
Draft ide.yml minimal valide statiquement.

NEXT:
ouvrir un GO separe de controlled session trial si la suite est acceptee.
```

## 18_VERDICT

```text
ALLOW_CONTROLLED_SESSION_TRIAL
```

## RISKS

- À qualifier.
