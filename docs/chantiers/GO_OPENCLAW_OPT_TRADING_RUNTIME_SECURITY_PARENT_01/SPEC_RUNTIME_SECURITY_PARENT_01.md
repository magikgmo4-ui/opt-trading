---
doc_id: SPEC_RUNTIME_SECURITY_PARENT_01
doc_type: chantier_parent_spec
repo: opt-trading
project: opt-trading
module: openclaw
go_id: GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
status: draft
lifecycle_stage: opening
surface: docs/chantiers
source_kind: canonical
updated_at: 2026-05-09
topic_keys:
  - openclaw
  - opt-trading
  - runtime_security
  - skill_permissions
  - why
  - orchestration
  - audit
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
---

# SPEC_RUNTIME_SECURITY_PARENT_01

## 1_MASTER_TARGET

Construire une specification canonique de securite runtime pour l'orchestration OpenClaw dans `opt-trading`, avant industrialisation des skills, workers, agents et automatisations multi-machines.

Objectif stable : permettre a OpenClaw d'orchestrer des actions reelles sans devenir une surface d'execution non bornee, non explicable ou destructrice.

## 2_INITIAL_PROJECT_DOC

Document initial transporteur du chantier :

`docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md`

Role :
- figer le cadrage parent ;
- separer ce chantier de la session conversationnelle ;
- poser le `FINAL_TARGET` ;
- integrer explicitement le nouvel axe `WHY` ;
- servir de reference de reprise locale.

Ce document reste la fiche de reference obligatoire du chantier tant qu'aucun changement explicite ou implicite du projet ne le remplace.

## 3_INITIAL_NEED

Le systeme `opt-trading` evolue vers une orchestration OpenClaw plus large :

- controle via chat / Telegram / gateway ;
- execution multi-machines ;
- workers specialises ;
- modules et skills ;
- automatisations de fichiers, services, Git, docs et runtime ;
- memoire operationnelle et traces de reprise.

Besoin initial : poser les garde-fous runtime avant de laisser l'orchestrateur agir plus profondement sur le systeme.

## 4_MASTER_PROJECT_PLAN

Plan parent valide :

1. Creer un chantier parent dedie.
2. Travailler sur une branche dediee.
3. Produire une documentation independante de la session.
4. Marquer explicitement le `FINAL_TARGET`.
5. Ajouter une section `WHY` obligatoire.
6. Rester en documentation uniquement au demarrage.
7. Ne modifier aucun runtime.
8. Ne pas toucher aux index globaux.
9. Creer seulement une entree courte dans `docs/index/inbox/` pour aggregation future.

## WHY

Ce chantier existe pour eviter qu'OpenClaw devienne seulement un orchestrateur puissant sans garde-fous.

Le but n'est pas de ralentir l'automatisation, mais de rendre chaque action IA :

- explicable ;
- tracable ;
- bornee ;
- reversible quand possible ;
- non destructive par defaut ;
- compatible avec une architecture multi-machine reelle ;
- rattachee a un besoin et a un perimetre prouve.

Le `WHY` prime sur l'execution : une action non justifiee, non tracable ou hors perimetre ne doit pas etre automatisee.

## 5_GO_PLAN

GO parent :

`GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`

Branche dediee :

`go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01`

Flux initial :

1. SPEC parent runtime security.
2. Inbox courte de continuite.
3. PR doc-only.
4. Revue humaine.
5. Child GO ulterieur pour modeliser les permissions, si le parent est accepte.

## 6_FINAL_TARGET

**FINAL_TARGET : produire une specification canonique de securite runtime OpenClaw pour `opt-trading`, couvrant les permissions, chemins, actions dangereuses, audit logs, separation agent / worker / machine, modele de confiance, anti prompt-injection, anti auto-fix destructif et integration future avec un skill registry.**

La cible finale de ce parent n'est pas d'implementer immediatement la securite runtime, mais de figer le cadre qui permettra ensuite d'ouvrir des child GO bornes et verifiables.

## 7_CANONICAL_STATE

Etat valide a l'ouverture :

- chantier parent valide ;
- branche dediee validee ;
- documentation independante requise ;
- `WHY` ajoute au scope ;
- `FINAL_TARGET` obligatoire ;
- demarrage doc-only ;
- aucun runtime a modifier ;
- aucun index global a modifier ;
- continuite locale parent prioritaire ;
- entree inbox courte autorisee.

## 8_VALIDATED_PLAN

Etapes validees :

1. Ouvrir le parent.
2. Creer la branche dediee.
3. Creer `SPEC_RUNTIME_SECURITY_PARENT_01.md`.
4. Creer `docs/index/inbox/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md`.
5. Ouvrir une PR vers `sot/mainline`.
6. Ne pas modifier `GO_INDEX`, `ACTIVE_STREAMS`, `NEXT_GO_CANDIDATES`, `REPRISE`, `BRANCH_STATE` sans instruction explicite.

## 9_SELECTED_SOLUTION

Approche retenue : gouvernance runtime avant implementation.

Le chantier commence par un modele documentaire, pas par du code, afin de definir :

- les permissions par type de skill ;
- les chemins autorises / interdits ;
- les actions a confirmation obligatoire ;
- les actions interdites par defaut ;
- les criteres de lecture seule ;
- les criteres warning-only ;
- le modele d'audit ;
- les limites des agents autonomes ;
- la separation entre agent, worker, machine et operateur humain.

## 10_SELECTED_SETUP

Structure initiale retenue :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/
  SPEC_RUNTIME_SECURITY_PARENT_01.md

docs/index/inbox/
  GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01.md
```

Branche :

```text
go/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01
```

## 11_KEY_DECISIONS

- Parent ouvert comme chantier documentaire structurant.
- Branche dediee obligatoire.
- Scope initial : documentation uniquement.
- `WHY` obligatoire.
- `FINAL_TARGET` marque explicitement.
- Pas de runtime.
- Pas d'auto-fix.
- Pas de secret.
- Pas de modification d'index global.
- Continuiter parent d'abord dans `docs/chantiers/<GO_PARENT>/`.
- Inbox atomique autorisee pour aggregation future.

## 12_INVARIANTS

Ne pas rouvrir sans raison explicite :

- OpenClaw doit rester borne par des permissions explicites.
- Toute action runtime doit etre explicable et tracable.
- Le mode lecture seule doit etre le defaut pour tout lint / analyse / audit non valide.
- Aucun auto-fix destructif ne doit etre autorise par defaut.
- Les secrets ne doivent jamais etre exposes dans les specs, logs ou prompts.
- Une branche dediee ne justifie pas la modification automatique des index globaux.
- Le parent porte sa continuite localement.

## 13_ESTABLISHED

- Le besoin de securiser l'orchestration OpenClaw est etabli.
- Le chantier parent est valide.
- La branche dediee est validee.
- Le document initial est obligatoire.
- `WHY` fait partie du scope.
- La premiere phase est doc-only.

## 14_HYPOTHESIS

A valider dans des child GO futurs :

- structure exacte du modele de permissions ;
- format du registre des skills ;
- niveaux de risque par action ;
- separation par machine ;
- integration avec Telegram / gateway / tmux ;
- integration avec les modules existants `cmd.sh`, `menu.sh`, `sanity_check.sh` ;
- compatibilite avec les futures surfaces de supervision OpenClaw.

## 15_REMAINING_GAP

Gaps restants :

- pas encore de modele de permission formel ;
- pas encore de taxonomie des actions dangereuses ;
- pas encore de matrice machine / agent / worker ;
- pas encore de schema d'audit runtime ;
- pas encore de policy d'execution par skill ;
- pas encore de lien concret avec un skill registry ;
- pas encore de test de non-destruction.

## 16_TODO

Suite documentaire proposee :

1. Definir une matrice `skill_permission_model`.
2. Definir les niveaux d'action : read, inspect, plan, propose, write, execute, destructive.
3. Definir les chemins autorises et interdits.
4. Definir les actions qui exigent confirmation humaine.
5. Definir les logs minimaux d'audit.
6. Definir les regles anti prompt-injection.
7. Definir les regles anti auto-fix destructif.
8. Definir le premier child GO de specification permissions.

## 17_RESUME_POINT

Reprendre depuis :

```text
docs/chantiers/GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01/SPEC_RUNTIME_SECURITY_PARENT_01.md
```

Point d'action suivant : ouvrir un child GO borne pour produire la matrice de permissions runtime.

Proposition :

```text
GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01
```

## 18_TO_DOCUMENT

TAGS :

- OPENCLAW_RUNTIME_SECURITY
- OPENCLAW_SKILL_PERMISSIONS
- OPENCLAW_WHY
- OPENCLAW_AUDIT
- OPENCLAW_AGENT_GUARDS
- OPT_TRADING_DOC_ONLY_PARENT

Blocs a extraire :

- `WHY`
- `6_FINAL_TARGET`
- `12_INVARIANTS`
- `15_REMAINING_GAP`
- `17_RESUME_POINT`

## 19_TO_REMEMBER

Memory Bricks candidats projet :

- `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_PARENT_01` etablit que la securite runtime OpenClaw doit etre documentee avant implementation.
- Le `WHY` de ce parent est de rendre les actions IA explicables, tracables, bornees, reversibles quand possible et non destructives par defaut.
- Les index globaux ne sont pas modifies pour ce parent sans instruction explicite.
- Suite logique forte : `GO_OPENCLAW_OPT_TRADING_RUNTIME_SECURITY_CHILD_PERMISSION_MATRIX_01`.
