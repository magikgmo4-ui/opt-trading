# Audit alias SSH

## Regle de lecture

- les alias ont ete verifies depuis le poste Windows local
- aucun `HostName` de config SSH locale n'est reproduit ici
- seules les preuves de presence d'alias, de reponse et de chemin utile sont conservees

## Commandes executees

```powershell
ssh -o BatchMode=yes -o ConnectTimeout=8 db-layer 'hostname; whoami; pwd; if [ -d /opt/trading ]; then echo HAS_OPT_TRADING; cd /opt/trading && pwd; else echo NO_OPT_TRADING; fi'
ssh -o BatchMode=yes -o ConnectTimeout=8 admin-trading 'hostname; whoami; pwd; if [ -d /opt/trading ]; then echo HAS_OPT_TRADING; cd /opt/trading && pwd; else echo NO_OPT_TRADING; fi'
ssh -o BatchMode=yes -o ConnectTimeout=8 student 'hostname; whoami; pwd; if [ -d /opt/trading ]; then echo HAS_OPT_TRADING; cd /opt/trading && pwd; else echo NO_OPT_TRADING; fi'
ssh -o BatchMode=yes -o ConnectTimeout=8 fantome 'hostname; whoami; pwd; if [ -d /opt/trading ]; then echo HAS_OPT_TRADING; cd /opt/trading && pwd; else echo NO_OPT_TRADING; fi'
hostname
whoami
(Get-Location).Path
```

## Resultats par alias

| Alias | Present dans `~/.ssh/config` | Resultat synthese | Statut |
| --- | --- | --- | --- |
| `db-layer` | oui | repond ; hostname `db-layer` ; user `ghost` ; `/opt/trading` present | `PASS` |
| `admin-trading` | oui | repond ; hostname `admin-trading` ; user `ghost` ; `/opt/trading` present | `PASS` |
| `student` | oui | repond ; hostname `student` ; user `student` ; `/opt/trading` present | `PASS` |
| `fantome` | oui | repond ; hostname `fantome` ; user `fantome` ; `/opt/trading` present | `PASS` |
| `cursor-ai` | oui | non force en SSH ; machine traitee comme poste local Windows d'orchestration | `LOCAL_DEFER` |

## Raccourcis operateur `reseau_ssh` verifies read-only

Les probes suivantes ont ete executees sur `db-layer`, `admin-trading`, `student` et `fantome` :

```bash
for f in /usr/local/bin/menu-reseau_ssh /usr/local/bin/cmd-reseau_ssh /usr/local/bin/sanity-reseau_ssh; do
  printf "%s -> " "$f"
  readlink -f "$f" || true
done
```

| Machine | Cible constatee | Statut |
| --- | --- | --- |
| `db-layer` | `/opt/trading/modules/reseau_ssh/scripts/{menu.sh,cmd.sh,sanity_check.sh}` | `PASS` |
| `admin-trading` | `/opt/trading/modules/reseau_ssh/scripts/{menu.sh,cmd.sh,sanity_check.sh}` | `PASS` |
| `student` | `/opt/trading/modules/reseau_ssh/scripts/{menu.sh,cmd.sh,sanity_check.sh}` | `PASS` |
| `fantome` | `/home/fantome/opt-trading/modules/reseau_ssh/scripts/{menu.sh,cmd.sh,sanity_check.sh}` | `PASS_NOTE` |

## Limites

- l'alias `cursor-ai` existe dans la config locale, mais sa probe SSH n'a pas ete forcee car ce lot traite `cursor-ai` comme poste Windows local
- aucune correction de config SSH globale n'a ete appliquee
- aucun alias absent bloquant n'a ete constate sur les quatre machines Linux prioritaires
