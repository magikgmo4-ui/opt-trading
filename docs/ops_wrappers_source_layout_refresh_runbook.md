# ops_wrappers source-layout refresh runbook

## But

Ce runbook couvre uniquement le refresh source-layout de `ops_wrappers` sur les cibles Linux.

Le chemin vise est:

- `/opt/trading/modules/ops_wrappers`

Ce runbook ne couvre pas un deploiement runtime standard sous `/opt/trading/ops_wrappers`.

## Perimetre

- Orchestrateur: `admin-trading`
- Cibles courantes: `student`, `db-layer`
- Source: `/opt/trading/modules/ops_wrappers`
- Cible autorisee: `/opt/trading/modules/ops_wrappers`

## Preconditions

- la source existe sur `admin-trading`
- l'acces SSH vers `student` et `db-layer` est OK
- le preflight source-layout suivant est propre:

```bash
ssh admin-trading 'cmd-deploy_module_multi_machine preflight --module-name ops_wrappers --source-dir /opt/trading/modules/ops_wrappers --install-path /opt/trading/modules/ops_wrappers --targets student,db-layer'
```

- aucune consigne d'installation globale n'est active

## Interdits explicites

- ne pas utiliser `/opt/trading/ops_wrappers`
- ne pas lancer `install_shortcuts`
- ne pas lancer `generate_and_install`
- ne pas ecrire dans `/usr/local/bin` sur les cibles
- ne pas utiliser `sudo` sur les cibles
- ne pas utiliser `--post-install`
- ne pas traiter `ops_wrappers` comme module runtime standard

## GO / NO-GO

### GO

- preflight source-layout `ok` sur toutes les cibles
- lock absent ou propre sur toutes les cibles
- source presente sur `admin-trading`
- cible `/opt/trading/modules/ops_wrappers` accessible

### NO-GO

- preflight non `ok` sur au moins une cible
- commande demandee vers `/opt/trading/ops_wrappers`
- besoin d'ecrire dans `/usr/local/bin`
- besoin de `sudo` sur cible
- consigne implicite d'installation globale

## Commandes exactes

### Preflight source-layout

```bash
ssh admin-trading 'cmd-deploy_module_multi_machine preflight --module-name ops_wrappers --source-dir /opt/trading/modules/ops_wrappers --install-path /opt/trading/modules/ops_wrappers --targets student,db-layer'
```

### Future commande de refresh autorisee

```bash
ssh admin-trading 'cmd-deploy_module_multi_machine deploy --module-name ops_wrappers --source-dir /opt/trading/modules/ops_wrappers --install-path /opt/trading/modules/ops_wrappers --targets student,db-layer'
```

### Validation post-refresh autorisee

```bash
ssh student 'bash /opt/trading/modules/ops_wrappers/scripts/sanity_check.sh'
ssh db-layer 'bash /opt/trading/modules/ops_wrappers/scripts/sanity_check.sh'

ssh student 'cmd-ops_wrappers scan | sed -n "1,80p"'
ssh db-layer 'cmd-ops_wrappers scan | sed -n "1,80p"'
```

### Verification de coherence de contenu

```bash
python - <<'PY'
import subprocess, textwrap
script = textwrap.dedent('''
import hashlib
from pathlib import Path
paths = [
    Path('/opt/trading/modules/ops_wrappers/ops_wrappers.sh'),
    Path('/opt/trading/modules/ops_wrappers/scripts/cmd.sh'),
    Path('/opt/trading/modules/ops_wrappers/scripts/menu.sh'),
    Path('/opt/trading/modules/ops_wrappers/scripts/sanity_check.sh'),
    Path('/opt/trading/modules/ops_wrappers/README.md'),
]
for p in paths:
    if p.exists():
        print(f"{p}|sha16={hashlib.sha256(p.read_bytes()).hexdigest()[:16]}")
''')
for host in ['admin-trading', 'student', 'db-layer']:
    print(f'===== {host} =====')
    subprocess.run(['ssh', host, 'python3', '-'], input=script, text=True, check=False)
PY
```

## Validation post-refresh

- `/opt/trading/modules/ops_wrappers` existe toujours sur chaque cible
- `ops_wrappers.sh`, `README.md`, `scripts/cmd.sh`, `scripts/menu.sh`, `scripts/sanity_check.sh` sont presents
- `bash /opt/trading/modules/ops_wrappers/scripts/sanity_check.sh` passe
- `cmd-ops_wrappers scan` fonctionne encore
- aucun changement involontaire dans `/usr/local/bin`

## Rollback

Le deployeur cree un backup cible sous:

- `/opt/trading/modules/ops_wrappers.bak/<run_id>`

Verification minimale apres echec:

```bash
ssh student 'ls -la /opt/trading/modules/ops_wrappers.bak/<run_id>'
ssh db-layer 'ls -la /opt/trading/modules/ops_wrappers.bak/<run_id>'
```

Restauration eventuelle: action manuelle explicite et documentee a partir du backup identifie.

## Limites

- ce runbook ne couvre pas la regeneration des wrappers de modules sur les cibles
- ce runbook ne couvre pas l'installation/reinstallation des raccourcis globaux
- ce runbook ne couvre pas les actions `sudo`
- ce runbook ne transforme pas `ops_wrappers` en module runtime standard
- tout changement impliquant `/usr/local/bin` exige une consigne explicite supplementaire
