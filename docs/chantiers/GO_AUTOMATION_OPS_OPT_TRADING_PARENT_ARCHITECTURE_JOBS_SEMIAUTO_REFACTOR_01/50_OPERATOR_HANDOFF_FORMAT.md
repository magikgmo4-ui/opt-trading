---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01_HANDOFF_FORMAT
doc_type: operator_handoff_format
repo: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01
status: open
updated_at: 2026-05-28
---

# 50_OPERATOR_HANDOFF_FORMAT

## Objectif

Standardiser les formats d'échange entre l'opérateur humain et l'agent Claude.
Deux directions : **opérateur → agent** (GO_PROMPT) et **agent → opérateur** (rapport / reprise).

---

## Format A — Opérateur → Agent (GO_PROMPT)

Champs obligatoires :

```text
ROLE: <rôle de l'agent pour ce GO>

GO_PARENT: <GO_ID parent si applicable>

NEXT_GO: <GO_ID à ouvrir>

OBJECTIF:
<description courte du but — 1-3 phrases>

CONTEXTE:
<état actuel du chantier — commits, verdicts, gaps>

CONTRAINTES:
- <contrainte 1>
- <contrainte 2>
...

LIVRABLES:
- <fichier à créer 1>
- <fichier à créer 2>
...

VALIDATIONS:
- <commande à exécuter 1>
- <commande à exécuter 2>
...

VERDICT:
<PASS_xxx>
ou
<BLOCKED_WITH_REASON>
```

Règles :
- `CONTRAINTES` est obligatoire — liste ce que l'agent ne peut pas faire.
- `LIVRABLES` est obligatoire — liste les fichiers attendus.
- `VALIDATIONS` est obligatoire — liste les commandes de vérification.
- `VERDICT` est obligatoire — définit la forme du retour attendu.

---

## Format B — Agent → Opérateur (Rapport de reprise)

Sections obligatoires :

```text
## 7_CANONICAL_STATE
<état vérifié du repo : commits, tests, verdicts>

## 13_ESTABLISHED
<faits prouvés dans ce GO>

## 15_REMAINING_GAP
<ce qui reste à faire — avec raison si BLOCKED>

## 16_TODO — NEXT_GO recommandé
<GO_ID suivant avec GO_PROMPT complet>

## 17_RESUME_POINT
<point de reprise textuel en cas d'interruption>
```

Règles :
- `7_CANONICAL_STATE` doit citer des commits ou des sorties de commandes.
- `17_RESUME_POINT` doit permettre de reprendre sans relire toute la session.
- Ne pas inventer de faits — seulement ce qui a été exécuté et vérifié.

---

## Format C — Retour screenshot / export

Quand l'opérateur fournit un screenshot ou un export :

```text
## 7_CANONICAL_STATE
<contenu observé dans le screenshot : état PR, tests, branch, CI>

## 13_ESTABLISHED
<faits déduits du screenshot>

## 16_TODO
<action déclenchée par observation>
```

---

## Anti-patterns à éviter

| Anti-pattern | Correction |
|---|---|
| GO_PROMPT sans LIVRABLES explicites | toujours lister les fichiers attendus |
| Rapport sans commits cités | citer au moins le hash de tête |
| Verdict implicite | toujours écrire PASS_xxx ou BLOCKED_WITH_REASON |
| NEXT_GO sans GO_PROMPT | toujours inclure le GO_PROMPT du prochain GO |
| Reprise sans 17_RESUME_POINT | obligatoire pour toute interruption |
| Agent merge sans instruction | `gh pr merge` uniquement sur instruction explicite |

---

## Livrable child GO

```text
GO_AUTOMATION_OPS_OPT_TRADING_CHILD_OPERATOR_HANDOFF_FORMAT_01
→ templates finalisés
→ exemples annotés
→ guide de validation du format
```
