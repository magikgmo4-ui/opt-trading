# SPEC_WHY_RUNTIME_VISUAL_MODEL_01

## 1_MASTER_TARGET

Définir le modèle visuel canonique WHY/runtime afin de représenter la cohérence entre intention, permission, machine, action, preuve, gate, évaluation et verdict.

## 5_GO_PLAN

Le modèle doit permettre de générer ou préparer :

- diagramme Figma / FigJam ;
- export Mermaid / Graphviz futur ;
- crosswalk Airtable ;
- scoring Google Sheets ;
- dashboard gouvernance WHY/runtime.

## 6_FINAL_TARGET

Créer une base documentaire permettant de visualiser :

```text
WHY -> OWNER -> PERMISSION -> MACHINE -> ACTION -> GATE -> TRACE -> EVAL -> VERDICT
```

avec extension multi-machine :

```text
RUNS_ON
DEPENDS_ON
OBSERVED_BY
REVIEWED_BY
RECOVERS_WITH
```

## 7_CANONICAL_STATE

La visualisation est une projection de gouvernance. Elle ne modifie pas le runtime, ne crée aucune exécution et ne décide aucun trade.

## 8_VALIDATED_PLAN

Ordre cible :

```text
GO_OPENCLAW_GOVERNANCE_WHY_POLICY_CROSSWALK_01
-> SPEC_WHY_RUNTIME_VISUAL_MODEL
-> MACHINE GRAPH
-> FIGMA TARGET
-> SCORING
-> DASHBOARD
```

## 9_SELECTED_SOLUTION

Représenter le WHY comme noeud racine ou méta-policy au-dessus des policies MCP :

```text
WHY
= raison canonique de l'action
+ justification du périmètre
+ lien avec owner
+ lien avec permission
+ lien avec gate
+ lien avec trace
+ lien avec verdict
```

## 13_ESTABLISHED

Le WHY doit couvrir :

| Dimension | Question |
|---|---|
| Intention | Pourquoi agir ? |
| Owner | Qui porte l'action ? |
| Permission | Avec quel droit ? |
| Machine | Où s'exécute ou se documente l'action ? |
| Action | Quelle famille d'action ? |
| Gate | Quelle barrière humaine ou mécanique ? |
| Trace | Quelle preuve existe ? |
| Eval | Quelle validation s'applique ? |
| Verdict | PASS / WARN / FAIL / NEVER_ALLOWED |

## 14_HYPOTHESIS

Hypothèse à valider plus tard : le même modèle pourra alimenter un dashboard runtime réel, mais seulement après stabilisation de l'export JSON et des gates.

## 15_REMAINING_GAP

Il manque encore :

- rendu Figma effectif ;
- export JSON réel ;
- mapping complet des GO existants ;
- score de confiance WHY ;
- score de risque runtime ;
- score de confiance worker ;
- visualisation observabilité multi-machine.

## 16_TODO

Créer ensuite :

```text
20_MACHINE_RELATION_GRAPH.md
30_FIGMA_EXPORT_TARGET.md
40_AIRTABLE_SCHEMA.md
50_SCORING_MODEL.md
60_DASHBOARD_TARGET.md
```

## 17_RESUME_POINT

Reprendre à :

```text
NEXT: 20_MACHINE_RELATION_GRAPH.md
```
