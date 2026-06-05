# 10_REQUIREMENTS_FROM_PINNED_TRIAL

## 1_MASTER_TARGET

Extraire les exigences utilisables depuis le trial pinne `tmux-ide@1.3.1`.

## 7_CANONICAL_STATE

Sources lues :

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01/30_GATE_DECISION.md`
- `docs/chantiers/GO_TMUX_IDE_OPT_TRADING_ADMIN_TRADING_TMUX_IDE_V1_PINNED_TRIAL_01/90_CLOSEOUT.md`

## 8_REQUIREMENTS

| Requirement | Source | Decision |
| --- | --- | --- |
| Rester sur le flux P0 TMUX IDE | `ACTIVE_STREAMS.md` | scope conserve |
| Cibler `admin-trading` | machine cible deja qualifiee | scope conserve |
| Utiliser `tmux-ide@1.3.1` | pinned trial PASS | version pinnee |
| Utiliser `npx -y` | trial precedent | pas d'installation globale |
| Ne pas creer `ide.yml` dans le GO precedent | gate precedente | ce GO documente le draft avant session |
| Ne pas lancer de session complete | invariants du trial | gate separee requise |
| Ne pas modifier les index globaux | consigne GO | aucune entree index creee |

## 9_BASELINE_FROM_TRIAL

| Element | Resultat |
| --- | --- |
| SSH `admin-trading` | PASS apres allumage |
| `tmux` | `3.3a` |
| `node` | `v18.20.4` |
| `npm` | `9.2.0` |
| `npx` | present |
| `tmux-ide@1.3.1 --version` | `tmux-ide v1.3.1` |
| `tmux-ide@1.3.1 --help` | PASS |

## 10_CONFIG_REQUIREMENTS

Le draft `ide.yml` doit rester minimal :

- nom de session explicite ;
- une structure `rows` / `panes` compatible avec `tmux-ide@1.3.1` ;
- commandes read-only ou locales de navigation ;
- aucun `before` hook ;
- aucune commande de demarrage runtime ;
- aucun `detect --write`, `init`, `config set` ou mutation automatique ;
- aucune dependance a une installation globale.

## 12_INVARIANTS

- Le draft ne prouve pas encore une session operateur stable.
- La validation statique ne vaut pas lancement de session.
- Le prochain GO doit rester controle si une session est testee.

## 17_RESUME_POINT

Les exigences autorisent un draft minimal et une validation statique. Elles n'autorisent pas encore une session complete.

## RISKS

- À qualifier.
