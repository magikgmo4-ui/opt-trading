---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_VALIDATION
doc_type: validation_matrix
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 70_VALIDATION_MATRIX.md

Matrice de validation pour le pipeline complet.

## 1_VALIDATION_PAR_ETAGE

### INPUT

| Critère | Acceptable | Test |
|---------|-----------|------|
| URL catalogue documenté | Oui | Lire 10_INPUT_SURFACES_INVENTORY.md |
| Priorités assignées | Oui | Vérifier colonne Priorité |
| Types de page définis | Oui | Vérifier colonne Type de page |
| Assets couverts | Au moins BTC, ETH, Gold, Oil, DXY | Vérifier liste |
| Screeners listés | Au moins biggest caps, AI, defense | Vérifier liste |
| Coinglass screens listés | Heatmap, funding, OI, L/S | Vérifier liste |

### CAPTURE

| Critère | Acceptable | Test |
|---------|-----------|------|
| Screen types définis | Au moins 6 | Voir 20_CAPTURE_CONTRACT.md §1 |
| Viewport spécifié | 1920x1080 minimum | Voir §3 |
| Timeframes listés | 1m, 5m, 15m, 1h, 4h, 1D | Voir §5 |
| Indicateurs minimum listés | EMA20/50/200, VWAP, Volume, RSI, MACD | Voir §6 |
| Triggers horaires définis | 8 fenêtres | Voir §4 plan fixe |
| Triggers événementiels définis | Prix, liquidité, macro, screener | Voir §4 triggers |
| Métadonnées capture spécifiées | JSON complet | Voir §2 |

### ANALYSIS

| Critère | Acceptable | Test |
|---------|-----------|------|
| Analyseur par screen type | 6 analyseurs | Voir 30_ANALYSIS_CONTRACT.md §2 |
| Champs de sortie par type | Définis | Voir §2.1 – §2.6 |
| Format JSON générique | Défini | Voir §3 |
| Confidence score défini | [0.0, 1.0] | Voir §5 |
| Méthodes d'analyse listées | OCR, LLM, etc. | Voir §4 |

### OUTPUTS

| Critère | Acceptable | Test |
|---------|-----------|------|
| Raw image | Oui | Voir 40_OUTPUTS_AND_PAYLOADS.md §2 |
| Annotated image | Défini | Voir §3 |
| Textual analysis JSON | Défini | Voir §4 |
| Setup summary JSON | Défini | Voir §5 |
| Telegram payload | Format défini | Voir §6 |
| Structured data payload | Format défini | Voir §7 |
| Règles de filtrage Telegram | Définies | Voir §8 |

### DATA CENTER

| Critère | Acceptable | Test |
|---------|-----------|------|
| Catégories de payload | 4 définies | Voir 50_DATA_CENTER_HANDOFF.md §2 |
| Schema max data out | Défini | Voir §3 |
| Endpoints listés | 4 endpoints | Voir §4 |
| Retry policy définie | Oui | Voir §5 |
| Volumétrie estimée | Oui | Voir §6 |
| Rétention définie | Oui | Voir §7 |

### DESKPRO

| Critère | Acceptable | Test |
|---------|-----------|------|
| Contrat consommateur défini | Oui | Voir 60_DESKPRO_CONSUMPTION.md §1 |
| Formats consommés listés | desk_snapshot, vision_analysis, setup_card | Voir §2 |
| Champs attendus listés | Par priorité | Voir §3 |
| Flux d'intégration défini | Oui | Voir §4 |
| Gap analysis vs V1 | 5 contrats évalués | Voir §5 |
| Vues DeskPro ciblées | 6 vues | Voir §6 |
| Format vision_analysis | Défini | Voir §7 |
| Format setup_card | Défini | Voir §8 |

## 2_VALIDATION_DE_LIVRABILITE

| Livrable | Critère de succès |
|----------|-------------------|
| 00_SCOPE_AND_OBJECTIVE.md | Pipeline canonique documenté, périmètre clair |
| 10_INPUT_SURFACES_INVENTORY.md | Catalogue complet, priorisé, par source |
| 20_CAPTURE_CONTRACT.md | Types, viewport, timeframes, triggers, métadonnées spécifiés |
| 30_ANALYSIS_CONTRACT.md | Analyseurs par type, champs de sortie, confidence, méthodes |
| 40_OUTPUTS_AND_PAYLOADS.md | 6 types d'output, formats, règles de filtrage |
| 50_DATA_CENTER_HANDOFF.md | Schéma max data out, endpoints, retry, volumétrie, rétention |
| 60_DESKPRO_CONSUMPTION.md | Contrat DeskPro, formats, champs, gap analysis, vues |
| 70_VALIDATION_MATRIX.md | Critères de validation pour chaque étage |
| 80_GAPS_AND_NEXT_GO.md | Gaps restants, prochaines actions |

## 3_TEST_PLAN_SUMMARY

| Test | Scope | Méthode |
|------|-------|---------|
| Smoke capture | 1 asset, 1 timeframe | Exécuter capture Playwright |
| Analyse LLM | 1 screenshot | Appel API analyse |
| Output JSON | 1 analyse complète | Valider JSON output |
| Data Center POST | 1 payload | POST vers DC (mock si nécessaire) |
| DeskPro read | 1 fichier analysis | Lire depuis DeskPro |
| Telegram send | 1 message | Envoyer test Telegram |
