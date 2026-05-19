# OT-OPS-01 — NOTE DE CLARIFICATION DES RÔLES DESK PRO

## OBJET
Clarifier la distinction entre Runner, Orchestrator et Dashboard pour éviter les confusions d'usage.

## 1. DÉFINITIONS

### A. DESK PRO RUNNER (`desk_pro_runner`)
- **Rôle** : Interface Homme-Machine (CLI/Menu).
- **Responsabilité** : Recevoir l'ordre de l'opérateur ("Lance un run", "Montre le dash").
- **Usage** : C'est le SEUL module que l'opérateur doit appeler directement en ligne de commande (`cmd-desk_pro_runner` ou via Menu Hub).

### B. DESK PRO ORCHESTRATOR (`desk_pro_orchestrator`)
- **Rôle** : Chef d'orchestre logique (Moteur).
- **Responsabilité** : Enchaîner les Engines (Market -> Risk -> Portfolio) de manière séquentielle et fiable.
- **Usage** : Appelé EXCLUSIVEMENT par le Runner ou un Cron. Jamais manuellement.

### C. DESK PRO DASHBOARD (`desk_pro_dashboard`)
- **Rôle** : Visualisation (Lecture seule).
- **Responsabilité** : Afficher l'état JSON produit par l'Orchestrator sous forme lisible (HTML/Terminal).
- **Usage** : Appelé par le Runner ("Run & Show") ou manuellement pour consulter un état passé.

## 2. FLUX CANONIQUE
1. **Opérateur** -> appelle -> **Runner**
2. **Runner** -> appelle -> **Orchestrator** (pour calculer)
3. **Orchestrator** -> produit -> **State JSON**
4. **Runner** -> appelle -> **Dashboard** (pour afficher State JSON)

## 3. CONSÉQUENCE SUR L'EXPOSITION
- `desk_pro_runner` : DOIT avoir un wrapper global (`cmd`, `menu`).
- `desk_pro_dashboard` : DOIT avoir un wrapper global (`cmd`).
- `desk_pro_orchestrator` : NE DOIT PAS avoir de wrapper global (interne).
