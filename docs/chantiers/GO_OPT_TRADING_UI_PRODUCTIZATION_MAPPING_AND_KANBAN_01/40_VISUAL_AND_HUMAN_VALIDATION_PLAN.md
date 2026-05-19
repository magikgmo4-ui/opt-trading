# 40_VISUAL_AND_HUMAN_VALIDATION_PLAN

Generated: 2026-05-19

## Objectif

Définir comment prouver que chaque surface UI est "produit fini" de façon humainement vérifiable,
pas seulement par tests automatiques.

## Plan de validation visuelle

### Pages à capturer

| Surface | URL | Contexte requis | Outil recommandé |
|---------|-----|----------------|-----------------|
| Desk Pro main | `http://127.0.0.1:8010/desk/ui` | ports 8000+8010 UP | navigateur / SSH tunnel Windows |
| Desk Pro toolbox | `http://127.0.0.1:8010/desk/toolbox` | port 8010 UP | navigateur |
| Desk Pro status raw | `http://127.0.0.1:8010/desk/status` | port 8010 UP | navigateur / curl |
| Desk Pro alerts | `http://127.0.0.1:8010/desk/alerts` | port 8010 UP | navigateur |
| localcms home | `http://127.0.0.1:8000/` | localcms running (pas webhook) | navigateur |

### Tunnel SSH Windows (référence)

```powershell
ssh -L 18010:127.0.0.1:8010 ghost@admin-trading
```
Puis navigateur Windows : `http://127.0.0.1:18010/desk/ui`

### Nommage screenshots

```
docs/screenshots/SURFACE_STATE_DATE.png
exemples :
  desk_ui_health_down_20260519.png
  desk_ui_health_healthy_20260519.png
  desk_toolbox_20260519.png
  localcms_home_20260519.png
```

---

## Checklist humaine d'acceptation — Desk Pro

Remplir par un humain après revue visuelle :

| Critère | PASS / FAIL / NA | Notes |
|---------|-----------------|-------|
| L'état système est lisible sans lire le JSON brut | | |
| Les états `healthy` / `degraded` / `down` sont distincts visuellement | | |
| Le badge rouge/orange/vert est compréhensible sans documentation | | |
| Chaque erreur affichée indique une action possible | | |
| Le bouton "Test Alert" existe et déclenche une action visible | | |
| Aucun token/secret visible dans l'UI | | |
| L'UI reste lisible sans env secret (Telegram non configuré) | | |
| Le lien vers `/desk/toolbox` est accessible | | |
| La page charge en moins de 3 secondes | | |
| L'UI est lisible depuis Windows via SSH tunnel | | |

**Signé :** __________________ **Date :** __________________ **Résultat global :** PASS / FAIL

---

## Checklist humaine d'acceptation — localcms

| Critère | PASS / FAIL / NA | Notes |
|---------|-----------------|-------|
| La page d'accueil charge sans erreur | | |
| La sidebar est visible et navigable | | |
| La section "use" et "dev" sont distinctes | | |
| L'explorateur de modules fonctionne | | |
| La contrainte port 8000 est documentée dans l'UI ou README | | |
| Aucun secret visible | | |

**Signé :** __________________ **Date :** __________________ **Résultat global :** PASS / FAIL

---

## États UI attendus vs observés

| État système | Rendu attendu `/desk/ui` | Mesurable comment |
|-------------|------------------------|-------------------|
| `health=healthy` | Badge vert, "Système OK" | Port 8000+8010 UP + webhook récent |
| `health=degraded` | Badge orange, avertissement | `webhook_activity:warn` (stale) |
| `health=down` (webhook_activity) | Badge rouge mais cause "activité" | Local sans TradingView — attendu |
| `health=down` (infra) | Badge rouge + alerte infra | Port 8000 DOWN |
| Cooldown actif | Alerte "cooldown Ns restantes" | 5min après dernière alerte |

---

## Smoke HTTP (automatisable)

```bash
# Desk Pro health
curl -sf http://127.0.0.1:8010/desk/health | python3 -c "import sys,json; d=json.load(sys.stdin); assert d['ok']"

# Desk Pro status — vérifier structure
curl -sf http://127.0.0.1:8010/desk/status | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert 'health' in d
assert 'status' in d['health']
assert 'checks' in d['health']
print('OK status='+d['health']['status'])
"

# Alert test (skip si non configuré)
curl -sf -X POST http://127.0.0.1:8010/desk/alert/test | python3 -c "
import sys,json; d=json.load(sys.stdin)
assert d['ok']
print('OK alert test dispatched')
"
```
