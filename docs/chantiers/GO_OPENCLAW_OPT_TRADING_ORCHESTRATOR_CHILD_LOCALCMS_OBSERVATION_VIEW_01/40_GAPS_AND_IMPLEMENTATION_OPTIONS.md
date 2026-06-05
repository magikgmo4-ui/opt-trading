---
go_id: GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_01
doc_type: gaps_and_options
repo: opt-trading
status: open
created_at: 2026-05-17
---

# 40_GAPS_AND_IMPLEMENTATION_OPTIONS

---

## Gaps identifiés

### GAP 1 — Bloc `observation` absent de `_build_metrics()`

```text
Les champs Phase 1 (seuils, éligibilité, progression) ne sont pas calculés.
Impact : l'opérateur ne peut pas lire l'éligibilité depuis LocalCMS.
Sévérité : MEDIUM — Phase 1 continue sans blocage, mais la lisibilité est dégradée.
```

### GAP 2 — `last_run` incomplet vs `ObservationEvent` V1

```text
session_id, localcms_ok, closeout_required absents de last_run.
Impact : pas d'alerte closeout visible dans le dashboard.
Sévérité : LOW pendant Phase 1 (closeout_required = false actuellement).
```

### GAP 3 — Dashboard HTML non adapté Phase 1

```text
/metrics ne montre pas la progression vers les seuils.
Impact : l'opérateur doit calculer manuellement depuis total_runs.
Sévérité : LOW — workaround : curl /metrics/daily | python3 -m json.tool.
```

---

## Options d'implémentation

### Option A — Extension minimale de `_build_metrics()` (recommandée)

```text
Modifier uniquement _build_metrics() dans modules/localcms/app/main.py :
- ajouter le bloc "observation" dans le dict retourné
- ajouter session_id, localcms_ok, closeout_required dans last_run
- aucun nouvel endpoint
- aucune migration
```

**Pour** : minimal, rétrocompatible, isolé à un seul fichier.
**Contre** : aucun.
**Statut** : retenue comme option principale.

### Option B — Endpoint dédié `/metrics/observation`

```text
Créer un endpoint séparé GET /metrics/observation qui retourne uniquement
le bloc observation.
```

**Pour** : séparation claire si les consommateurs divergent.
**Contre** : duplication de logique, deux endpoints à maintenir.
**Statut** : non retenue pour l'instant.

### Option C — Extension du dashboard HTML

```text
Ajouter un bloc visuel Phase 1 dans _metrics_html() :
- barre de progression runs_to_threshold
- barre de progression days_to_threshold
- badge ELIGIBLE / NON ELIGIBLE
- alerte rouge si closeout_required_count > 0
```

**Pour** : lisibilité opérateur immédiate sans curl.
**Contre** : plus de code HTML, risque de drift.
**Statut** : souhaitable, à inclure dans le GO d'implémentation si périmètre accepté.

---

## Périmètre du GO d'implémentation recommandé

```text
GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01
```

### Scope minimal (option A seule)

- [ ] Modifier `_build_metrics()` — ajouter bloc `observation`
- [ ] Étendre `last_run` — ajouter `session_id`, `localcms_ok`, `closeout_required`
- [ ] Test manuel : `curl localhost:8700/metrics/daily | python3 -m json.tool`
- [ ] Vérifier que les champs existants sont inchangés

### Scope complet (option A + C)

- [ ] Tout le scope minimal
- [ ] Étendre `_metrics_html()` — bloc Phase 1 avec progressions
- [ ] Alerte `closeout_required_count > 0` dans le dashboard
- [ ] Test manuel : ouvrir `/metrics` dans le navigateur

---

## Ce que ce child GO ne décide pas

```text
- Le moteur de persistance BDD (hors scope — cf. DB_LAYER_INGESTION_PHYSICAL_SCHEMA_DECISION_01.md)
- L'historique par run dans LocalCMS (hors scope Phase 1)
- L'extension LocalCMS vers un dashboard multi-source (hors scope)
- La modification du pipeline OpenClaw (hors scope)
```

---

## Décision de suite

```text
DECISION_RECOMMANDEE :
  Ouvrir GO_OPENCLAW_OPT_TRADING_ORCHESTRATOR_CHILD_LOCALCMS_OBSERVATION_VIEW_IMPL_01
  avec scope minimal (Option A) + dashboard (Option C) si périmètre accepté.

CONDITION :
  Attendre seuil Phase 1 (≥2026-05-30) avant implémentation,
  OU décider d'implémenter maintenant si l'éligibilité doit être lisible
  pendant l'observation (recommandé).
```

L'implémentation maintenant est préférable : voir l'éligibilité progresser
pendant l'observation est plus utile qu'après le seuil.

## RISKS

- À qualifier.
