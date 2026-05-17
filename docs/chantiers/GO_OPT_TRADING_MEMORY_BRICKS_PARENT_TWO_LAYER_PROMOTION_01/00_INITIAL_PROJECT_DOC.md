---
doc_id: GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01_INITIAL_PROJECT_DOC
doc_type: chantier_initial_project_doc
repo: opt-trading
project: opt-trading
module: memory_bricks
go_id: GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01
status: open
lifecycle_stage: parent_opening
surface: memory_bricks
machine_target: fantome
branch: go/GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01
source_kind: session_canon
created_at: 2026-05-17
---

# GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01 — INITIAL PROJECT DOC

## 1_MASTER_TARGET

Construire une chaine persistante pour transformer la tache ChatGPT quotidienne `19_TO_REMEMBER` en pipeline Memory Bricks operable :

```text
ChatGPT Task quotidienne
  -> COUCHE_1_AUTO / AUTO_LOG
  -> promotion scoring automatique
  -> COUCHE_2_PROMOTED / PROMOTED_MEMORY
  -> Memory Bricks MB-*
  -> exports Sheets / API / LocalCMS
```

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche de reference initiale du parent. Il fige le plan de session valide :

- la tache quotidienne existe et s'execute ;
- l'extraction actuelle n'est pas persistante ;
- Memory Bricks existe deja dans le repo ;
- le chantier ne doit pas recreer Memory Bricks ;
- le chantier doit ajouter une chaine deux couches `AUTO_LOG -> promotion -> MB-*` ;
- la machine cible est `FANTOME` ;
- la branche dediee est `go/GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01`.

## 3_INITIAL_NEED

La tache ChatGPT produit ou peut produire les blocs :

```text
19_TO_REMEMBER

MEM_CANDIDATE:
- [Nom du bloc] : contenu candidat

SAVE_MEMORY:
- [Bloc a valider] : contenu pret a enregistrer si validation
```

Mais l'etat reel observe est :

```text
Task: PASS
Extraction: ephemere / non persistante
AUTO_LOG: missing
Promotion scoring: missing
Memory Bricks sync: missing pour cette source
Sheets/UI: missing
```

## 4_MASTER_PROJECT_PLAN

1. Auditer les surfaces Memory Bricks existantes.
2. Poser le modele deux couches.
3. Definir le schema `AUTO_LOG` JSONL/Sheets.
4. Definir le scoring de promotion automatique.
5. Definir le sync vers Memory Bricks CLI V1.
6. Definir les exports pratiques pour le setup utilisateur : Sheets maintenant, LocalCMS ensuite.
7. Decouper les childs.
8. Fournir un bundle IDE autonome pour implementation.
9. Enregistrer le routage machine anti-conflit.

## 5_GO_PLAN

Parent :

```text
GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01
```

Childs poses :

```text
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_EXISTING_SURFACES_AUDIT_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_AUTO_LOG_JSONL_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_PROMOTION_SCORING_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_MB_SYNC_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_SHEETS_EXPORT_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_LOCALCMS_VIEWER_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_AUTOMATION_CONNECTOR_01
GO_OPT_TRADING_MEMORY_BRICKS_CHILD_CLOSEOUT_01
```

## 6_FINAL_TARGET

Livrer une chaine ou chaque run quotidien est persistable comme suit :

- `AUTO_LOG` conserve toutes les extractions candidates ;
- le scoring classe les candidats par recurrence, stabilite, impact workflow et absence de contradiction ;
- seuls les candidats au-dessus du seuil deviennent `PROMOTED_MEMORY` ;
- `PROMOTED_MEMORY` cree de vraies briques `MB-*` via la surface existante ;
- Sheets expose la couche pratique mobile ;
- LocalCMS/API exposent la couche consultation/recherche ;
- aucun enregistrement direct non trace depuis la tache ChatGPT.

## 7_CANONICAL_STATE

Etat au demarrage :

- branche dediee ouverte depuis `sot/mainline` ;
- Memory Bricks V1 existe ;
- API V2 read-only existe/spec existe ;
- KIL -> Memory Bricks sync existe ;
- la tache ChatGPT n'est pas reliee a ces surfaces ;
- aucune preuve d'un `AUTO_LOG` durable pour `19_TO_REMEMBER` ;
- aucun stockage JSONL/SQLite/Sheets dedie a cette source n'est confirme.

## 8_VALIDATED_PLAN

Le plan valide est :

```text
Session task -> AUTO_LOG -> Scoring -> PROMOTED_MEMORY -> MB-* -> Sheets/LocalCMS
```

## 9_SELECTED_SOLUTION

- Couche 1 : JSONL local + export Sheets.
- Couche 2 : Memory Bricks `MB-*` via CLI V1 existante.
- UI courte : Google Sheets.
- UI projet : LocalCMS/API read-only.
- Machine cible : FANTOME.

## 10_SELECTED_SETUP

Structure doc du parent :

```text
docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01/
  00_INITIAL_PROJECT_DOC.md
  01_EXISTING_MEMORY_BRICKS_AUDIT.md
  02_TARGET_ARCHITECTURE.md
  03_GAP_REGISTER.md
  04_CHILDS_MAP.md
  05_IDE_BUNDLE.md
  06_SESSION_DOC.md
  07_FINAL_TARGET.md
```

## 11_KEY_DECISIONS

- Ne pas recreer Memory Bricks.
- Ne pas transformer `SAVE_MEMORY` en enregistrement automatique direct.
- Ajouter une couche `AUTO_LOG` avant toute promotion.
- Promouvoir automatiquement seulement selon scoring stable.
- Garder la traçabilite vers les sources de session et docs stabilises.
- Router le chantier sur FANTOME.

## 12_INVARIANTS

- `memory_bricks` reste une compaction derivee.
- La documentation stabilisee prime sur la sortie brute.
- Pas de mutation runtime trading.
- Pas de global index non demande sauf routage machine explicitement demande.
- Pas de secret, pas de token, pas de donnees personnelles non necessaires.
- Aucune brique `MB-*` ne doit etre creee sans payload source trace.

## 13_ESTABLISHED

- La tache ChatGPT quotidienne s'est executee mais sa sortie est ephemere.
- La definition de tache est stockee dans l'automation, mais pas la memoire durable.
- Le repo contient deja Memory Bricks V1 et des surfaces read-only/API.

## 14_HYPOTHESIS

- FANTOME est la meilleure machine pour orchestrer le pipeline memoire durable.
- Sheets est la meilleure UI immediate.
- LocalCMS est la meilleure UI projet apres stabilisation.

## 15_REMAINING_GAP

- Schema JSONL couche 1.
- Seuils de scoring.
- Regles contradiction/redundance.
- Connecteur depuis la tache vers stockage.
- Export Sheets.
- Viewer LocalCMS.
- Closeout avec preuve d'un run complet.

## 16_TODO

1. Executer le bundle IDE.
2. Verifier l'etat local/remote de la branche.
3. Auditer `modules/memory_bricks`, `modules/kil_v1`, `modules/localcms`, `docs/governance`.
4. Implementer `AUTO_LOG` minimal.
5. Ajouter scoring dry-run.
6. Ajouter sync vers CLI V1 en mode controlled.
7. Ajouter export Sheets ou payload pret a coller.
8. Ajouter LocalCMS viewer read-only si API suffisante.
9. Tester avec une sortie `19_TO_REMEMBER` factice.
10. Closeout.

## 17_RESUME_POINT

Reprendre depuis :

```text
GO_OPT_TRADING_MEMORY_BRICKS_PARENT_TWO_LAYER_PROMOTION_01
-> lire 00_INITIAL_PROJECT_DOC.md
-> executer 05_IDE_BUNDLE.md
-> choisir child courant
-> implementer sans rouvrir le scope parent
```

## 18_TO_DOCUMENT

- Architecture deux couches.
- Schema `AUTO_LOG`.
- Scoring promotion.
- Sync MB.
- Exports Sheets/LocalCMS.

## 19_TO_REMEMBER

MEM_CANDIDATE:
- MEMORY_BRICKS_TWO_LAYER_PARENT_OPENED_01 : parent ouvert pour connecter tache quotidienne a pipeline durable.

SAVE_MEMORY:
- MEMORY_BRICKS_PARENT_SCOPE_01 : scope valide = pipeline deux couches `AUTO_LOG -> promotion -> MB-*`, pas refonte Memory Bricks.
