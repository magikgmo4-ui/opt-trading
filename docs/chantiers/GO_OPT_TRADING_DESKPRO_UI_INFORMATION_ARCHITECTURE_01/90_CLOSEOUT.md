# GO_OPT_TRADING_DESKPRO_UI_INFORMATION_ARCHITECTURE_01
# 90_CLOSEOUT

Generated: 2026-05-19

## Résumé

Restructuration de l'architecture d'information de `/desk/ui` — séparation visuelle Runtime Health / Analysis Tools.

## Gaps adressés

| Gap | Statut |
|-----|--------|
| G2 — Status card et Form card au même niveau visuel | DONE |
| G5 — Liens /desk/errors et /desk/alerts absents | DONE |
| G6 — Snapshot auto-chargé à chaque ouverture | DONE |
| G7 — Formulaire toujours déplié | DONE |
| G8 — Pas de responsive | DONE |

## Changements

### `modules/desk_pro/ui/page.py`

Nouveau layout :

```
[h1] Desk Pro  — pills endpoints

[h2] Runtime Health
[card id=runtimeHealthCard]
  Pipeline Status (checks, badges, guidance, alert, errors inline)
  liens: errors log | alerts history

[details.tools-section id=analysisTools] ▶ Analysis Tools  (collapsé par défaut)
  [grid 2-col]
    [card] Snapshot (Refresh à la demande uniquement)
    [details.card id=formCard] ▶ Formulaire → Probabilité  (collapsé par défaut)
      ...champs...
```

- `refreshSnap()` retiré de l'initialisation auto — snapshot sur demande uniquement
- `refreshStatus()` seul appelé au chargement
- Media query `@media(max-width:900px)` : grid 1 colonne
- `<details class="tools-section">` : Analysis Tools collapsé, flèche ▶/▼ CSS pure

### `tests/test_desk_pro_ui_information_architecture.py`

27 tests nouveaux couvrant :
- Runtime Health section (heading, id, ordre, liens)
- Analysis Tools `<details>` (id, summary, snapshot dedans)
- Form card collapsible (details element, pas open, champs dedans)
- Snapshot pas auto-chargé + refreshStatus auto-appelé
- Media query 900px
- Régression : badges, guidance, titre dynamique, raw JSON, pas de secrets

## Résultats tests

```
Ran 221 tests in 0.663s  OK
```

(27 nouveaux + 194 existants)

## Prochaine étape

```
GO_OPT_TRADING_DESKPRO_UI_ACTION_PANEL_01
```

Actions start/status/alert/logs — panel actions safe.
