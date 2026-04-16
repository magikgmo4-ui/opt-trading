# reseau_ssh — Step 1 (Inventory + SSH baseline)

## Family status (reseau_ssh*)
- Legacy / doc pre-step (does not carry active continuity)
- Canonical survivor (active continuity): `reseau_ssh_step2`
- Kept prerequisite: `reseau_ssh_step1b` (apply baseline before Step 2)
- Reference decision: `docs/chantiers/GO_OPT_TRADING_RESEAU_SSH_CONSOLIDATION_03/00_cadrage.md`

Goal of Step 1:
- Single source of truth inventory for 4 machines (names, users, LAN IPs)
- Consistent SSH aliasing scheme (same ~/.ssh/config on every Linux host)
- Scripts (sanity/cmd/menu) to validate connectivity + hostname basics
- WireGuard + Firewall plan placeholders (Step 2+)

This step does NOT change your system automatically. It produces:
- `hosts.yaml` inventory to fill
- SSH config templates
- Commands to apply safely per machine in Step 1b/Step 2
