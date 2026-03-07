# Student DeepSeek - Runbook

## 1. Objectif
Ce document guide l'opérateur pour utiliser le pack **DeepSeek Student** sur la machine `student` (Linux Headless).
Il permet d'exécuter les analyses DeepSeek locales et de consulter les logs de manière robuste.

## 2. Pré-requis
- Accès SSH à `student`
- Module `deepseek_hub` présent dans `modules/`
- Pack `deepseek-student` installé

## 3. Commandes Globales
Les wrappers suivants sont disponibles après installation :

| Commande | Description |
|---|---|
| `deepseek-student` | Wrapper principal (status, run, summary) |
| `menu-deepseek-student` | Menu interactif simple |
| `sanity-deepseek-student` | Vérification de l'environnement DeepSeek |
| `deepseek-student-run-logged` | Exécuter une analyse avec logs (Terminal + Fichier) |
| `deepseek-student-tail-log` | Voir la fin du dernier log |

## 4. Flux Opérateur : Exécution DeepSeek

1. **Connexion SSH**
   ```bash
   ssh user@student
   ```

2. **Vérification de Santé**
   ```bash
   sanity-deepseek-student
   ```
   *Attendu : "DeepSeek Student Sanity Check Passed"*

3. **Lancer une Analyse Loggée**
   ```bash
   deepseek-student-run-logged status
   # OU
   deepseek-student-run-logged models
   ```
   *Affiche la progression à l'écran ET écrit dans `data/logs/deepseek_student/`.*

4. **Consulter le Résultat**
   ```bash
   deepseek-student-tail-log
   ```

## 5. Gestion des Incidents Courants

### Cas : Logs introuvables
**Symptôme** : `tail-latest-log` échoue.
**Diagnostic** :
1. Aucun run n'a encore été lancé.
2. Droits d'écriture manquants dans `data/logs`.

**Action** :
1. Lancer un run : `deepseek-student-run-logged status`
2. Vérifier les permissions : `ls -ld data/logs`

### Cas : Module DeepSeek manquant
**Action** :
1. Vérifier que `modules/deepseek_hub` est présent.
2. Relancer l'installation des wrappers si nécessaire :
   ```bash
   sudo ./scripts/student/deepseek_student_install.sh
   ```

## 6. Emplacements Clés

- **Racine Repo** : `/opt/trading` (typique)
- **Logs DeepSeek** : `data/logs/deepseek_student/`
  - `latest.log` : Lien vers le dernier log
- **Module Hub** : `modules/deepseek_hub/scripts/`

---
*Dernière mise à jour : 2026-03-06*
