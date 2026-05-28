# Tasker Integration — Termux:Tasker → SSH → Fleet

## 1. Pré-requis

- Termux installé (F-Droid)
- Termux:Tasker installé (F-Droid)
- Tasker installé (Google Play ou F-Droid)
- Bootstrap Termux effectué (clé SSH + config)

## 2. Installation du plugin Termux:Tasker

1. Installer `Termux:Tasker` depuis F-Droid.
2. Ouvrir Termux : `pkg install termux-tasker`.
3. Dans Tasker, ajouter une action `Plugin → Termux:Tasker`.
4. Configurer :
   - **Executable** : `/data/data/com.termux/files/usr/bin/bash`
   - **Argument** : chemin du script à exécuter
   - **Working directory** : `/data/data/com.termux/files/home`
   - **Timeout** : ≥ 30 secondes (ne pas mettre 0)

## 3. Scripts disponibles pour Tasker

Les scripts dans `~/.termux/tasker/` sont appelables par Tasker.
Des templates versionnés existent dans le dépôt :

```bash
bash ~/opt-trading/modules/termux_operator/scripts/install_tasker_scripts.sh
```

Cette commande installe :

| Script | Action | Destructif |
|---|---|---|
| `health_summary.sh` | Health check complet (SSH + tmux + fleet) | NON |
| `sessions_list.sh` | Liste les sessions tmux sur toutes les machines | NON |
| `log_tail.sh` | Dernières N lignes d'un log (paramétrable) | NON |
| `attach_hint.sh` | Affiche la commande SSH+tmux pour une session | NON |

## 4. Créer un script personnalisé pour Tasker

Exemple : créer `~/.termux/tasker/mon_script.sh`

```bash
#!/data/data/com.termux/files/usr/bin/bash
set -Eeuo pipefail
exec bash ~/opt-trading/modules/termux_operator/scripts/health_probes.sh
```

Rendre exécutable :

```bash
chmod +x ~/.termux/tasker/mon_script.sh
```

## 5. Tasker — Profil recommandé V1

### Bouton health check (READ-ONLY)

1. Créer une **Task** : `TASK_HEALTH_CHECK`
2. Ajouter action : `Plugin → Termux:Tasker`
   - Executable : `bash`
   - Argument : `~/.termux/tasker/health_summary.sh`
   - Timeout : 30s
3. Ajouter action : `Alert → Flash`
   - Text : `%stdout`
4. Créer un **Widget** → Task → `TASK_HEALTH_CHECK`

### Widget session list

1. Créer une **Task** : `TASK_SESSIONS_LIST`
2. Ajouter action : `Plugin → Termux:Tasker`
   - Executable : `bash`
   - Argument : `~/.termux/tasker/sessions_list.sh`
   - Timeout : 15s
3. Ajouter action : `Alert → Flash`
   - Text : `%stdout`
4. Créer un **Widget** → Task → `TASK_SESSIONS_LIST`

## 6. Variables Tasker disponibles

Le plugin Termux:Tasker retourne ces variables :

| Variable | Contenu |
|---|---|
| `%stdout` | Sortie standard du script |
| `%stderr` | Sortie d'erreur |
| `%result` | Code de retour (0 = succès) |
| `%err` | Message d'erreur si échec |

Toujours valider `%result` avant d'utiliser `%stdout`.

## 7. Règles

- **READ-ONLY par défaut** : tous les scripts Tasker V1 sont read-only
- **Pas de passphrase** : la clé SSH n'a pas de passphrase (Tasker ne peut pas en gérer)
- **Timeout suffisant** : 30s minimum pour les health checks multi-machines
- **Pas de secret** : ne pas stocker de mot de passe ou token dans une variable Tasker
- **Confirmation** : toute action destructive nécessite une confirmation séparée

## 8. Dépannage Tasker

| Symptôme | Cause | Solution |
|---|---|---|
| `%result` non nul | Script non trouvé | Vérifier le chemin absolu |
| `%stdout` vide | Timeout trop court | Passer à ≥30s |
| `%err` = Permission denied | Plugin non installé | Installer Termux:Tasker |
| Script non exécutable | `chmod +x` manquant | `chmod +x ~/.termux/tasker/*` |
| Tasker ne voit pas Termux:Tasker | Plugin pas installé | Vérifier F-Droid |
