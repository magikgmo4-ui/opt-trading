# INVENTAIRE TRANSVERSAL — KANBAN PM (ARCHIVE-FIRST)

Date : 2026-03-20

## 1. RÔLE
Ce fichier sert de **kanban transversal d’inventaire** et de **plan opérationnel** pour l’ensemble du périmètre visible dans l’archive fournie.

Méthode retenue :
- **source de vérité structurelle** = archive sandbox fournie par l’utilisateur ;
- **limite assumée** = l’archive ne prouve pas à elle seule l’état exact des commits / ahead-behind ;
- **usage GitHub complémentaire** = utile seulement pour l’état des refs si nécessaire, pas pour dire ce qu’on a dans le bundle.

Règle :
- ce fichier classe ce qui est **présent**, **intégré**, **séparé**, **documenté comme runtime**, ou **absent du bundle** ;
- il ne prétend pas convertir automatiquement chaque périmètre en repo Git distinct.

## 1B. SYNTHÈSE OPÉRATIONNELLE

| Bloc | Type réel | Support principal | État | Nature | Réouverture | Suite |
|---|---|---|---|---|---|---|
| opt-trading / sot-mainline | repo / branche pivot | archive + audit | ÉTABLI / CANONIQUE / ACTIVE | pivot produit + ops + doc | non | conserver comme centre de pilotage |
| opt-trading / autres branches auditées | repo / branches dérivées | archive + audit | ÉTABLI / CLASSÉ | historique, absorption, archives | selon branche | suivre le kanban PM d’audit |
| student | sous-périmètre intégré | `opt-trading/student/` + docs + scripts | ÉTABLI / INTÉGRÉ | surface opérateur / module structuré | oui, si chantier student repris | traiter comme sous-projet interne à opt-trading |
| db-layer | machine / cible infra | docs, runbooks, snapshots, matrices | ÉTABLI / DOCUMENTÉ | cible d’exploitation / infra | oui, si mission infra | traiter comme runtime/machine, pas comme repo |
| admin-trading | machine / cible infra | docs, runbooks, snapshots, matrices | ÉTABLI / DOCUMENTÉ | hub opératoire principal | oui, si mission infra | garder comme hub runtime |
| cursor-ai | machine / surface utilisateur | docs, snapshots, mappings | ÉTABLI / DOCUMENTÉ | surface Windows / usage opérateur | oui, si mission UI / workflow | traiter comme machine, pas comme repo |
| api collector | module présent | `modules/derivatives_collector` et surfaces liées si présentes | ÉTABLI / PRÉSENT | collecte de données / collector | oui, si chantier collecte repris | qualifier le module avant extension |
| openclaw | périmètre externe au bundle | hors archive actuelle | HORS BUNDLE / À CADRER | chantier séparé / runtime externe | oui | ne pas l’inventer dans l’inventaire structurel du bundle |
| localcms | repo séparé | archive dédiée locale + branches dédiées | ÉTABLI / SÉPARÉ | CMS / outil distinct | oui, si chantier CMS repris | piloter à part de opt-trading |
| Magikgmo | repo historique | archive / repo séparé | HISTORIQUE / SÉPARÉ | héritage ancien | non, sauf besoin historique | mémoire uniquement |
| hf_trading | repo visible, non qualifié dans le bundle | GitHub seulement, bundle non probant ici | À QUALIFIER | repo séparé potentiel | oui | vérifier contenu réel avant pilotage |
| algo_hf | repo visible, non qualifié dans le bundle | GitHub seulement, bundle non probant ici | À QUALIFIER | repo séparé potentiel | oui | vérifier contenu réel avant pilotage |

## 2. CE QU’ON A RÉELLEMENT DANS LE BUNDLE

### A. Périmètre pivot prouvé
- un snapshot riche de `opt-trading`, avec `sot-mainline` comme surface la plus complète et la plus canonique ;
- plusieurs snapshots de branches `opt-trading` déjà auditées ;
- deux snapshots `localcms` ;
- un snapshot `Magikgmo-main`.

### B. Sous-périmètres visibles à l’intérieur de `opt-trading`
- `student/` comme surface structurée avec docs, bin, config et logique opérateur ;
- `modules/` avec plusieurs modules réels, dont au minimum les modules déjà documentés par la passe d’audit ;
- surfaces documentaires fortes : `docs/`, `docs/ot/`, `docs/master_pack/`, `registry/`, runbooks, kanban, closings, reports.

### C. Cibles runtime documentées
- `admin-trading`
- `student`
- `db-layer`
- `cursor-ai`

Ces cibles apparaissent dans la documentation, les matrices, les runbooks, les snapshots et la gouvernance. Elles doivent être lues comme **machines / surfaces runtime**, pas comme repos autonomes, sauf preuve contraire.

## 3. CE QU’ON N’A PAS À SURINTERPRÉTER
- `student` n’est pas, dans ce bundle, un repo Git séparé prouvé ;
- `db-layer` n’est pas un repo Git séparé prouvé ;
- `openclaw` n’est pas visible comme surface structurelle dans ce bundle ;
- `hf_trading` et `algo_hf` existent côté GitHub, mais ce fichier ne les classe pas comme périmètres actifs du bundle sans preuve archive-first.

## 4. INVENTAIRE PM PAR PÉRIMÈTRE

### 4.1 OPT-TRADING
**Statut PM**
- canon = `sot/mainline`
- branches secondaires = déjà classées dans l’audit de branches

**Contenu réel**
- produit principal
- ops / runbooks / wrappers / registry
- documentation canonique
- sous-périmètre `student`
- modules opérateurs et techniques

**Décision PM**
- continuer à piloter le projet principal depuis `sot/mainline`
- éviter de disperser la lecture sur `main` ou les `feat/*`

### 4.2 STUDENT
**Statut PM**
- sous-projet intégré à `opt-trading`
- pas traité comme repo séparé dans cette passe

**Contenu réel attendu dans le bundle**
- docs dédiées
- scripts / bin / config
- logique de façade opérateur
- consolidation/migration des surfaces legacy student

**Décision PM**
- traiter `student` comme un **chantier structuré interne** à `opt-trading`
- prévoir, plus tard si nécessaire, une fiche dédiée “student canonique” dans le repo principal

### 4.3 DB-LAYER
**Statut PM**
- cible infra / machine documentée
- pas un repo séparé prouvé par le bundle

**Contenu réel**
- runbooks, matrices, snapshots, mappings machines
- rôle d’exploitation dans le système multi-machine

**Décision PM**
- traiter `db-layer` comme surface runtime
- ne pas le mélanger avec la hiérarchie des branches Git

### 4.4 OPENCLAW
**Statut PM**
- hors bundle pour cette passe

**Décision PM**
- chantier séparé
- à réintégrer dans le pilotage uniquement avec un bundle ou repo canonique dédié

### 4.5 API COLLECTOR
**Statut PM**
- module présent dans le périmètre `opt-trading`

**Décision PM**
- le classer comme **module / sous-système**, pas comme repo séparé, tant que le support canonique reste dans `opt-trading`
- prochaine étape utile : fiche module dédiée si le chantier collector reprend

### 4.6 LOCALCMS
**Statut PM**
- projet séparé
- socle + surcouche locale déjà classés

**Décision PM**
- maintenir un pilotage séparé
- ne pas le dissoudre dans `opt-trading`

### 4.7 MAGIKGMO
**Statut PM**
- historique séparé

**Décision PM**
- mémoire seulement
- pas de pilotage actif

### 4.8 HF_TRADING / ALGO_HF
**Statut PM**
- visibles côté GitHub
- non prouvés comme périmètres actifs du bundle dans cette passe

**Décision PM**
- laisser en état **À QUALIFIER**
- ne pas les intégrer au plan d’exécution tant qu’un contenu réel n’est pas audité

## 5. KANBAN SYNTHÉTIQUE

| Périmètre | Statut | Support canonique retenu | Action PM |
|---|---|---|---|
| opt-trading | CANONIQUE / ACTIF | `sot/mainline` | piloter depuis cette branche |
| student | INTÉGRÉ / À STRUCTURER | sous-arbre `opt-trading` | documenter comme sous-projet interne |
| db-layer | DOCUMENTÉ / RUNTIME | docs + runbooks + snapshots | traiter comme machine/cible infra |
| admin-trading | DOCUMENTÉ / HUB | docs + runbooks + snapshots | garder comme hub opératoire |
| cursor-ai | DOCUMENTÉ / SURFACE USER | docs + snapshots | garder comme surface opérateur |
| api collector | PRÉSENT / MODULE | module dans `opt-trading` | qualifier avant extension |
| openclaw | HORS BUNDLE | support séparé requis | sortir du plan actuel |
| localcms | SÉPARÉ / ACTIF | repo + branches CMS | pilotage distinct |
| Magikgmo | HISTORIQUE | repo historique | mémoire seulement |
| hf_trading | À QUALIFIER | repo visible hors bundle | audit dédié si besoin |
| algo_hf | À QUALIFIER | repo visible hors bundle | audit dédié si besoin |

## 6. PLAN OPÉRATIONNEL

### Phase 1 — Geler la topologie canonique
1. garder `opt-trading / sot/mainline` comme pivot principal ;
2. considérer `student` comme sous-périmètre de `opt-trading` ;
3. considérer `db-layer`, `admin-trading`, `cursor-ai` comme surfaces runtime documentées ;
4. maintenir `localcms` hors du canon `opt-trading`.

### Phase 2 — Réduire la confusion des supports
1. ne plus mélanger branches Git, machines et modules dans la même taxonomie ;
2. utiliser quatre catégories opposables :
   - repo/branche,
   - sous-projet intégré,
   - module,
   - machine/runtime.

### Phase 3 — Formaliser les trous utiles
1. produire une fiche dédiée pour `student` si ce chantier repart ;
2. produire une fiche dédiée pour `api collector` si le collector repart ;
3. ne réintroduire `openclaw` qu’avec son support canonique ;
4. qualifier `hf_trading` et `algo_hf` uniquement si on ouvre réellement ces repos.

### Phase 4 — Ordre opérationnel conseillé
1. `opt-trading` (canon)
2. `student` (sous-projet interne)
3. `api collector` (module interne)
4. `localcms` (projet séparé)
5. `openclaw` (hors bundle, chantier séparé)
6. `hf_trading` / `algo_hf` (si et seulement si besoin explicite)

## 7. CE QUI EST PRÉVU CONCRÈTEMENT
- stabiliser la taxonomie de ce qu’on a ;
- éviter les faux repos ou faux canons ;
- piloter `opt-trading` depuis `sot/mainline` ;
- traiter `student` et `api collector` comme surfaces internes ;
- traiter `db-layer` comme runtime ;
- garder `localcms` séparé ;
- sortir `openclaw` du périmètre actif tant que son support canonique n’est pas rouvert.

## 8. POINT DE REPRISE
- `GO_CROSS_PROJECT_ARCHIVE_FIRST_PM_01`
