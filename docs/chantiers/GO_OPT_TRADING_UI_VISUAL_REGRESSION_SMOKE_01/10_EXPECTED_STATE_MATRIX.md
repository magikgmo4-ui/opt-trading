# Expected UI State Matrix

Generated: 2026-05-19

## /desk/ui — éléments attendus dans la capture HTML

### Structure

| Élément | Sélecteur / Texte | Attendu |
|---------|-------------------|---------|
| Titre page | `<h1>Desk Pro` | présent |
| Action Panel | `id="actionPanel"` | présent |
| Bouton Refresh Status | `id="btnStatus"` | présent |
| Bouton Test Alert | `id="btnTestAlert"` | présent |
| Lien errors | `href="/desk/errors"` | présent |
| Lien alerts | `href="/desk/alerts"` | présent |
| Lien logs | `href="/desk/logs/latest"` | présent |
| Lien toolbox | `href="/desk/toolbox"` | présent |
| Lien localcms | `href="http://127.0.0.1:8000"` | présent |
| Note conflit port 8000 | `id="portConflictNote"` | présent |
| Section Runtime Health | `id="runtimeHealthCard"` | présent |
| Résumé Pipeline | `id="pipelineSummary"` | présent |
| Error Diagnostics | `id="errorDiagnostics"` | présent |
| Raw JSON | `id="pipelineStatus"` | présent |
| Analysis Tools | `id="analysisTools"` | présent |
| Form card | `id="formCard"` | présent |
| Snapshot table | `id="snapTable"` | présent |
| JS guidance | `id="healthGuidance"` (dans JS) | dans source |
| JS titre dynamique | `document.title` | dans source |
| Media query responsive | `max-width:900px` | dans source |

### Badges et états

| État système | Badge attendu | Couleur |
|-------------|---------------|---------|
| `healthy` | `HEALTHY` | `#2e7d32` vert |
| `degraded` | `DEGRADED` | `#e65100` orange |
| `down` | `DOWN` | `#c62828` rouge |
| check:pass | badge vert | `#2e7d32` |
| check:warn | `WARN` | `#e65100` |
| check:fail | valeur fail | `#c62828` |

### Guidance contextuelle

| Cause health=down/degraded | Message attendu dans JS |
|---------------------------|------------------------|
| `webhook_activity` | "Aucun signal TradingView récent" |
| `webhook` | "Port 8000 injoignable" |
| `perf` | "Module Perf injoignable" |
| `probe_errors` | "consulter /desk/errors" |

---

## /desk/toolbox — éléments attendus

| Élément | Attendu |
|---------|---------|
| HTTP 200 | oui |
| Contenu HTML | > 1 000 octets |
| Contenu non vide | oui |

---

## /desk/status — champs JSON attendus

| Champ | Attendu |
|-------|---------|
| `desk_pro.ok` | `true` |
| `health.status` | `"down"` ou `"degraded"` ou `"healthy"` |
| `health.checks` | array non vide |
| `error_count` | entier >= 0 |
| `ts` | ISO timestamp |

---

## /desk/errors — format attendu

```json
{"ok": true, "count": N, "errors": [...]}
```

---

## Matrice régression visuelle — checksum desk_ui.html

Le SHA-256 du snapshot `desk_ui.html` change si la structure de la page change.  
Mettre à jour `00_SMOKE_MANIFEST.md` après chaque GO qui modifie `page.py`.

Baseline actuelle : `9e6d8a913978345c0f84c3da1df47d575a11eaf3e43019ff82c87a462c2bd8af`
