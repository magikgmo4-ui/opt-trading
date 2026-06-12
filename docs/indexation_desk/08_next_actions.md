# 08_next_actions.md

## Next actions ordonnées

### Action 1 — Compléter l’inventaire analytique
Remplir proprement les fichiers d’indexation à partir du raw log :
- `01_inventory_modules.md`
- `02_inventory_menus.md`
- `03_inventory_wrappers.md`
- `04_inventory_logs_timers.md`

**But** : passer d’une collecte brute à une lecture exploitable.

---

### Action 2 — Construire la liste des modules cœur réellement opérateur
Dresser une shortlist “desk cœur” à exposer proprement, au minimum :
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

**But** : figer la vraie surface fonctionnelle à standardiser.

---

### Action 3 — Audit ciblé wrappers manquants / wrappers incohérents
Comparer pour chaque module cœur :
- scripts standards présents ?
- wrappers globaux présents ?
- nommage cohérent ?
- alias historiques à conserver temporairement ?

**Livrable attendu** : une table “module -> cmd/menu/sanity -> wrapper global oui/non -> action requise”.

---

### Action 4 — Séparer opérateur / dev / maintenance
Classifier l’inventaire par usage réel :
- opérateur
- dev
- maintenance/admin

**But** : éviter que MSI devienne un mélange confus d’outils techniques et d’outils desk.

---

### Action 5 — Stabiliser la façade MSI
À partir de l’inventaire, définir la surface MSI cible :
- écran 1 : desk / dashboard / toolbox / commandes user-friendly
- écran 2 : Coinglass

**But** : préparer une façade claire avant tout ajout réseau.

---

### Action 6 — Définir le rôle exact du futur écran réseau Debian
Décider ce que cet écran affichera réellement :
- panneau réseau ?
- support visuel d’état ?
- extension simple du desk ?

**But** : ne pas construire une extension visuelle sans fonction précise.

---

### Action 7 — Reporter l’intégration API large après rationalisation
Alternative.me / Bitget / autres intégrations doivent venir **après** :
- clarification de la surface opérateur
- mapping machines / écrans stabilisé
- wrappers et nomenclature remis au propre sur les briques critiques

---

## Premier chantier recommandé après l’indexation
### Standardisation de la surface opérateur Desk Pro
C’est le chantier le plus rentable maintenant.

#### Focus initial
- wrappers globaux manquants
- cohérence de nommage
- exposition homogène des modules cœur
- lisibilité terminal + logs + sanity

#### Pourquoi maintenant
Parce que l’inventaire montre que la puissance fonctionnelle existe déjà, mais que l’opérabilité unifiée reste incomplète.

---

## Commit recommandé
Pas immédiatement après le raw log seul.

Faire d’abord :
1. préremplissage analytique des fichiers d’indexation
2. revue rapide de cohérence
3. commit documentaire propre de la phase d’indexation

---

## Proposition de titre pour le prochain micro-chantier
**Standardisation surface opérateur Desk Pro (wrappers, nommage, exposition modules cœur)**

## RISKS

- À qualifier.
