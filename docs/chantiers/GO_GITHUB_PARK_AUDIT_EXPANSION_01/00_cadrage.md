---
doc_id: OPT_TRADING_GO_GITHUB_PARK_AUDIT_EXPANSION_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
go_id: GO_GITHUB_PARK_AUDIT_EXPANSION_01
status: open
lifecycle_stage: cadrage
topic_keys:
  - github
  - audit
  - branches
  - trunks
  - module_families
  - cartography
surface: park
source_kind: canonical
updated_at: 2026-04-14
links:
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/INDEX.md
  - docs/master_pack/mission_starter_pack/00_mission_start_guide.md
  - journal/index/ACTIVE_GO_MATRIX.md
  - docs/governance/HUMAN_CONTINUITY_TRANSMISSION.md
  - docs/ot/kanban/opt_trading_kanban_source_of_truth.md
  - docs/ot/closings/OT_GITHUB_PARK_CONSOLIDATION_DECISION_02B_CLOSING.txt
  - docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02C.md
---

# GO_GITHUB_PARK_AUDIT_EXPANSION_01 — Cadrage

## Objet

Ouvrir un chantier structuré en plusieurs GO pour prolonger l’inventaire du parc GitHub à partir des trunks ZIP déjà lus, avec trois sorties distinctes :

1. audit croisé `branches ↔ trunks`
2. audit de consolidation par familles de modules dans `opt-trading`
3. cartographie canonique `doc / code / runtime / gouvernance / consumer / legacy` fichier par fichier

---

## Sources canoniques consultées avant cadrage

Ce cadrage a été posé en utilisant explicitement les fichiers de référence demandés par `docs/governance/SESSION_DOCUMENTATION_GATE.md` :

- `docs/INDEX.md`
- `docs/master_pack/mission_starter_pack/00_mission_start_guide.md`
- `journal/index/ACTIVE_GO_MATRIX.md`
- `docs/governance/HUMAN_CONTINUITY_TRANSMISSION.md`

Comme l’impose aussi le starter pack, ce cadrage tient compte de :

- la dernière clôture pertinente : `docs/ot/closings/OT_GITHUB_PARK_CONSOLIDATION_DECISION_02B_CLOSING.txt`
- la source of truth kanban : `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`
- l’addendum de gouvernance utilisateur sur `Llm-wiki` : `docs/governance/GITHUB_PARK_CONSOLIDATION_DECISION_02C.md`

---

## Besoin initial

Le parc a déjà été :

- inventorié à partir des ZIP reçus
- lu documentairement de manière exhaustive
- consolidé côté rôles de repo et surfaces legacy

Le besoin suivant est de transformer cette base en chantier opératoire durable, transmissible et séquencé, sans tout mélanger dans un audit unique trop large.

---

## Cible finale / objectif final

Obtenir un dispositif de lecture et de consolidation du parc en trois couches complémentaires :

### Couche 1 — branches ↔ trunks
Établir, repo par repo, l’écart entre :
- le trunk réellement inspecté
- les branches visibles via GitHub
- les chantiers branchés qui prolongent, divergent ou dupliquent le trunk

### Couche 2 — familles de modules (`opt-trading`)
Établir, dans `opt-trading`, les familles de modules :
- canoniques
- concurrentes
- versionnées
- dépréciées
- archives
- miroirs / wrappers / outputs

### Couche 3 — cartographie canonique fichier par fichier
Produire une cartographie stable :
- `doc`
- `code`
- `runtime`
- `gouvernance`
- `consumer`
- `legacy`

Cette cartographie doit être exploitable pour la reprise, la consolidation et les futurs GO de nettoyage.

---

## Plan validé

### Règle générale
Ne pas tenter un audit global monolithique.
Descendre le chantier en plusieurs GO spécialisés, avec un résultat exploitable à chaque étape.

### Séquence retenue

#### GO_1
`GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`

But :
- croiser les trunks inspectés et les branches GitHub visibles
- identifier où une branche prolonge réellement un trunk, où elle porte un chantier distinct, et où elle double un travail déjà absorbé

#### GO_2
`GO_OPT_TRADING_MODULE_FAMILY_CONSOLIDATION_AUDIT_01`

But :
- auditer les familles de modules dans `opt-trading`
- classer chaque famille en : canonique / concurrente / versionnée / archive / miroir / output
- dégager les prochains GO de consolidation physique

#### GO_3
`GO_GITHUB_PARK_FILE_ROLE_CARTOGRAPHY_01`

But :
- construire la cartographie canonique fichier par fichier
- permettre ensuite une lecture fiable par rôle plutôt que par simple emplacement

---

## État établi courant

### 1. Canon documentaire de session
Le gate de session exige que tout chantier documenté préserve au minimum :
- besoin initial
- cible finale
- plan validé
- état établi
- gap restant
- next GO

### 2. Canon d’ouverture de mission
Le starter pack impose :
- lecture des standards et closings pertinents
- usage du kanban comme source of truth
- point de reprise clair
- hiérarchie stricte entre état réel et helpers documentaires

### 3. État actif GO matrix
La matrice GO active ne porte pas encore ce chantier comme GO actif dédié.
Le chantier doit donc être documenté de façon transmissible, avec point de reprise clair, sans prétendre à une activation déjà propagée dans la matrice générée.

### 4. Continuité humaine
La transmission doit rester :
- soutenable
- hiérarchisée
- claire sur les seuils de validation
- transmissible à une reprise ultérieure sans dépendre de la mémoire contextuelle seule

### 5. État du parc déjà tranché
Les décisions consolidées déjà validées sont :
- `opt-trading` = canon d’exécution
- `openclaw` = canon de gouvernance transverse
- `localcms` = repo produit / consumer
- `hf_trading` = lane laboratoire
- `Llm-wiki-minimal` = lane de pré-consolidation à conserver
- `Llm-wiki` = legacy obsolète
- `Magikgmo` = legacy obsolète
- `algo_hf` = legacy obsolète

---

## Gap restant

Le parc est documenté et lu, mais il manque encore :

1. le rattachement propre `branch ↔ trunk ↔ chantier`
2. le découpage complet des familles de modules dans `opt-trading`
3. la cartographie canonique fichier par fichier par rôle réel

Sans ces trois couches, la consolidation reste partielle.

---

## Rôles séparés

### Rôle repo
- `opt-trading` = repo canonique qui porte la gouvernance locale de ce chantier

### Rôle produit / parc
- le parc GitHub = objet audité

### Rôle IA / IDE
- rôle courant = cartographe de parc + auditeur de consolidation
- pas de rôle machine runtime engagé à ce stade

### Rôle machine
- non lié pour l’instant à une machine d’exécution spécifique
- chantier documentaire / d’audit avant patchs runtime

---

## Next GO

### GO immédiat retenu
`GO_GITHUB_PARK_BRANCH_TRUNK_CROSS_AUDIT_01`

### Pourquoi lui en premier
Parce qu’il sert de couche de raccord entre :
- l’inventaire réel des trunks ZIP
- les branches visibles côté GitHub
- les chantiers qui doivent ensuite être consolidés dans `opt-trading`

Il permet d’éviter qu’un audit de familles de modules ou une cartographie fichier par fichier soit menée sans rattachement propre aux branches et aux chantiers déjà existants.

---

## Règle d’exécution issue de ce cadrage

Tant que ce chantier n’est pas descendu par GO spécialisés :

- ne pas produire un unique audit monolithique “parc total” comme s’il suffisait à la consolidation
- ne pas rouvrir les repos legacy obsolètes comme s’ils redevenaient actifs
- garder `Llm-wiki-minimal` comme seule lane utile sur son périmètre
- conserver la séparation entre audit de branches, audit de familles de modules, et cartographie des rôles de fichiers

---

## Statut

**OPEN — cadrage validé, chantier séquencé, next GO défini**
