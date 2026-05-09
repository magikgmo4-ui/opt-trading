---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01_INSTALLATION
doc_type: installation_steps
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_AUTOMATION_TIMER_INSTALL_GATED_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-09
---

# 20_INSTALLATION_STEPS - Installation Steps

## Actions systeme executees

```bash
sudo install -m 0644 modules/desk_pro/systemd/desk_pro_dry_run.service /etc/systemd/system/desk_pro_dry_run.service
sudo install -m 0644 modules/desk_pro/systemd/desk_pro_dry_run.timer /etc/systemd/system/desk_pro_dry_run.timer
sudo systemctl daemon-reload
sudo systemctl enable desk_pro_dry_run.timer
```

## Fichiers installes

- `/etc/systemd/system/desk_pro_dry_run.service`
- `/etc/systemd/system/desk_pro_dry_run.timer`

## Verification de conformite

```text
service sha256 source = d6a985ab29d45b8f27669abfd8470b53853ee5cb1951c0808c2173459f1df030
service sha256 dest   = d6a985ab29d45b8f27669abfd8470b53853ee5cb1951c0808c2173459f1df030
timer sha256 source   = 74586381633bfed1aabb31db63b770f7eb2b7f999c52be5267d404335af4c912
timer sha256 dest     = 74586381633bfed1aabb31db63b770f7eb2b7f999c52be5267d404335af4c912
```

## Gating applique

- installation effectuee
- `daemon-reload` effectue
- timer `enabled`
- timer non demarre manuellement
- service non demarre manuellement
