# SSH Key Generation Guide — Termux → Fleet

## 1. Génération

Le bootstrap (`bootstrap.sh`) génère automatiquement une clé Ed25519 :

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_termux -N "" -C "termux_$(date +%Y%m%d)"
```

Génération manuelle (si besoin de recréer) :

```bash
ssh-keygen -t ed25519 -f ~/.ssh/id_ed25519_termux -N "" -C "termux_manual"
chmod 600 ~/.ssh/id_ed25519_termux
```

## 2. Afficher la clé publique

```bash
cat ~/.ssh/id_ed25519_termux.pub
```

## 3. Propager sur la flotte

**Depuis db-layer** (autorise la clé sur toutes les machines) :

```bash
bash /opt/trading/modules/termux_operator/scripts/authorize_termux_key.sh "ssh-ed25519 AAAA... termux_YYYYMMDD"
```

**Manuellement** (machine par machine) :

```bash
# Sur chaque machine distante
echo "ssh-ed25519 AAAA... termux_YYYYMMDD" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

## 4. SSH config

Le bootstrap écrit `~/.ssh/config` avec :

```
Host *
  ServerAliveInterval 30
  ServerAliveCountMax 3
  TCPKeepAlive yes
  IdentitiesOnly yes
  IdentityFile ~/.ssh/id_ed25519_termux
  StrictHostKeyChecking accept-new

Host db-layer
  HostName 192.168.0.100
  User ghost

Host admin-trading
  HostName 192.168.0.111
  User ghost

Host fantome
  HostName 192.168.0.191
  User fantome

Host student
  HostName 192.168.0.142
  User student
```

Ajuster les IP/noms si nécessaire.

## 5. Test SSH depuis Termux

```bash
ssh -o BatchMode=yes db-layer 'hostname'
ssh -o BatchMode=yes admin-trading 'hostname'
ssh -o BatchMode=yes fantome 'hostname'
ssh -o BatchMode=yes student 'hostname'
```

Toutes doivent répondre sans prompt de mot de passe.

## 6. Sécurité

- Clé privée jamais partagée
- Jamais de passphrase stockée dans Tasker
- `~/.ssh/` en mode 700
- `~/.ssh/id_ed25519_termux` en mode 600
- Rotation recommandée : générer une nouvelle clé tous les 6 mois
- En cas de compromission : supprimer la clé des `authorized_keys` de chaque machine

## 7. Dépannage

| Symptôme | Cause | Solution |
|---|---|---|
| Permission denied (publickey) | Clé non autorisée | Lancer `authorize_termux_key.sh` |
| Host key verification failed | Host inconnu | `ssh -o StrictHostKeyChecking=accept-new` |
| Connection timed out | Réseau / IP erronée | Vérifier `~/.ssh/config` |
| Bad permissions | Mode incorrect | `chmod 600 ~/.ssh/id_ed25519_termux && chmod 700 ~/.ssh` |
