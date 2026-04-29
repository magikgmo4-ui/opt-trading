# 20_INTEGRATION_PLAN

## Architecture cible

OpenClaw
  ↓
web3_data_adapters (module opt-trading)
  ↓
Providers (Chainbase / Covalent / Graph)
  ↓
Normalized JSON
  ↓
risk_engine / probability_engine / desk_pro

## Règles strictes

- Aucun appel direct fournisseur depuis runtime trading
- Adapter layer obligatoire
- Format JSON normalisé unique
- Gestion fallback provider

## Module cible

modules/web3_data_adapters/
  - app/
  - adapters/
  - schema/
  - scripts/

## Plan d'implémentation futur

1. Adapter Covalent (balances / tx)
2. Adapter Chainbase (MCP / agents)
3. Adapter Graph (requêtes ciblées)
4. Normalisation commune
5. CLI test

## Risques

- API instability
- Rate limits
- Vendor lock-in

## Mitigation

- Multi-provider
- Cache local
- Fail-open
