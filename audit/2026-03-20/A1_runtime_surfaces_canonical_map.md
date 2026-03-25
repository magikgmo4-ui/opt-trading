# RUNTIME SURFACES — CARTE CANONIQUE MINIMALE

```
Date     : 2026-03-20
Mission  : GO_RUNTIME_SURFACES_CANONICAL_MAP_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ — 3 surfaces qualifiées, rôles établis, limites documentées
```

---

## 1. RÔLE DE CE DOCUMENT

Fixer une carte canonique minimale des surfaces runtime du périmètre `opt-trading` :
- distinguer machine physique / rôle runtime / repo Git associé
- ne pas traiter ces machines comme des repos
- ne pas inventer de services non prouvés
- fournir un point de reprise stable par surface

Sources terrain :
- `infra_context_sanitized/machines/*/fiche_machine.md`
- `infra_context_sanitized/machines/*/roles.md`
- `infra_context_sanitized/machines/*/snapshot/`
- `infra_context_sanitized/OVERVIEW.md`
- `infra_context_sanitized/scripts/generate_pdf_fiches.py`
- `scripts/admin_trading/README_ENTRYPOINTS.md`

---

## 2. TABLEAU DE SYNTHÈSE — VUE D'ENSEMBLE

| Surface | Type | OS | IP LAN | Rôle principal | Repo associé | Statut |
|---|---|---|---|---|---|---|
| `admin-trading` | machine / runtime Linux | Debian 12 | 192.168.16.155 | OPS / bastion / services trading actifs | `opt-trading` cloné sur `/opt/trading/` | ÉTABLI / ACTIF |
| `db-layer` | machine / runtime Linux | Ubuntu 24.04 | 192.168.16.179 | Backend persistant / DB / API secondaires | `opt-trading` présent, `algo_hf` séparé | ÉTABLI / QUALIFIÉ |
| `cursor-ai` | machine / surface opérateur Windows | Windows 10 Pro | 192.168.16.224 | Poste de développement — push/pull/deploy | `opt-trading` cloné sur `C:\Users\ghost\opt-trading\` | ÉTABLI / ACTIF |

---

## 3. FICHE — ADMIN-TRADING

### 3.1 Identité

| Attribut | Valeur |
|---|---|
| Nom canonique | `admin-trading` |
| Type | machine physique / runtime Linux |
| Hardware | HP EliteBook 840 G1 (laptop) |
| OS | Debian 12 (bookworm) — kernel 6.1.0-42-amd64 |
| CPU | Intel Core i5-4300U @ 1.90 GHz (4 threads) |
| RAM | 7,7 Go |
| Disque | 219 Go (ext4 sur `/`) |
| IP LAN | 192.168.16.155 / subnet 192.168.16.0/24 |
| Interface réseau | wlo1 (Wi-Fi) |
| Docker | NON |

### 3.2 Rôle principal

```
OPS / hôte principal des services trading
Bastion SSH + orchestration services
APIs et UI exposées uniquement en LAN
```

### 3.3 Services actifs (snapshot 2026-02-26)

| Service | Description |
|---|---|
| `sshd` | Bastion SSH LAN |
| `tv-webhook.service` | TradingView Webhook Server (FastAPI/Uvicorn) |
| `tv-bitget-runner.service` | Bitget → TV runner (poll candles, send /tv) |
| `<REDACTED_TUNNEL>-tv.service` | Tunnel pour TradingView webhook (URL redacted) |

Ports en écoute : `22, 631, 4040, 5353, 8000, 8010, 42029, 51385, 51820`

### 3.4 Repo et déploiement

| Attribut | Valeur |
|---|---|
| Repo déployé | `opt-trading / sot/mainline` |
| Chemin local | `/opt/trading/` |
| Modules | `/opt/trading/modules/` |
| Scripts | `/opt/trading/scripts/`, `/usr/local/bin/` |
| Logs | `/var/log/`, `/opt/trading/tmp/` |

### 3.5 Couche scripts runtime

Dossier canonique de pilotage runtime : `scripts/admin_trading/`

```
⚠️ Ce dossier est le pilote réel (README_ENTRYPOINTS.md).
Les scripts à la racine scripts/ sont des alias historiques limités.
```

Scripts présents :
- `desk_pro_cmd.sh` — orchestrateur principal modules Python
- `desk_pro_menu.sh` — menu opérateur
- `desk_pro_sanity_check.sh` — vérification santé
- `desk_pro_run_logged.sh` — lancement avec log
- `desk_pro_incident_checklist.sh` — checklist incident
- `desk_pro_ops_summary.sh` — résumé ops
- `desk_pro_session_journal.sh` — journal de session
- `desk_pro_db_cmd.sh` / `desk_pro_db_menu.sh` — couche DB depuis admin-trading
- Shortcut opérateur : `menu-ops_menu_hub`

### 3.6 Workstreams principaux liés (prouvés)

| Workstream | Preuve |
|---|---|
| Desk Pro | services 8010, scripts/admin_trading/, modules/ |
| TradingView webhook | `tv-webhook.service` actif |
| Bitget runner | `tv-bitget-runner.service` actif |
| `derivatives_collector` | module dans /opt/trading/modules/ (déployable) |

### 3.7 Établi vs à confirmer

| Item | État |
|---|---|
| Machine physique Debian 12 | ÉTABLI (snapshot 2026-02-26) |
| Rôle OPS / bastion SSH | ÉTABLI |
| Services tv-webhook, tv-bitget-runner actifs | ÉTABLI |
| Repo opt-trading déployé sur /opt/trading/ | ÉTABLI |
| `scripts/admin_trading/` = couche pilote runtime | ÉTABLI |
| État des services au-delà du snapshot 2026-02-26 | À CONFIRMER live |
| Intégration live derivatives_collector → Risk Engine | À CONFIRMER |

---

## 4. FICHE — DB-LAYER

### 4.1 Identité

| Attribut | Valeur |
|---|---|
| Nom canonique | `db-layer` |
| Type | machine physique / runtime Linux |
| Hardware | MSI GE62 2QD (laptop) |
| OS | Ubuntu 24.04.4 LTS — kernel 6.17.0-14-generic |
| Hostname système | `ghost` |
| CPU | Intel Core i7-5700HQ @ 2.70 GHz (8 threads) |
| RAM | 11 Go |
| Disque | 915 Go (ext4 sur `/`) |
| IP LAN | 192.168.16.179 / subnet 192.168.16.0/24 |
| Interface réseau | enp4s0 (Ethernet) |
| Docker | NON |

### 4.2 Rôle principal

```
Couche base de données / services backend persistants
Hébergement des services de type API secondaire et persistance (LAN-only)
```

### 4.3 Services actifs (snapshot 2026-02-26)

| Service | Description |
|---|---|
| `sshd` | SSH LAN |
| `algo-hf-api.service` | API FastAPI — algo_hf webhook |
| `plexmediaserver` | Plex Media Server (port 32400) |
| `gnome-remote-desktop.service` | Remote desktop GNOME |

Ports en écoute : `22, 53, 631, 1901, 5353, 9100, 32400-32414, 32600, ...`

Note : la passe live a confirmé que le port `9100` est utilisé par `algo-hf-api.service` (processus Python / Uvicorn).

### 4.4 Repo et déploiement

| Attribut | Valeur |
|---|---|
| Repo `opt-trading` déployé ? | OUI observé sur `/opt/trading/` (branche `sot/mainline`) |
| Clone audit (`opt-trading-audit`) | Mentionné dans `98_claude_cowork_relaunch_pack.md` — usage : audit uniquement |
| Chemins `opt-trading` sur db-layer | `/opt/trading/` observé ; aucun module `algo_hf`/`hf_trading` observé dedans |

### 4.5 Lien `algo-hf-api` → workstream `algo_hf`

`algo-hf-api.service` tourne sur `db-layer`. Le workstream `algo_hf` est listé comme "À QUALIFIER" dans la topologie.

Ce lien est désormais **prouvé** par la passe live :
- unit file : `/etc/systemd/system/algo-hf-api.service`
- `WorkingDirectory=/home/ghost/dev/nouveau-systeme`
- `ExecStart=/home/ghost/dev/nouveau-systeme/scripts/commandes/api_service.sh`
- lancement Python : `from algo_hf.api.run import main; main()`

Le workstream `algo_hf` reste séparé de `opt-trading`.

### 4.6 Établi vs à confirmer

| Item | État |
|---|---|
| Machine physique Ubuntu 24.04 | ÉTABLI (snapshot 2026-02-26) |
| Rôle backend persistant / DB | ÉTABLI |
| `algo-hf-api.service` actif | ÉTABLI (snapshot) |
| Plex Media Server actif | ÉTABLI (snapshot) |
| Repo `opt-trading` déployé sur db-layer | ÉTABLI — `/opt/trading/` observé, branche `sot/mainline` |
| Chemins base de données réels | À CONFIRMER |
| Lien algo-hf-api ↔ workstream `algo_hf` | ÉTABLI — code prouvé sous `/home/ghost/dev/nouveau-systeme` |
| État des services au-delà du snapshot 2026-02-26 | À CONFIRMER live |

---

## 5. FICHE — CURSOR-AI

### 5.1 Identité

| Attribut | Valeur |
|---|---|
| Nom canonique | `cursor-ai` |
| Type | machine physique / surface opérateur Windows |
| Hardware | Dell (poste de dev) |
| OS | Windows 10 Pro (build 22621) |
| Hostname système | DESKTOP-1KDTQBH |
| CPU | Intel Core i5-1145G7 @ 2.60 GHz (8 threads) |
| RAM | ~16 Go |
| IP LAN | 192.168.16.224 (Wi-Fi) |
| Tunnel WireGuard | 10.8.0.2 → admin-trading |
| Docker | NON (Windows, non applicable) |

Note : la `fiche_machine.md` dans le repo est vide (hostname, OS, RAM, ports absents). Les données ci-dessus proviennent du snapshot Windows et de `generate_pdf_fiches.py`.

### 5.2 Rôle principal

```
Poste de développement principal
IDE Cursor, UI, navigateur
Push/pull + déploiement vers les hôtes Debian via SSH
```

### 5.3 Workflow de déploiement

```
cursor-ai (Windows)
  1. Code dans Cursor IDE
     C:\Users\ghost\Desktop\cursor_ai_workflow\
     C:\Users\ghost\Downloads\  (staging)

  2. Git commit + push (remote)

  3. SSH vers cibles Linux
     ssh admin-trading  |  ssh db-layer  |  ssh student

  4. git pull sur cibles
     /opt/trading/  (admin-trading, student)

  5. Restart services
     systemctl restart tv-webhook, tv-bitget-runner (admin-trading)
     systemctl restart algo-hf-api (db-layer)
```

### 5.4 Repo et chemins

| Attribut | Valeur |
|---|---|
| Repo `opt-trading` local | `C:\Users\ghost\opt-trading\` (= pivot de la session courante) |
| Workflow actif | `C:\Users\ghost\Desktop\cursor_ai_workflow\` |
| Staging / transferts | `C:\Users\ghost\Downloads\` |
| Connexion tunnel | WireGuard → admin-trading (10.8.0.2) |

### 5.5 Surface active dans la session courante

La session d'audit cowork actuelle (Claude + ChatGPT) s'exécute **depuis cursor-ai** :
- repo `C:\Users\ghost\opt-trading\` = source locale des fichiers édités
- Linux path visible dans cowork : `/sessions/magical-serene-mayer/mnt/ghost/opt-trading/`

### 5.6 Établi vs à confirmer

| Item | État |
|---|---|
| Machine physique Windows 10 Pro | ÉTABLI (snapshot 2026-02-26) |
| Rôle poste de dev / surface opérateur | ÉTABLI |
| Tunnel WireGuard actif vers admin-trading | ÉTABLI (snapshot réseau) |
| Repo `opt-trading` local C:\Users\ghost\ | ÉTABLI (contexte session) |
| Aucun service opt-trading actif en local sur cursor-ai | ÉTABLI |
| `fiche_machine.md` incomplète dans le repo | OBSERVÉ — limite documentaire |
| IP WAN / état réseau actuel | À CONFIRMER live |

---

## 6. TOPOLOGIE RÉSEAU LAN (SYNTHÈSE)

```
192.168.16.0/24 — toutes machines en LAN uniquement

  cursor-ai          admin-trading      db-layer           student
  .224 (Wi-Fi)  ──▶  .155 (Wi-Fi)      .179 (Ethernet)    .103 (Ethernet)
  Windows 10         Debian 12          Ubuntu 24.04        Debian 12
  Poste dev          OPS / Services     Backend / DB        Sandbox / POC

  WireGuard tunnel:
  cursor-ai (10.8.0.2) ──▶ admin-trading (hub tunnel)
```

Note : `student` apparaît dans l'OVERVIEW et dans le tunnel — elle est mentionnée ici pour exhaustivité topologique mais reste hors scope de cette mission (déjà cadrée par `GO_STUDENT_*`).

---

## 7. LIMITES DE CETTE PASSE

- **Audit documentaire uniquement** — aucun accès SSH live aux machines.
- **Snapshot daté 2026-02-26** — l'état réel des services peut avoir évolué.
- **`fiche_machine.md` de cursor-ai est vide** dans le repo — données reconstituées depuis snapshot et `generate_pdf_fiches.py` uniquement.
- **Repo `opt-trading` observé sur db-layer** — aucun lien d'intégration directe avec `algo_hf` n'est prouvé.
- **Lien `algo-hf-api` ↔ `algo_hf`** = prouvé ; relation avec `hf_trading` non prouvée.
- Les URL de tunnel sont redacted (`<REDACTED_TUNNEL>`) — non déchiffrables dans cette passe.

---

## 8. POINT DE REPRISE

```
GO_RUNTIME_SURFACES_CANONICAL_MAP_01 → LIVRÉ

Ce qui est établi :
  ✓ admin-trading : Debian 12, OPS/bastion, services tv-webhook + tv-bitget actifs
                    repo opt-trading déployé sur /opt/trading/
                    couche runtime : scripts/admin_trading/ + shortcuts
  ✓ db-layer       : Ubuntu 24.04, backend persistant, algo-hf-api actif
                    lien potentiel avec workstream algo_hf (hypothèse)
  ✓ cursor-ai      : Windows 10, poste dev, repo C:\Users\ghost\opt-trading\
                    = surface d'où s'exécute la session cowork courante

Ce qui reste conditionné à une passe ultérieure :
  → GO_ALGO_HF_AUDIT_01 : qualifier workstream algo_hf / lien db-layer
  → GO_HF_TRADING_AUDIT_01 : qualifier hf_trading
  → corriger fiche_machine.md cursor-ai dans le repo (données manquantes)
  → vérifier repo déployé sur db-layer si besoin

Prochain chantier portefeuille recommandé :
  GO_LOCALCMS_CANON_DECISION_01
  → décision canonique socle / surcouche localcms
  → ou GO_ALGO_HF_AUDIT_01 si priorité infra avant CMS
```
