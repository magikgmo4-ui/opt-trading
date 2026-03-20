# AUDIT INTER-REPOS — DÉCISION PM FINALE

Date : 2026-03-20

## 1. Objet
Cette page clôt la passe d’audit inter-repos et fixe la décision de pilotage issue des rapports, de la matrice de convergence et du kanban PM.

Périmètre audité :
- `opt-trading`
- `localcms`
- `Magikgmo`

## 2. Décision centrale

### Canon unique
Le canon de travail retenu pour la trajectoire `opt-trading` est :
- **`opt-trading / sot/mainline`**

Décision :
- le considérer comme source de vérité principale pour lecture, continuité, reprise et décisions PM sur `opt-trading`.

### Hiérarchie des branches `opt-trading`
Classement retenu :
1. `sot/mainline` = canonique
2. `sot/build` = témoin intermédiaire
3. `main` = témoin historique avec restes ciblés, non canonique
4. `fix/desk-ui-toolbox` = archive spécialisée
5. `feat/*` auditées = absorbées
6. `antigravity/main` = archive laboratoire
7. `backup/main-before-filter` = archive froide

### Périmètre `localcms`
Classement retenu :
- `feature/localcms-shared-explorer-cms-installer-v1` = socle fonctionnel
- `tools/localcms-dev-host` = surcouche d’hébergement local

Décision :
- ne pas traiter ces deux branches comme concurrentes ;
- lire `tools/...` comme extension locale du socle CMS.

### Périmètre `Magikgmo`
Classement retenu :
- `Magikgmo / main` = héritage historique

Décision :
- ne pas l’utiliser comme source active de pilotage courant.

## 3. Ce qui doit être conservé

### Pivot actif
- `opt-trading / sot/mainline`

### Mémoire utile
- `opt-trading / sot/build`
- `opt-trading / main`
- `fix/desk-ui-toolbox`
- `antigravity/main`
- `backup/main-before-filter`
- `Magikgmo / main`

### Base séparée de chantier
- `localcms / feature/localcms-shared-explorer-cms-installer-v1`
- `localcms / tools/localcms-dev-host`

## 4. Ce qui ne doit pas être fait
- ne pas rouvrir `main` comme si c’était la ligne canonique du projet ;
- ne pas merger automatiquement `fix/desk-ui-toolbox` ;
- ne pas réactiver les branches `feat/*` comme branches de développement vivantes ;
- ne pas confondre `tools/localcms-dev-host` avec une base produit autonome ;
- ne pas utiliser `Magikgmo/main` comme source de vérité active.

## 5. Actions PM retenues

| Priorité | Action | Décision |
|---|---|---|
| P0 | garder `sot/mainline` comme pivot canonique | retenu |
| P1 | conserver les rapports d’audit dans la branche `audit` | retenu |
| P1 | conserver le kanban PM et la matrice comme outils de reprise | retenu |
| P2 | ne réexaminer `main` qu’en cas de besoin explicite sur un artefact résiduel | retenu |
| P2 | garder `localcms` dans un pilotage séparé de `opt-trading` | retenu |
| P3 | archiver logiquement les branches absorbées dans la documentation PM | retenu |

## 6. Statut de clôture
La passe d’audit est considérée clôturée proprement au niveau PM parce que :
1. un plan d’audit a été posé,
2. des rapports individuels ont été produits,
3. un kanban PM a été établi,
4. une matrice de convergence a été établie,
5. une décision finale de pilotage est maintenant figée.

## 7. Point de reprise suivant
- **Point de reprise final** : `GO_REPO_BRANCH_PM_NEXT_ACTION_01`

Sens :
- soit intégrer les éléments d’audit restants si un trou est détecté,
- soit basculer vers une nouvelle mission à partir de ce classement,
- soit produire un pack de reprise pour une autre session.

## 8. Résumé exécutable
- canon `opt-trading` : `sot/mainline`
- `localcms` : socle produit + surcouche locale
- `Magikgmo` : historique seulement
- `feat/*` auditées : absorbées
- archives spécialisées : conservées mais non réactivées
