# reseau_fix v1 — Normalisation LAN / SSH / UFW / WireGuard (SAFE d’abord)

Objectif: appliquer une baseline cohérente sur:
- admin-trading (serveur WireGuard wg0 + wg-mgmt)
- student (client wg-mgmt)
- db-layer (client wg-mgmt, UFW à activer)

Le module est **idempotent** et fait des backups timestampés avant d’écrire.
