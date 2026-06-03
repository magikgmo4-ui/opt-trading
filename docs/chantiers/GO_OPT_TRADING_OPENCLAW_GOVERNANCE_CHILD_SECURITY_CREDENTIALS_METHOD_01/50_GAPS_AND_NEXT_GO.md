# 50_GAPS_AND_NEXT_GO

## Gaps identifiés — classés par priorité

### P1 — Telegram groupAllowFrom vide (impact immédiat)

| Champ | Valeur |
|-------|--------|
| Gap | `channels.telegram.groupAllowFrom` absent dans `openclaw.json` |
| Impact | Messages de groupe droppés silencieusement |
| Fix | `openclaw configure set channels.telegram.groupAllowFrom [...]` |
| Prerequis | Lire CHAT_IDs depuis `.env`, ne pas committer |
| Prochain GO | `GO_OPT_TRADING_OPENCLAW_TELEGRAM_GROUPALLOWFROM_FIX_01` ou action directe |

---

### P2 — `/etc/opt-trading/env.d/roles/` non créé

| Champ | Valeur |
|-------|--------|
| Gap | Pattern système documenté mais répertoire inexistant |
| Impact | Les rôles env vivent dans `configs/env/roles/` (repo) plutôt que `/etc/` (système) |
| Fix | Créer `/etc/opt-trading/env.d/roles/`, déplacer les fichiers réels |
| Prochain GO | `GO_OPT_TRADING_ENV_ROLES_SYSTEM_MIGRATION_01` |

---

### P3 — Bitget scope à vérifier

| Champ | Valeur |
|-------|--------|
| Gap | Le scope API `readonly_main` doit être confirmé en lecture seule côté Bitget |
| Impact | Si mal configuré : risque de write accidentel |
| Fix | Vérifier les permissions sur la console Bitget |
| Prochain GO | Audit exchange credentials |

---

### P4 — Rotation des credentials non documentée

| Champ | Valeur |
|-------|--------|
| Gap | Aucune procédure de rotation pour TELEGRAM_BOT_TOKEN, TV_WEBHOOK_KEY, Bitget keys |
| Impact | Pas de plan de réponse à incident |
| Fix | Documenter une procédure de rotation par service |
| Prochain GO | Runbook rotation credentials |

---

### P5 — ClickUp non intégré

| Champ | Valeur |
|-------|--------|
| Gap | Aucune preuve d'intégration ClickUp dans le repo |
| Impact | Si voulu, toute l'intégration est à créer |
| Fix | Définir le besoin, créer le module |
| Prochain GO | `GO_OPT_TRADING_CLICKUP_INTEGRATION_01` si décidé |

---

### P6 — `modules/auth/secrets.py` non systématiquement utilisé

| Champ | Valeur |
|-------|--------|
| Gap | Certains modules lisent `os.environ.get()` directement sans passer par `secrets.py` |
| Impact | Pas de centralisation des erreurs de secrets manquants |
| Fix | Migrer progressivement vers `require_secret()` / `get_secret()` |
| Prochain GO | Refactor progressif, non urgent |

---

## Tableau récapitulatif

| # | Gap | Priorité | Bloquant | Next GO suggéré |
|---|-----|----------|----------|-----------------|
| 1 | groupAllowFrom vide | P1 | Non (DM OK) | Fix direct ou GO dédié |
| 2 | env.d/roles/ système absent | P2 | Non | Migration future |
| 3 | Bitget scope non vérifié | P3 | Non | Audit exchange |
| 4 | Rotation credentials | P4 | Non | Runbook |
| 5 | ClickUp absent | P5 | Non | Décision produit requise |
| 6 | secrets.py non systématique | P6 | Non | Refactor progressif |

---

## Prochains GOs suggérés

```
GO_OPT_TRADING_OPENCLAW_TELEGRAM_GROUPALLOWFROM_FIX_01
  → Fix groupAllowFrom dans openclaw.json
  → Aligner avec les TELEGRAM_CHAT_ID_* du .env multi-canal
  → Smoke test Telegram groupe après fix

GO_OPT_TRADING_ENV_ROLES_SYSTEM_MIGRATION_01
  → Créer /etc/opt-trading/env.d/roles/
  → Documenter la procédure de déploiement système

GO_OPT_TRADING_EXCHANGE_CREDENTIALS_AUDIT_01
  → Auditer scope Bitget readonly_main
  → Documenter procédure de rotation

GO_OPT_TRADING_CLICKUP_INTEGRATION_01  (si décidé)
  → Intégration ClickUp depuis zéro
```
