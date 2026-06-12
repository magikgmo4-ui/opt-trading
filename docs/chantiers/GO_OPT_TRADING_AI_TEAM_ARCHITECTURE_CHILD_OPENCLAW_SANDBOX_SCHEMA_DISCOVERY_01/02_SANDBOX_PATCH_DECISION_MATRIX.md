# 02_SANDBOX_PATCH_DECISION_MATRIX

## Objectif

Transformer l'audit `01_SANDBOX_SCHEMA_SOURCE_AUDIT.md` en matrice de décision pour corriger le blocage SSH/network OpenClaw.

## Verdict source

```text
PATCHABLE_SAFE_MODE_FOUND
```

## Pivot important

Le blocage initialement attribué à `sandbox.mode = "all"` est reclassé.

```text
Blocage réel identifié : tools deny policy = group:runtime
```

## État observé

| Surface | Valeur | Evidence |
| :--- | :--- | :--- |
| sandbox effectif | mode `off` | `openclaw sandbox explain` |
| session sandboxée | false | `sessionIsSandboxed = false` |
| source sandbox | default | pas de règle custom active |
| repo config | `sandbox.mode = "all"` | `modules/openclaw_config_modulaire/app/agents.json5` |
| bloquant réel | `deny: ["group:runtime", ...]` | agents builder / reviewer / lab |

## Invariants

```text
Aucun runtime OpenClaw.
Aucun patch dans ce document.
Aucune connexion SSH réelle.
Aucun secret dans repo.
Aucun patch global si un patch par agent suffit.
Aucun WAN / bridge / admin-trading.
Aucun closeout DB_LAYER rouvert.
Aucun index global modifié.
```

## Options de patch

| Option | Description | Scope | Avantage | Risque | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- |
| A | Retirer `group:runtime` du `deny` de l'agent ciblé | agent | simple, borné | peut ouvrir plus d'outils runtime que strictement nécessaire | PENDING |
| B | Ajouter explicitement les outils nécessaires dans `allow` par agent | agent | plus fin | dépend du nom exact des outils supportés | PENDING |
| C | Modifier globalement `tools.sandbox.tools.deny` | global | rapide | trop large | NOT_RECOMMENDED |
| D | Activer elevated tools | global / elevated | contournement possible | surface de risque élevée | NOT_RECOMMENDED |
| E | Ne rien modifier | none | sûr | runtime reste bloqué | FALLBACK |

## Agents candidats

| Agent | Evidence | Besoin runtime/SSH | Patch autorisé ? |
| :--- | :--- | :--- | :--- |
| orchestrateur | `openclaw sandbox explain` agentId courant | À confirmer | PENDING |
| builder | deny contient `group:runtime` | À confirmer | PENDING |
| reviewer | deny contient `group:runtime` | À confirmer | PENDING |
| lab | deny contient `group:runtime` | À confirmer | PENDING |

## Décision recommandée

```text
Préférer un patch par agent ciblé.
Éviter tout patch global.
Ne pas modifier sandbox.mode dans cette étape.
```

## Gate avant patch

Un patch ne devient autorisé que si :

* l'agent exact qui doit exécuter SSH/network est identifié ;
* la règle retirée ou ajoutée est minimale ;
* le diff ne modifie pas les autres agents ;
* aucun runtime n'est lancé dans le même lot ;
* rollback git est trivial.

## NEXT_GO

Créer ensuite :

```text
03_TOOL_POLICY_PATCH_PLAN.md
```

Rôle :

1. sélectionner Option A ou B ;
2. cibler l'agent exact ;
3. préparer le diff minimal sur `agents.json5` ;
4. définir rollback ;
5. interdire encore le runtime.

## RISKS

- À qualifier.
