# 30_PRODUCTIZATION_KANBAN

Generated: 2026-05-19

## Kanban — séquence GO produit fini UI

| Colonne | GO | Objectif | Gap(s) adressé(s) | Sortie | Validation |
|---------|----|---------|--------------------|--------|------------|
| DONE | `MAPPING_AND_KANBAN_01` | mapping + gaps + Kanban | tous | 6 docs + ZIP | grep + tests |
| NEXT | `DESKPRO_UI_PRODUCT_SHELL_REVIEW_01` | revoir `/desk/ui` comme produit | D1 D2 D4 | état UX + gaps visuels | screenshot + humain |
| NEXT | `DESKPRO_UI_INFORMATION_ARCHITECTURE_01` | organiser les sections UI | D4 D7 | layout cible | revue humaine |
| NEXT | `DESKPRO_UI_STATE_BADGES_HARDENING_01` | badges état lisibles | D1 D4 | badges + aide inline | tests + screenshot |
| NEXT | `DESKPRO_UI_ACTION_PANEL_01` | panel actions rapides | D5 | start/status/alert-test safe | smoke HTTP |
| NEXT | `DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01` | panel erreurs + next action | D6 | panel diagnostic intégré | tests |
| NEXT | `LOCALCMS_UI_BRIDGE_LINKS_01` | lien docs localcms ↔ Desk Pro | L2 L1 | page/liens docs/runtime | localcms smoke |
| NEXT | `UI_VISUAL_REGRESSION_SMOKE_01` | screenshots pages clés | T1 T3 | captures versionnées / bundle | humain |
| NEXT | `UI_HUMAN_ACCEPTANCE_REVIEW_01` | validation humaine finale | T2 T6 | checklist PASS/FAIL | signature doc |
| NEXT | `UI_PRODUCT_FINAL_BUNDLE_01` | bundle final ZIP | T5 | zip docs/screenshots/checklists | archive |

## Définition de DONE par GO

### `DESKPRO_UI_PRODUCT_SHELL_REVIEW_01`
- [ ] `/desk/ui` chargé et scrollé visuellement
- [ ] Chaque card identifiée et son état documenté
- [ ] Screenshot annoté présent
- [ ] Gaps visuels listés avec fichier source + ligne

### `DESKPRO_UI_STATE_BADGES_HARDENING_01`
- [ ] Badge `healthy` / `degraded` / `down` visible sans JSON brut
- [ ] Couleur ou icône par état
- [ ] Aide inline (tooltip ou légende)
- [ ] Test unitaire badge render
- [ ] Screenshot avant/après

### `DESKPRO_UI_ACTION_PANEL_01`
- [ ] Bouton "Test Alert" déclenche `POST /desk/alert/test`
- [ ] Bouton "Refresh Status" déclenche `GET /desk/status`
- [ ] Aucun secret exposé dans l'UI
- [ ] Smoke HTTP `curl -X POST /desk/alert/test` PASS

### `DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01`
- [ ] Section "Erreurs récentes" dans `/desk/ui` (source `/desk/errors`)
- [ ] Message d'action si erreurs présentes
- [ ] Message "aucune erreur" si count=0
- [ ] Tests unitaires

### `LOCALCMS_UI_BRIDGE_LINKS_01`
- [ ] Conflit port 8000 documenté dans UI et/ou README
- [ ] Lien vers Desk Pro accessible depuis localcms (ou doc)
- [ ] Smoke localcms `GET /health` PASS
- [ ] Aucun secret

### `UI_VISUAL_REGRESSION_SMOKE_01`
- [ ] Screenshot `/desk/ui` (health=down, local)
- [ ] Screenshot `/desk/toolbox`
- [ ] Screenshot localcms `/` (si accessible)
- [ ] Fichiers dans `docs/screenshots/` ou bundle ZIP

### `UI_HUMAN_ACCEPTANCE_REVIEW_01`
- [ ] Checklist remplie par un humain (pas par l'IA seule)
- [ ] Chaque critère produit fini évalué PASS/FAIL/NA
- [ ] Date et contexte de la revue
- [ ] Au moins 1 surface à PASS complet avant "produit fini"

### `UI_PRODUCT_FINAL_BUNDLE_01`
- [ ] ZIP contient : docs + screenshots + checklists + manifest
- [ ] Aucun secret, .env, log sensible dans le ZIP
- [ ] Tests 172+/172 PASS avant packaging
- [ ] SHA256 du ZIP documenté

## Priorisation recommandée

1. `PRODUCT_SHELL_REVIEW_01` — d'abord voir l'existant visuellement (navigateur)
2. `STATE_BADGES_HARDENING_01` — l'amélioration la plus visible/impactante
3. `ERROR_DIAGNOSTICS_PANEL_01` — complète le diagnostic
4. `VISUAL_REGRESSION_SMOKE_01` — captures avant les modifications suivantes
5. `HUMAN_ACCEPTANCE_REVIEW_01` + `FINAL_BUNDLE_01` — clôture
