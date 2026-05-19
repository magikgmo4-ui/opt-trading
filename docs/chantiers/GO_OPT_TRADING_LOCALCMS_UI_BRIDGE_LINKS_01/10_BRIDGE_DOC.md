# Bridge localcms ↔ Desk Pro

Generated: 2026-05-19

## Les deux surfaces

| Surface | Port | Repo | Rôle |
|---------|------|------|------|
| localcms | 8000 | `/home/ghost/localcms` | Viewer docs / navigation modules / CMS installer |
| Desk Pro | 8010 | `/opt/trading` | UI opérationnelle : status, alertes, diagnostics, scoring |

Ces deux surfaces sont **distinctes et indépendantes**. Ne pas les fusionner.

---

## Conflit port 8000 — CRITIQUE

**localcms** et le **webhook server** (opt-trading) partagent le port 8000.  
Ils **ne peuvent pas tourner simultanément**.

| Contexte | Service à démarrer sur 8000 | Conséquence |
|----------|-----------------------------|-------------|
| Consultation docs / modules | localcms | Webhook server arrêté — TradingView ne peut pas envoyer de signaux |
| Trading live / réception signaux | webhook server | localcms inaccessible |
| Dev Desk Pro (status, scoring) | aucun sur 8000 (ou webhook) | localcms inaccessible |

### Note dans Desk Pro UI

La page `/desk/ui` affiche une note visible :

> ⚠ Port 8000 partagé — localcms et webhook server ne peuvent pas coexister. Choisir l'un ou l'autre avant de démarrer.

Le badge `webhook:fail` dans Pipeline Status indique que rien ne tourne sur 8000.  
Le guidance banner contextualise : "Port 8000 injoignable — démarrer le webhook server ou localcms."

---

## Navigation entre les deux surfaces

### Desk Pro → localcms

Depuis `/desk/ui`, le bouton **localcms** dans l'Action Panel ouvre `http://127.0.0.1:8000` dans un nouvel onglet.

> Note : ce lien n'est actif que si localcms est démarré.

### localcms → Desk Pro

Depuis localcms, utiliser directement `http://127.0.0.1:8010/desk/ui` dans le navigateur.  
(Pas de lien injecté dans le SPA localcms — repo externe, modification hors scope.)

---

## Démarrage

### Démarrer localcms

```bash
cd /home/ghost/localcms
uvicorn main:app --host 127.0.0.1 --port 8000
# ou
./run.sh
```

### Démarrer webhook server (opt-trading)

```bash
cd /opt/trading
bash scripts/webhook_daemon.sh start
```

### Démarrer Desk Pro (port 8010)

```bash
cd /opt/trading
bash scripts/deskpro_api_daemon.sh start
# Desk Pro fonctionne indépendamment du port 8000
```

---

## Smoke localcms

```bash
# Démarrer localcms d'abord
curl -sf http://127.0.0.1:8000/health
# Attendu : {"ok": true}

curl -sf http://127.0.0.1:8000/
# Attendu : 200 HTML (localcms-v5.html)
```

---

## Smoke Desk Pro

```bash
curl -sf http://127.0.0.1:8010/desk/health
# Attendu : {"ok": true}

curl -sf http://127.0.0.1:8010/desk/ui | wc -c
# Attendu : ~14 000 octets HTML
```

---

## Invariants

- Ne jamais démarrer localcms et le webhook server en même temps.
- Ne pas modifier le SPA `localcms-v5.html` pour injecter des données opt-trading.
- Desk Pro reste sur port 8010, localcms sur port 8000 — aucune collusion.
- Aucun secret dans les liens ou la documentation.
