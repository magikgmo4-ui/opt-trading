---
doc_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01_INVENTORY
doc_type: cluster_inventory
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_inventory
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - deepseek
  - inventory
  - student
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/01_DEEPSEEK_CLUSTER_INVENTORY.md
point_de_reprise: "Inventaire complet de la famille deepseek* et des surfaces student associees."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_DEEPSEEK_CLUSTER_01/00_CADRAGE.md
---

# 01_DEEPSEEK_CLUSTER_INVENTORY

## 1_DEEPSEEK_HUB — modules/deepseek_hub/

```text
Rôle : menu unifie DeepSeek (Ollama), facade de famille la plus avancee cote modules/
Contenu : scripts/ + patches/
README : explicite que deepseek_hub unifie/corrige deepseek_response et deepseek_thinking

Points clefs du README :
  - ajoute tail
  - bascule sur /api/chat
  - orchestre encore deepseek_thinking, deepseek_response et deepseek_student
  - n'ecrase pas la verite runtime actuelle, qui reste scripts/student/
```

## 2_DEEPSEEK_STUDENT — modules/deepseek_student/

```text
Rôle : structure standard en attente de migration/consolidation
Statut : INCOMPLET
README : dit explicitement
  - "n'est pas la source de verite runtime actuelle"
  - la logique active reste dans scripts/student/
  - ne pas deployer ce module comme remplacement
  - deepseek_hub = candidat famille le plus avance
```

## 3_DEEPSEEK_RESPONSE — modules/deepseek_response/

```text
Rôle : produire les reponses finales DeepSeek cote student
Fonctions : run, tail, roadmap_module
Statut : actif en compatibilite operatoire
Decision README : non survivant de famille, conserve car orchestre par deepseek_hub
```

## 4_DEEPSEEK_THINKING — modules/deepseek_thinking/

```text
Rôle : produire le thinking DeepSeek cote student
Fonctions : run, tail, roadmap_module
Statut : actif en compatibilite operatoire
Decision README : non survivant de famille, conserve car orchestre par deepseek_hub
```

## 5_SCRIPTS_STUDENT — scripts/student/

```text
Rôle : legacy runtime encore present a la racine
Contenu visible :
  - deepseek_student_menu.sh / cmd.sh / install.sh / run_logged.sh
  - daily_ai_report / daily_log_thinking / show_latest_* / tail_latest_log
  - wrappers desk_pro_student_*
  - sanity checks

Constat : runtime legacy large et encore present.
```

## 6_STUDENT_ROOT — student/

```text
Rôle : workspace canonique declare pour l'operateur student
README :
  - official project root for student = /opt/trading/student
  - official global shortcuts = student/scripts/student_menu.sh, student_cmd.sh, student_sanity_check.sh
  - legacy locations are compatibility sources only

Structure :
  - scripts/deepseek_hub/
  - scripts/deepseek_student/
  - scripts/wrappers/
  - docs/
  - validation/
  - exports/kanban/

Constat : student/ est deja une cible de consolidation creee, plus avancee que ce que laissait entendre le plan AUDIT initial.
```

## 7_DEPENDANCES ET CROSS-REFERENCES

```text
Type principal de couplage : shell / documentation / shortcuts
Pas de couplage Python fort identifie dans cette lecture.

References clefs :
  - scripts/post_change.sh appelle cmd-deepseek_response et cmd-deepseek_thinking
  - workflow_post_change_v2/README.md appelle aussi ces commandes
  - deepseek_hub patches des scripts deepseek_response et deepseek_thinking
  - student/ duplique deja des wrappers deepseek_hub et deepseek_student
```

## 8_MATRICE DE ROLE

| Surface | Role reel | Statut |
|---|---|---|
| `student/` | root canonique operateur | CANONIQUE |
| `modules/deepseek_hub/` | facade famille la plus avancee | SURVIVANT_CANDIDAT |
| `modules/deepseek_student/` | transition incomplete | TRANSITION |
| `modules/deepseek_response/` | satellite compatibilite reponse | COMPAT |
| `modules/deepseek_thinking/` | satellite compatibilite thinking | COMPAT |
| `scripts/student/` | legacy runtime encore present | LEGACY_COMPAT |

## 9_RESUME

```text
Le cluster n'a pas un seul centre ; il a deux axes :
  - axe operateur canonique : student/
  - axe module famille : deepseek_hub

deepseek_student n'est pas survivant.
response/thinking restent necessaires en compatibilite.
scripts/student/ n'est pas encore retire.
```
