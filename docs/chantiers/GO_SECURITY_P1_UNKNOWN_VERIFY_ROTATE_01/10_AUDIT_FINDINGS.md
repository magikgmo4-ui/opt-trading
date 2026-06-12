# Audit Findings — P1 UNKNOWN Credentials — 2026-06-12

Aucune valeur secrète dans ce document.

---

## 1. TV_WEBHOOK_KEY

**Rôle :** `webhook_receiver`  
**Fichier :** `/opt/trading/.env`  
**Consumers runtime :** `webhook_server.py` (auth gate), `emit_tv_payload.py`, `bitget_to_tv_runner.py`, `modules/auth/webhook_key.py`

### Âge

| Source | Date | Méthode |
|--------|------|---------|
| Premier commit git contenant la var | 2026-02-16 | `git log -S "TV_WEBHOOK_KEY"` |
| Date estimée de création | ≈ 2026-02-16 | premier commit = première utilisation probable |
| Âge calculé (2026-06-12) | **~116 jours** | — |
| TTL recommandé | 90 jours | rotation_schedule.md |

### Verdict : **STALE** → **ROTATE_NOW**

Dépassement : +26 jours au-delà du TTL de 90j.

### Impact rotation

- `webhook_server.py` : chargé au démarrage — reload requis
- TradingView : chaque alerte envoie `key=<valeur>` dans le payload — **l'utilisateur doit mettre à jour la valeur dans TradingView** avant ou après rotation (fenêtre courte de service interrompu)
- `emit_tv_payload.py` / `bitget_to_tv_runner.py` : scripts manuels — `.env` rechargé à chaque run

### Portée machines

Seul `admin-trading` (local) a le rôle `webhook_receiver` actif. Pas de propagation fleet.

---

## 2. OPS_ADMIN_KEY

**Rôle :** `webhook_receiver`  
**Fichier :** `/opt/trading/.env`  
**Consumers runtime :** `webhook_server.py` (admin endpoints HMAC)

### Âge

| Source | Date | Méthode |
|--------|------|---------|
| Premier commit git contenant la var | 2026-02-16 | `git log -S "OPS_ADMIN_KEY"` |
| Âge calculé (2026-06-12) | **~116 jours** | — |
| TTL recommandé | 90 jours | — |

### Verdict : **STALE** → **ROTATE_NOW**

Dépassement : +26 jours.

### Impact rotation

- Seul `webhook_server.py` consomme cette clé (endpoints admin)
- Reload server suffisant
- Aucune dépendance externe (pas TradingView, pas fleet)

### Portée machines

`admin-trading` uniquement.

---

## 3. TELEGRAM_BOT_TOKEN

**Rôle :** `telegram_collector`  
**Fichier :** `/etc/opt-trading/env.d/roles/telegram_collector.env`  
**Consumers runtime :** `shared/telegram_notify.py`, `bot_vision_step2`, `notification_dispatcher`, `runtime_health`, `desk_pro`

### Âge

| Source | Date | Méthode |
|--------|------|---------|
| Première référence git (mimo v2 pro) | 2026-03-25 | `git log -S "TELEGRAM_BOT_TOKEN"` |
| Bot creation (BotFather) | UNKNOWN — à vérifier | BotFather `/mybots` → token info |
| Âge minimum estimé | ≈ 79 jours | depuis première ref git |
| TTL recommandé | 365 jours | — |

### Verdict : **KEEP** — vérifié 2026-06-12

BotFather `/mybots` consulté par l'utilisateur le 2026-06-12.  
Token créé récemment — dans le TTL de 365j. Aucune rotation requise.

---

## 4. Plan d'action décidé

| Credential | Verdict | Action | Responsable |
|------------|---------|--------|-------------|
| `TV_WEBHOOK_KEY` | STALE | **ROTATED 2026-06-12** | ⚠️ utilisateur : mettre à jour TradingView |
| `OPS_ADMIN_KEY` | STALE | **ROTATED 2026-06-12** | Rotation complète |
| `TELEGRAM_BOT_TOKEN` | KEEP | Vérifié BotFather 2026-06-12 — dans TTL | Clôturé |

---

## 5. Procédure rotation TV_WEBHOOK_KEY + OPS_ADMIN_KEY

**Conditions :**
- `webhook_server.py` non running comme service systemd (port 8000 non actif, `algo-hf-api.service` = service différent)
- Rotation `.env` local uniquement

**Étapes :**
1. Générer deux nouvelles valeurs aléatoires (64 hex chars)
2. Remplacer dans `/opt/trading/.env`
3. Vérifier syntaxe `.env`
4. Mettre à jour TradingView (TV_WEBHOOK_KEY uniquement — action manuelle utilisateur)
5. Documenter la date de rotation dans ce fichier
