# GO_OPT_TRADING_DESKPRO_UI_STATE_BADGES_HARDENING_01 — CLOSEOUT

Generated: 2026-05-19

## État final

| Élément | Statut |
|---------|--------|
| Tests | 194/194 PASS (172 existants + 22 nouveaux) |
| `modules/desk_pro/ui/page.py` | patché — guidance + titre onglet |
| `tests/test_desk_pro_ui_badges_hardening.py` | 22 tests |
| Secrets | absents |

## Changements

### `modules/desk_pro/ui/page.py`

**G1 + G3 — Guidance contextuelle sous le badge DOWN/DEGRADED**

Bloc JS ajouté dans `refreshStatus()` après le badge health :

```js
if(h.status === 'down' || h.status === 'degraded'){
  const causes = failing.map(c => c.check);
  // Messages par cause :
  webhook_activity → "Aucun signal TradingView récent — normal en dev local, vérifier en production"
  webhook          → "Port 8000 injoignable — démarrer le webhook server"
  perf             → "Module Perf injoignable — vérifier le service sur le port 8010"
  probe_errors     → "Erreurs de sonde accumulées — consulter /desk/errors"
  autres           → "Composants en échec : <liste>"
}
```

Rendu : bandeau jaune `#fff8e1` avec bordure gauche orange `#f9a825`, id `healthGuidance`.

**G4 (bonus) — Titre onglet dynamique**

```js
document.title = 'Desk Pro' + (h.status !== 'healthy' ? ' — ' + h.status.toUpperCase() : '');
```

Résultat : onglet affiche `Desk Pro — DOWN` quand health=down.

## Comportement en production

| Scénario | Message guidance affiché |
|----------|--------------------------|
| `webhook_activity:fail` (local, pas de TradingView) | "Aucun signal TradingView récent — normal en dev local..." |
| `webhook:fail` (port 8000 DOWN) | "Port 8000 injoignable — démarrer le webhook server" |
| `perf:fail` | "Module Perf injoignable — vérifier le service sur le port 8010" |
| `probe_errors:fail` | "Erreurs de sonde accumulées — consulter /desk/errors" |
| `health=healthy` | Aucun bandeau affiché |

## Note serveur live

Le serveur FastAPI en cours d'exécution sert la version en mémoire.
La nouvelle UI sera active au prochain démarrage : `scripts/deskpro_api_daemon.sh restart`
ou équivalent.

## Prochaine étape

```
GO_OPT_TRADING_DESKPRO_UI_INFORMATION_ARCHITECTURE_01
```

Adresse G2 : séparer visuellement "Runtime Health" (status + alert) de "Analysis Tools" (snapshot + form).
