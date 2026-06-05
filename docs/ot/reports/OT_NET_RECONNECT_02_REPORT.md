# OT-NET-RECONNECT-02 — REPORT

Date (America/Montreal) : 2026-03-14

## 1. Résumé exécutif
- Connectivité SSH projet vérifiée en mode non-interactif (BatchMode) depuis le poste opérateur (Windows).
- Aliases SSH confirmés via `~/.ssh/config` : `admin-trading`, `db-layer`, `student`.
- Repo accessible sur `admin-trading` (`/opt/trading`) et wrappers principaux `validated_prompt_factory` présents côté cible.

## 2. Environnement opérateur
- Machine : `desktop-1kdqtbh`
- User : `ghost`
- Shell : PowerShell 7+
- Repo path : `C:\Users\ghost\opt-trading`

## 3. Configuration SSH observée
Fichier :
- `C:\Users\ghost\.ssh\config`

Aliases présents :
- `admin-trading` → `10.66.66.1` (User `ghost`)
- `db-layer` → `10.66.66.2` (User `ghost`)
- `student` → `10.66.66.3` (User `student`)

Preuve de résolution (exemple) :
- `ssh -G admin-trading` : `user ghost`, `hostname 10.66.66.1`, `port 22`, `identityfile ~/.ssh/id_ed25519` (+ `id_ed25519_fantome`)

## 4. Tests de connectivité
Commandes (forme canonique) :
- `ssh -o BatchMode=yes -o ConnectTimeout=5 <host> 'echo HOST=$(hostname); echo USER=$(whoami)'`

Hosts testés :
- `admin-trading`
- `db-layer`
- `student`

## 5. Résultats observés
### admin-trading
Sortie :
- `HOST=admin-trading`
- `USER=ghost`
- `SHELL=/bin/bash`

### db-layer
Sortie :
- `HOST=db-layer`
- `USER=ghost`
- `SHELL=/bin/bash`

### student
Sortie :
- `HOST=student`
- `USER=student`
- `SHELL=/bin/bash`

## 6. Vérifications côté admin-trading (repo + wrappers)
### Repo
Commande :
- `ssh ... admin-trading 'cd /opt/trading && git rev-parse --short HEAD'`
Observé :
- `f774757`

### Wrappers principaux (validated_prompt_factory)
Commande :
- `ssh ... admin-trading 'command -v cmd-validated_prompt_factory sanity-validated_prompt_factory menu-validated_prompt_factory'`
Observé :
- `/usr/local/bin/cmd-validated_prompt_factory`
- `/usr/local/bin/sanity-validated_prompt_factory`
- `/usr/local/bin/menu-validated_prompt_factory`

Résolution (symlinks) observée :
- `/usr/local/bin/cmd-validated_prompt_factory -> /opt/trading/modules/validated_prompt_factory/cmd.sh`
- `/usr/local/bin/sanity-validated_prompt_factory -> /opt/trading/modules/validated_prompt_factory/sanity.sh`
- `/usr/local/bin/menu-validated_prompt_factory -> /opt/trading/modules/validated_prompt_factory/menu.sh`

## 7. Corrections appliquées
- Néant (tout passe en BatchMode).

## 8. État réseau final
**PASS** : les trois connexions SSH attendues sont fonctionnelles en non-interactif, et `admin-trading` expose bien le repo + wrappers.


## RISKS

- À qualifier.
