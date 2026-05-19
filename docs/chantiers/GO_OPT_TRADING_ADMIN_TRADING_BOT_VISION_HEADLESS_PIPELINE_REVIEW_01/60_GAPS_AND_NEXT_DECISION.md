---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01_GAPS_DECISION
doc_type: gaps_and_decision
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 60_GAPS_AND_NEXT_DECISION - Gaps and Next Decision

## Gaps classés

### Tracked source gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-TS-01 | `modules/bot_vision/headless_capture/` n'est pas suivi Git (dans `.gitignore` ou absent) | MEDIUM | OPEN |
| G-TS-02 | `node_modules/` non installé — `playwright` manquant | HIGH | OPEN (cause du fail) |
| G-TS-03 | `profiles.example.json` contient un seul profil (BTCUSDT.P) | LOW | OPEN |

### Runtime unit gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-RU-01 | `bot-vision-headless-capture.service` en état `failed` à chaque trigger | HIGH | OPEN |
| G-RU-02 | `headless_capture/` en quarantaine sous `/tmp/opt-trading-quarantine/` | MEDIUM | DOCUMENTED |
| G-RU-03 | Le fichier tracked `modules/bot_vision/headless_capture/capture_headless.js` existe mais le service appelle un chemin qui nécessite `node_modules/` | HIGH | OPEN |

### Artifact schema gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-AS-01 | Sidecar JSON actuel n'a pas de `capture_id` | LOW | RESOLVABLE |
| G-AS-02 | Sidecar JSON actuel n'a pas de `payload_hash` | LOW | RESOLVABLE |
| G-AS-03 | Sidecar JSON actuel n'a pas de `signal_event_ref` | LOW | EXPECTED (futur) |
| G-AS-04 | Sidecar JSON actuel n'a pas de `desk_snapshot_ref` | LOW | EXPECTED (futur) |

### Metadata gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-MD-01 | `latest.json` a `source: null` et `host: null` pour toutes les entrées | LOW | OPEN |
| G-MD-02 | Le sidecar JSON n'est pas propagé dans `latest.json` par `desk_snapshot_ingest` | LOW | OPEN |
| G-MD-03 | Normalisation symbol: `BTCUSDT` (webhook) vs `BTCUSDT.P` (capture) | MEDIUM | OPEN |

### Freshness gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-FR-01 | Pas de règle de fraîchesse documentée pour `visual_context` | MEDIUM | RESOLVABLE |
| G-FR-02 | `desk_bridge` traite le fichier le plus récent sans vérifier l'âge | LOW | OPEN |
| G-FR-03 | `headless_capture` ne produit qu'un seul BTCUSDT.P — les 3 autres symboles viennent du crop ShareX | MEDIUM | OPEN |

### desk_bridge compatibility gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-DB-01 | `desk_bridge` ne lit pas le sidecar JSON — métadonnées V1 perdues | LOW | OPEN |
| G-DB-02 | Le mapping 2x2 quadrants est hardcodé (BTC, XAU, SOL, ETH) | LOW | DOCUMENTED |
| G-DB-03 | `desk_bridge` suppose un screenshot 2x2 ShareX — incompatible avec headless single-symbol | MEDIUM | OPEN |

### Desk Pro readiness gaps

| Gap | Description | Severity | Status |
| --- | --- | --- | --- |
| G-DP-01 | Desk Pro dernier run 2026-04-05 (> 1 mois) | MEDIUM | DOCUMENTED (40_DEPENDENCIES_AND_GAPS.md) |
| G-DP-02 | `shared/desk_pro/latest/` n'existe pas | MEDIUM | OPEN |
| G-DP-03 | Contrat d'entrée Desk Pro non formalisé | MEDIUM | FUTURE GO |
| G-DP-04 | Desk Pro ne peut pas consommer `visual_context` sans `desk_snapshot` | LOW | EXPECTED |

## Décision

### Verdict: PASS

Le contrat `visual_context` V1 peut être défini proprement. Les artefacts de la pipeline sont observables et documentables. Les gaps identifiés sont des lacunes d'implémentation, pas des blocages contractuels.

### Raisonnement

1. **Le format PNG + JSON metadata est établi**: `capture_headless.js` produit des artefacts avec sidecar JSON couvrant les champs principaux
2. **Les règles de compatibilité desk_bridge sont formulables**: gardes anti `.uploading` et 0-byte documentées, flux crop 2x2 documenté
3. **Le passage visual_context → desk_snapshot est documenté**: `desk_snapshot_ingest` transforme les fichiers inbox en `latest.json` + PNG dans `desk/snapshots/`
4. **Le gap critique (playwright manquant) est un gap d'implémentation**, pas un gap contractuel — le contrat V1 est valide indépendamment de l'état runtime

### Prochain GO

```
GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01
```

Ce GO consommera les contrats `signal_event` V1, `visual_context` V1 et `desk_snapshot` pour auditer Desk Pro comme consumer final.

### Si FAIL/BLOCKED

Non applicable — le verdict est PASS.
