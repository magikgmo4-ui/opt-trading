# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |
| Objet | Documenter la tablette comme panneau d'entrée pur : clavier, souris, stylet, raccourcis, multi-PC |
| Déclencheur | Parent `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01` mergé — Unified Remote/Stream Deck identifiés comme UI opérateur mais pas creusés comme produit d'entrée principal |
| Base | `sot/mainline` |
| Branche | `go/GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |

## 6_FINAL_TARGET

Produit à prouver :

```
Tablette Android
→ périphérique d'entrée pur
→ souris / trackpad (Unified Remote)
→ clavier Android ou clavier physique branché
→ stylet pointeur
→ raccourcis personnalisés
→ bascule PC 1 / PC 2
→ Stream Deck Mobile en alternative cockpit
```

Sans SSH, sans tmux, sans Tasker obligatoire.

## 7_SCOPE

Unified Remote comme produit central.
Stream Deck Mobile comme alternative cockpit visuel.
Clavier/souris/stylet Android natif comme couche de base.

Hors scope :
- Installation Termux / SSH (délégué au child Termux)
- Tasker automation
- tmux session management
- Runtime trading

## Livrables

| # | Livrable |
|---|---|
| 1 | Unified Remote : setup, appairage, raccourcis custom, bascule multi-PC |
| 2 | Stream Deck Mobile : profils, boutons, UX cockpit vs Unified Remote |
| 3 | Clavier Android + clavier physique : limites, latence, productivité |
| 4 | Souris/trackpad Android : test de précision, clic droit, scroll |
| 5 | Stylet pointeur : usage réel, limites dessin/pression, alternatives |
| 6 | Comparatif Unified Remote vs Stream Deck Mobile vs clavier/souris seul |
| 7 | Plan de test manuel (sans device = doc-only PASS) |

## 12_INVARIANTS

- Doc-only : pas de script, pas de mutation runtime
- Pas de dépendance à Termux/SSH/tmux/Tasker
- Unified Remote reste optionnel (pas de dépendance critique)
- Pas de secret dans les docs
