# GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_BUILDER_FIRST_CONTROLLED_JOB_01

## 3_INITIAL_NEED

Après la clôture PASS_WITH_PIVOTS du child OpenClaw sandbox schema discovery, le gateway V2 est actif et stable, et les agents `orchestrateur` et `builder` ont répondu correctement à un premier test runtime non destructif.

## 6_FINAL_TARGET

Cadrer et exécuter un premier job contrôlé du builder via gateway OpenClaw, sans SSH réel, sans commande remote, sans patch runtime non validé.

## 13_ESTABLISHED

- Child précédent : GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_CHILD_OPENCLAW_SANDBOX_SCHEMA_DISCOVERY_01
- PR précédente : #389
- Merge commit : 482e2f21d347992f15de237c3bf9dc285f8daf44
- Gateway : UP_AND_STABLE
- orchestrateur : ALIVE
- builder : ALIVE
- SSH réel : non lancé
- remote exec : non lancé
- WAN exposure : absent
- repo V1.2.1 brute : NO_GO
- config effective : OpenClaw Remote V2

## 12_INVARIANTS

```text
Aucun SSH réel.
Aucune commande remote.
Aucun secret dans le repo.
Aucun patch runtime sans gate explicite.
Aucun WAN.
Aucun bridge.
Aucun admin-trading.
Aucun closeout DB_LAYER rouvert.
Aucun index global modifié sans instruction explicite.
Premier job builder = non destructif, borné, loggé.
```

## 16_TODO

1. Définir le premier job builder contrôlé.
2. Définir la commande exacte.
3. Définir la preuve attendue.
4. Définir les stop conditions.
5. Obtenir validation humaine avant exécution.
6. Créer ensuite `01_BUILDER_FIRST_JOB_GATE.md`.

## RISKS

- À qualifier.
