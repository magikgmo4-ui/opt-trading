---
doc_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01_TEMPLATES
doc_type: operator_templates
repo: opt-trading
project: opt-trading
go_id: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
status: open
updated_at: 2026-05-28
---

# 20_TEMPLATES

Templates canoniques opérateur ↔ agent.  
Chaque template est accompagné d'un exemple rempli tiré de GOs réels.

---

## Template A — Opérateur → Agent (GO_PROMPT)

### Schéma vide

```text
ROLE: <rôle de l'agent pour ce GO>

GO_PARENT: <GO_ID parent>

NEXT_GO: <GO_ID à ouvrir>

OBJECTIF:
<description courte du but — 1-3 phrases>

CONTEXTE:
<état actuel : dernier commit, verdicts obtenus, gaps restants>

CONTRAINTES:
- <contrainte 1>
- <contrainte 2>

LIVRABLES:
- <chemin/fichier 1>
- <chemin/fichier 2>

VALIDATIONS:
- <commande 1>
- <commande 2>

VERDICT:
PASS_<NOM> ou BLOCKED_WITH_REASON
```

### Règles de remplissage

| Champ | Obligatoire | Règle |
|---|---|---|
| ROLE | oui | nommer le rôle précis (architecte, auditeur, exécuteur) |
| GO_PARENT | oui | GO_ID parent, même si self-referencing |
| NEXT_GO | oui | GO_ID du prochain child ou "PARENT_CLOSEOUT" |
| OBJECTIF | oui | 1-3 phrases, pas de liste |
| CONTEXTE | oui | citer commits ou verdicts réels |
| CONTRAINTES | oui | au moins 1, liste exhaustive |
| LIVRABLES | oui | chemins explicites, pas "des fichiers" |
| VALIDATIONS | oui | commandes exécutables, pas "vérifier" |
| VERDICT | oui | forme exacte : `PASS_<NOM>` ou `BLOCKED_<RAISON>` |

### Exemple rempli — JOBS_DEDUP_AUDIT_01

```text
ROLE: Auditeur jobs — qualifier les doublons du JOBS_REGISTRY sans aucune suppression

GO_PARENT: GO_AUTOMATION_OPS_OPT_TRADING_PARENT_ARCHITECTURE_JOBS_SEMIAUTO_REFACTOR_01

NEXT_GO: GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01

OBJECTIF:
Auditer les ~86 entrées du JOBS_REGISTRY v1 pour identifier les candidats doublons.
Qualifier chaque suspect en FALSE_POSITIVE, NOT_DEDUP, ou LEGACY_REPLACED.
Produire une table de décision documentée.

CONTEXTE:
JOBS_REGISTRY v1 mergé dans PR #914 (commit 333beaf3).
6 anomalies ouvertes : B01 (tasks.index statut), B02 (22 DRAFT_ONLY),
B03 (orchestration contrat), B04 (signal_processor sans test),
B05 (gha_strict_workers_schedule sans test), B06 (8 scripts apply_desk_pro_*).

CONTRAINTES:
- Doc-only — aucune modification de code ni de workflow.
- Aucune suppression sans preuve de consommateur négatif.
- Classifier chaque anomalie explicitement.
- Aucun fichier hors scope modifié.

LIVRABLES:
- docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/10_DUPLICATE_CANDIDATES.md
- docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/20_CONSUMER_MAP.md
- docs/chantiers/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01/30_DECISION_TABLE.md
- docs/index/inbox/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01.md

VALIDATIONS:
- git grep "apply_desk_pro" -- "*.py" "*.sh" (hors scripts eux-mêmes) → 0 résultat
- grep "toolbox" modules/desk_pro/api/routes.py → PRÉSENT lignes 299-354
- bash -n sur chaque script B06 → PASS syntaxe

VERDICT:
PASS_JOBS_DEDUP_AUDIT
```

---

## Template B — Agent → Opérateur (Rapport de fin de GO)

### Schéma vide

```text
## 7_CANONICAL_STATE
<état vérifié : commits, branche, tests>

## 13_ESTABLISHED
<faits prouvés dans ce GO — citer commandes exécutées>

## 15_REMAINING_GAP
<ce qui reste — avec raison si BLOCKED>

## 16_TODO — NEXT_GO recommandé
GO_ID : <NEXT_GO>
GO_PROMPT :
<GO_PROMPT complet Template A>

## 17_RESUME_POINT
<point de reprise textuel — suffisant pour reprendre sans relire>
```

### Règles de remplissage

| Section | Obligatoire | Règle |
|---|---|---|
| 7_CANONICAL_STATE | oui | citer hash commit ou output commande |
| 13_ESTABLISHED | oui | seulement ce qui a été exécuté et vérifié |
| 15_REMAINING_GAP | oui | vide si aucun, sinon liste avec raison |
| 16_TODO | oui | GO_PROMPT complet du NEXT_GO |
| 17_RESUME_POINT | oui | 3-5 phrases max, auto-suffisant |

### Exemple rempli — après JOBS_DEDUP_AUDIT_01

```text
## 7_CANONICAL_STATE
Branche : go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
Commit HEAD : b7eb4e1f
PR : #915 (ouverte, CI PASS)
Tests governance : 29/29 PASS sur sot/mainline @ 333beaf3

## 13_ESTABLISHED
- B01 tasks.index.json : FALSE_POSITIVE — référencé par run_task.sh et strict-workers
- B02 22 DRAFT_ONLY : FALSE_POSITIVE — validés par CI, DRAFT = statut schema
- B03 orchestration contrat : FALSE_POSITIVE — forward-spec, 0 consommateur actif
- B04 signal_processor + oauth : NOT_DEDUP — problème de test coverage, hors scope
- B05 gha_strict_workers_schedule : NOT_DEDUP — hors scope, ADD_TEST batch dédié
- B06 8 scripts apply_desk_pro_*.sh : LEGACY_REPLACED — routes.py:299-354 déjà patché,
  0 consommateur externe (git grep négatif), commits 4e01dc4a + 3ef76eb3

## 15_REMAINING_GAP
- Suppression B06 dans batch dédié : GO_AUTOMATION_OPS_OPT_TRADING_CHILD_CLEANUP_LEGACY_SCRIPTS_01
- ADD_TEST B04+B05 : batch test lock dédié (hors scope parent actuel)

## 16_TODO — NEXT_GO recommandé
GO_ID : GO_AUTOMATION_OPS_OPT_TRADING_CHILD_SEMIAUTO_LOOP_PROTOCOL_01
GO_PROMPT :
[voir Template A — exemple SEMIAUTO_LOOP_PROTOCOL_01 ci-dessous]

## 17_RESUME_POINT
JOBS_DEDUP_AUDIT_01 PASS. B01-B05 = FALSE_POSITIVE/NOT_DEDUP, aucune suppression.
B06 = LEGACY_REPLACED, 8 scripts à supprimer dans batch CLEANUP_LEGACY_SCRIPTS_01.
JOBS_REGISTRY mis à jour (v1.1). PR #915 sur sot/mainline.
NEXT_GO = SEMIAUTO_LOOP_PROTOCOL_01.
```

---

## Template C — Retour opérateur (screenshot / export)

### Schéma vide

```text
## 7_CANONICAL_STATE
<contenu observé : état PR, CI, tests, branche>

## 13_ESTABLISHED
<faits déduits — seulement ce qui est visible dans le screenshot>

## 16_TODO
<action déclenchée par l'observation>
```

### Exemple rempli — CI PASS sur PR

```text
## 7_CANONICAL_STATE
Screenshot PR #915 :
- CI : 2/2 checks PASS (gated-pr + governance)
- Branche : go/GO_AUTOMATION_OPS_OPT_TRADING_CHILD_JOBS_DEDUP_AUDIT_01
- Reviewer : aucun (doc-only GO)
- État : Mergeable

## 13_ESTABLISHED
- Tous les tests CI PASS sur la branche du GO.
- Diff limité aux fichiers docs/ du GO.
- Aucun fichier runtime modifié.

## 16_TODO
Merger PR #915 sur instruction opérateur → confirmer NEXT_GO SEMIAUTO_LOOP_PROTOCOL_01.
```

---

## Guide de validation du format

Avant d'émettre un GO_PROMPT, vérifier :

```text
□ ROLE nommé explicitement
□ GO_PARENT présent
□ OBJECTIF en 1-3 phrases, sans liste
□ CONTEXTE cite un commit ou verdict récent
□ CONTRAINTES : au moins 1, toutes explicites
□ LIVRABLES : chemins complets listés
□ VALIDATIONS : commandes exécutables
□ VERDICT : PASS_xxx ou BLOCKED_xxx
```

Avant de soumettre un rapport agent, vérifier :

```text
□ 7_CANONICAL_STATE cite un commit hash
□ 13_ESTABLISHED ne contient que des faits vérifiés
□ 15_REMAINING_GAP est honnête (pas "aucun gap" si BLOCKED)
□ 16_TODO inclut le GO_PROMPT complet du NEXT_GO
□ 17_RESUME_POINT est auto-suffisant (ne cite pas "la session")
```
