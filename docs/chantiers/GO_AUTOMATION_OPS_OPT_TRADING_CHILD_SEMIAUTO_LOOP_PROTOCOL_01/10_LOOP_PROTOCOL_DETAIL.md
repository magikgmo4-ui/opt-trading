---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01_LOOP_DETAIL
doc_type: loop_protocol_detail
repo: opt-trading
project: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
status: open
updated_at: 2026-05-28
---

# 10_LOOP_PROTOCOL_DETAIL

## La boucle canonique — 7 étapes

```
[1] Opérateur valide un plan
       ↓
[2] ChatGPT émet un GO_PROMPT (contexte + contraintes + livrables)
       ↓
[3] IDE / Claude Code exécute (code, git, tests)
       ↓
[4] Preuves produites : PR / diff / rapport / test results
       ↓
[5] Retour opérateur : screenshot ou export + 7_CANONICAL_STATE
       ↓
[6] ChatGPT analyse l'état, émet NEXT_GO ou closeout
       ↓
[7] Opérateur approuve ou redirige → retour à [1] ou [2]
```

---

## Étape 1 — Validation opérateur

**Qui :** Opérateur humain.  
**Quoi :** Confirmer le GO_ID, le scope, les livrables, les contraintes.  
**Format :** Message texte ou approval de PR.

**Exemples de formulations valides :**
```text
"next go"
"go pour CLEANUP_LEGACY_SCRIPTS_01"
"applique B06 — suppression 8 scripts"
```

**Exemples de formulations invalides (insuffisantes) :**
```text
"fais quelque chose avec les scripts"   ← scope ambigu
"continue"                              ← sans GO_ID
```

---

## Étape 2 — Émission du GO_PROMPT

**Qui :** ChatGPT (ou operateur) → transmis à l'agent Claude.  
**Quoi :** GO_PROMPT au format canonique (voir `20_TEMPLATES.md`).  
**Règles :**
- Doit contenir ROLE, GO_PARENT, OBJECTIF, CONTEXTE, CONTRAINTES, LIVRABLES, VALIDATIONS, VERDICT.
- Doit citer le dernier commit ou état connu.
- Doit nommer explicitement les fichiers à créer.

---

## Étape 3 — Exécution agent

**Qui :** Claude Code (IDE, OpenClaw, CLI).  
**Quoi :** Crée les fichiers, commits, push.  
**Règles :**
- Créer une branche `go/<GO_ID>` depuis `sot/mainline`.
- Commits atomiques par livrable.
- `git diff` présenté avant chaque push.
- Tests exécutés avant création PR.

**Conditions de stop obligatoires :**
| Situation | Action |
|---|---|
| Test inattendu échoue | Stop — rapport d'état — demander validation |
| Conflit git non résolvable sans décision domaine | Stop — décrire le conflit |
| Fichier hors scope à modifier | Stop — nommer le fichier — demander autorisation |
| Permission / secret manquant | Stop — BLOCKED_WITH_REASON |
| Scope dépassé | Stop — rapport de scope dépassé |

---

## Étape 4 — Production des preuves

**Qui :** Claude Code.  
**Quoi :** PR créée, rapport produit, tests PASS.  
**Format minimal :**
```text
PR : #<number> — <titre>
Branche : go/<GO_ID> → sot/mainline
Tests : <N> PASS / 0 FAIL
Diff : <nb fichiers> fichiers, +<N>/-<N> lignes
```

**Livrable toujours inclus :** rapport au format B (voir `20_TEMPLATES.md`).

---

## Étape 5 — Retour opérateur

**Qui :** Opérateur humain.  
**Quoi :** Screenshot CI / état PR / confirmation merge.  
**Format :** Message texte ou screenshot transmis à ChatGPT.

**Exemples de retour valide :**
```text
"CI PASS — PR #917 — merge ok"
"tests failure sur test_xxx — voir screenshot"
"merge fait — confirme NEXT_GO"
```

---

## Étape 6 — Analyse état / NEXT_GO

**Qui :** ChatGPT → émet le prochain GO_PROMPT.  
**Quoi :** Lit le rapport agent + état PR.  
**Output :** NEXT_GO avec GO_PROMPT complet ou closeout parent.

**Conditions de closeout parent :**
- Tous les child GOs de la liste parent = `status: closed`.
- Aucune anomalie ouverte non traitée.
- Tests governance PASS sur `sot/mainline`.

---

## Étape 7 — Approbation ou redirection

**Qui :** Opérateur humain.  
**Options :**
- `→ [1]` : approuve NEXT_GO → nouvelle itération.
- `→ [2]` : modifie le scope du GO_PROMPT → réémission.
- `→ closeout` : ferme le parent GO.

---

## Conditions de merge d'une PR

Une PR peut être mergée (sur instruction opérateur explicite) si :

| Condition | Vérification |
|---|---|
| Tests CI PASS | Screenshot ou `gh pr checks` |
| Diff limité au scope GO_PROMPT | `git diff sot/mainline...HEAD` |
| Aucun fichier hors scope modifié | `git diff --name-only` |
| Whitespace check PASS | CI |
| Rapport de validation produit | fichier `40_ACCEPTANCE_REPORT.md` présent |

---

## Conditions de rollback

Déclencher `git revert <merge_commit>` si :
- Test de régression échoue après merge sur `sot/mainline`.
- Un consommateur externe signale une interface cassée.
- Un comportement runtime inattendu est détecté post-merge.

Méthode préférée : nouvelle PR corrective plutôt que force-push.

---

## Invariants permanents

| Invariant | Non-négociable |
|---|---|
| Gate humain | Jamais bypasser l'approbation opérateur |
| GO_PROMPT avec LIVRABLES | Toujours lister les fichiers attendus explicitement |
| Rapport avec commits cités | Toujours citer le hash de tête |
| Verdict explicite | Toujours écrire PASS_xxx ou BLOCKED_WITH_REASON |
| NEXT_GO avec GO_PROMPT | Inclure le GO_PROMPT complet du prochain GO |
| 17_RESUME_POINT | Obligatoire pour toute interruption de session |
| Pas de merge sans instruction | `gh pr merge` uniquement sur instruction explicite |

---

## Exemples annotés

### Exemple 1 — GO doc-only (JOBS_DEDUP_AUDIT_01)

```
[1] Opérateur : "next go" (après JOBS_REGISTRY_01 closed)
[2] ChatGPT : émet GO_PROMPT JOBS_DEDUP_AUDIT_01
    → OBJECTIF : auditer ~80 jobs du JOBS_REGISTRY pour identifier doublons
    → LIVRABLES : 10_DUPLICATE_CANDIDATES.md, 20_CONSUMER_MAP.md, 30_DECISION_TABLE.md
    → CONTRAINTES : doc-only, aucune suppression sans preuve
[3] Claude Code : crée branche go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
    → grep consommateurs B06, rédige 3 fichiers, commit
[4] PR #915 créée — rapport : B01-B05 FALSE_POSITIVE, B06 LEGACY_REPLACED
[5] Opérateur : "CI PASS — merge ok"
[6] ChatGPT : PASS_JOBS_DEDUP_AUDIT, NEXT_GO = SEMIAUTO_LOOP_PROTOCOL_01
[7] Opérateur : "next go" → itération suivante
```

### Exemple 2 — GO avec suppression (CLEANUP_LEGACY_SCRIPTS_01)

```
[1] Opérateur : "go pour CLEANUP_LEGACY_SCRIPTS_01 — suppression 8 scripts B06"
[2] ChatGPT : émet GO_PROMPT CLEANUP_LEGACY_SCRIPTS_01
    → OBJECTIF : supprimer les 8 scripts apply_desk_pro_*.sh
    → PREUVE : routes.py:299-354 déjà patché, 0 consommateur externe
    → LIVRABLES : git rm 8 fichiers + inbox entry closed
[3] Claude Code : git rm scripts/apply_desk_pro_*.sh, bash -n routes.py PASS
[4] PR #916 créée — diff : -8 fichiers, 0 modification runtime
[5] Opérateur : "CI PASS — merge ok"
[6] ChatGPT : PASS_CLEANUP_LEGACY_SCRIPTS, NEXT_GO = parent_closeout
[7] Opérateur : "next go" → closeout parent
```
