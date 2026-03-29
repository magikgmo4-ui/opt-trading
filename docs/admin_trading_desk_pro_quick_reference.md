# Admin Trading Desk Pro - Quick Reference

| Action | Commande | Description |
|---|---|---|
| **Santé** | `sanity-desk_pro` | Vérifier l'état global du système |
| **Status** | `desk-pro status` | Afficher les composants disponibles |
| **Guard** | `desk-pro runtime-guard` | Verifier les signaux runtime consolides |
| **Info Run** | `desk-pro-last-run` | Résumé du dernier run/log |
| **Exécuter** | `desk-pro-run-logged` | Lancer un run complet avec logs |
| **Log** | `desk-pro-tail-log` | Voir les 50 dernières lignes du log |
| **Dashboard** | `desk-pro dashboard-latest` | Afficher le résumé portefeuille |
| **Journal** | `desk-pro show-session-journal` | Lire les notes de session |
| **Note** | `desk-pro add-session-note "..."` | Ajouter une note rapide |
| **Export HTML** | `desk-pro export-html-latest` | Générer le rapport HTML |
| **Partager** | `desk-pro-copy-latest` | Copier HTML/JSON vers /shared |
| **Menu** | `menu-desk_pro` | Interface interactive complète |

---
**Runtime Guard** : lancer `desk-pro runtime-guard` avant session, après incident/doute runtime, et après changement services/wrappers/Desk Pro.
**Lecture** : `PASS` = continuer ; `WARN` = lire la cause principale et vérifier si c'est transitoire/récupéré ; `FAIL` = traiter avant exploitation.
**Rappel Guard** : garde-fou opérateur, pas preuve absolue de santé métier.
**Rappel** : Mode **PAPER** uniquement. Aucune action réelle sur le marché.
**Logs** : `/opt/trading/data/logs/desk_pro/`
**Partage** : `/shared/desk_pro/latest/`
