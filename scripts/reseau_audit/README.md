# reseau_audit v1.3 — Collecte logs réseau/SSH/VPN (NON destructif)

Linux:
```bash
cd /tmp
unzip -o reseau_audit_v1_3_pack.zip
cd modules/reseau_audit/reseau_audit_v1_3
sudo bash install_reseau_audit.sh
sudo cmd-reseau_audit collect
```

Output:
- /opt/trading/_reseau_audit/<HOST>_<TIMESTAMP>.tgz

Windows:
- windows\collect_reseau_audit.ps1 (PowerShell Admin)
