# 08_GATEWAY_ACTIVATION_EXECUTION_PLAN

## Objectif

Planifier le démarrage contrôlé du gateway OpenClaw avec la configuration effective V2. Ce document définit la commande, les vérifications, les stop conditions et le rollback.

**Ce document ne démarre pas le gateway.**

## Source

- `07_GATEWAY_ACTIVATION_PREFLIGHT.md` — PREFLIGHT_STATUS = PASS

## Invariants

```text
NO_GATEWAY_START_IN_THIS_DOCUMENT
NO_MIGRATION_V121
NO_REMOTE_COMMAND
NO_SSH_CONNECTION
NO_SECRET_LOGGED
NO_WAN_NO_BRIDGE_NO_ADMIN_TRADING
```

---

## Prérequis vérifiés

| Prérequis | Statut | Evidence |
| :--- | :--- | :--- |
| CLI openclaw disponible | **OUI** | `/home/ghost/.npm-global/bin/openclaw 2026.3.11` |
| Config V2 valide | **OUI** | `openclaw config validate --json → valid:true` |
| `gateway.mode = local` | **OUI** | `openclaw.json: gateway.mode=local` |
| Token présent | **OUI** | `gateway.token_present=true` [REDACTED] |
| Port 18789 libre | **À VÉRIFIER** | ECONNREFUSED = actuellement libre |
| Gateway pas déjà démarré | **OUI** | status=stopped, ECONNREFUSED |
| Docker non requis | **OUI** | sandbox mode=off |
| Tailscale non requis | **OUI** | pas de config tailscale dans V2 |

---

## Commande de démarrage

### Commande minimale

```bash
openclaw gateway run
```

Utilise les valeurs de `~/.openclaw/openclaw.json` :
- `gateway.mode: local`
- port : 18789 (défaut)
- bind : loopback — 127.0.0.1 uniquement

### Commande avec logs détaillés (recommandée pour le premier démarrage)

```bash
openclaw gateway run --verbose
```

### Commande explicite (tous les flags)

```bash
openclaw gateway run \
  --port 18789 \
  --bind loopback \
  --verbose
```

**Flags à NE PAS utiliser :**

| Flag | Raison |
| :--- | :--- |
| `--tailscale serve/funnel` | expose WAN — interdit |
| `--auth none` | désactive l'auth token — interdit |
| `--allow-unconfigured` | inutile, mode=local déjà configuré |
| `--force` | tue un process écoutant sur 18789 — vérifier avant usage |
| `--reset` | réinitialise config et workspace — DESTRUCTIF |

---

## Séquence de démarrage

Le démarrage se fait en **deux terminaux** ou en **foreground + vérification rapide**.

### Terminal 1 — démarrage foreground

```bash
# Vérifier l'état avant démarrage
openclaw gateway status

# Démarrer
openclaw gateway run --verbose
# Laisser tourner. Le processus bloque le terminal.
# Stop : Ctrl+C
```

### Terminal 2 (ou après confirmation Terminal 1) — vérifications post-start

```bash
# 1. Statut service + probe
openclaw gateway status

# 2. Health via RPC
openclaw gateway health --json

# 3. Appel direct méthode health
openclaw gateway call health --json

# 4. Sandbox explain post-start
openclaw sandbox explain --json

# 5. Log gateway
tail -n 50 /tmp/openclaw/openclaw-2026-05-13.log
```

---

## Vérifications post-start attendues

| Vérification | Valeur attendue | Action si différent |
| :--- | :--- | :--- |
| `gateway status` | Runtime: running | STOP_CONDITIONS ci-dessous |
| `gateway health` | `{"ok": true}` ou équivalent | STOP_CONDITIONS |
| Port 18789 | accessible loopback | STOP_CONDITIONS |
| `sandbox explain mode` | `off` (inchangé) | noter si différent |
| Logs | pas d'erreur auth, pas de WAN | STOP_CONDITIONS |

---

## Stop conditions

Arrêt immédiat (`Ctrl+C`) si :

```text
- Port 18789 déjà occupé par un autre processus
- Erreur d'authentification token au démarrage
- Gateway essaie de se connecter à un endpoint WAN non attendu
- Logs montrent un démarrage de session/job runtime automatique
- Message "tailscale" ou "funnel" ou "wan" inattendu dans les logs
- Toute sortie contenant le token en clair dans les logs
- Crash immédiat (exit code non nul)
```

---

## Rollback

### Stop foreground

```bash
Ctrl+C
# dans le terminal où gateway run tourne
```

### Stop si processsus orphelin

```bash
lsof -ti:18789 | xargs kill -SIGTERM 2>/dev/null || true
```

### Vérification après rollback

```bash
openclaw gateway status
# → doit montrer "stopped"
openclaw gateway probe
# → doit montrer ECONNREFUSED
```

**Aucune modification de `~/.openclaw/openclaw.json` n'est requise pour le rollback.**

---

## Fichier log gateway

```text
/tmp/openclaw/openclaw-2026-05-13.log
```

À surveiller en temps réel si besoin :

```bash
tail -f /tmp/openclaw/openclaw-2026-05-13.log
```

---

## Gate — validation humaine requise

```text
GATEWAY_START_REQUIRES_HUMAN_VALIDATION = true
```

Ce plan ne doit être exécuté que si l'opérateur approuve explicitement le démarrage du gateway.

Critères d'approbation :

1. Opérateur confirme que le port 18789 est disponible.
2. Opérateur confirme qu'aucun job runtime ne doit se lancer automatiquement.
3. Opérateur confirme que le context loopback-only est acceptable.

---

## NEXT_GO (si validation humaine obtenue)

```text
09_GATEWAY_ACTIVATION_EXECUTION_LOG.md
```

Rôle :

1. Exécuter `openclaw gateway run --verbose` ;
2. Enregistrer la sortie et les vérifications post-start ;
3. Statuer `GATEWAY_UP` ou `GATEWAY_START_FAILED` ;
4. Si `GATEWAY_UP` : préparer le plan d'activation des agents.

## RISKS

- À qualifier.
