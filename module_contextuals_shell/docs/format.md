# Format de Fichier Contextuel (.ctx)

Le format contextuel est un fichier texte simple, séparé par des `|` (pipes), conçu pour être parsé facilement en Bash.

## Structure

Chaque ligne valide représente une **action** possible pour le module.
Les lignes vides ou commençant par `#` sont ignorées.

Format :
`action_id|label|description|category|order|visible_module_menu|visible_ops_super|frequency|type|target`

## Champs

1. **action_id** (string) : Identifiant unique interne de l'action (ex: `run_demo`).
2. **label** (string) : Libellé affiché dans le menu (ex: `Lancer la démo`).
3. **description** (string) : Description courte affichée en aide (ex: `Affiche une démo du menu`).
4. **category** (string) : Catégorie de regroupement (ex: `main`, `debug`, `config`).
5. **order** (int) : Ordre de tri dans le menu (ex: `10`, `20`).
6. **visible_module_menu** (bool) : Visible dans le menu local du module ? (`true`/`false`).
7. **visible_ops_super** (bool) : Visible dans le menu global `ops_super` ? (`true`/`false`).
8. **frequency** (enum) : Fréquence d'usage suggérée (`always`, `daily`, `weekly`, `rare`).
9. **type** (enum) : Type d'exécution (`script`, `function`, `command`).
10. **target** (string) : Cible à exécuter (chemin script, nom fonction, commande shell).

## Exemple

```bash
# ID | Label | Desc | Cat | Order | VisMod | VisOps | Freq | Type | Target
run_demo|Lancer Démo|Affiche le menu démo|main|10|true|false|always|script|scripts/demo.sh
check_status|Vérifier Statut|Vérifie l'état du module|debug|99|true|true|daily|function|check_status
```
