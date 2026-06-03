# 40_TELEGRAM_GROUP_POLICY_AND_ALLOWLIST

## Warning actif

```
channels.telegram.groupPolicy = allowlist
groupAllowFrom = (vide / absent)
allowFrom      = (vide / absent)
```

Rapporté par : `openclaw gateway health` et `openclaw gateway probe`

---

## Explication du mécanisme

OpenClaw gateway Telegram a deux modes de réception des messages :

| Mode | Comportement |
|------|-------------|
| `groupPolicy: open` | Accepte les messages de tous les groupes |
| `groupPolicy: allowlist` | N'accepte que les groupes dont l'ID est dans `groupAllowFrom` ou `allowFrom` |

Avec `groupPolicy: allowlist` et `groupAllowFrom: []` (ou absent) :
**tous les messages de groupe sont droppés silencieusement** — aucune erreur, aucun log visible côté expéditeur.

Les DM (`dmPolicy: pairing`) ne sont pas affectés par ce warning.

---

## Impact actuel

| Canal | Type | Impact |
|-------|------|--------|
| Messages directs (DM) | dm | Non affecté |
| Alertes canal pipeline | groupe | DROPPED si envoyé depuis groupe |
| Alertes canal ops | groupe | DROPPED si envoyé depuis groupe |
| Alertes canal push | groupe | DROPPED si envoyé depuis groupe |

**Si les TELEGRAM_CHAT_ID_* sont des groupes et non des canaux privés** → les messages ne passent pas.

---

## Méthode canonique de fix

### Option A — Passer en mode `open` (moins sécurisé)

```bash
sudo -u openclaw openclaw configure set channels.telegram.groupPolicy open
```

Impact : OpenClaw acceptera les messages de n'importe quel groupe. À utiliser uniquement si le bot est privé et que l'accès est contrôlé par Telegram lui-même.

### Option B — Renseigner `groupAllowFrom` (recommandé)

```bash
# Récupérer les chat_ids depuis .env (sans les afficher ici)
# Puis appliquer via openclaw configure

sudo -u openclaw openclaw configure set \
  channels.telegram.groupAllowFrom '["CHAT_ID_1","CHAT_ID_2","CHAT_ID_3"]'
```

Les valeurs à injecter proviennent des variables `.env` :
- `TELEGRAM_CHAT_ID`
- `TELEGRAM_CHAT_ID_PIPELINE`
- `TELEGRAM_CHAT_ID_OPS`
- `TELEGRAM_CHAT_ID_PUSH`

**Ne jamais écrire les chat_ids en clair dans un fichier versionné.**

### Procédure d'application sûre

```bash
# 1. Vérifier config actuelle
sudo -u openclaw openclaw configure status | grep telegram

# 2. Lire les chat_ids depuis .env (en mémoire, ne pas echo)
source /opt/trading/.env 2>/dev/null

# 3. Appliquer
sudo -u openclaw openclaw configure set \
  channels.telegram.groupAllowFrom "[\"$TELEGRAM_CHAT_ID\",\"$TELEGRAM_CHAT_ID_PIPELINE\",\"$TELEGRAM_CHAT_ID_OPS\",\"$TELEGRAM_CHAT_ID_PUSH\"]"

# 4. Vérifier sans exposer
sudo -u openclaw openclaw configure status | grep -A3 telegram

# 5. Relancer le gateway
sudo -u openclaw tmux send-keys -t openclaw-gateway C-c
sudo -u openclaw tmux send-keys -t openclaw-gateway \
  "openclaw gateway run >> ~/.openclaw/logs/gateway_foreground.log 2>&1" Enter

# 6. Health check
sudo -u openclaw openclaw gateway health
```

---

## Lien avec la branche courante

La branche `go/GO_OPT_TRADING_SECURITY_CREDENTIALS_TELEGRAM_MULTICHANNEL_CHILD_01` et le commit `75fb0a83` ont ajouté les `TELEGRAM_CHAT_ID_*` dans `.env` / `.env.example`.

Le prochain GO doit aligner :
1. Les variables `.env` multi-canal
2. La config `openclaw.json` `groupAllowFrom`
3. Les tests smoke Telegram multi-canal

---

## Verdict

| Point | État |
|-------|------|
| Warning gateway health | ACTIF — non bloquant pour DM |
| Impact sur groupes | DROPPING silencieux si groupes |
| Fix disponible | OUI — 2 options documentées |
| Action requise | Prochain GO dédié ou action directe |
| Secret exposé dans ce doc | AUCUN |
