# 07_target_structure.md

## Vision cible
La structure cible ne vise pas à recréer le système. Elle vise à rendre **l’existant compréhensible, lançable et exploitable** avant toute extension visuelle ou fonctionnelle.

---

## 1) Principe directeur
Avant d’ajouter de nouvelles sources de données ou de nouveaux écrans, il faut :
- une surface opérateur claire
- une séparation nette entre backend réel et façade UI
- une nomenclature cohérente
- des points de lancement standardisés
- des vérifications simples (`sanity`) pour chaque brique importante

---

## 2) Répartition cible par machine
### `admin-trading`
Doit rester le **socle backend réel** :
- webhook / perf / vision / ingest / journal / logique serveur locale
- repo canonique de travail
- services et timers critiques
- maintenance / logs / diagnostic

### `db-layer` (MSI)
Doit devenir la **façade desk opérateur** :
- dashboard et vue desk
- toolbox lisible
- commandes user-friendly
- visualisation consolidée
- écran 2 dédié Coinglass

### `cursor-ai` (Dell)
Doit rester le **poste de pilotage/dev** :
- Trae / Cursor
- ChatGPT
- revue / prompts / coordination / git ciblé

### `student`
Doit rester une **surface spécialisée séparée**, stable, sans mélange avec la refonte desk globale.

### Debian écran réseau futur
Doit être traité comme **extension d’affichage**, pas comme nouveau centre logique improvisé.

---

## 3) Surface opérateur cible
### Ce que l’opérateur doit avoir
- un **menu principal desk**
- un **toolbox principal** cohérent
- un accès clair aux modules cœur utiles
- des sorties visibles dans le terminal
- des logs identifiables
- des sanity checks simples

### Modules cœur à exposer proprement
- `desk_pro_dashboard`
- `desk_pro_orchestrator`
- `desk_pro_runner`
- `derivatives_collector`
- `derivatives_analyzer`
- `probability_engine`
- `decision_engine`
- `risk_engine`
- `position_engine`
- `portfolio_engine`
- `journal_engine`
- `market_scanner`
- `opportunity_ranker`
- `liquidation_analyzer`

### Règle de packaging
Chaque module opérateur important devrait idéalement avoir :
- `cmd-<module>`
- `menu-<module>`
- `sanity-<module>`
- nommage cohérent avec le module réel
- README ou quick reference exploitable

---

## 4) Surface dev cible
La surface dev peut rester plus brute, mais doit être clairement distinguée de la surface opérateur. Elle inclut notamment :
- modules historiques
- correctifs / variantes `fix*`
- outils d’installation / ownership / hygiene
- scripts réseau et infra
- prompts et workflow AI

---

## 5) Surface maintenance cible
Doivent être identifiés comme maintenance :
- wrappers et menus de diagnostic
- hygiene repo
- ownership / artifacts locaux
- réseau / shared / mounts
- services systemd / timers / logs / relances

---

## 6) Règles de nommage cible
### Objectif
Réduire les ambiguïtés entre :
- `desk-pro` vs `desk_pro`
- wrappers historiques vs wrappers canonisés
- modules présents mais non exposés

### Règle souhaitée
- choisir une convention canonique par module
- maintenir éventuellement quelques aliases temporaires si nécessaire
- documenter les alias historiques, puis converger progressivement

---

## 7) Règle d’évolution
On ne passe à la phase suivante (écran réseau / reprise API large) qu’une fois :
- la surface opérateur principale clarifiée
- les wrappers critiques manquants identifiés et traités
- le mapping machines / écrans stabilisé
- la séparation opérateur / dev / maintenance rendue lisible

---

## Conclusion
La structure cible n’est pas un grand refactor. C’est une **rationalisation de l’existant** pour rendre le desk réellement exploitable, compréhensible et extensible sans chaos.
