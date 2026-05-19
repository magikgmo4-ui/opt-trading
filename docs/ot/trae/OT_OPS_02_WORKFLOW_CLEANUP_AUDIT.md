# OT-OPS-02 — AUDIT DE CLEANUP WORKFLOW

## 1. CONTEXTE
Dette technique identifiée autour de `workflow_post_change_v2` (canonique cassé) et ses variantes `fix1`, `fix2`, `fix3` (candidats).

## 2. INVENTAIRE
- **v2** : Contenait un appel `sudo` incompatible avec l'env actuel.
- **fix1/fix2** : Tentaient des contournements `ssh -t` inutiles.
- **fix3** : Retirait simplement `sudo`, ce qui est la bonne solution.

## 3. ANALYSE D'USAGE
- `fix3` était référencé temporairement dans le registry.
- Aucune dépendance externe dure vers `fix1` ou `fix2` trouvée.

## 4. ACTION CHOISIE
**PATCH & DEPRECATE** (plutôt que DELETE).
- Le code de `fix3` a été promu dans `v2`.
- `v2` redevient la source de vérité active.
- Les dossiers variantes sont conservés pour archive/rollback mais marqués dépréciés.
