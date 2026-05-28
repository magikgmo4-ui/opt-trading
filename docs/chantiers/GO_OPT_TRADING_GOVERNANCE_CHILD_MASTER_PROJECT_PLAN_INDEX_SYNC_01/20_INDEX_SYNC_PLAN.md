# 20_INDEX_SYNC_PLAN

## Périmètre initial

| Fichier | Action initiale | Statut |
|---|---|---|
| `docs/index/GO_INDEX.md` | Aucune modification — déjà à jour | ✅ inchangé |
| `docs/index/ACTIVE_STREAMS.md` | Aucune modification — déjà à jour | ✅ inchangé |
| `docs/index/NEXT_GO_CANDIDATES.md` | Update `updated_at` + enfants Android | ⛔ différé — lock overlap avec 9 autres GO |
| `docs/index/REPRISE.md` | Update `updated_at` + next action | ⛔ différé — lock overlap avec 9 autres GO |
| `docs/index/GO_CLOSED_INDEX.md` | Hors scope | ✅ |
| `docs/index/BRANCH_STATE.md` | Hors scope | ✅ |

## Décision

Les index `NEXT_GO_CANDIDATES.md` et `REPRISE.md` sont déjà revendiqués par 9 autres GO
dans leurs `FILE_SCOPE.txt`. La gate `no-lock-overlap` bloque leur modification dans ce GO.

**Correction** : ce GO livre l'audit complet + le constat de ce qui devrait être modifié.
Les modifications réelles des index sont différées vers un GO dédié avec libération
préalable des locks ou coordination inter-GO.

## Modifications réelles

- Chantier : 6 fichiers + FILE_SCOPE.txt
- Bundle : TARGETS.md + target_card.json
- Index : audio seu elementum — consultés, audités, documentés, non modifiés
