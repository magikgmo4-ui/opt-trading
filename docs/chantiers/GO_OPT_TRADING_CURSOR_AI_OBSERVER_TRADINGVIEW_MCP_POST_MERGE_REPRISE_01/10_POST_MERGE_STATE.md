# 10_POST_MERGE_STATE — Etat post-merge

## 13_ESTABLISHED

### Merge

- PR #200 merged dans `sot/mainline` le 2026-05-05.
- Merge commit : `718490d`.
- 28 fichiers, +2562 insertions, 0 suppressions.

### Parents

- Parent produit ferme : `GO_OPT_TRADING_CURSOR_AI_OBSERVER_TRADINGVIEW_MCP_01` (CLOSED)
- Parent machine actif : `GO_OPT_TRADING_MACHINE_CURSOR_AI_PARENT_01` (ACTIVE)

### Produit livre

| Module | Fichiers | Description |
|--------|----------|-------------|
| `tradingview_observer/` | `cmd.ps1`, `sanity_check.ps1`, `observer_runner.ps1`, `export_bridge_packet.ps1`, `product_sanity.ps1`, `README.md`, `output/` | Wrapper read-only |
| `tradingview_observer_openclaw/` | `run.ps1`, `skill.md`, `README.md` | Skill OpenClaw safe |

### Decisions canoniques

- Option A retenue : bridge packet local manuel seulement.
- Option B shared folder documentee mais non activee.
- Option C ingestion admin-trading reservee a GO separe.
- Aucun transfert admin-trading actif.
- Webhook admin-trading inchange.
- Admin-trading runtime inchange.

### Securite

- Mutations TradingView verrouillees (flag `-AllowMutation` requis).
- OpenClaw n'accede jamais directement a CDP ou tradingview-mcp.
- Outputs live JSON ignores par git.
- Aucun secret, .env, token commis.
- Aucun trade reel.

## 14_HYPOTHESIS

- Le produit est utilisable depuis n'importe quel checkout de `sot/mainline` (tant que TradingView Desktop et tradingview-mcp sont installes).
- Le produit ne depend pas d'un parent non merge (seulement des fichiers dans mainline).

## Source de verite

`sot/mainline`, branche canonique du repo `opt-trading`.
