# 00_CADRAGE — GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01

## Identité

| Champ | Valeur |
|-------|--------|
| GO_ID | GO_OPT_TRADING_OPENCLAW_GOVERNANCE_CHILD_SECURITY_CREDENTIALS_METHOD_01 |
| Parent | GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01 |
| Surface | OPENCLAW / GOVERNANCE / INTEGRATIONS |
| Branche | go/GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01 |
| Date | 2026-06-03 |
| Statut | IN_PROGRESS |

## Contexte

Suite directe du check dispatcher + gateway health :
- Dispatcher PASS — 16/16 tests, dry-run fix appliqué
- Gateway RUNNING — port 18789, health OK, Telegram connecté
- Warning actif : `channels.telegram.groupPolicy=allowlist` avec `groupAllowFrom` vide

Ce GO documente l'état réel des credentials et intégrations externes dans opt-trading + openclaw,
produit la méthode canonique de gestion sécurisée, et prépare les prochains GO d'action.

## Périmètre

**In scope :**
- Inventaire de toutes les surfaces credentials (sans exposer les valeurs)
- Méthode canonique de gestion des secrets
- Inventaire des intégrations externes actives
- Warning Telegram groupPolicy + remédiation documentée

**Out of scope :**
- Modification des credentials live
- Rotation de secrets
- Déploiement de nouvelles intégrations

## Contraintes

- Aucun secret ne doit apparaître dans ce dossier ni dans le diff git
- Aucune modification de fichiers d'index globaux
- Aucun WRITE_GATED sans --gate-approved explicite
- Lecture et inventaire uniquement

## Livrables

```
00_CADRAGE.md                          (ce fichier)
10_CURRENT_CREDENTIALS_INVENTORY.md   (surfaces + méthodes actuelles)
20_SECURITY_CANONICAL_CREDENTIALS_METHOD.md  (méthode cible)
30_EXTERNAL_INTEGRATIONS_ACTIVE_INVENTORY.md (intégrations + statut)
40_TELEGRAM_GROUP_POLICY_AND_ALLOWLIST.md    (fix groupAllowFrom)
50_GAPS_AND_NEXT_GO.md                (gaps restants + prochains GO)
90_SESSION_HANDOFF.md                 (reprise session)
```
