---
doc_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01_CONSOLIDATION_MAP
doc_type: consolidation_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_consolidation_map
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - deepseek
  - map
  - student
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/02_DEEPSEEK_CONSOLIDATION_MAP.md
point_de_reprise: "Carte de consolidation documentaire DeepSeek : survivant, satellites, legacy, NEXT_GO."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/01_DEEPSEEK_CLUSTER_INVENTORY.md
---

# 02_DEEPSEEK_CONSOLIDATION_MAP

## 1_DECISION DOCUMENTAIRE

```text
Point d'entree canonique operateur : student/
Facade module survivante candidate : modules/deepseek_hub/
Satellites de compatibilite : modules/deepseek_response/, modules/deepseek_thinking/
Transition incomplete : modules/deepseek_student/
Legacy a resorber : scripts/student/
```

## 2_POURQUOI CETTE DECISION

```text
1. student/ a deja une decision canonique ecrite dans son README.
2. deepseek_hub se declare lui-meme comme facade unifiee la plus avancee.
3. deepseek_student se declare lui-meme non runtime et incomplet.
4. response/thinking sont encore appeles par des scripts shell reels.
5. scripts/student/ reste vivant comme legacy compat, donc non supprimable ici.
```

## 3_CARTE CIBLE (SANS MIGRATION EXECUTEE)

```text
student/
├── scripts/student_*                  ← raccourcis globaux canoniques
├── scripts/deepseek_hub/              ← facade famille operateur
├── scripts/deepseek_student/          ← scripts de transition utiles
├── scripts/wrappers/                  ← wrappers de compatibilite
├── docs/                              ← runbook, architecture, handoff
└── validation/                        ← validation live / runbook

modules/deepseek_hub/                  ← facade module survivante candidate
modules/deepseek_response/             ← satellite compat reponse
modules/deepseek_thinking/             ← satellite compat thinking
modules/deepseek_student/              ← transition incomplete
scripts/student/                       ← legacy compat a resorber plus tard
```

## 4_CE QUE CE GO CONSOLIDE VRAIMENT

```text
- la lecture du cluster
- le survivant logique
- les surfaces encore compatibles
- la distinction canonique vs transition vs legacy
```

## 5_CE QUE CE GO NE FAIT PAS

```text
- ne migre pas scripts/student/ vers student/
- ne deplace pas modules/deepseek_*/
- ne supprime pas les doublons
- ne change pas les shortcuts
- ne touche pas au runtime Ollama
```

## 6_NEXT_GO RECOMMANDE

```text
GO_OPT_TRADING_DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01

Mission du GO suivant :
  - cartographier exactement les doublons entre scripts/student/ et student/scripts/
  - fixer le point d'entree final unique
  - definir le plan de retrait progressif du legacy
  - verifier les callers shell (post_change, workflow_post_change_v2, wrappers)
  - produire rollback plan avant toute migration
```

## 7_RISQUES SI ON MIGRE TROP TOT

| Risque | Impact |
|---|---|
| casser les shortcuts student | perte d'entree operateur |
| casser les callers `cmd-deepseek_response` / `cmd-deepseek_thinking` | post_change endommage |
| supprimer scripts/student trop vite | perte du runtime legacy encore utilise |
| promouvoir deepseek_student comme survivant | contradiction avec README actuel |

## 17_RESUME_POINT

```text
Consolidation DeepSeek = clarifier, pas migrer.
student/ = canonique operateur.
deepseek_hub = survivant candidat cote modules.
scripts/student/ = legacy encore actif.
Prochain GO : DEEPSEEK_RUNTIME_CONSOLIDATION_PLAN_01.
```

## RISKS

- À qualifier.
