# Human Acceptance Review — Desk Pro UI
# GO_OPT_TRADING_UI_HUMAN_ACCEPTANCE_REVIEW_01

Checklist d'acceptation produit fini.  
Les items **[AUTO]** sont vérifiés programmatiquement.  
Les items **[HUMAN]** requièrent une évaluation visuelle / jugement humain.

---

## Contexte de la revue

| Champ | Valeur |
|-------|--------|
| Date | _(à remplir par le reviewer)_ |
| Reviewer | _(à remplir)_ |
| Branche | `sot/mainline` |
| Commit | `d4c0c364` |
| Tests | 343/343 PASS |
| URL | http://127.0.0.1:8010/desk/ui |

---

## Section 1 — Vérifications automatiques [AUTO]

Ces items sont couverts par les tests unitaires. Tous PASS au moment de la revue.

| # | Critère | Résultat | Test |
|---|---------|----------|------|
| A1 | Tests 343/343 PASS | **PASS** | `python3 -m unittest discover` |
| A2 | Badge HEALTHY/DEGRADED/DOWN visible et coloré | **PASS** | `test_desk_pro_ui_badges_hardening` |
| A3 | Guidance banner quand health=down/degraded | **PASS** | `test_guidance_block_rendered_for_degraded_or_down` |
| A4 | Message webhook_activity contextuel | **PASS** | `test_webhook_activity_guidance_message` |
| A5 | Titre onglet dynamique (DOWN/DEGRADED) | **PASS** | `test_document_title_update_present` |
| A6 | Action Panel statique (btnStatus, btnTestAlert) | **PASS** | `test_btn_test_alert_static_in_html` |
| A7 | Liens diagnostics (errors, alerts, logs, toolbox) | **PASS** | `test_action_panel_links` |
| A8 | Lien localcms dans action panel | **PASS** | `test_localcms_link_present` |
| A9 | Note conflit port 8000 visible | **PASS** | `test_port_conflict_note_present` |
| A10 | Runtime Health séparé de Analysis Tools | **PASS** | `test_runtime_health_before_analysis_tools` |
| A11 | Analysis Tools collapsé par défaut | **PASS** | `test_analysis_tools_is_details_element` |
| A12 | Form card collapsé par défaut | **PASS** | `test_form_card_not_open_by_default` |
| A13 | Snapshot ne s'auto-charge pas | **PASS** | `test_snap_not_auto_called_at_init` |
| A14 | Error Diagnostics panel présent | **PASS** | `test_error_diagnostics_div_present` |
| A15 | "Aucune erreur" quand count=0 | **PASS** | `test_no_error_state_rendered` |
| A16 | Table erreurs + action suggérée si count>0 | **PASS** | `test_error_table_rendered` |
| A17 | Responsive 900px media query | **PASS** | `test_media_query_900px_present` |
| A18 | Aucun secret dans le HTML | **PASS** | `test_no_secret_in_html` |
| A19 | HTTP 200 sur /desk/ui | **PASS** | smoke manifest |
| A20 | HTTP 200 sur /desk/toolbox | **PASS** | smoke manifest |
| A21 | HTTP 200 sur /desk/health /status /errors /alerts /logs | **PASS** | smoke manifest |
| A22 | Capture HTML desk_ui.html présente | **PASS** | `test_desk_ui_capture_exists` |
| A23 | Watchdog WARN-only sur webhook_activity:fail | **PASS** | `test_desk_pro_health_classification` |

---

## Section 2 — Jugement visuel / UX [HUMAN]

À évaluer en ouvrant http://127.0.0.1:8010/desk/ui dans un navigateur.

### 2a — Premier écran (sans scroll)

| # | Critère | Résultat | Notes |
|---|---------|----------|-------|
| H1 | L'état système est clair au premier coup d'œil (badge visible, pas de JSON brut) | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H2 | L'Action Panel est immédiatement visible et utilisable | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H3 | La note de conflit port 8000 est lisible sans être intrusive | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H4 | Le badge DOWN/DEGRADED/HEALTHY est reconnaissable sans légende | `[ ] PASS  [ ] FAIL  [ ] NA` | |

### 2b — Guidance et diagnostics

| # | Critère | Résultat | Notes |
|---|---------|----------|-------|
| H5 | Le message de guidance (bannière jaune) explique clairement l'état | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H6 | Le panel "Erreurs récentes" est compréhensible (aucune erreur = rassurant) | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H7 | Les liens errors/alerts/logs/toolbox sont discoverables | `[ ] PASS  [ ] FAIL  [ ] NA` | |

### 2c — Navigation et architecture

| # | Critère | Résultat | Notes |
|---|---------|----------|-------|
| H8 | La séparation "Runtime Health" / "Analysis Tools" est claire | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H9 | "▶ Analysis Tools" collapsé ne perturbe pas la lecture du status | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H10 | Le formulaire collapsé réduit la charge cognitive | `[ ] PASS  [ ] FAIL  [ ] NA` | |

### 2d — Actions

| # | Critère | Résultat | Notes |
|---|---------|----------|-------|
| H11 | Clic "Refresh Status" → mise à jour visible | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H12 | Clic "Test Alert" → résultat affiché en ligne (✓/✗ destination) | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H13 | Lien "localcms" → ouvre port 8000 dans un nouvel onglet | `[ ] PASS  [ ] FAIL  [ ] NA` | |

### 2e — Qualité générale

| # | Critère | Résultat | Notes |
|---|---------|----------|-------|
| H14 | L'UI est utilisable sans lire de documentation | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H15 | Aucune régression visuelle évidente par rapport à la session précédente | `[ ] PASS  [ ] FAIL  [ ] NA` | |
| H16 | L'UI reste utilisable sans variable d'environnement secrète | `[ ] PASS  [ ] FAIL  [ ] NA` | |

---

## Section 3 — Critères "produit fini" par surface

### Desk Pro (/desk/ui)

| Critère produit fini | Auto | Human | Résultat global |
|---------------------|------|-------|-----------------|
| Premier écran explique l'état système | A2 A3 | H1 | `[ ] PASS  [ ] FAIL` |
| Chaque badge a une signification lisible | A2 A5 | H4 | `[ ] PASS  [ ] FAIL` |
| Chaque état healthy/degraded/down visible | A2 | H4 | `[ ] PASS  [ ] FAIL` |
| Erreur propose une action | A16 | H5 H6 | `[ ] PASS  [ ] FAIL` |
| UI utilisable sans secret | A18 A21 | H16 | `[ ] PASS  [ ] FAIL` |
| Tests passent | A1 | — | **PASS** |
| Screenshots/captures présents | A22 | — | **PASS** |
| Revue humaine signée | — | voir ci-dessous | `[ ] PASS  [ ] FAIL` |

### Verdict Desk Pro

```
[ ] PRODUIT FINI — tous les critères PASS
[ ] CONDITIONNEL — critères humains en attente
[ ] BLOQUÉ — critères FAIL (lister les items)
```

Items bloquants (si applicable) :
```
_____________________________________________
_____________________________________________
```

---

## Signature

```
Reviewer  : ________________________________
Date      : ________________________________
Verdict   : [ ] PASS  [ ] FAIL  [ ] CONDITIONNEL
Remarques : ________________________________
           ________________________________
```

---

## Commandes de validation rapide

```bash
# Démarrer le serveur si arrêté
cd /opt/trading
python3 -m uvicorn modules.perf.app:app --host 127.0.0.1 --port 8010 --log-level warning &

# Ouvrir dans le navigateur
xdg-open http://127.0.0.1:8010/desk/ui

# Tests
python3 -m unittest discover -s tests -p "test_*.py"

# Smoke
curl -sf http://127.0.0.1:8010/desk/health   # {"ok":true}
curl -sf http://127.0.0.1:8010/desk/ui | wc -c  # ~18000 bytes
```
