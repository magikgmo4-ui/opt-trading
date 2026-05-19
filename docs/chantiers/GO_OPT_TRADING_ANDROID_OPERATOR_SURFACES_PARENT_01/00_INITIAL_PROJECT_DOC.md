# GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_PARENT_01 — Android Operator Surfaces Parent

## 1_MASTER_TARGET
Construire une surface opérateur Android robuste pour piloter l'infrastructure opt-trading sans transformer Android en runtime principal.

Le produit fini attendu est un cockpit mobile/IDE-support permettant:
- boutons opérateur sûrs;
- SSH vers machines;
- reprise tmux;
- checks santé;
- logs;
- notifications;
- documentation de debug;
- bundle IDE exécutable par Cursor/OpenCode/OpenClaw.

## 2_INITIAL_PROJECT_DOC
Document initial figé du chantier parent.

Ce chantier formalise les surfaces Android utiles pour l'environnement opt-trading:
- Termux + OpenSSH;
- Tasker + Termux:Tasker;
- MacroDroid;
- Unified Remote;
- Stream Deck Mobile / Web UI;
- cockpit LocalCMS ou page opérateur légère;
- scripts versionnés et garde-fous.

## 3_INITIAL_NEED
L'utilisateur veut approfondir les alternatives à Unified Remote et créer un chantier parent avec toute la documentation, le plan complet, les surfaces attendues, le produit fini à livrer, et un bundle ZIP utilisable dans l'IDE.

Demandes complémentaires:
- ajouter une documentation support/debug/tuto;
- orienter le bundle vers les produits à utiliser dans l'IDE.

## 4_MASTER_PROJECT_PLAN
1. Définir les produits retenus et leur rôle.
2. Séparer surface tactile, automation Android, exécution SSH, persistance tmux et cockpit visuel.
3. Définir V1 non destructive: boutons, health, logs, tmux attach.
4. Définir V2 automation: triggers, notifications, profils horaires.
5. Définir V3 cockpit: Stream Deck/Web UI/LocalCMS.
6. Ajouter support debug IDE: tests, diagnostics, commandes paste-safe, erreurs connues.
7. Préparer les child GO d'implémentation.

## 6_FINAL_TARGET
Produit fini attendu: `ANDROID_OPERATOR_COCKPIT_V1`.

Livrables V1:
- tablette Android utilisable comme console opérateur;
- Termux configuré;
- scripts SSH paste-safe;
- Tasker ou MacroDroid capable de déclencher les scripts;
- Unified Remote ou Stream Deck utilisé uniquement pour raccourcis/UI;
- aucun bouton destructif sans confirmation;
- documentation support IDE.

## 7_CANONICAL_STATE
Android reste console opérateur.
tmux reste couche persistante.
db-layer reste ancre d'orchestration.
Les machines restent responsables de l'exécution réelle.
Les boutons Android appellent des scripts versionnés, pas des commandes critiques improvisées.

## 12_INVARIANTS
- Pas de secret dans les docs.
- Pas de commande destructive directe depuis bouton tactile.
- Pas de runtime trading sur Android.
- Pas de dépendance critique à Unified Remote.
- Scripts critiques versionnés.
- Sorties de health check visibles avant action de restart.
- Toute action WRITE/RESTART doit être séparée des actions READ/OBSERVE.

## 17_RESUME_POINT
Reprendre par `10_PRODUCT_SELECTION.md`, puis ouvrir le child GO V1 minimal:
`GO_OPT_TRADING_ANDROID_OPERATOR_SURFACES_CHILD_TERMUX_TASKER_V1_01`.
