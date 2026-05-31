---
doc_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01_GAPS
doc_type: gaps_and_next_go
repo: opt-trading
go_id: GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_INPUT_CAPTURE_ANALYSIS_OUTPUT_PIPELINE_01
---

# 80_GAPS_AND_NEXT_GO.md

Gaps restants et prochaines actions concrètes.

## 1_REMAINING_GAPS

### Input gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-IN-01 | URLs TradingView exactes non stabilisées (paramètres, indicateurs, layout) | P0 | OPEN |
| G-IN-02 | URLs Coinglass exactes non stabilisées (sections, filtres) | P0 | OPEN |
| G-IN-03 | Mapping URL → screen_type non automatisé | P1 | OPEN |
| G-IN-04 | Screener TV : colonnes et filtres non figés | P1 | OPEN |
| G-IN-05 | Format d'entrée pour les sources "news" non défini | P2 | OPEN |

### Capture gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-CAP-01 | Playwright : profiles.json existants à valider pour toutes les URLs | P0 | OPEN |
| G-CAP-02 | Multi-section capture non implémentée | P1 | OPEN |
| G-CAP-03 | Crop zone par section non défini en configuration | P1 | OPEN |
| G-CAP-04 | Capture timeout / retry non testé pour toutes les pages | P1 | OPEN |
| G-CAP-05 | Viewport response design : vérifier que toutes les pages rendent correctement en 1920x1080 | P1 | OPEN |

### Analysis gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-AN-01 | Pipeline OCR non branché | P0 | OPEN |
| G-AN-02 | Analyseur LLM vision non intégré | P0 | OPEN |
| G-AN-03 | Analyseur par screen_type non implémenté (tous à faire) | P0 | OPEN |
| G-AN-04 | Format analyse JSON non testé contre un vrai output | P1 | OPEN |
| G-AN-05 | Score de confiance non calibré | P2 | OPEN |

### Output gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-OUT-01 | Annotated image generator non implémenté | P1 | OPEN |
| G-OUT-02 | Setup detection non implémentée | P1 | OPEN |
| G-OUT-03 | Règles de filtrage Telegram non codées | P1 | OPEN |
| G-OUT-04 | Structured data payload non produit | P1 | OPEN |

### Data Center gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-DC-01 | Endpoint Data Center vision non existant | P0 | OPEN |
| G-DC-02 | Schéma max data out non validé avec l'équipe Data Center | P1 | OPEN |
| G-DC-03 | Fallback local non implémenté | P2 | OPEN |
| G-DC-04 | Retry policy non codée | P2 | OPEN |

### DeskPro gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-DP-01 | vision_analysis.json non produit sur le disque DeskPro | P0 | OPEN |
| G-DP-02 | setup_card.json non produit | P1 | OPEN |
| G-DP-03 | DeskPro runtime non notifié des mises à jour | P1 | OPEN |
| G-DP-04 | Vue DeskPro "analysis" non implémentée | P2 | OPEN |
| G-DP-05 | Vue DeskPro "setups" non implémentée | P2 | OPEN |

### Integration gaps

| # | Gap | Priorité | Status |
|---|-----|----------|--------|
| G-INT-01 | Pipeline complet non testé end-to-end | P0 | OPEN |
| G-INT-02 | Pas de smoke test pour le pipeline élargi | P1 | OPEN |
| G-INT-03 | Pas de monitoring / alerting sur le pipeline | P2 | OPEN |
| G-INT-04 | Documentation des profiles.json non synchronisée avec le nouveau scope | P1 | OPEN |

## 2_NEXT_ACTIONS_IMMEDIATES

| # | Action | Responsable | Priorité |
|---|--------|-------------|----------|
| A-01 | Valider les URLs TradingView avec les profiles Playwright existants | — | P0 |
| A-02 | Valider les URLs Coinglass avec les profiles Playwright existants | — | P0 |
| A-03 | Brancher l'analyseur LLM vision sur une capture réelle | — | P0 |
| A-04 | Produire un premier payload structuré vers Data Center (mock) | — | P0 |
| A-05 | Écrire vision_analysis.json vers le répertoire DeskPro | — | P0 |

## 3_NEXT_GO_RECOMMANDE

```text
GO_OPT_TRADING_BOT_VISION_HEADLESS_CHILD_PIPELINE_IMPL_POC_01
```

Objectif : POC fonctionnel du pipeline complet sur un actif unique (BTCUSDT 15m).

Livrables :
1. Capture Playwright validée sur TV BTCUSDT 15m
2. Analyse LLM/OCR sur le screenshot
3. Production du JSON vision_analysis
4. Production du payload Data Center
5. Test Telegram avec le résultat
6. Écriture desk/analysis/btcusdt.latest.json

## 4_MILESTONES

| Milestone | Cible | Description |
|-----------|-------|-------------|
| M1 | J+7 | POC BTCUSDT 15m fonctionnel |
| M2 | J+14 | Extension à 5 actifs (BTC, ETH, Gold, Oil, DXY) |
| M3 | J+21 | Ajout Coinglass (liquidation + funding) |
| M4 | J+28 | Ajout screener actions |
| M5 | J+35 | Intégration Data Center complète |
| M6 | J+42 | Intégration DeskPro complète |
| M7 | J+49 | Tests E2E + documentation finale |

## 5_CLOSE_GATE_CONDITIONS

Le présent child GO pourra être clos quand :

- [ ] 10_INPUT_SURFACES_INVENTORY.md est validé avec les URLs réelles
- [ ] 20_CAPTURE_CONTRACT.md est respecté par l'implémentation
- [ ] 30_ANALYSIS_CONTRACT.md est respecté par l'implémentation
- [ ] 40_OUTPUTS_AND_PAYLOADS.md est respecté
- [ ] Au moins un POC fonctionnel (M1) est livré et documenté
- [ ] Les gaps prioritaires (P0) ont un plan d'action
- [ ] Le prochain GO child est défini
