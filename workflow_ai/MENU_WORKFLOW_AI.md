## MENU — Workflow AI Gated (opt-trading)

> Mode : Institutionnel Gated + 4 machines  
> Règle : toujours passer par les Gates 0 → 3 avant tout code.

---

### Rappel rapide (humain)

- **Gate 0** : cadrage / lecture / plan (AUCUN code).  
- **Gate 1** : cartographie & design (toujours sans code).  
- **Gate 2** : plan d’implémentation + stratégie backup/rollback (sans code).  
- **Gate 3** : validation finale avant implémentation.  
- **Après GO Gate 3** : implémentation incrémentale avec :
  - `cmd-workflow_ai backup` avant chaque bloc réel,
  - fichiers modifiés, résumé diff, commandes, expected output, rollback.

Architecture :
- `admin-trading` = prod/ops (services, webhook, Desk Pro)  
- `cursor-ai` = dev (Cursor, édition)  
- `db-layer` = DB only  
- `student` = compute/tests/POC  

---

### 1) Démarrer un travail — Gate 0 (cadrage)

**Prompt type :**

> *Mode Gated opt-trading — Gate 0*  
> Objectif : `[décris en 1–2 phrases]`  
> Lis : `@workflow_ai/templates/specs.md`, `@workflow_ai/templates/tasks.md`, `@workflow_ai/templates/db_schema.md`, `@workflow_ai/templates/api_contract.md`  
> - Ne modifie aucun fichier.  
> - Propose :  
>   - résumé du contexte,  
>   - fichiers candidats à modifier (`@File` / `@Folder`),  
>   - plan Gates 1–3 + Impl.  
> Fin de Gate 0 : STOP + « GO ou STOP ? ».

---

### 2) Cartographie & design — Gate 1

**Prompt type :**

> *Mode Gated opt-trading — Gate 1*  
> Objectif : détailler cartographie + design pour l’objectif validé.  
> - Cartographie : modules/fonctions/endpoints/tables impactés, par machine (admin-trading, db-layer, student).  
> - Design technique compatible avec `specs.md`, `tasks.md`, `db_schema.md`, `api_contract.md`.  
> - Liste des fichiers à modifier/créer (sans les toucher).  
> Ne code rien.  
> Fin de Gate 1 : STOP + « GO ou STOP ? ».

---

### 3) Plan d’implémentation + backup/rollback — Gate 2

**Prompt type :**

> *Mode Gated opt-trading — Gate 2*  
> Pour le design Gate 1 validé :  
> - Détailler les incréments (1, 2, 3, …) :  
>   - fichiers concernés,  
>   - commandes prévues (dont `cmd-workflow_ai backup`),  
>   - expected output,  
>   - rollback pour chaque incrément.  
> Ne modifie aucun fichier, ne lance aucune commande.  
> Fin de Gate 2 : STOP + « GO ou STOP ? ».

---

### 4) Validation finale — Gate 3

**Prompt type :**

> *Mode Gated opt-trading — Gate 3*  
> - Récapitule : objectif, design, incréments, backup/rollback.  
> - Vérifie cohérence 4 machines (dev/prod/DB/test).  
> - Propose une checklist finale d’implémentation.  
> Ne modifie rien.  
> Fin de Gate 3 : STOP + « GO ou STOP ? ».

---

### 5) Implémentation d’un incrément (après GO Gate 3)

Pour chaque incrément, lancer explicitement un bloc :

**Prompt type :**

> *Mode Gated opt-trading — Implémentation incrément X*  
> Incrément : `[nom court]`  
> - D’abord : proposer l’exécution de `cmd-workflow_ai backup` (ne PAS la lancer si je ne l’ai pas demandée).  
> - Puis, appliquer le plan validé :  
>   - fichiers à modifier (`@File` / `@Folder`),  
>   - patchs proposés,  
>   - commandes exactes à exécuter (en précisant la machine : admin-trading / db-layer / student / cursor-ai),  
>   - expected output,  
>   - plan de rollback.  
> À la fin de l’incrément : récapitulatif complet (1–5) sans passer à l’incrément suivant tant que je n’ai pas dit GO.

---

### 6) Rappel sécurité / redaction

- LAN-only : ne pas exposer d’URLs publiques ou de tunnels.  
- Jamais coller dans les prompts : secrets, .env complet, clés privées, tokens, webhooks.  
- Toujours redacter : `<REDACTED>` ou `***` pour toute valeur sensible.  

