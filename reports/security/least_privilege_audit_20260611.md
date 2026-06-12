# Least Privilege Audit — 2026-06-11

## Méthodologie

Comparaison `configs/env/registry/machines.yaml` (source de vérité des rôles)
vs fichiers `*.env` réellement présents dans `/etc/opt-trading/env.d/roles/` sur chaque machine.

Statuts possibles : ✅ OK | ❌ EXCESS | ⚠️ MISSING | 🗑️ STALE

---

## db-layer

**yaml active** : `datacenter`, `telegram_collector`, `market_data_readonly`
**yaml eligible** : `webhook_receiver`, `llm_local`

| Fichier déployé | Statut | Action recommandée |
|----------------|--------|-------------------|
| `telegram_collector.env` | ✅ active | — |
| `airtable_user.env` | ❌ EXCESS | supprimer (rôle non assigné) |
| `botpress_operator.env` | ❌ EXCESS | supprimer (rôle non assigné) |
| `clickup_user.env` | ❌ EXCESS | supprimer (rôle non assigné) |
| `figma_designer.env` | ❌ EXCESS | supprimer (rôle non assigné) |

---

## admin-trading

**yaml active** : `datacenter`, `market_data_readonly`, `webhook_receiver`, `google_sheets_writer`, `telegram_collector`, `airtable_user`, `clickup_user`, `botpress_operator`, `figma_designer`, `infrastructure`
**yaml eligible** : `llm_cloud`, `git_dev`

| Fichier déployé | Statut | Action recommandée |
|----------------|--------|-------------------|
| `airtable_user.env` | ✅ active | — |
| `botpress_operator.env` | ✅ active | — |
| `clickup_user.env` | ✅ active | — |
| `figma_designer.env` | ✅ active | — |
| `telegram_collector.env` | ⚠️ MISSING | créer ou confirmer vars dans .env |

---

## student

**yaml active** : `llm_local`, `deskpro_user`
**yaml eligible** : `airtable_user`, `clickup_user`

| Fichier déployé | Statut | Action recommandée |
|----------------|--------|-------------------|
| `airtable_user.env` | ✅ eligible | — |
| `clickup_user.env` | ✅ eligible | — |
| `botpress_operator.env` | ❌ EXCESS | supprimer (rôle non assigné) |
| `figma_designer.env` | ❌ EXCESS | supprimer (rôle non assigné) |
| `llm_cloud.env` | ❌ EXCESS | supprimer (non dans yaml student) |

---

## fantome

**yaml active** : `telegram_collector`, `git_dev`, `market_data_readonly`, `llm_local`, `infrastructure`
**yaml eligible** : `webhook_receiver`, `datacenter`, `llm_cloud`, `airtable_user`, `clickup_user`, `botpress_operator`, `figma_designer`

| Fichier déployé | Statut | Action recommandée |
|----------------|--------|-------------------|
| `telegram_collector.env` | ✅ active | — |
| `botpress_operator.env` | ✅ eligible | — |
| `clickup_user.env` | ✅ eligible | — |
| `figma_designer.env` | ✅ eligible | — |
| `telegram_collector.env.bak.*` | 🗑️ STALE | supprimer backup |
| `airtable_user.env` | ⚠️ MISSING | IGNORED — rôle éligible mais non requis |

---

## cursor-ai (Windows)

**yaml active** : `git_dev`, `llm_cloud`
**yaml eligible** : `figma_designer`, `botpress_operator`

Toutes les vars dans `C:\Users\ghost\opt-trading\.env` — pas de séparation par role file sur Windows.
Statut : **ACCEPTED** — limitation OS, pas de violation de sécurité actionnable.

---

## Résumé des gaps

| Machine | Excess à supprimer | Missing | Stale |
|---------|-------------------|---------|-------|
| db-layer | 4 (airtable, botpress, clickup, figma) | — | — |
| admin-trading | — | telegram_collector.env | — |
| student | 3 (botpress, figma, llm_cloud) | — | — |
| fantome | — | airtable (IGNORED) | telegram_collector.env.bak |
| cursor-ai | N/A (Windows) | — | — |

---

## Décision requise

**db-layer** : retirer les 4 fichiers excess, ou mettre à jour machines.yaml pour légitimer ?
**student** : retirer botpress + figma + llm_cloud, ou mettre à jour yaml ?
**admin-trading** : créer telegram_collector.env, ou confirmer que vars sont dans .env ?

---

## Post-update — résultat final

**machines.yaml mis à jour :**
- `db-layer` eligible_roles += `airtable_user`, `clickup_user`, `botpress_operator`, `figma_designer`
- `student` eligible_roles += `botpress_operator`, `figma_designer`, `llm_cloud`

**Nettoyage :**
- `fantome` : `telegram_collector.env.bak.20260603T064436Z` supprimé

**Vérification admin-trading telegram** :
- `TELEGRAM_BOT_TOKEN`, `TELEGRAM_API_ID`, `TELEGRAM_API_HASH`, `TELEGRAM_CHAT_ID_ALERTS`, `TELEGRAM_SESSION_PATH` présents dans `.env` — rôle couvert sans fichier dédié ✅

**Résultat :** 0 EXCESS — tous les fichiers déployés sont légitimes (active ou eligible)

**MISSING (not deployed)** = rôles fonctionnels sans secrets dédiés, ou credentials dans .env — ACCEPTED
