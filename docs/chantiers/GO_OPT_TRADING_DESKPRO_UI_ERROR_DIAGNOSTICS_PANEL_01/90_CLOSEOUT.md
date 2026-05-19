# GO_OPT_TRADING_DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01
# 90_CLOSEOUT

Generated: 2026-05-19

## Résumé

Panel de diagnostic des erreurs récentes intégré dans `/desk/ui` — adresse gap D6.

## Gap adressé

| Gap | Statut |
|-----|--------|
| D6 — Pas de panel erreurs récentes dans l'UI | DONE |

## Changements

### `modules/desk_pro/ui/page.py`

**`<div id="errorDiagnostics">`** ajouté dans `runtimeHealthCard`, entre `pipelineSummary` et le Raw JSON collapsible.

**`async function refreshErrors()`** :
- Fetch `GET /desk/errors`
- Si `count === 0` : affiche `✓ Aucune erreur` en vert
- Si `count > 0` :
  - Badge rouge avec total
  - Banner orange "Action suggérée" — message contextualisé par probe :
    - probe contient `8000`/`webhook` → "Port 8000 injoignable — démarrer le webhook server ou localcms"
    - probe contient `8010`/`perf` → "Erreur de sonde Perf — vérifier le service sur port 8010"
    - défaut → "Consulter /desk/logs/latest pour le détail"
  - Table des 5 dernières erreurs (heure, probe, message)
  - Lien "voir errors log" si count > 5
- Fallback gracieux si `/desk/errors` inaccessible

**Appelée depuis `refreshStatus()`** : chaque Refresh Status déclenche aussi refreshErrors(). Aucun listener séparé nécessaire.

**Ancienne inline error block** (`j.error_count > 0`) supprimée de `refreshStatus()`.

### `tests/test_desk_pro_ui_error_diagnostics.py`

26 tests couvrant :
- Présence statique de `errorDiagnostics` (avant `<script>`, dans `runtimeHealthCard`)
- `refreshErrors()` : fetch `/desk/errors`, état "aucune erreur", rouge si erreurs, action, table, overflow, fallback
- Appelée depuis `refreshStatus()` — ancienne block supprimée
- Sécurité (no secrets)
- Régression : action panel, IA sections, guidance, badges

## Résultats tests

```
Ran 276 tests in 0.668s  OK
```

(26 nouveaux + 250 existants)

## Critères DONE Kanban

- [x] Section "Erreurs récentes" dans `/desk/ui` (source `/desk/errors`)
- [x] Message d'action si erreurs présentes (contextualisé par probe)
- [x] Message "aucune erreur" si count=0
- [x] Tests unitaires (26 tests)

## Prochaine étape

```
GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01
```

Lier docs localcms ↔ Desk Pro — page pont ou liens croisés.
