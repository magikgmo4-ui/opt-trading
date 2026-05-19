# 05_mapping_machines_screens.md

## Vue d’ensemble
Le setup cible repose sur une séparation fonctionnelle entre **pilotage/dev**, **hub opérationnel**, **UI desk**, et **extension d’affichage réseau**. L’indexation actuelle est réalisée sur `admin-trading`, mais la structure visée est multi-machine.

---

## 1) `cursor-ai` (Dell Windows 11)
### Rôle principal
- poste principal utilisateur
- Trae / Cursor / ChatGPT
- terminal et pilotage des sessions
- capture ponctuelle / screenshot / coordination bot vision / Telegram
- TradingView en poste de travail principal côté utilisateur

### Nature d’usage
- **dev / pilotage / coordination**
- pas destiné à porter toute la logique serveur du desk

### Surfaces attendues
- prompts Trae ciblés
- revue git / journal / orchestration humaine
- éventuels outils de capture ou interaction opérateur

### Niveau de stabilité attendu
- élevé côté usage quotidien
- flexible côté dev

---

## 2) `admin-trading` (Debian 12 headless)
### Rôle principal
- hub opérationnel actuel
- machine de référence pour services et workflows serveur
- point d’ancrage du repo `/opt/trading`
- lieu principal d’exécution des services existants

### Services réellement observés en exploitation
- `tv-perf.service`
- `tv-webhook.service`
- `vision_bot.service`
- `bot_vision_step2.service`
- `ngrok-tv.service`

### Rôle effectif dans le setup actuel
- collecte / webhook / perf / vision
- stockage de travail et journalisation
- point de vérité technique pour l’état du repo et des modules

### Nature d’usage
- **ops / maintenance / intégration / backend local**

### Remarque
`admin-trading` porte déjà la réalité opérationnelle du système. L’indexation confirme qu’il ne manque pas de briques, mais surtout une meilleure surface opérateur unifiée et une meilleure cartographie de ce qui doit rester ici vs ce qui doit être exposé ailleurs.

---

## 3) `db-layer` (MSI Ubuntu)
### Rôle cible validé
- machine UI / desk principal
- écran 1 : interfaces Desk Pro / perf / toolbox / commandes user-friendly
- écran 2 : Coinglass

### Fonction attendue
- surface visuelle principale pour le desk
- exécution d’outils lisibles par l’opérateur
- consultation des sorties consolidées

### Nature d’usage
- **opérateur / visualisation / desk UI**

### État par rapport à l’indexation actuelle
L’inventaire a été fait sur `admin-trading`, donc il ne confirme pas encore le contenu réel de `db-layer`. En revanche, la structure cible reste claire : MSI doit devenir la façade desk cohérente, pas le lieu d’accumulation de bricolages techniques.

---

## 4) `student` (HP ProDesk Debian 12 headless)
### Rôle stabilisé
- machine DeepSeek student / rapport déterministe / pack opérateur spécifique
- chantier séparé et considéré stable à la référence `student_deepseek_ops_v1.0_hotfix2`

### Nature d’usage
- **spécialisé / IA complémentaire / workflow étudiant**

### Règle
Ne pas rouvrir ce chantier sauf régression. Cette machine peut servir de référence de standard UX/opérateur, mais n’est pas le cœur du chantier desk actuel.

---

## 5) Debian additionnel / futur écran réseau
### Rôle cible
- fournir au minimum un écran réseau prêté à Windows
- potentiellement accueillir plus tard un panneau auxiliaire léger si pertinent

### Ce qu’on ne fait pas encore
- pas de migration UI finale
- pas de bascule massive d’affichage
- pas d’intégration réseau improvisée

### Ce que cette phase prépare
- définir ce qui sera affiché sur cet écran
- définir la dépendance vis-à-vis de `admin-trading` et/ou `db-layer`
- éviter de déplacer un composant avant de savoir s’il est opérateur, dev ou maintenance

---

## Mapping synthétique par zone
### Dell / `cursor-ai`
- Trae / GPT / terminal
- coordination humaine
- dev et prompts ciblés

### `admin-trading`
- backend réel actuel
- webhook / perf / vision / journal / repo
- ops et maintenance

### MSI / `db-layer`
- UI desk principale
- toolbox opérateur
- panneaux lisibles
- Coinglass séparé

### Debian écran réseau
- extension d’affichage future
- réseau / support visuel auxiliaire

---

## Conclusion
Le mapping cible est cohérent, mais l’indexation suggère qu’avant toute extension d’écran ou ajout d’API, il faut d’abord **stabiliser la surface opérateur Desk Pro** et clarifier quels modules doivent être visibles/lançables depuis MSI, tout en gardant `admin-trading` comme socle opérationnel réel.
