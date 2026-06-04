"""
analysis_bundles — producteur de bundles d'analyse multi-source.

Chaque bundle agrège des inputs hétérogènes (market_metrics, Coinglass OCR,
Telegram signals) en un contrat JSON canonique consommable par l'Analysis Consumer.

Bundles actifs:
    btc_core.v1          — BTC (market_metrics + coinglass + telegram)
    macro.v1             — DXY + Gold (dégradé: VIX/SPX/US10Y absents)

Bundles en hypothèse:
    energy_oil.v1        — Brent/WTI (symboles non validés)

Invariants:
    - Chaque bundle a un contrat 'bundle.<name>.v1'
    - fresh_state = FRESH si toutes sources < cadence/2
    - fresh_state = STALE si au moins une source > cadence
    - missing_inputs n'est jamais vide si fresh_state = STALE
    - confidence = LOW si au moins une source STALE
"""
