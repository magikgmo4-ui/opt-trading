# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_REAL_TEST_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_REAL_TEST_01` |
| GO_STRUCTURAL_ROLE | `GO_CHILD_ATTACHED_TO_PARENT` |
| Parent | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01` |
| Previous child | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |
| Objectif | Exécuter les tests réels tablette + PC 1 + PC 2 pour Unified Remote / Stream Deck Mobile |

## 6_FINAL_TARGET

Prouver matériellement `TABLET_INPUT_PANEL_V1` sur vraie tablette.

## 7_SCOPE

Tests réels :
- appairage Unified Remote PC 1 / PC 2 ;
- bascule multi-PC ;
- trackpad / clic / scroll / drag ;
- clavier virtuel Android ;
- clavier physique branché tablette ;
- stylet comme pointeur ;
- custom remotes ;
- comparaison Stream Deck Mobile.

## 12_INVARIANTS

- Aucun SSH / tmux / Tasker.
- Aucun runtime trading.
- Aucun script.
- Tests manuels uniquement.
- Résultats documentés dans ce chantier.

## 16_TODO

1. Tester setup Unified Remote.
2. Tester PC 1.
3. Tester PC 2.
4. Tester bascule PC.
5. Tester raccourcis custom.
6. Tester clavier physique.
7. Tester stylet.
8. Remplir PASS/FAIL réel.
