# GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01
# 90_CLOSEOUT

Generated: 2026-05-19

## Résumé

Liens pont localcms ↔ Desk Pro + documentation conflit port 8000 — adresse gaps L1, L2.

## Gaps adressés

| Gap | Statut |
|-----|--------|
| L1 — Port 8000 partagé sans documentation dans l'UI | DONE |
| L2 — Pas de page pont localcms ↔ Desk Pro | DONE (via doc + lien UI) |

## Changements

### `modules/desk_pro/ui/page.py`

**Lien localcms dans l'Action Panel** :
```html
<a href="http://127.0.0.1:8000" class="action-link" id="localcmsLink"
   target="_blank"
   title="localcms docs viewer — port 8000 (incompatible avec webhook server)">
  localcms
</a>
```

**Note conflit port 8000** (`id="portConflictNote"`) sous l'action panel :
```
⚠ Port 8000 partagé — localcms et webhook server ne peuvent pas coexister.
Choisir l'un ou l'autre avant de démarrer.
```

### `docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/10_BRIDGE_DOC.md`

Documentation bridge complète :
- Tableau des deux surfaces (port, repo, rôle)
- Conflit port 8000 — tableau des contextes d'usage
- Navigation croisée (Desk Pro → localcms via lien UI ; localcms → Desk Pro via URL directe)
- Commandes de démarrage de chaque service
- Smoke commands attendus
- Invariants (ne jamais coexister, ne pas fusionner les surfaces)

### Décision : SPA localcms non modifiée

Le SPA `localcms-v5.html` (9 287 lignes, repo externe) n'est pas modifié — hors scope et contrainte "ne pas fusionner". La navigation depuis localcms → Desk Pro se fait via l'URL directe `http://127.0.0.1:8010/desk/ui`.

### `tests/test_desk_pro_ui_localcms_bridge.py`

26 tests couvrant :
- Lien localcms statique dans action panel (port 8000, target=_blank, class, title)
- Note conflit port 8000 (présente, contenu, position)
- Bridge doc (fichier, contenu, smoke, no secrets)
- Isolation (pas d'API localcms dans Desk Pro)
- Régression : tous les panneaux précédents intacts

## Résultats tests

```
Ran 302 tests in 0.688s  OK
```

(26 nouveaux + 276 existants)

## Critères DONE Kanban

- [x] Conflit port 8000 documenté dans UI (portConflictNote) et doc (10_BRIDGE_DOC.md)
- [x] Lien vers Desk Pro accessible depuis localcms (via doc bridge — SPA hors scope)
- [x] Smoke localcms `GET /health` documenté (commande + résultat attendu)
- [x] Aucun secret

## Smoke localcms (documentation)

```bash
# Démarrer localcms SEUL (pas de webhook server simultané)
cd /home/ghost/localcms && uvicorn main:app --host 127.0.0.1 --port 8000
# Smoke :
curl -sf http://127.0.0.1:8000/health   # → {"ok": true}
```

## Prochaine étape

```
GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01
```

Captures visuelles des pages clés (screenshots ou bundle HTML).
