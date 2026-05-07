---
doc_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01_PRODUCT_STATUS_TAXONOMY
doc_type: taxonomy
repo: opt-trading
go_id: GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01
status: reference
lifecycle_stage: cadrage
source_kind: canonical
updated_at: 2026-05-07
---

# 01_PRODUCT_STATUS_TAXONOMY - Taxonomie produit canonique

## Statuts autorises

```text
PRODUCT_FINISHED
USABLE_NOW
USABLE_LIMITED
DOC_ONLY_READY
SIMULATED_PASS
NOT_USABLE_YET
DO_NOT_USE_LIVE
```

## Definitions

| Statut | Definition canonique |
| --- | --- |
| `PRODUCT_FINISHED` | Produit fini, prouve, documente, guide operateur present, usage borne et accepte. |
| `USABLE_NOW` | Produit utilisable maintenant pour son role actuel, meme si des ameliorations restent possibles. |
| `USABLE_LIMITED` | Produit utilisable, mais avec limites connues qui doivent etre explicites avant usage. |
| `DOC_ONLY_READY` | Documentation, spec ou cartographie suffisante pour comprendre la surface, sans droit de conclure a un usage runtime valide. |
| `SIMULATED_PASS` | Le passage est prouve en simulation ou smoke borne, pas en usage reel complet. |
| `NOT_USABLE_YET` | La surface ne doit pas etre utilisee actuellement. |
| `DO_NOT_USE_LIVE` | Interdiction explicite d'usage live ou reel, meme si la surface est documentee. |

## Regles de lecture

1. Un closeout `PASS` n'est pas un statut produit.
2. Un verdict `GO_LIMITED` peut apparaitre comme overlay de chantier, mais ne remplace pas un statut produit.
3. `DOC_ONLY_READY` ne peut pas etre promu vers `USABLE_NOW` sans preuve runtime ou usage operateur borne.
4. `SIMULATED_PASS` ne peut pas etre promu vers `PRODUCT_FINISHED` sans usage reel controle et preuve repo.
5. `NOT_USABLE_YET` et `DO_NOT_USE_LIVE` peuvent etre combines pour expliciter une interdiction forte.

## Regles de promotion

Une promotion de statut exige au minimum :
- une preuve repo lisible ;
- un closeout ou une evidence equivalente ;
- une clarification des limites restantes ;
- un guide mis a jour si le mode d'usage change.

## Regles d'ecriture

- Ne pas marquer Airtable `USABLE_NOW` tant que le bridge produit n'existe pas.
- Ne pas marquer Botpress `PRODUCT_FINISHED` tant que Telegram reel et le webhook reel ne sont pas valides.
- Ne pas marquer BTC COIN-M utilisable tant que le cadre mathematique reste draft et non valide.
- Ne pas retirer `USABLE_LIMITED` a ClickUp tant que les limites du plan gratuit structurent encore l'usage.
