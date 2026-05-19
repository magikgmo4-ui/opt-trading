# deploy_module_multi_machine

Module d'orchestration infra pour deployer automatiquement un module vers plusieurs machines Linux via SSH, a partir de `admin-trading` comme hub.

## But

Ce module couvre le flux standard suivant:

1. resoudre les machines cibles via le registry central (`registry/machines_registry.yaml`) quand il est disponible,
2. resoudre les metadonnees module via `registry/modules_registry.yaml` si elles existent,
3. empaqueter un module local en `tar.gz`,
4. copier l'artefact vers chaque hote distant via `scp`,
5. installer proprement sous `/opt/trading/<module>`,
6. lancer le sanity check du module distant.

## Hypotheses retenues

- `admin-trading` reste l'orchestrateur principal.
- le chemin d'installation runtime cible est `/opt/trading/<module>`.
- le module source local peut rester dans le repo sous `/opt/trading/modules/<module>`.
- ce module cible uniquement des hotes POSIX/Linux. `cursor-ai` reste visible dans l'inventaire mais n'est pas une cible de deploiement `/opt/trading/...`.
- `--targets` accepte des aliases SSH, des hostnames, des cibles explicites `user@host` et `user@ip`.
- si un alias SSH est obsolete ou pointe vers un mauvais reseau sur `admin-trading`, utiliser une cible explicite LAN/WireGuard comme `student@192.168.0.103`.

## Structure

```text
deploy_module_multi_machine/
|- README.md
|- app/
|  `- deploy_module_multi_machine.py
|- config/
|  `- hosts_fallback.json
`- scripts/
   |- deploy_module_multi_machine_cmd.sh
   |- deploy_module_multi_machine_menu.sh
   |- deploy_module_multi_machine_sanity_check.sh
   `- install_module.sh
```

## Commandes cles

### 1) installer les wrappers du module lui-meme

```bash
cd /opt/trading/deploy_module_multi_machine
bash scripts/install_module.sh
```

### 2) verifier l'etat registry / fallback

```bash
cmd-deploy_module_multi_machine status
```

### 2b) sonder les cibles avant un deploiement reel

```bash
cmd-deploy_module_multi_machine preflight --module-name module_contextuals_shell --source-dir /opt/trading/modules/module_contextuals_shell --targets student,db-layer
```

### 2c) sonder les cibles avec prediction du post-install

```bash
cmd-deploy_module_multi_machine preflight --module-name deploy_module_multi_machine --source-dir /opt/trading/deploy_module_multi_machine --targets student,db-layer --post-install
```

### 3) planifier un deploiement sans executer

```bash
cmd-deploy_module_multi_machine plan --module-name module_contextuals_shell --source-dir /opt/trading/modules/module_contextuals_shell --targets student@192.168.0.103,ghost@192.168.0.100 --dry-run
```

### 4) deployer reellement

```bash
cmd-deploy_module_multi_machine deploy --module-name module_contextuals_shell --source-dir /opt/trading/modules/module_contextuals_shell --targets student@192.168.0.103,ghost@192.168.0.100
```

### 4b) deployer reellement avec post-install optionnel

```bash
cmd-deploy_module_multi_machine deploy --module-name deploy_module_multi_machine --source-dir /opt/trading/deploy_module_multi_machine --targets student,db-layer --post-install
```

### 5) relancer uniquement la sanity distante

```bash
cmd-deploy_module_multi_machine sanity --module-name module_contextuals_shell --source-dir /opt/trading/modules/module_contextuals_shell --targets student@192.168.0.103,ghost@192.168.0.100
```

## Comportement reel V1.5.1

- le script shell distant est genere en multi-lignes puis valide localement avec `bash -n` avant execution via `ssh`.
- le module accepte les cibles explicites `user@host` et `user@ip` quand les aliases ne sont pas fiables.
- si le registry n'est pas exploitable, le module retombe sur `config/hosts_fallback.json` puis sur les cibles passees en ligne de commande.
- le deploiement installe uniquement l'arborescence module sous `/opt/trading/<module>` et execute la sanity distante si detectee.
- `--post-install` reste optionnel et execute `scripts/install_module.sh` sur la cible seulement s'il est demande.
- si `scripts/install_module.sh` est absent, le deploiement reste `ok` avec `post_install: skipped`.
- si le post-install existe mais echoue, le module reste deploie mais le resultat machine devient `partial` et la commande sort en non-zero.
- les wrappers globaux `/usr/local/bin/menu-*`, `cmd-*`, `sanity-*` restent dependants du contexte privilege de chaque cible.
- `preflight` probe les cibles avant de deployer et remonte un JSON machine par machine.
- `preflight` verifie la joignabilite SSH, l'utilisateur effectif, `bash`, `tar`, `python3`, `/opt/trading`, l'ecriture dans `/tmp`, et la prediction du post-install si `--post-install` est demande.
- chaque execution de `deploy` genere maintenant un `run_id` unique, utilise dans le nom du bundle local, du bundle distant `/tmp/<module>_<run_id>.tar.gz`, du backup `<install_path>.bak/<run_id>` et du prefix de staging distant.
- ce durcissement evite les collisions observees quand deux deploiements du meme module demarrent dans la meme seconde.
- chaque cible prend maintenant un lock distant par `install_path` sous `/tmp/deploy_module_multi_machine_locks/` avant upload/install/post-install.
- si le lock est deja pris, la machine remonte `status=blocked`, `stage=lock` et un bloc `lock` detaille sans toucher a l'installation existante.
- un lock ecrit maintenant des metadonnees minimales (`owner_run_id`, `created_at_epoch`, `created_at_utc`) pour faciliter l'inspection et la detection stale.
- `preflight` remonte aussi l'etat du lock cible (`exists`, `owner_run_id`, `created_at_utc`, `age_seconds`, `stale`).
- `deploy --cleanup-stale-lock` tente explicitement un cleanup d'un lock stale avant de reacquerir le lock.
- `--lock-stale-after-seconds` permet d'ajuster le seuil stale lock; la valeur par defaut est `3600` secondes.

## Integration registry

Le module lit, quand disponibles:

- `/opt/trading/registry/machines_registry.yaml`
- `/opt/trading/registry/modules_registry.yaml`

Comme le schema exact n'a pas ete fige ici, le parseur est tolerant et cherche plusieurs cles usuelles (`alias`, `hostname`, `ssh_target`, `targets`, `install_path`, etc.). Si le registry n'est pas exploitable, le module retombe sur `config/hosts_fallback.json` puis sur les cibles explicites passees via `--targets`.

## Strategie d'installation distante

Pour chaque cible:

- acquisition d'un lock par cible + `install_path` sous `/tmp/deploy_module_multi_machine_locks/`
- upload d'un bundle temporaire vers `/tmp/<module>_<run_id>.tar.gz`
- extraction dans un repertoire de staging
- backup de l'ancienne version sous `<install_path>.bak/<run_id>`
- remplacement atomique du repertoire cible
- execution du sanity check distant si detecte
- suppression du bundle temporaire distant, sauf si `--keep-tmp` est demande
- liberation du lock en fin de run, y compris apres post-install

## Validation terrain V1.5.1

- deploiement reel valide de `module_contextuals_shell` depuis `admin-trading`
- cibles reelles validees: `student@192.168.0.103`, `ghost@192.168.0.100`
- sanity distante OK sur les deux cibles
- deploiement via alias `student` et `db-layer` valide apres correction SSH sur `admin-trading`
- post-install distant optionnel valide en dry-run et en execution reelle avec remontee de statut machine
- preflight distant valide sur `student` et `db-layer`
- prediction `ok`, `skipped`, `will_require_password` et `blocked` remontee sans toucher au registry
- deux dry-runs rapproches du meme module produisent des chemins temporaires differents grace au `run_id`
- deploiement reel V1.4 valide sans collision de bundle temporaire
- lock distant valide sur deploiement reel simple
- contention semi-reelle validee via lock deja present: le second run est bloque proprement au stage `lock`
- inspection stale lock validee avec metadonnees sur lock existant
- cleanup stale lock explicite valide avec `--cleanup-stale-lock`

## Limites reelles de la V1.5.1

- pas de deploiement Windows
- pas d'ecriture automatique dans `modules_registry.yaml` ni `wrappers_registry.yaml`
- pas d'integration systemd/timer/service dans cette version
- le post-install distant ne contourne pas les privileges: si `sudo` est requis sur la cible, l'erreur remonte telle quelle
- `preflight` reste predictif: il estime le comportement du post-install a partir du script source et de `sudo -n`, sans executer le script cible
- le lock V1.5.1 serialize les runs par cible + `install_path`, et sait maintenant signaler / nettoyer explicitement un stale lock, mais il n'embarque pas encore de cleanup automatique silencieux
- un lock recent mais legitime reste bloquant tant que son owner ne le relache pas; le cleanup stale exige une demande explicite via `--cleanup-stale-lock`
- depend de `ssh`, `scp`, `tar` et `bash` presents sur l'orchestrateur
- depend de la connectivite SSH reelle depuis `admin-trading`; un alias obsolete peut casser le deploiement
- depend de `PyYAML` seulement si le registry YAML doit etre lu
