# GO_OPENCLAW_GOVERNANCE_WHY_POLICY_CROSSWALK_01 — Initial Project Doc

## 1_MASTER_TARGET

Créer une surface documentaire de visualisation WHY/runtime pour `cursor-ai`, transformant les relations gouvernance -> machine -> runtime -> verdict en artefacts visuels exploitables : diagrammes, dashboard et crosswalk.

## 2_INITIAL_PROJECT_DOC

GO documentaire :

```text
GO_OPENCLAW_GOVERNANCE_WHY_POLICY_CROSSWALK_01
```

Branche :

```text
go/GO_OPENCLAW_GOVERNANCE_WHY_POLICY_CROSSWALK_01
```

Machine propriétaire :

```text
cursor-ai
```

Nature :

```text
DOC_ONLY
READ_ONLY
NO_RUNTIME_CHANGE
NO_GLOBAL_INDEX_CHANGE
NO_AUTOFIX
NO_ALERT
```

## 3_INITIAL_NEED

Transformer les couches WHY existantes en représentation exploitable :

```text
WHY
-> OWNER
-> PERMISSION
-> MACHINE
-> ACTION
-> GATE
-> TRACE
-> EVAL
-> VERDICT
```

Relier aussi les surfaces machine :

```text
student
cursor-ai
admin-trading
db-layer
fantome
```

## 4_MASTER_PROJECT_PLAN

Produire une documentation stable pour :

1. canoniser le modèle visuel WHY/runtime ;
2. préparer un graph multi-machine ;
3. définir une cible Figma ;
4. définir un schéma Airtable crosswalk ;
5. définir un scoring Sheets/dashboard ;
6. préparer le point de reprise vers visualisation réelle.

## 6_FINAL_TARGET

Obtenir le premier modèle documentaire pour :

```text
premier dashboard WHY/runtime
+
premier graph multi-machine
+
première couche visuelle gouvernance
+
export exploitable Figma
```

## 7_CANONICAL_STATE

Établi :

- la couche WHY existe déjà ;
- runtime-security existe ;
- human gates existent ;
- overlays WHY/runtime existent ;
- lint WHY reste détecteur non destructif ;
- visualisation exploitable encore absente ;
- ce GO démarre en documentation seulement.

## 9_SELECTED_SOLUTION

Approche retenue :

```text
Documentation -> visualisation -> dashboard
```

et non :

```text
runtime -> implémentation -> outil
```

## 11_KEY_DECISIONS

- Figma = visualisation prioritaire.
- Airtable = crosswalk données.
- Sheets = scoring.
- Aucun index global.
- Aucun runtime réel.
- Machine propriétaire : cursor-ai.

## 12_INVARIANTS

```text
NO_RUNTIME_MUTATION
NO_GLOBAL_INDEX_CHANGE
NO_AUTOFIX
DOC_ONLY
READ_ONLY
NO_SECRET
NO_TRADE
```

## 17_RESUME_POINT

Reprendre depuis :

```text
GO_OPENCLAW_GOVERNANCE_WHY_POLICY_CROSSWALK_01
STATUS: OPEN_DOC_ONLY
NEXT: 10_SPEC_WHY_RUNTIME_VISUAL_MODEL.md
```
