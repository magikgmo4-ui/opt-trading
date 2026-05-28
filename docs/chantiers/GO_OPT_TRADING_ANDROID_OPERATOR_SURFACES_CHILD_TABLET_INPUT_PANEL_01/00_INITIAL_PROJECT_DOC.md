# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |
| GO_STRUCTURAL_ROLE | `GO_CHILD_ATTACHED_TO_PARENT` |
| Parent | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01` |
| Objet | Documenter la tablette comme panneau d'entrée pur : clavier, souris, stylet, raccourcis, multi-PC |
| Déclencheur | Parent Android operator surfaces mergé ; Unified Remote / Stream Deck identifiés comme UI opérateur mais pas encore creusés comme produit d'entrée principal |
| Base | `sot/mainline` |
| Branche | `go/GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |

## 6_FINAL_TARGET

Produit à cadrer :

```txt
TABLET_INPUT_PANEL_V1
```

Chaîne fonctionnelle cible :

```txt
Tablette Android
→ périphérique d'entrée pur
→ souris / trackpad (Unified Remote)
→ clavier Android ou clavier physique branché tablette
→ stylet pointeur simple
→ raccourcis personnalisés
→ bascule PC 1 / PC 2
→ Stream Deck Mobile en alternative cockpit
```

Sans SSH, sans tmux, sans Tasker obligatoire, sans duplication écran.

## 7_SCOPE

Unified Remote est le produit central à documenter.
Stream Deck Mobile est l'alternative cockpit visuel si les raccourcis deviennent le besoin principal.
Le clavier/souris/stylet Android natif est la couche de base à tester.

Hors scope :
- Installation Termux / SSH (délégué au child Termux)
- Tasker automation
- tmux session management
- Runtime trading
- Bureau distant / duplication d'écran

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

## Matrice décisionnelle

| Besoin | Unified Remote | Stream Deck Mobile | Clavier/souris direct | Verdict |
|---|---|---|---|---|
| Trackpad tablette | Fort | Faible | N/A | Unified Remote |
| Clavier tablette vers PC | Fort | Faible | Fort si direct | Unified Remote ou direct |
| Clavier physique branché tablette vers PC | À tester | Faible | Fort si branché au PC | Unified Remote seulement si latence OK |
| Gros boutons raccourcis | Moyen/Fort | Fort | Faible | Stream Deck si cockpit lourd |
| Bascule PC 1 / PC 2 | Moyen | Moyen | Faible | Unified Remote si appairage stable |
| Stylet pointeur | Moyen | N/A | N/A | Unified Remote pour pointage simple |
| Dessin avec pression | Faible | N/A | Tablette graphique directe | Hors scope Unified Remote |
| Multi-écran / déplacement fenêtres | Moyen | Moyen via raccourcis | Moyen | À tester selon OS |
| Usage trading / bureau rapide | Moyen/Fort | Fort | Fort | Mix possible |

## Plan de test manuel

### Test A — Setup / appairage
1. Installer serveur Unified Remote sur PC 1.
2. Installer serveur Unified Remote sur PC 2.
3. Installer app tablette.
4. Vérifier détection PC 1 / PC 2.
5. Basculer PC cible depuis l'application.

PASS si la tablette contrôle chaque PC séparément sans reconnecter manuellement le réseau.

### Test B — Souris / trackpad
1. Tester déplacement lent.
2. Tester déplacement rapide.
3. Tester clic gauche.
4. Tester clic droit.
5. Tester scroll.
6. Tester drag/drop simple.

PASS si navigation bureau fiable pendant 10 minutes.
FAIL si latence ou pertes rendent le pointage imprécis.

### Test C — Clavier
1. Tester clavier virtuel Android.
2. Tester clavier physique branché à la tablette.
3. Tester saisie longue.
4. Tester raccourcis `Ctrl+C`, `Ctrl+V`, `Alt+Tab`, `Ctrl+S`.

PASS si les touches arrivent dans le bon ordre et sans répétition parasite.

### Test D — Stylet
1. Utiliser le stylet comme pointeur.
2. Tester clic sur petits boutons.
3. Tester tracé simple dans Paint/Krita/Whiteboard.
4. Vérifier absence/présence de pression.

PASS pour pointage simple.
FAIL pour dessin artistique si pression/inclinaison non transmise.

### Test E — Custom remotes
Créer un profil minimal :

```txt
[Ctrl+Z] [Ctrl+S]
[B]      [E]
[Space]  [Alt+Tab]
[PC1]    [PC2]
```

PASS si les boutons déclenchent les raccourcis attendus sur le PC actif.

### Test F — Stream Deck Mobile comparaison
1. Créer profil 8 boutons.
2. Tester lisibilité, vitesse, ergonomie.
3. Comparer avec Unified Remote Custom Remote.

PASS si Stream Deck est plus clair pour cockpit raccourcis.
FAIL si la bascule PC / pointage reste plus utile dans Unified Remote.

## PASS/FAIL sans appareil

Ce GO peut passer en doc-only si :

- le scope est strictement séparé de Termux/Tasker ;
- la matrice décisionnelle est présente ;
- le plan de test manuel couvre Unified Remote, Stream Deck, clavier, souris, stylet, multi-PC ;
- les limites de dessin/stylet sont explicites ;
- la suite recommandée est un test réel matériel, pas une simulation.

## 12_INVARIANTS

- Doc-only : pas de script, pas de mutation runtime.
- Pas de dépendance à Termux/SSH/tmux/Tasker.
- Unified Remote reste optionnel et non critique.
- Pas de secret dans les docs.
- Pas de dépendance à un appareil réel pour merger ce cadrage.
- Les tests matériels restent à exécuter dans un child séparé si nécessaire.

## 17_RESUME_POINT

Après merge doc-only, reprendre par un test manuel réel :

```txt
GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_REAL_TEST_01
```

Objectif : exécuter les tests A-F avec la tablette, PC 1 et PC 2.