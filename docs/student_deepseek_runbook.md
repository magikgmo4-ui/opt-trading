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

3. **Lancer une Analyse (Think)**
   ```bash
   deepseek-student think "Analyser le module market_scanner"
   ```
   *La sortie s'affiche et est logguée.*

4. **Demander une Réponse (Response)**
   ```bash
   deepseek-student response "Expliquer la stratégie de risque"
   ```

5. **Roadmap et Modules**
   ```bash
   # Voir les prochains événements
   deepseek-student roadmap-events
   
   # Analyser un module spécifique
   deepseek-student roadmap-think-module deepseek_hub
   ```

6. **Consulter les Logs et Archives**
   ```bash
   # Dernier log technique
   deepseek-student tail-latest-log
   
   # Dernier résultat Thinking
   deepseek-student show-latest-thinking
   
   # Dernier résultat Response
   deepseek-student show-latest-response
   ```

## 5. Automatisation Quotidienne

### Installation du Timer
Le pack inclut un job quotidien qui analyse les logs récents pour détecter les problèmes.
Pour l'installer (timer systemd utilisateur) :

```bash
deepseek-student install-daily-timer
```
*Le job tournera tous les jours à 06:30.*

### Lancement Manuel
Pour forcer l'exécution immédiate de l'analyse quotidienne :
```bash
deepseek-student daily-log-thinking
```

### Consultation du Résultat
Le résultat de l'analyse quotidienne est stocké dans `_student_archive/thinking/daily/` et lié via `daily_latest.md`.
Pour le lire :
```bash
# Via wrapper (à implémenter ou cat direct)
cat /opt/trading/_student_archive/thinking/daily/daily_latest.md
```

## 7. Structure du Menu Opérateur

Le menu interactif (`menu-deepseek-student`) est structuré pour simplifier l'exploitation :

1. **Utilisation Quotidienne** : Actions métier fréquentes (Think, Response, Roadmap).
2. **Résultats / Archives** : Consultation rapide des derniers outputs sans chercher les fichiers.
3. **Automatisation** : Gestion du job quotidien (Timer, Logs, Run manuel).
4. **Dev / Debug** : Outils techniques pour l'ingénieur (Sanity, Models, Paths).

## 8. Gestion des Incidents Courants

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
