# reseau_ssh — Step 2 Pack (SSH + Firewall + WireGuard)

Objectif: standardiser l’accès SSH + durcissement minimal + pare-feu (UFW) + Fail2Ban + WireGuard (overlay VPN) entre tes machines.

Ce pack est **idempotent**: tu peux relancer les commandes sans casser la conf (les fichiers modifiés sont sauvegardés dans `/var/backups/reseau_ssh/`).

## Machines (inventaire)
- **student** (Debian 12): `student@192.168.16.103`
- Les autres IPs peuvent être différentes chez toi. Le module te laisse les renseigner plus tard sans bloquer.

## Installation (Linux Debian/Ubuntu)
1) Dézippe le pack sur la machine (ou copie-le dans `/tmp`)
2) Installe le module:
```bash
cd modules/reseau_ssh/reseau_ssh_step2
sudo bash install_reseau_ssh.sh
```
3) Lance le menu:
```bash
menu-reseau_ssh
```

## Actions conseillées (ordre)
### A) Bootstrap sécurité (par machine Linux)
Dans le menu:
- `Bootstrap (packages + UFW + Fail2Ban)`
- `SSH hardening SAFE (ne casse pas les logins)`
- `Sanity check`

### B) Clé SSH unique (recommandé)
- Génère une clé ed25519 (si pas déjà fait) sur **Windows** OU sur une machine Linux.
- Ajoute la clé publique sur toutes les machines:
  - Linux: `ssh-copy-id user@host`
  - Windows OpenSSH Server: utilise le script PowerShell fourni (voir `windows/README_Windows.md`).

### C) WireGuard (overlay VPN LAN)
Le module fournit 2 modes:
- **Hub**: `admin-trading` comme serveur WireGuard, les autres comme clients.
- **LAN-only**: si tout est sur le même réseau, WireGuard sert surtout à **chiffrer** et créer une IP stable (10.66.66.x).

Dans le menu:
- Sur le serveur: `WG server init`
- Sur chaque client: `WG client init (génère un fichier .conf à importer)`
- Ajoute les peers côté serveur: `WG add peer`

> Important: **ne coupe pas PasswordAuthentication** tant que tu n’as pas validé que ta clé SSH marche partout.

## Fichiers / scripts principaux
- `reseau_ssh_menu.sh` : menu interactif
- `reseau_ssh_cmd.sh` : commandes non-interactives (automatisables)
- `sanity_reseau_ssh.sh` : diagnostic rapide
- `windows/` : scripts PowerShell (OpenSSH + firewall + WireGuard)
- `templates/` : snippets sshd/fail2ban

## Journal (à coller dans ton journal /opt/trading/journal)
Voir `journal/2026-03-01_go_network.md`.
