# AUDIT INTER-REPOS — KANBAN PM (ALIGNÉ SUR LA LOGIQUE `sot/mainline`)

Date : 2026-03-20

## 1. RÔLE
Ce fichier est le **kanban PM de synthèse** de la passe d’audit inter-repos.
Il reprend la logique de `sot/mainline` :
- vision synthétique, lisible d’un coup d’œil ;
- statut par brique / branche ;
- règle de réouverture ;
- suite logique / point de reprise.

Règle :
une branche n’est pas considérée **clôturée proprement** dans cette passe tant que :
1. le rapport individuel existe,
2. le classement PM est posé,
3. la suite logique est explicitée.

## 1B. SYNTHÈSE OPÉRATIONNELLE DU KANBAN

### Tableau de synthèse

| Bloc | Repo | Branche | État | Nature | Réouverture | Suite |
|---|---|---|---|---|---|---|
| Canon principal | opt-trading | `sot/mainline` | ÉTABLI / CANONIQUE / ACTIVE | source de vérité repo | non | conserver comme pivot de décision |
| Socle intermédiaire | opt-trading | `sot/build` | ÉTABLI / TÉMOIN INTERMÉDIAIRE | historique de consolidation | non | conserver comme repère historique |
| Ligne historique | opt-trading | `main` | HISTORIQUE / RÉSIDUEL | témoin historique | oui, si un artefact unique doit être extrait | revoir seulement les paquets résiduels documentés |
| Archive Desk Pro UI | opt-trading | `fix/desk-ui-toolbox` | ARCHIVE / SPÉCIALISÉE | branche spécialisée UI / Desk Pro | oui, si besoin UI précis réapparaît | préserver, ne pas merger automatiquement |
| Moteur de risque | opt-trading | `feat/risk-engine` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Moteur d’exécution | opt-trading | `feat/execution-engine` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Moteur de position | opt-trading | `feat/position-engine` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Garde de position | opt-trading | `feat/position-guard` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Persistance d’état | opt-trading | `feat/persistent-state` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Registry engines | opt-trading | `feat/engines-plugin` | CLOSE / ABSORBÉ | jalon technique | non | documenter puis archiver logiquement |
| Périmètre labo | opt-trading | `antigravity/main` | ARCHIVE / LABORATOIRE | isolat expérimental | oui, si chantier Antigravity relancé | conserver hors canon |
| Snapshot pré-filtrage | opt-trading | `backup/main-before-filter` | ARCHIVE / FROIDE | snapshot historique | non | conservation mémoire uniquement |
| Socle CMS | localcms | `feature/localcms-shared-explorer-cms-installer-v1` | ÉTABLI / FONCTIONNEL | socle produit | oui, si reprise active du chantier CMS | garder comme base fonctionnelle |
| Hôte de dev CMS | localcms | `tools/localcms-dev-host` | ÉTABLI / SURCOUCHE | hébergement / exécution locale | oui, si reprise packaging local | traiter comme surcouche du socle CMS |
| Héritage historique | Magikgmo | `main` | HISTORIQUE / ABSORBÉ | snapshot ancien | non | conserver pour mémoire, pas pour pilotage courant |

### Règle de maintenance de la synthèse
- cette synthèse est un **résumé vivant** ;
- elle doit être mise à jour si un nouveau rapport change :
  - le statut PM,
  - la nature d’une branche,
  - la règle de réouverture,
  - ou la suite logique ;
- elle **ne remplace pas** les rapports détaillés ;
- en cas de conflit, les **rapports individuels** priment.

## 2. ÉTAT — OPT-TRADING

### ÉTABLI
- `sot/mainline` est la branche canonique opérationnelle.
- `sot/build` reste un repère utile pour comprendre la montée en consolidation.
- les branches `feat/*` auditées n’ont pas de delta vivant au-dessus du canon actuel.

### CLOSE (ABSORBÉ)
- `feat/risk-engine`
- `feat/execution-engine`
- `feat/position-engine`
- `feat/position-guard`
- `feat/persistent-state`
- `feat/engines-plugin`

### HISTORIQUE / ARCHIVE
- `main` : historique avec artefacts résiduels documentés
- `fix/desk-ui-toolbox` : archive spécialisée
- `antigravity/main` : archive laboratoire
- `backup/main-before-filter` : archive froide

### À CONFIRMER
- aucune branche `opt-trading` auditée dans cette passe ne nécessite un merge automatique supplémentaire.
- seule une extraction manuelle ciblée depuis `main` pourrait encore être justifiée, **si** un besoin réel réapparaît.

## 3. ÉTAT — LOCALCMS

### ÉTABLI
- `feature/localcms-shared-explorer-cms-installer-v1` sert de **socle fonctionnel**.
- `tools/localcms-dev-host` sert de **surcouche d’hébergement local**.

### POINT PM
- ne pas confondre :
  - la base produit,
  - et la couche d’exécution locale / dev-host.

### À CONFIRMER
- choix canonique futur si le chantier CMS reprend :
  - soit garder `feature/...` comme base produit,
  - soit promouvoir une branche consolidée qui absorbe proprement la couche `tools/...`.

## 4. ÉTAT — MAGIKGMO

### ÉTABLI
- `Magikgmo/main` ne porte pas, dans cette passe, de valeur concurrente face à `opt-trading`.

### DÉCISION PM
- conserver comme héritage historique,
- ne pas l’utiliser comme source active de pilotage.

## 5. DÉCISION PM — CLASSEMENT FINAL

### CANONIQUE
- `opt-trading / sot/mainline`

### ÉTABLI / FONCTIONNEL
- `localcms / feature/localcms-shared-explorer-cms-installer-v1`
- `localcms / tools/localcms-dev-host`

### TÉMOINS / HISTORIQUES
- `opt-trading / sot/build`
- `opt-trading / main`
- `Magikgmo / main`

### ARCHIVES SPÉCIALISÉES
- `opt-trading / fix/desk-ui-toolbox`
- `opt-trading / antigravity/main`
- `opt-trading / backup/main-before-filter`

### ABSORBÉES / À CLOTURER LOGIQUEMENT
- `opt-trading / feat/risk-engine`
- `opt-trading / feat/execution-engine`
- `opt-trading / feat/position-engine`
- `opt-trading / feat/position-guard`
- `opt-trading / feat/persistent-state`
- `opt-trading / feat/engines-plugin`

## 6. ACTIONS RECOMMANDÉES (PM)

| Priorité | Action | Portée | But |
|---|---|---|---|
| P0 | conserver `sot/mainline` comme pivot canonique | opt-trading | éviter toute confusion de source de vérité |
| P1 | figer ce kanban comme tableau maître de lecture des branches | inter-repos | rendre le suivi lisible et stable |
| P1 | conserver les rapports de branches comme preuves détaillées | inter-repos | garder la traçabilité d’audit |
| P2 | ne rouvrir `main` que si un besoin concret vise un artefact résiduel | opt-trading | éviter les retours arrière inutiles |
| P2 | traiter `tools/localcms-dev-host` comme extension du socle CMS, pas comme canon séparé | localcms | clarifier le pilotage CMS |
| P3 | archiver logiquement les branches absorbées dans la doc PM | opt-trading | simplifier la lecture future |

## 7. POINT DE REPRISE SUIVANT
- **Point de reprise proposé** : `GO_REPO_BRANCH_PM_KANBAN_01`

But :
- reprendre depuis ce tableau,
- décider si ce kanban doit :
  1. rester hors repo comme livrable PM,
  2. être intégré dans la branche d’audit,
  3. ou être transformé en tableau canonique de suivi plus compact.

## 8. RÉSUMÉ EXÉCUTABLE
- canon actuel : `opt-trading / sot/mainline`
- CMS : `feature/...` = socle, `tools/...` = surcouche
- historique : `sot/build`, `main`, `Magikgmo/main`
- archives spécialisées : `fix/desk-ui-toolbox`, `antigravity/main`, `backup/main-before-filter`
- branches `feat/*` auditées : absorbées
