---
doc_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01_MATRIX
doc_type: audit_matrix
repo: opt-trading
project: opt-trading
go_id: GO_OPT_TRADING_RESEAU_SSH_LEGACY_COMMANDS_RETIRE_OR_REHOME_01
status: pass
mode: doc-only
surface: modules
source_kind: repo_read
machine_owner: db-layer
---

# 91_LEGACY_COMMANDS_MATRIX

## Matrix

| Command | Current implementation | Canonical replacement | Decision |
| --- | --- | --- | --- |
| `wg-server-init` | creates `/etc/wireguard/wg0.conf`, keypair, sysctl, starts `wg-quick@wg0` | `wg-genkeys`, `wg-render`, `wg-apply`, `wg-up`, `wg-status` | retire |
| `wg-client-init` | creates client `/etc/wireguard/wg0.conf` with placeholder server pubkey | `wg-genkeys`, `wg-showpub`, hub pubkey exchange, `wg-render`, `wg-apply`, `wg-up`, `wg-status` | retire |
| `wg-add-peer` | appends peer blocks directly into `/etc/wireguard/wg0.conf` | peer pubkeys in `/opt/trading/data/reseau_ssh/wireguard/peers/` then `wg-render` and `wg-apply` | retire |

## Technical reasoning

- legacy commands mutate live config directly in a `wg0.conf` model
- canonical implementation uses inventory-driven rendering into `wg-mgmt.conf`
- both models should not coexist as first-class supported operator paths

## Verdict

`PASS`
