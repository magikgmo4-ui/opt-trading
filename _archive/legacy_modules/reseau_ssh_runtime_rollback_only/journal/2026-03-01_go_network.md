# Journal — 2026-03-01 (America/Montreal) — go network

1) Objectif
- Reprendre le module réseau/SSH/WireGuard (reseau_ssh step 2+) pour standardiser l’accès entre machines + ajouter un overlay VPN WireGuard + firewall.

2) Livraison
- Pack ZIP `reseau_ssh_step2_pack.zip` contenant:
  - scripts Linux: menu/cmd/sanity + install + templates
  - scripts Windows: fix ACL authorized_keys + firewall LAN
  - README d’usage + ordre d’exécution conseillé

3) Plan d’exécution (next)
- Sur chaque machine Linux: installer le module -> bootstrap -> ssh-hardening-safe -> sanity.
- Côté Windows: corriger ACL de `authorized_keys` si nécessaire.
- WireGuard: choisir un hub (admin-trading) et initialiser server/client + ajout peers.

4) Commandes clés (Linux)
- `sudo bash install_reseau_ssh.sh`
- `menu-reseau_ssh`
- `sanity-reseau_ssh`
