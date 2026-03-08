# Stack 4 machines — Vue d'ensemble

> Source : machines/*/fiche_machine.md, machines/*/reseau.md, machines/*/roles.md, machines/*/snapshot/*.txt  
> Règles : SECURITY_REDACTION_RULES.md (aucun secret, LAN-only)

---

## 1. Tableau des 4 machines

| Machine        | OS                    | IP LAN          | Rôle                              | Ports clés                                   |
|----------------|------------------------|-----------------|-----------------------------------|----------------------------------------------|
| **admin-trading** | Debian 12 (bookworm)  | 192.168.16.155  | OPS / bastion / APIs trading      | 22 (SSH), 8000, 8010 (API/UI), 51820         |
| **cursor-ai**     | Windows 10 Pro (22621)| 192.168.16.224  | Poste de dev (Cursor, UI, browser)| —                                            |
| **db-layer**      | Ubuntu 24.04 LTS      | 192.168.16.179  | DB / services backend persistants | 22, 53, 9100, 32400 (Plex), algo-hf-api      |
| **student**       | Debian 12 (bookworm)  | 192.168.16.103  | Sandbox / POC / agents            | 22, 8020 (ingest API), fail2ban              |

**Réseau** : subnet 192.168.16.0/24 — toutes les machines sont en LAN uniquement.

---

## 2. Flux de travail (dev → déploiement)

```
cursor-ai (Windows)                    admin-trading / db-layer / student (Linux)
─────────────────────                  ─────────────────────────────────────────

1. Code dans Cursor
   C:\Users\ghost\Desktop\cursor_ai_workflow\
   C:\Users\ghost\Downloads\  (staging)

2. Git commit + push
   (remote non mentionné)

3. SSH vers cible
   ssh admin-trading  |  ssh db-layer  |  ssh student

4. git pull dans dossier cible
   /opt/trading/  (admin-trading, student)
   (selon config sur db-layer)

5. Démarrage / redémarrage services
   - systemd : systemctl restart tv-webhook, tv-bitget-runner...
   - scripts : menu-desk_pro, cmd-desk_pro (admin-trading)
   - scripts : menu-student, cmd-student (student)

6. Logs et diagnostics
   /var/log/
   /opt/trading/tmp/
   journalctl -u <service>
```

**Points de déploiement typiques** :
- **admin-trading** : APIs Desk Pro (8010), webhook TV, bitget runner
- **db-layer** : algo-hf-api, bases de données
- **student** : student-ingest, student-watchdrop (API 8020), tests POC

---

## 3. Points de sécurité

| Règle | Détail |
|-------|--------|
| **LAN-only** | Aucune exposition WAN directe. Ports et services accessibles uniquement sur 192.168.16.0/24. |
| **Aucun secret** | Pas de clés API, tokens, webhooks, .env complet, clés privées dans les docs/prompts. |
| **Redaction** | URLs de tunnel, credentials → remplacer par `<REDACTED>` ou `***`. |
| **Autorisé** | IP privées (192.168.x.x), ports internes, chemins locaux, noms de services. |

Voir `SECURITY_REDACTION_RULES.md` pour la checklist avant partage de logs ou configs.

---

## 4. Résumé des 4 machines

| Machine        | Résumé en une ligne |
|----------------|----------------------|
| **admin-trading** | Debian 12, HP EliteBook. Bastion OPS, APIs trading (8010), webhook TV, scripts menu-desk_pro. |
| **cursor-ai**     | Windows, Dell. Poste de dev principal, Cursor, push/pull vers Linux via SSH. |
| **db-layer**      | Ubuntu 24, MSI. DB, algo-hf-api, Plex, services backend. |
| **student**       | Debian 12, HP ProDesk. Sandbox, ingest API (8020), fail2ban, expérimentations. |
