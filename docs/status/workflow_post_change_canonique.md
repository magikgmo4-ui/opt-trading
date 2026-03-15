# WORKFLOW POST-CHANGE (CANONIQUE)

**Statut :** ACTIVE / PATCHED (2026-03-12)
**Module Cible :** `modules/workflow_post_change_v2`
**Script Métier :** `scripts/post_change.sh`

## 1. Contexte
Ce module gère le hook post-modification pour enregistrer les changements, mettre à jour le journal, et notifier l'utilisateur student (DeepSeek).

## 2. Historique & Patch
- **v2 (Original)** : Contenait une commande `sudo` incompatible avec l'environnement student/admin actuel.
- **fix1 / fix2** : Tentatives de contournement `ssh -t` (Obsolètes).
- **fix3** : Suppression de `sudo`. Correctif validé.

**État Actuel :**
Le contenu de `fix3` a été fusionné dans `v2`.
`workflow_post_change_v2` est désormais la version canonique et fonctionnelle (sans sudo).

## 3. Points d'Entrée
- **Direct (Script)** : `/opt/trading/modules/workflow_post_change_v2/scripts/post_change.sh`
- **Wrapper (Générique)** : `cmd-workflow_post_change_v2` (Fournit info/readme/ls, pas l'exécution du hook).
- **Orchestrateur** : Appelle le script directement.

## 4. Maintenance
- **Ne pas utiliser** : `workflow_post_change_v2_fix*` (Dépréciés).
  - `fix3` : Merged (Code intégré dans v2).
  - `fix1/fix2` : Obsolete (Code inutile/cassé).
- **Ne pas supprimer** : Les dossiers `fix*` sont conservés pour archive/rollback en cas de régression, mais ne doivent plus être appelés.

## 5. Validation Runtime
Le patch a été déployé physiquement sur `admin-trading` le 2026-03-12 (OT-OPS-02B).
La commande `grep` confirme l'absence de `sudo`.
