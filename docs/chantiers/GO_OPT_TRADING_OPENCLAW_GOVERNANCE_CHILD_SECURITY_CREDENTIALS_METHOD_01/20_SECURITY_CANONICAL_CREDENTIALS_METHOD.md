# 20_SECURITY_CANONICAL_CREDENTIALS_METHOD

## Principe général

**Un secret ne doit jamais apparaître dans le git.** Tout ce qui est versionné est un template ou un pointeur.

## Méthode canonique — 4 niveaux

### Niveau 1 — Secrets runtime (`.env`, `.secrets/`)

```
.env                    ← non versionné, chargé par load_env()
.secrets/<service>.env  ← non versionné, chargé à la demande
```

**Règle :** toujours avoir un `.env.example` versionné avec les clés et valeurs vides.
**Chargement :** via `modules/env/env.py` → `load_env()` au démarrage de chaque service.

```python
# Pattern canonique pour lire un secret
from modules.auth.secrets import require_secret
token = require_secret("TELEGRAM_BOT_TOKEN")
```

---

### Niveau 2 — Rôles modulaires (`configs/env/roles/`)

```
configs/env/roles/<role>.env.example   ← versionné (clés seulement)
configs/env/roles/<role>.env           ← gitignored (valeurs réelles)
```

Utilisation : charger un rôle spécifique selon le service qui démarre.
Permet un profil minimal (ex: `base.env` + `telegram_collector.env` sans `llm_cloud.env`).

**Cible future :** migrer vers `/etc/opt-trading/env.d/roles/<role>.env` pour les déploiements système.

---

### Niveau 3 — Outils tiers (`~/.openclaw/`, `~/.config/`)

- Credentials gérés exclusivement par l'outil propriétaire (openclaw wizard, `openclaw configure set`)
- Ne jamais éditer `openclaw.json` manuellement
- Ne jamais copier les tokens dans des fichiers versionnés
- Backup autorisé dans `~/.openclaw/openclaw.json.bak.*` — hors git

---

### Niveau 4 — CI/CD (GitHub Actions)

- Utiliser uniquement le `GITHUB_TOKEN` automatique quand possible
- Si un secret externe est requis : le déclarer dans GitHub Settings → Secrets, jamais dans les fichiers YAML
- Format dans workflow :

```yaml
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}
```

---

## Règles absolues

| Règle | Raison |
|-------|--------|
| Jamais de secret dans un fichier `.md`, `.json`, `.yml` versionné | Historique git permanent |
| Jamais de `echo $TOKEN` dans les logs | Fuite dans stdout |
| Toujours utiliser `require_secret()` ou `get_secret()` de `modules/auth/secrets.py` | Centralisation, testabilité |
| `.gitignore` doit couvrir `.env`, `.env.*`, `.secrets/`, `*.session`, `*.pem`, `*.key` | Barrière primaire |
| Les fichiers `.example` ne doivent jamais contenir de valeurs réelles | Même partielles |

---

## Vérification canonique anti-leak

```bash
# Avant tout commit
git diff --cached | grep -Ei 'token|secret|api_key|api_hash|password|bearer|webhook' || echo "CLEAN"

# Audit global (lecture seule)
grep -r "TELEGRAM_BOT_TOKEN\s*=" /opt/trading --include="*.py" --include="*.env" \
  | grep -v ".example" | grep -v "__pycache__"
```

---

## Structure cible complète

```
opt-trading/
├── .env.example          ← versionné, clés + commentaires
├── .env                  ← gitignored, valeurs réelles
├── .secrets/
│   ├── bitget.env.example ← versionné
│   └── bitget.env         ← gitignored
├── configs/env/roles/
│   ├── base.env.example
│   ├── telegram_collector.env.example
│   └── ...               ← un fichier par rôle
└── modules/auth/
    ├── secrets.py         ← get_secret() / require_secret()
    └── bitget_credentials.py ← chargement bitget

/etc/opt-trading/          ← (cible future)
└── env.d/roles/
    └── <role>.env         ← fichiers système non versionnés

/home/openclaw/.openclaw/
└── openclaw.json          ← géré par openclaw CLI uniquement
```
