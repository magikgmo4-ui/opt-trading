# GO_OPT_TRADING_UI_LOCALCMS_CONSUMER_PARENT_01

## Classification

module durable — chantier parent de cadrage producer/consumer UI

## Rôle recommandé

Architecte d’intégration producer/consumer

---

## Besoin initial

Prévoir l’intégration progressive des UI de `opt-trading` dans `localcms` sans migrer le repo canonique, ni déplacer la logique métier, ni casser la séparation des responsabilités.

---

## Cible finale

Avoir une architecture claire où :

- `opt-trading` reste le **producer canonique**
- `localcms` agit comme **consumer UI**
- les UI consommables sont exposées via des contrats explicites
- la logique métier, le runtime et la gouvernance restent côté `opt-trading`
- chaque lot de bascule UI est traçable, réversible et documenté

---

## Source canonique

- Repo canonique : `opt-trading`
- Branche canonique de continuité : `sot/mainline`

---

## ETABLI

- Ce chantier ne vise **pas** une migration de repo.
- `localcms` est le **consumer**.
- `opt-trading` reste le **producer**.
- La migration visée concerne la **surface UI consommée**, pas le noyau produit.
- La logique métier critique, le runtime, les secrets et les services couplés machine ne doivent pas être déplacés dans `localcms`.

---

## Plan validé

### Axe 1 — Inventaire UI source

Inventorier les UI existantes dans `opt-trading` et les classer par rôle :
- viewer / read-only
- dashboard / reporting
- admin léger
- console opératoire
- UI couplée runtime

### Axe 2 — Matrice producer / consumer

Pour chaque UI, statuer :
- `producer-only`
- `consumer-compatible`
- `consumer-compatible with adapter`
- `excluded`

### Axe 3 — Contrats d’exposition

Définir le mode de consommation cible par UI :
- build exporté
- manifest + assets
- fragment HTML
- JSON de config / schéma UI
- API + renderer côté `localcms`
- proxy / embed / viewer

### Axe 4 — Lots d’adoption

Ordre par défaut :
1. viewers read-only
2. dashboards / reporting
3. admin léger non critique
4. consoles hybrides
5. exclusions explicites pour les UI fortement couplées runtime

### Axe 5 — Gouvernance

Documenter pour chaque lot :
- origine canonique
- contrat exposé
- dépendances runtime
- limites
- stratégie de rollback
- point de reprise

---

## Anti-cibles

Ne pas faire :
- fusion des repos
- duplication massive non gouvernée
- migration du runtime trading vers `localcms`
- réécriture globale des UI sans contrat figé
- déplacement de la logique métier hors `opt-trading`

---

## Gap restant

Il reste à produire :

1. l’inventaire réel des UI `opt-trading`
2. la matrice producer/consumer par UI
3. les premiers contrats d’exposition
4. la liste d’exclusion explicite
5. le premier lot pilote de consommation côté `localcms`

---

## GO suivants proposés

### GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01
Inventaire réel des UI de `opt-trading` et classification par famille.

### GO_OPT_TRADING_UI_LOCALCMS_MATRIX_01
Décision producer-only / consumer-compatible / adapter / excluded pour chaque UI.

### GO_OPT_TRADING_UI_LOCALCMS_CONTRACTS_01
Définition des contrats d’exposition cibles par UI ou famille d’UI.

### GO_OPT_TRADING_UI_LOCALCMS_PILOT_READONLY_01
Premier lot pilote sur une UI read-only ou dashboard faiblement couplé.

---

## TODO

- recenser les UI réelles dans `opt-trading`
- établir la matrice producer/consumer
- choisir le format de contrat cible par famille d’UI
- sélectionner un premier lot read-only
- documenter les exclusions runtime sensibles

---

## REPRISE

Point de reprise recommandé :
`GO_OPT_TRADING_UI_LOCALCMS_INVENTORY_01`

Séquence de reprise :
inventaire réel repo-first → matrice producer/consumer → contrats → lot pilote

---

## MEM_CANDIDATE

Règle projet potentielle :
pour les UI partagées entre `opt-trading` et `localcms`, `opt-trading` reste producer canonique et `localcms` reste consumer, sauf décision documentée contraire.

## RISKS

- À qualifier.
