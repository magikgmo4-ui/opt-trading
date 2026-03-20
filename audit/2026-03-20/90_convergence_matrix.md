# AUDIT INTER-REPOS — MATRICE DE CONVERGENCE

Date : 2026-03-20

## 1. RÔLE
Cette matrice sert à visualiser, en un seul endroit, la relation entre les branches auditées et le pivot canonique retenu.

Pivot de convergence retenu :
- `opt-trading / sot/mainline`

Règle de lecture :
- **converge vers** = la branche ne concurrence pas le pivot et doit être lue par rapport à lui ;
- **absorbé par** = la valeur technique principale est déjà intégrée dans le pivot ;
- **témoin de** = la branche reste utile surtout comme repère historique ;
- **archive de** = la branche conserve un périmètre spécialisé ou froid ;
- **hors convergence directe** = repo/périmètre séparé, non fusionné au pivot.

## 2. MATRICE

| Repo | Branche | Relation au pivot | Type de valeur restante | Risque de confusion | Action PM recommandée |
|---|---|---|---|---|---|
| opt-trading | `sot/mainline` | pivot canonique | opératoire + structurelle + documentaire | moyen | conserver comme source de vérité |
| opt-trading | `sot/build` | converge vers `sot/mainline` | témoin intermédiaire de consolidation | faible | conserver comme repère historique |
| opt-trading | `main` | converge vers `sot/mainline` | témoin historique avec résidus ciblés | moyen | ne rouvrir qu’en extraction manuelle ciblée |
| opt-trading | `fix/desk-ui-toolbox` | converge vers `sot/mainline` | archive spécialisée Desk Pro / UI | moyen | préserver, ne pas merger automatiquement |
| opt-trading | `feat/risk-engine` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `feat/execution-engine` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `feat/position-engine` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `feat/position-guard` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `feat/persistent-state` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `feat/engines-plugin` | absorbé par `sot/mainline` | historique architecturale | faible | documenter puis archiver logiquement |
| opt-trading | `antigravity/main` | converge vers `sot/mainline` sans concurrence | archive laboratoire / isolat expérimental | faible | conserver hors canon |
| opt-trading | `backup/main-before-filter` | converge vers `sot/mainline` sans concurrence | snapshot froid / restauration mémoire | très faible | conserver en archive froide |
| localcms | `feature/localcms-shared-explorer-cms-installer-v1` | hors convergence directe | socle fonctionnel CMS | faible | garder comme base produit du chantier CMS |
| localcms | `tools/localcms-dev-host` | hors convergence directe | surcouche d’hébergement local | moyen | traiter comme extension du socle CMS |
| Magikgmo | `main` | hors convergence directe | héritage historique absorbé par trajectoire `opt-trading` | faible | conserver pour mémoire seulement |

## 3. LECTURE PM

### A. Convergence forte vers le pivot
Branches qui ne portent plus de ligne concurrente crédible face à `sot/mainline` :
- `sot/build`
- `main`
- `fix/desk-ui-toolbox`
- toutes les `feat/*` auditées
- `antigravity/main`
- `backup/main-before-filter`

### B. Absorption technique complète
Branches dont le cœur technique a déjà été repris par le pivot :
- `feat/risk-engine`
- `feat/execution-engine`
- `feat/position-engine`
- `feat/position-guard`
- `feat/persistent-state`
- `feat/engines-plugin`

### C. Témoins et archives
Branches utiles surtout pour lecture historique, restitution d’intention ou audit :
- `sot/build`
- `main`
- `fix/desk-ui-toolbox`
- `antigravity/main`
- `backup/main-before-filter`
- `Magikgmo/main`

### D. Hors convergence directe mais actives dans leur propre périmètre
- `localcms / feature/localcms-shared-explorer-cms-installer-v1`
- `localcms / tools/localcms-dev-host`

## 4. RISQUES DE CONVERGENCE À ÉVITER
- rouvrir `main` comme si c’était une branche canonique vivante ;
- merger automatiquement `fix/desk-ui-toolbox` alors que son périmètre est spécialisé ;
- traiter `tools/localcms-dev-host` comme base produit autonome au lieu d’une surcouche ;
- confondre archive laboratoire (`antigravity/main`) et branche produit ;
- garder plusieurs sources de vérité en parallèle à `sot/mainline`.

## 5. CONCLUSION DE MATRICE
La convergence globale est nette :
- **un pivot canonique unique** : `opt-trading / sot/mainline`
- **un ensemble de branches absorbées ou historiques** côté `opt-trading`
- **un périmètre séparé CMS** avec une base produit claire et une surcouche locale
- **un héritage Magikgmo** sans rôle de pilotage actif

## 6. POINT DE REPRISE
- `GO_REPO_BRANCH_PM_DECISION_01`
