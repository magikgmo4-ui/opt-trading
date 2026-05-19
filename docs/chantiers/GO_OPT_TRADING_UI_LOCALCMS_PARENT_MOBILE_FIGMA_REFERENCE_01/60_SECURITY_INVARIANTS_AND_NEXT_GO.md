---
doc_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01_SECURITY_NEXT_GO
doc_type: security_and_next_go
repo: opt-trading
project: opt-trading
module: ui_localcms_figma
go_id: GO_OPT_TRADING_UI_LOCALCMS_PARENT_MOBILE_FIGMA_REFERENCE_01
status: open
lifecycle_stage: next_go
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-19
topic_keys:
  - security
  - invariants
  - next-go
  - figma
  - localcms
---

# 60_SECURITY_INVARIANTS_AND_NEXT_GO

## Invariants sécurité

```text
NO_SECRET_IN_GIT
NO_FIGMA_AS_CANON
NO_FIGMA_RUNTIME
NO_MCP_THIRD_PARTY_UNAUDITED
NO_TRADE_FROM_FIGMA
NO_TRADE_FROM_STREAM_DECK
NO_PROD_WRITE_FROM_MCP
NO_GLOBAL_INDEX_AUTO
NO_DESKPRO_LOCALCMS_CONFUSION
NO_DIRECT_SIGNAL_TRADE
```

## Invariants produit

- LocalCMS = cockpit système/gouvernance read-only.
- Desk Pro = cockpit trading actif.
- Figma = référence design.
- Stream Deck = commandes safe bornées.
- RustDesk/RDP = intervention visuelle.
- Web cockpit = supervision permanente.
- Repo = source de vérité.

## Child GO recommandés

### Phase 1 — Design reference

```text
GO_OPT_TRADING_UI_LOCALCMS_CHILD_FIGMA_WIREFRAMES_01
```

Scope : créer ou référencer le fichier Figma, produire les wireframes LocalCMS mobile/web et documenter le lien repo.

```text
GO_OPT_TRADING_UI_LOCALCMS_CHILD_DESIGN_SYSTEM_COCKPIT_01
```

Scope : composants visuels, statuts, machines, couleurs, badges, cards.

```text
GO_OPT_TRADING_UI_LOCALCMS_CHILD_STREAM_DECK_SAFE_PROFILE_01
```

Scope : mapping visuel et documentaire du profil Stream Deck safe, sans automatisation destructive.

### Phase 2 — Code Connect

```text
GO_OPT_TRADING_UI_LOCALCMS_CHILD_CODE_CONNECT_MAPPING_01
```

Scope : relier composants Figma aux composants LocalCMS réels uniquement après stabilisation du code.

### Phase 3 — MCP Figma

```text
GO_OPT_TRADING_UI_LOCALCMS_CHILD_FIGMA_MCP_READONLY_HANDOFF_01
```

Scope : tester le MCP Figma en lecture / patch-draft, sans écriture prod.

## Ordre recommandé

```text
1. Figma wireframes
2. Design system cockpit
3. Stream Deck safe profile
4. LocalCMS components hardening
5. Code Connect mapping
6. MCP Figma read-only handoff
```

## Critères de fermeture du parent

- Tous les documents du parent existent.
- Les phases Code Connect/MCP sont différées et bornées.
- Les invariants sécurité sont explicites.
- L'entrée inbox existe.
- Aucun runtime, secret ou index global n'a été modifié.

## 17_RESUME_POINT

Reprendre depuis `00_INITIAL_PROJECT_DOC.md`, section `7_CANONICAL_STATE`, puis suivre l'ordre des child GO listés ci-dessus.
