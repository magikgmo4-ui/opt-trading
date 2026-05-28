# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_REAL_TEST_01

| Champ | Valeur |
|---|---|
| GO | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_REAL_TEST_01` |
| GO_STRUCTURAL_ROLE | `GO_CHILD_ATTACHED_TO_PARENT` |
| Parent principal | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01` |
| Parent mobile/Figma à recroiser | `GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01` |
| Previous child | `GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TABLET_INPUT_PANEL_01` |
| Objectif | Exécuter les tests réels tablette + PC 1 + PC 2 pour Unified Remote / Stream Deck Mobile en tenant compte du cockpit mobile LocalCMS/Figma |

## 6_FINAL_TARGET

Prouver matériellement `TABLET_INPUT_PANEL_V1` sur vraie tablette, tout en vérifiant que ce panneau d'entrée reste compatible avec la logique mobile cockpit déjà documentée dans `GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01`.

## 7_SCOPE

Tests réels :
- appairage Unified Remote PC 1 / PC 2 ;
- bascule multi-PC ;
- trackpad / clic / scroll / drag ;
- clavier virtuel Android ;
- clavier physique branché tablette ;
- stylet comme pointeur ;
- custom remotes ;
- comparaison Stream Deck Mobile ;
- compatibilité avec les vues mobile LocalCMS/Figma ;
- séparation `voir / commander / intervenir`.

## 8_CROSS_REFERENCE_MOBILE_FIGMA

À intégrer depuis `GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01` :

### Mobile cockpit
Le parent mobile/Figma définit :

```txt
Mobile = snapshot opérateur rapide
Desktop = cockpit système complet
LocalCMS = read-only au départ
Desk Pro = trading actif séparé
```

Le test tablette doit donc vérifier que la tablette peut servir deux rôles distincts :

1. périphérique d'entrée pur via Unified Remote ;
2. surface de consultation mobile LocalCMS/Web cockpit sans devenir runtime.

### Vues mobiles à prendre en compte
Le test réel doit vérifier que les raccourcis/panneaux n'entrent pas en conflit avec les vues mobiles prévues :

- `Mobile Operator Snapshot` ;
- `OpenClaw Runtime Mobile` ;
- `TMUX Sessions Mobile` ;
- `Strict Workers Mobile` ;
- `External Apps Mobile`.

### Surfaces support à inclure
Le parent mobile/Figma établit la hiérarchie :

```txt
LocalCMS Web Cockpit = supervision permanente read-only
Stream Deck = commandes safe bornées
Unified Remote = télécommande mobile secondaire
RustDesk = support visuel cross-machine
RDP / Bureau distant = intervention GUI complète
Desk Pro = trading actif séparé
```

Ce GO doit donc tester Unified Remote et Stream Deck sans les confondre avec :

- LocalCMS/Web cockpit : supervision permanente ;
- RustDesk/RDP : support visuel/intervention ;
- Desk Pro : trading actif séparé.

## 9_TEST_MATRIX_EXTENDED

| Surface | À tester | Critère PASS | Hors scope |
|---|---|---|---|
| Unified Remote | trackpad, clavier, stylet, raccourcis, PC switch | contrôle fiable PC 1/PC 2 sans écran dupliqué | source de vérité, cockpit canonique |
| Stream Deck Mobile | profils/boutons safe | accès rapide aux vues/apps sans action destructive | trading live, git push/merge |
| LocalCMS mobile | ouverture rapide depuis raccourci | consultation read-only claire | runtime, mutation |
| RustDesk/RDP | raccourci d'ouverture seulement | support visuel accessible si besoin | monitoring permanent |
| Desk Pro | raccourci d'ouverture seulement | trading actif séparé de la tablette input | ordre live depuis bouton tactile |

## 12_INVARIANTS

- Aucun SSH / tmux / Tasker dans ce GO.
- Aucun runtime trading.
- Aucun script.
- Tests manuels uniquement.
- Résultats documentés dans ce chantier.
- Repo > Figma.
- Docs chantiers > commentaires Figma.
- LocalCMS reste read-only au démarrage.
- Desk Pro reste UI trading active séparée.
- Aucune action destructive via Stream Deck ou Unified Remote.
- Unified Remote reste télécommande mobile secondaire, pas cockpit canonique.

## 16_TODO

1. Tester setup Unified Remote.
2. Tester PC 1.
3. Tester PC 2.
4. Tester bascule PC.
5. Tester raccourcis custom.
6. Tester clavier physique.
7. Tester stylet.
8. Vérifier raccourci vers LocalCMS mobile / Web cockpit.
9. Vérifier raccourci vers RustDesk/RDP sans action automatique.
10. Vérifier Stream Deck Mobile safe profile, boutons non destructifs.
11. Remplir PASS/FAIL réel.

## 17_RESUME_POINT

Reprendre par la matrice `9_TEST_MATRIX_EXTENDED`, puis exécuter les tests matériels sur tablette + PC 1 + PC 2.
