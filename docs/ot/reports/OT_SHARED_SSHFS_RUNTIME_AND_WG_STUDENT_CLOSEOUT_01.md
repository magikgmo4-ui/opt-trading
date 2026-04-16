# OT_SHARED_SSHFS_RUNTIME_AND_WG_STUDENT_CLOSEOUT_01

Date (America/Montreal): 2026-04-16

## Objet

Clore documentairement les GO `GO_ADMIN_TRADING_SHARED_SSHFS_RUNTIME_HARDENING_01` et `GO_ADMIN_TRADING_WG_MGMT_STUDENT_REPAIR_01` avec l'etat final valide en repo et en machine.

## Contexte

- Repo canonique: `opt-trading`
- Branche canonique: `sot/mainline`
- La source canonique est le repo et l'etat reel machine/session constate pendant la qualification.
- Perimetre de closeout: hardening runtime `shared_sshfs_permanent` + reparation du lien `wg-mgmt` entre `admin-trading` et `student`.

## GO 1 : hardening runtime SSHFS

### Probleme

`shared-sshfs.service` pointait vers des scripts runtime sous `/opt/trading/scripts` et pouvait tomber en echec `203/EXEC` si `shared_sshfs_permanent_mount.sh` ou `shared_sshfs_permanent_umount.sh` etaient absents. La `sanity` initiale ne detectait pas explicitement ce drift runtime.

### Correctif retenu

- tentative invalidee ecartee: `ConditionPathIsExecutable=...`, ignore sur `student`
- garde compatible retenue dans le service:
  - `ExecStartPre=/usr/bin/test -x /opt/trading/scripts/shared_sshfs_permanent_mount.sh`
  - `ExecStartPre=/usr/bin/test -x /opt/trading/scripts/shared_sshfs_permanent_umount.sh`
- `shared_sshfs_permanent_sanity.sh` durcie pour verifier explicitement:
  - existence des scripts runtime
  - bit executable
  - message operatoire explicite si runtime absent

### Qualification

- retrait temporaire du script mount pour qualification negative a froid
- refus propre du service sur `ExecStartPre`
- plus de dependance a un `203/EXEC` opaque
- validation finale sur `student`:
  - service `shared-sshfs.service` en `active (running)`
  - `sanity` finale: `PASS=10 FAIL=0`

### Verdict

`CLOS / PASS`

## GO 2 : reparation WG student

### Probleme

Aucun handshake WireGuard `wg-mgmt` entre `admin-trading` (`10.66.66.1`) et `student` (`10.66.66.3`). `student` utilisait encore un chemin LAN `192.168.0.111` pour le partage au lieu du chemin normal via `10.66.66.1`.

### Cause racine

UFW sur `admin-trading` bloquait `51821/udp` depuis le LAN reel `192.168.0.0/24`, ce qui empechait l'etablissement du tunnel `wg-mgmt` malgre l'ecoute WireGuard active sur le hub.

### Correctif live

- regle live retenue sur `admin-trading`:
  - `ufw allow proto udp from 192.168.0.0/24 to any port 51821`

### Qualification

- ping WG revenu entre `admin-trading` et `student`
- `latest handshake` revenu
- trafic WireGuard bidirectionnel revenu
- `student` remonte `/shared` via `ghost@10.66.66.1:/srv/sftp/shared_files/shared`
- `192.168.0.111` n'est plus le chemin normal d'exploitation pour ce partage

### Verdict

`CLOS / PASS`

## Realignement repo

Fichier realigne:

- `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/inventory.yaml`

Valeurs realignees:

- `admin-trading.lan_ip = 192.168.0.111`
- `admin-trading.wg_listen_port = 51821`
- `student.lan_ip = 192.168.0.142`

## Resultat final consolide

- le trou runtime `shared_sshfs_permanent` vise par `GO_ADMIN_TRADING_SHARED_SSHFS_RUNTIME_HARDENING_01` est ferme
- le lien `wg-mgmt` entre `admin-trading` et `student` est retabli et requalifie
- le partage `/shared` sur `student` revient sur son chemin d'exploitation normal via `10.66.66.1`
- le repo a ete realigne sur les parametres reseau reels retenus

## Point de reprise

Reprise a partir d'un etat clos pour ces deux GO. En cas de revalidation future, repartir de:

- `shared-sshfs.service` + `shared_sshfs_permanent_sanity.sh` sur `student`
- `wg show wg-mgmt`, `ufw status`, et le montage `/shared` via `10.66.66.1` sur `admin-trading` et `student`
- `modules/reseau_ssh_step2/modules/reseau_ssh/reseau_ssh_step2/inventory.yaml` pour la source repo reseau

## Suites logiques eventuelles

- verifier que les usages operatoires et aliases SSH restants privilegient bien `10.66.66.1` pour le chemin mgmt normal
- surveiller tout drift futur entre inventaire repo, UFW live et endpoints WireGuard reels

## Tags finaux

- ETABLI
- TODO
- REPRISE
- MEM_CANDIDATE
- NO_MEMORY
