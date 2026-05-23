---
doc_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01_NEXT_PATCHES
doc_type: decision_next_patches
repo: opt-trading
project: opt-trading
module: collectors
go_id: GO_OPT_TRADING_COLLECTORS_CHILD_PROVIDER_COVERAGE_REPORT_01
parent_go_id: GO_OPT_TRADING_COLLECTORS_PARENT_API_NORMALIZATION_01
status: open
surface: docs/chantiers
source_kind: canonical
created_at: 2026-05-23
updated_at: 2026-05-23
---

# 40_NEXT_PATCHES

## Objet

Decision sur les prochains patches apres validation de la couverture provider/metric documentee dans ce child.

---

## Etat de la decision

Basee sur le rapport `10_PROVIDER_COVERAGE_REPORT.md` et les tests `30_MARKET_METRICS_SCHEMA_TESTS.md` :

| Critere | Etat |
|---|---|
| Fixtures Bitget PASS schema | OUI |
| Fixtures Binance Derivatives PASS schema | OUI |
| Coinglass adapter prouve | NON |
| Liquidations prouvees sur un provider | NON |
| market_metrics.v1 materialise runtime | NON — doc uniquement |
| Desk Pro consumer read-only implemente | NON |

---

## Patches recommandes — priorite A

### PATCH-A1 : materialiser market_metrics.v1 schema/fixtures en Python

**Pourquoi maintenant** : les fixtures sont documentees et validees (Bitget, Binance). Le schema est fige. Le prochain pas logique est de creer le module Python de serialisation/validation `market_metrics.v1`.

Scope :
- `modules/derivatives_collector/app/market_metrics_v1.py` (ou `packages/collectors_core/`)
- Classe ou dataclass `MarketMetricsV1` avec validation des invariants
- Serialisation vers JSON
- Tests unitaires contre les fixtures de `20_FIXTURE_MATRIX.md`

Critere de PASS : les fixtures Bitget et Binance Derivatives passent la validation Python sans erreur.

Critere de BLOCKED : ne pas implanter avant merge du parent #663 dans `sot/mainline` (ou rebase explicite).

### PATCH-A2 : Desk Pro read-only consumer

**Pourquoi** : le contrat `market_metrics.v1` est documente. Desk Pro peut lire `data/deskpro/inputs/market_metrics/latest.json` sans ecriture DB.

Scope :
- `modules/desk_pro/` : ajouter lecture `market_metrics.v1` latest
- Pas d'ecriture DB, pas de Sheets, pas de Telegram
- Tests: verifier que la lecture echoue proprement si `latest.json` absent

Prerequis : PATCH-A1 termine et valide.

---

## Patches recommandes — priorite B

### PATCH-B1 : adapter Bitget long_short_ratio

**Pourquoi** : Bitget expose l'endpoint long/short ratio mais l'adapter ne le lit pas. Combler ce gap monterait Bitget de 3 a 4 metriques.

Scope :
- `modules/derivatives_collector/app/bitget_adapter.py`
- Ajouter appel endpoint `/api/v2/mix/market/account-long-short-ratio`
- Propager vers `DerivativesRow.long_short_ratio`
- Mise a jour du rapport coverage : Bitget passe de 3 a 4 metriques

Critere de PASS : fixture TC-BITGET-01 mise a jour avec `long_short_ratio` non null.

### PATCH-B2 : Coinglass adapter reel

**Pourquoi** : les liquidations sont le seul gap structurel qui reste apres Bitget LSR. Coinglass est le provider canonique.

Scope :
- Creer `modules/derivatives_collector/app/coinglass_adapter.py`
- Endpoints : liquidations (long/short), optionnellement LSR et OI
- Authentification Coinglass API key (`.env`)
- Tests smoke avec cle sandbox ou mock

Critere de PASS : fixture TC-COINGLASS-01 avec adapter reel, liquidations non nulles.
Critere de BLOCKED : necessite cle API Coinglass ; ne pas faker les donnees.

### PATCH-B3 : Binance liquidations

**Pourquoi** : l'endpoint `/fapi/v1/forceOrders` existe mais n'est pas implemente dans l'adapter.

Scope :
- `modules/derivatives_collector/app/binance_derivatives_adapter.py`
- Ajouter lecture `forceOrders` (liquidations long + short)
- Propager vers `DerivativesRow.liquidations_long` et `.liquidations_short`

Critere de PASS : fixture TC-BINANCE-DERIV-02 mise a jour avec liquidations non nulles.

---

## Decision

**Prochain patch recommande : PATCH-A1** (materialiser `market_metrics.v1` en Python).

Raison : les fixtures sont valides et le schema est fige. Le passage de doc a code est la prochaine etape la moins risquee. Elle ne necessite pas de cle API externe et peut etre livree en child GO borde.

**PATCH-A2** vient immediatement apres PATCH-A1, une fois le schema Python valide.

**PATCH-B1, B2, B3** sont des ameliorations de couverture — utiles mais non bloquantes pour Desk Pro read-only.

---

## Child GOs proposes

```text
GO_OPT_TRADING_COLLECTORS_CHILD_MARKET_METRICS_CONTRACT_01    — PATCH-A1
GO_OPT_TRADING_COLLECTORS_CHILD_DESKPRO_READONLY_CONSUMER_01  — PATCH-A2
GO_OPT_TRADING_COLLECTORS_CHILD_BITGET_LSR_PATCH_01           — PATCH-B1
GO_OPT_TRADING_COLLECTORS_CHILD_COINGLASS_ADAPTER_01          — PATCH-B2
GO_OPT_TRADING_COLLECTORS_CHILD_BINANCE_LIQUIDATIONS_01       — PATCH-B3
```

Ordre recommande : A1 → A2 → (B1 ou B2 ou B3 en parallele selon disponibilite cle API).
