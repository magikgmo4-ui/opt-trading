---
doc_id: OPT_TRADING_STATUS_WORKFLOW_POST_CHANGE_CANONIQUE
doc_type: family_status
repo: opt-trading
project: opt-trading
module: workflow_post_change_v2
go_id:
status: validated
lifecycle_stage: consolidation
topic_keys:
  - opt-trading
  - status
  - workflow_post_change
  - module_family
  - runtime
search_tags:
  - surface:module_family
  - doc_role:carte
surface: module_family
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Section 6. Reprise"
updated_at: 2026-04-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03.md
---

# WORKFLOW POST-CHANGE (CANONIQUE)

**Statut :** ACTIVE / PATCHED (2026-03-12)
**Module Cible :** `modules/workflow_post_change_v2`
**Script Métier :** `scripts/post_change.sh`

## Role documentaire

- role_actuel: fiche courte de statut de famille / patch pour `workflow_post_change_v2`
- role_cible: fiche annexe de consolidation de lignee, non souveraine
- souverainete: ne remplace ni la decision de consolidation, ni les preuves runtime, ni une doctrine transverse
- lecture_de_reprise: lire d'abord `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`, puis recroiser `MATRICE_GOUVERNANTE_V2.md` et la decision de consolidation locale avant d'utiliser cette fiche pour retrouver la maintenance et la validation runtime utiles

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

## 6. Reprise
- relire `docs/governance/GO_OPT_TRADING_WORKFLOW_POST_CHANGE_CONSOLIDATION_03.md`
- verifier que `modules/workflow_post_change_v2` reste l'unique surface active
- revalider le deploiement runtime avant toute extension ou cleanup des `fix*`
