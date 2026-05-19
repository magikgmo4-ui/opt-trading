# OT-OPS-02 — MATRICE DIFF & DÉCISION

## 1. COMPARAISON TECHNIQUE
| Variante | Spécificité | Résultat Runtime | Statut Final |
| :--- | :--- | :--- | :--- |
| `v2` (avant) | Utilise `sudo` | FAIL (TTY/Permission) | PATCHED (écrasé) |
| `fix1` | `ssh -t sudo` | FAIL (Inutile) | OBSOLETE |
| `fix2` | `ssh -tt sudo` | FAIL (Inutile) | OBSOLETE |
| `fix3` | Pas de `sudo` | PASS | MERGED & DEPRECATED |

## 2. DÉCISIONS
- **v2** : PROMOTE -> ACTIVE
- **fix3** : DEPRECATE -> ARCHIVE_CANDIDATE
- **fix1/fix2** : DEPRECATE -> DELETE_CANDIDATE (Prochaine passe)

## 3. ROLLBACK
Un backup de l'ancien `v2` existe dans `_archive/workflow_post_change_v2_broken_backup`.
Le dossier `fix3` est intact pour référence.
