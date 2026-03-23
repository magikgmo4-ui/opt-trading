# OT_TRAE_DOC_CONVERGENCE_PROTOCOL_V1

```
Date     : 2026-03-20
Mission  : GO_TRAE_DOC_CONVERGENCE_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ
```

---

## 1. OBJET

Ce document est le protocole de convergence documentaire pour les sessions Claude Cowork sur `opt-trading`.

Son rôle est de garantir qu'un même chantier ne vit pas dans plusieurs vérités parallèles : repo, kanban, index, reprise, journal, pack local, TODO doivent tous pointer vers le même état.

Il ne réécrit pas le socle Trae V1 déjà présent dans `docs/ot/trae/`. Il le complète pour le contexte spécifique de collaboration ChatGPT (PM) ↔ Claude (cowork local).

Ce qui est déjà couvert dans le socle Trae V1 et que ce document ne répète pas :
- Classes de mission : `03_MISSION_CLASSES_V1.txt`
- Skills canoniques : `04_SKILLS_V1.txt`
- Format Orchestrator : `12_ORCHESTRATOR_ENTRYPOINT_V1.txt`
- Checklist multi-étapes : `08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`

---

## 2. SOURCES DE VÉRITÉ ET ORDRE DE LECTURE

### 2.1 Sources de vérité actives (passe 2026-03-20 et suite)

| Priorité | Fichier | Rôle |
|---|---|---|
| 1 | `audit/2026-03-20/A4_audit_2026_03_20_formal_close.md` | Clôture formelle de la passe — décisions figées, ÉTABLI/PARTIEL/DIFFÉRÉ |
| 2 | `audit/2026-03-20/97_cross_project_master_kanban.md` | **Kanban maître actif** — statut de tous les chantiers courants |
| 3 | `audit/2026-03-20/00_audit_master_index.md` | Index des livrables produits et points de reprise |
| 4 | Document canonique du périmètre concerné | Fiche spécifique au chantier (92/93/94/A0/A1/... selon le périmètre) |
| 5 | `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md` | Reprise Trae — à lire si le chantier est lié à un item Trae V1 |
| 6 | `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` | Kanban Trae — source de vérité pour les chantiers Trae V1 internes |

### 2.2 Ordre de lecture obligatoire en début de session Claude

```
Lecture minimale avant tout chantier :
  1. A4_audit_2026_03_20_formal_close.md    ← décisions figées, ne pas rouvrir
  2. 97_cross_project_master_kanban.md      ← état courant de chaque périmètre
  3. 00_audit_master_index.md               ← localiser les livrables existants
  4. [document du périmètre concerné]       ← fiche canonique du chantier visé
```

Lecture complémentaire si chantier Trae V1 :
```
  5. docs/ot/trae/OT_TRAE_SESSION_REPRISE.md
  6. docs/ot/kanban/opt_trading_kanban_source_of_truth.md
```

### 2.3 Règle de priorité entre kanbans

Le **kanban maître `97_cross_project_master_kanban.md`** est la source de vérité courante pour les chantiers de la passe 2026-03-20 et ceux qui en découlent.

Le kanban Trae `docs/ot/kanban/opt_trading_kanban_source_of_truth.md` reste la source de vérité pour les chantiers Trae V1 internes (items `GO_OT_*`).

En cas de conflit entre les deux : le kanban maître `97_*` prime pour tout ce qui concerne `student`, `api collector`, runtime surfaces, `localcms`, `algo_hf`, `hf_trading`, `openclaw`. Le kanban Trae prime pour tout ce qui concerne les briques V1 internes Trae (`GO_OT_TRAE_*`).

---

## 3. PROTOCOLE CHATGPT ↔ CLAUDE

### 3.1 Rôles

| Rôle | Outil | Responsabilité |
|---|---|---|
| **PM / cadrage / validation** | ChatGPT | Décide les chantiers, fixe les statuts, valide les livrables, met à jour le kanban maître, tranche les ambiguïtés de périmètre |
| **Exécution locale** | Claude (Cowork) | Produit les livrables documentaires, lit les fichiers locaux, applique les corrections bornées, rend compte |

### 3.2 Flux de mission standard

```
ChatGPT → formule la mission avec :
  - MISSION_ID (ex. GO_TRAE_DOC_CONVERGENCE_01)
  - contexte établi
  - objectif
  - contraintes
  - livrable attendu

Claude → exécute et rend :
  - état réel observé localement
  - fichiers produits / modifiés
  - corrections appliquées
  - limites réelles observées
  - statut final
  - point de reprise suivant

ChatGPT → valide et :
  - met à jour le kanban maître (statut du chantier)
  - confirme ou recadre le point de reprise
  - ouvre ou ferme le chantier suivant
```

### 3.3 Ce que Claude ne fait jamais sans mandat PM explicite

- Modifier le statut d'un chantier dans le kanban maître (sauf corrections de formulation mandatées)
- Créer un nouveau périmètre ou une nouvelle surface canonique
- Pousser sur Git
- Committer
- Modifier les décisions figées dans `A4_audit_2026_03_20_formal_close.md`

### 3.4 Ce que Claude fait systématiquement

- Lire les sources dans l'ordre §2.2 avant toute production
- Signaler explicitement ce qui est ÉTABLI vs HYPOTHÈSE
- Signaler toute contradiction entre sources lues
- Rendre un état de reprise exploitable immédiatement après

---

## 4. CLASSIFICATION CANONIQUE D'UN CHANTIER

### 4.1 Définitions

| Statut | Définition | Condition de changement |
|---|---|---|
| **ÉTABLI** | Décision figée. Preuve documentée. Ne pas rouvrir sans besoin PM explicite. | Décision PM + clôture formelle |
| **PARTIEL** | Chantier commencé, livrable documentaire produit, mais validation live manquante ou cleanup non exécuté. | Validation live OK + PM signe le passage en ÉTABLI |
| **DIFFÉRÉ** | Chantier identifié, cadré, mais intentionnellement hors périmètre actif. Point de reprise nommé. | PM décide de l'activer |
| **HORS PÉRIMÈTRE** | Pas dans le bundle actif. Pas de support canonique. Ne pas adresser sans entrée PM explicite. | PM décide d'un point de réentrée |

### 4.2 Usage en pratique

Un chantier ne change de statut que dans le kanban maître, après validation PM.

Claude peut proposer un changement de statut dans son compte-rendu d'exécution, mais ne l'applique pas unilatéralement dans le kanban.

### 4.3 Correspondance avec les classes Trae V1

| Statut chantier | Classe Trae V1 typique |
|---|---|
| ÉTABLI | le chantier a produit un CLOSE (closing) |
| PARTIEL | le chantier a produit un livrable mais reste EN_COURS ou PARTIELLE |
| DIFFÉRÉ | le chantier est CLOSE_PREV1 ou TODO non activé |
| HORS PÉRIMÈTRE | hors kanban — pas de MISSION_ID actif |

---

## 5. FORMAT MINIMAL DE MISSION LOCALE

Toute mission envoyée à Claude doit contenir au minimum :

```
MISSION_ID       : identifiant unique (ex. GO_STUDENT_LIVE_VALIDATION_PACK_01)
OBJECTIF         : 1 à 5 lignes — ce qui doit être produit
CONTEXTE ÉTABLI  : ce qui est figé, ne pas rouvrir
CONTRAINTES      : ce que Claude ne doit pas faire
SCOPE            : périmètre exact autorisé
LIVRABLE ATTENDU : liste des fichiers / documents / corrections attendus
STATUT CIBLE     : ÉTABLI / PARTIEL / DIFFÉRÉ attendu après la mission
```

Référence de format étendu pour missions multi-étapes : `docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt` + `docs/ot/trae/08_MULTI_STEP_MISSION_CHECKLIST_V1.txt`

---

## 6. FORMAT MINIMAL D'EXÉCUTION / HANDOFF / CLÔTURE / REPRISE

### 6.1 Compte-rendu d'exécution (obligatoire, chaque mission)

Claude rend systématiquement les 7 points suivants :

```
1. État réel observé localement
   → ce qui a été constaté dans le repo, les fichiers, les scripts

2. Documents / fichiers produits
   → liste précise avec chemins

3. Corrections / décisions appliquées
   → formulation exacte de chaque remplacement ou ajout

4. Scripts modifiés ou non
   → confirmation explicite (même si aucun)

5. Limites réelles observées
   → ce qui n'a pas pu être vérifié (SSH inaccessible, GitHub non consulté, etc.)

6. Statut final du chantier
   → ÉTABLI / PARTIEL / DIFFÉRÉ (proposition — validation PM requise)

7. Point de reprise suivant
   → MISSION_ID du prochain chantier logique + prérequis
```

### 6.2 Handoff (si la mission est passée de Claude à l'opérateur ou à ChatGPT)

Le handoff doit contenir :
- Ce qui a été produit (liens directs)
- Ce qui reste à faire manuellement (accès SSH, validation live, etc.)
- Les points en attente de validation PM
- Le prochain chantier logique

### 6.3 Clôture formelle d'une mission (closing)

Une mission est considérée **formellement close** quand :
1. Le compte-rendu d'exécution est rendu (§6.1)
2. Le kanban maître est mis à jour par PM avec le nouveau statut
3. Si applicable, un fichier closing est déposé dans `docs/ot/closings/`

Un closing n'est pas obligatoire pour toutes les missions Claude. Il est requis pour :
- les chantiers qui passent à ÉTABLI
- les chantiers qui modifient une décision PM figée
- les missions AUDIT_REALIGNEMENT

Format de closing : s'appuyer sur les closings existants dans `docs/ot/closings/` comme référence de style.

### 6.4 Point de reprise

Un point de reprise valide doit contenir :
- `MISSION_ID` nommé
- État du chantier laissé
- Prérequis pour continuer
- Action concrète première (une seule ligne)

Exemple canonique :
```
GO_STUDENT_LIVE_VALIDATION_PACK_01 → LIVRÉ / EN ATTENTE VALIDATION LIVE
  Prérequis : accès SSH sur machine Linux cible où /opt/trading/student est déployé
  Action : bash /opt/trading/student/validation/validate_student_live.sh
```

---

## 7. RÈGLES DE NON-RÉGRESSION

Ces règles s'appliquent à toutes les sessions Claude dans le contexte opt-trading :

```
R01 — Ne pas pousser sur Git depuis Claude Cowork
R02 — Ne pas committer depuis Claude Cowork
R03 — Ne pas modifier la topologie canonique sans validation PM
R04 — Ne pas créer de couche de pilotage concurrente au kanban maître
R05 — Ne pas changer le statut d'un chantier sans validation PM
R06 — Ne pas mélanger ÉTABLI et HYPOTHÈSE dans un compte-rendu
R07 — Ne pas supprimer de script ou de fichier sans preuve que rien ne l'appelle en production
R08 — Ne pas traiter db-layer comme un déploiement opt-trading (confirmé absent)
R09 — Ne pas mélanger la machine student (runtime) et le workstream student (sous-projet)
R10 — Ne pas fusionner localcms dans opt-trading
R11 — Ne pas réactiver openclaw, hf_trading, algo_hf sans entrée PM explicite
R12 — Signaler toute contradiction entre sources lues — ne pas la lisser silencieusement
R13 — Lire les sources dans l'ordre §2.2 avant toute production
R14 — Ne pas créer un nouveau fichier OT_* à la racine du repo (migration docs/ot/* établie)
```

---

## 8. CONVERGENCE — RÉCONCILIATION DES SOURCES PARALLÈLES

### 8.1 Le problème à éviter

Un même chantier peut apparaître sous plusieurs formes dans des fichiers différents :
- dans le kanban maître (`97_*`) avec un statut
- dans l'index (`00_*`) avec une note de livraison
- dans un fichier de reprise (`A4_*`) avec une classification
- dans un closing Trae avec un statut différent
- dans le journal avec une note informelle

Si ces états divergent, le chantier vit dans plusieurs vérités parallèles.

### 8.2 Règle de réconciliation

```
Source primaire  : 97_cross_project_master_kanban.md (pour chantiers passe 2026-03-20+)
Source secondaire : A4_audit_2026_03_20_formal_close.md (décisions figées)
Source tertiaire  : 00_audit_master_index.md (localisation des livrables)
```

En cas de divergence entre ces trois sources : signaler immédiatement à PM. Ne pas trancher unilatéralement.

### 8.3 Synchronisation minimale après chaque mission Claude

Après chaque mission exécutée par Claude, le PM (ChatGPT) doit mettre à jour **au minimum** :
- le statut dans `97_cross_project_master_kanban.md`
- le point actif dans §12 du kanban maître

Claude ne met à jour le kanban que si la mission est une correction de formulation bornée avec mandat explicite.

---

## 9. POINT DE REPRISE

```
GO_TRAE_DOC_CONVERGENCE_01 → LIVRÉ

Document produit : docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_PROTOCOL_V1.md
Checklist complémentaire : docs/ot/trae/OT_TRAE_DOC_CONVERGENCE_CHECKLIST_V1.md

Prochain chantier logique selon kanban maître (§12) :
  → GO_STUDENT_LIVE_VALIDATION_PACK_01 : validation live sur machine Linux cible
    (SSH requis — hors périmètre Claude Cowork local)
  ou
  → GO_ALGO_HF_DEEP_AUDIT_01 : SSH db-layer + GitHub algo_hf
    (SSH requis — hors périmètre Claude Cowork local)

Chantier documentaire faisable sans SSH :
  → tout chantier de type PATCH_LOCAL ou AUDIT_REALIGNEMENT sur le repo local
```
