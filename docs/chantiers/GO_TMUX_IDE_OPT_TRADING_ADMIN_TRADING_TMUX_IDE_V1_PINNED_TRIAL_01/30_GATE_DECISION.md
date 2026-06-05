# 30_GATE_DECISION

## 1_MASTER_TARGET

Prendre la decision de gate apres trial pinne `tmux-ide@1.3.1`.

## 7_CANONICAL_STATE

Resultat observe :

```text
tmux-ide@1.3.1 --version PASS
tmux-ide@1.3.1 --help PASS
```

## 8_GATE_VERDICT

```text
PASS_TRIAL
```

Motif :

- SSH vers `admin-trading` fonctionne apres allumage de la machine ;
- baseline `tmux`, `node`, `npm`, `npx` presente ;
- `tmux-ide@1.3.1` demarre via `npx -y` ;
- le help expose `doctor`, `validate`, `detect`, `init`, `status`, `inspect`.

## 9_IDE_YML_DECISION

```text
ALLOW_NEXT_GO
```

Cette decision signifie :

- autoriser un GO suivant dedie a `doctor` / `validate` / modele `ide.yml` ;
- ne pas creer `ide.yml` dans ce GO ;
- ne pas lancer `init`, `detect --write`, `config set`, `add-pane` ou session runtime dans ce GO.

## 10_NEXT_GO_RECOMMENDED

```text
GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_IDE_YML_GATE_01
```

Objectif recommande :

- cadrer un `ide.yml` minimal ;
- tester `doctor` et `validate` seulement avec limites explicites ;
- ne pas installer globalement ;
- ne pas lancer une session persistante avant validation.

## 12_INVARIANTS

- `PASS_TRIAL` ne vaut pas installation durable.
- `PASS_TRIAL` ne vaut pas creation immediate de `ide.yml`.
- `ALLOW_NEXT_GO` ne vaut pas autorisation de runtime persistant.

## 17_RESUME_POINT

La prochaine etape doit ouvrir un GO separe pour la gate `ide.yml`, si cette suite est validee.

## RISKS

- À qualifier.
