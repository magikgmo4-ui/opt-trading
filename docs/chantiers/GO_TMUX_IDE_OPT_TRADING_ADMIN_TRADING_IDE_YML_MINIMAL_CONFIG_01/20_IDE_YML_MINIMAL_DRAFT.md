# 20_IDE_YML_MINIMAL_DRAFT

## 1_MASTER_TARGET

Proposer un `ide.yml` minimal pour `admin-trading`, sans creer de fichier `ide.yml` actif dans le repo.

## 7_CANONICAL_STATE

Le format utilise vient du README npm de `tmux-ide@1.3.1` :

- `name` : nom de session tmux ;
- `rows` : lignes de layout ;
- `panes` : panneaux par ligne ;
- `title` : label de pane ;
- `command` : commande initiale optionnelle ;
- `focus` : focus initial optionnel.

## 8_MINIMAL_DRAFT

Draft propose :

```yaml
name: opt-trading-admin-trading
rows:
  - size: 70%
    panes:
      - title: Shell
        command: pwd
        focus: true
      - title: Git
        command: git status --short --branch
  - size: 30%
    panes:
      - title: Docs
        command: ls docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_IDE_YML_MINIMAL_CONFIG_01
```

## 9_FIELD_JUSTIFICATION

| Champ | Justification |
| --- | --- |
| `name` | nom explicite, stable et rattache a `admin-trading` |
| `rows[0].size` | surface principale pour shell et Git |
| `rows[0].panes[0].title` | pane shell neutre |
| `rows[0].panes[0].command` | `pwd` ne lance pas de runtime |
| `rows[0].panes[0].focus` | point d'entree operateur explicite |
| `rows[0].panes[1].title` | pane Git dediee |
| `rows[0].panes[1].command` | `git status --short --branch` est read-only |
| `rows[1].size` | bande secondaire pour documentation |
| `rows[1].panes[0].title` | pane docs dediee |
| `rows[1].panes[0].command` | liste le dossier GO sans lancer d'application |

## 10_EXCLUDED_FROM_DRAFT

Le draft exclut volontairement :

- `before` ;
- commandes `npm`, `pnpm`, `python`, `pytest` ou runtime ;
- commandes reseau ;
- commandes de mutation Git ;
- `tmux-ide init` ;
- `tmux-ide detect --write` ;
- configuration d'equipe ou agent.

## 12_INVARIANTS

- Ce contenu est un draft documente, pas un `ide.yml` actif.
- Le fichier actif ne doit etre cree que dans une suite explicitement autorisee.
- Le lancement de session reste hors scope.

## 17_RESUME_POINT

Utiliser ce draft comme entree de validation statique, puis lire la decision dans `40_GATE_DECISION.md`.
