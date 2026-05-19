# GO_OPT_TRADING_DESKPRO_UI_PRODUCT_SHELL_REVIEW_01
# 00_PRODUCT_SHELL_REVIEW

Generated: 2026-05-19

## Baseline

| Élément | Valeur |
|---------|--------|
| Branche | `sot/mainline` @ `df9bf336` |
| Tests | 172/172 PASS |
| Port 8010 | UP |
| Port 8000 | UP (webhook ou localcms) |
| `/desk/health` | `ok: true` |
| `/desk/status` health | `down` — cause : `webhook_activity:fail` (attendu sans signal TradingView) |
| `/desk/errors` count | 0 |
| Alert test (Telegram) | DELIVERED |
| Alert test (webhook) | failed — URL configurée est l'API Telegram, pas un webhook générique |

---

## Structure actuelle de `/desk/ui`

### Layout

```
[h1] Desk Pro
[header] pills: /desk/health  /desk/snapshot  /desk/form  /desk/toolbox (injecté)

[grid 2 colonnes]
┌─────────────────────────────┬─────────────────────────────┐
│ Card: Pipeline Status        │ Card: Snapshot               │
│ - Badge health (color)       │ - Table métriques            │
│ - Checks table               │ - Refresh button             │
│ - Mini-cards: Desk/Webhook/  │                              │
│   Perf (3 colonnes)          │                              │
│ - Sources row                │                              │
│ - Test Alert button          │                              │
│ - Alert triggered/cooldown   │                              │
│ - Errors inline (si > 0)     │                              │
│ - Refresh button             │                              │
│ - Raw JSON (collapsible)     │                              │
├─────────────────────────────┴─────────────────────────────┤
│ Card: Formulaire → Probabilité (2 colonnes entières)        │
│ - 8 champs inputs/selects                                   │
│ - Textarea JSON S/R                                         │
│ - Bouton Calculer                                           │
│ - Pre résultat JSON                                         │
└────────────────────────────────────────────────────────────┘
```

### Badges et couleurs

| État | Couleur | Texte affiché |
|------|---------|---------------|
| `healthy` | `#2e7d32` vert | `HEALTHY` |
| `degraded` | `#e65100` orange | `DEGRADED` |
| `down` | `#c62828` rouge | `DOWN` |
| check:pass | vert | badge vert avec valeur |
| check:warn | orange | `WARN` |
| check:fail | rouge | valeur fail |

### Auto-chargement au démarrage

- `refreshStatus()` appelé au load → `/desk/status`
- `refreshSnap()` appelé au load → `/desk/snapshot`

---

## Ce qui fonctionne bien (à conserver)

| Élément | Appréciation |
|---------|-------------|
| Badge santé coloré (DOWN/DEGRADED/HEALTHY) | Lisible au premier coup d'œil |
| Checks table avec badges par check | Granularité suffisante |
| Mini-cards Desk Pro / Webhook / Perf | Résumé compact des composants |
| Test Alert button dans le status card | Action accessible sans naviguer |
| Errors inline (rouge, count + last error) | Visible sans chercher |
| Alert cooldown/triggered avec dispatch | Feedback immédiat |
| Raw JSON collapsible | Puissance sans polluer la vue |
| Toolbox link injecté dans header | Navigation vers outils |
| Snapshot table avec métriques | Données live compactes |

---

## Gaps identifiés

### P0 — Bloquants produit fini

| ID | Gap | Symptôme observé | Fichier source |
|----|-----|-----------------|----------------|
| G1 | Pas de guidance quand `health=down` | Badge rouge "DOWN" sans explication ni action | `page.py:167-171` |
| G2 | Status card et Form card dans le même niveau visuel | Un opérateur voulant surveiller le système doit cohabiter avec un formulaire d'analyse | `page.py:32-162` |
| G3 | `webhook_activity:fail` sans label contextuel | La raison "Xs since last event" est dans le tableau mais aucun message "attendu sans signal TradingView" | `page.py:198-203` |

### P1 — Friction UX

| ID | Gap | Symptôme observé | Fichier source |
|----|-----|-----------------|----------------|
| G4 | Titre de page statique "Desk Pro" | L'onglet navigateur ne reflète pas l'état health | `page.py:9` |
| G5 | Pas de lien `/desk/errors` ni `/desk/alerts` dans l'UI | Historique erreurs et alertes non accessibles depuis la page | `routes.py:242-264` |
| G6 | Snapshot auto-chargé à chaque ouverture | `/desk/snapshot` appelé même si l'opérateur veut juste le status | `page.py:373-374` |
| G7 | Formulaire toujours déplié et visible | La card Form prend toute la largeur en bas — charge cognitive | `page.py:58-161` |
| G8 | Pas de responsive | Grid 2 colonnes fixe sans media query | `page.py:14,21` |
| G9 | Webhook config note absente de l'UI | ALERT_WEBHOOK_URL ne doit pas pointer vers l'API Telegram — non documenté dans l'UI | `routes.py:160-161` |

---

## Priorisation des correctifs

### Sprint 1 — Badges hardening (GO suivant)

Adresse G1, G3 :
- Ajouter une ligne de contexte sous le badge DOWN : afficher la cause principale en clair
- Pour `webhook_activity:fail` : ajouter "(aucun signal TradingView récent — attendu en dev)"
- Pour `webhook:fail` : ajouter "(port 8000 injoignable — démarrer le webhook server)"

### Sprint 2 — Architecture information

Adresse G2, G7 :
- Séparer visuellement "Runtime Health" (status + alert) de "Analysis Tools" (snapshot + form)
- Rendre la card Form collapsible par défaut

### Sprint 3 — Panneaux diagnostics

Adresse G5 :
- Intégrer `/desk/errors` inline dans Pipeline Status (déjà partiellement fait pour error_count)
- Ajouter lien vers `/desk/alerts` (historique JSONL)

### Sprint 4 — Polish

Adresse G4, G6, G8, G9 :
- Titre onglet dynamique : `document.title = 'Desk Pro — ' + status.toUpperCase()`
- Snapshot : charger à la demande uniquement
- Responsive basique : media query 900px
- Note configuration webhook dans la section alert

---

## État "produit fini" cible pour `/desk/ui`

```
[ ] Badge DOWN + cause principale en une phrase lisible
[ ] "Attendu en dev / Action suggérée en prod" selon la cause
[ ] Séparation visuelle Runtime Health vs Analysis Tools
[ ] Titre onglet reflète l'état (DOWN/DEGRADED/HEALTHY)
[ ] Lien /desk/errors et /desk/alerts accessibles
[ ] Formulaire collapsible par défaut
[ ] Responsive 900px minimum
[ ] Tests 172+/172 PASS
[ ] Screenshot avant/après
[ ] Revue humaine PASS
```

---

## Smoke HTTP confirmés

```bash
curl -sf http://127.0.0.1:8010/desk/ui        # 200, ~13K HTML
curl -sf http://127.0.0.1:8010/desk/health     # {"ok":true}
curl -sf http://127.0.0.1:8010/desk/status     # health=down (attendu)
curl -sf http://127.0.0.1:8010/desk/errors     # {"count":0}
curl -sf -X POST http://127.0.0.1:8010/desk/alert/test  # telegram: delivered
```

## Prochaine étape

```
GO_OPT_TRADING_DESKPRO_UI_STATE_BADGES_HARDENING_01
```

Adresse G1 + G3 en premier : ajouter guidance contextuelle sous le badge DOWN.
C'est le correctif le plus visible, le plus impactant, et le moins risqué.
