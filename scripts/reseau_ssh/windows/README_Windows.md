# Windows — reseau_ssh (OpenSSH + Firewall + WireGuard)

## 1) Fix permissions for OpenSSH authorized_keys (si 'Access denied')
Ouvre PowerShell **en administrateur** puis:
```powershell
cd <chemin_vers_ce_dossier>
.\fix_openssh_authorized_keys.ps1 -User "$env:USERNAME" -PublicKey "ssh-ed25519 AAAA.... comment"
```

Si tu veux juste corriger les ACL sans ajouter de clé:
```powershell
.\fix_openssh_authorized_keys.ps1 -User "$env:USERNAME"
```

## 2) Firewall (LAN)
Toujours en admin:
```powershell
.\firewall_allow_lan.ps1
```

## 3) WireGuard
- Installe WireGuard for Windows (client)
- Tu peux importer un fichier `*.conf` généré côté Linux (client ou peer).

Le module Linux imprime les clés/public key; tu peux créer un peer Windows dans WireGuard GUI.
