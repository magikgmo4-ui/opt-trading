---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: automation
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: parent_opening
topic_keys:
  - opt-trading
  - openclaw
  - automation
  - strict_workers
  - ai_team
  - external_apps
  - gap_closure
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "17_RESUME_POINT"
updated_at: 2026-05-20
links:
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/10_GAPS_REGISTER.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/20_EXECUTION_ROADMAP.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/30_CHECKLIST_MASTER.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/40_NO_CLOSEOUT_POLICY.md
  - docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/BRANCH_STATE.md
  - docs/index/inbox/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01.md
---

# GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01 — 00_INITIAL_PROJECT_DOC

## 1_MASTER_TARGET

Tous les gaps d'automatisation listés dans ce chantier parent doivent être comblés, prouvés, testés, documentés et validés avant toute fermeture.

Le chantier parent ne doit pas être clos tant que la checklist maître `30_CHECKLIST_MASTER.md` n'est pas entièrement en `PASS_WITH_EVIDENCE`.

La cible finale n'est pas seulement de documenter les gaps. La cible finale est que le système d'automatisation `opt-trading / OpenClaw / strict workers / team AI / apps externes` atteigne un état opérationnel cohérent, gated, observable, auditable, récupérable et réutilisable hors session.

## 2_INITIAL_PROJECT_DOC

Ce document est la fiche initiale figée du parent.

Rôle obligatoire :
- transporter le besoin original complet ;
- figer le master target ;
- lister le périmètre ;
- définir les invariants de non-fermeture ;
- servir de point d'ancrage indépendant de la session ;
- empêcher toute fermeture prématurée ou closeout cosmétique.

Ce document peut être amendé seulement si le projet change réellement. Les progressions, preuves et états d'exécution doivent aller dans les documents spécialisés du chantier, pas remplacer cette fiche.

## 3_INITIAL_NEED

Demande originale utilisateur :

> Ouvrir un chantier parent. Master target = tous les gaps sont comblés. Le chantier ne doit pas être fermé avant. Créer une checklist complète de tous les gaps listés. Commencer par documenter le chantier pour qu'il soit indépendant de la session. Détailler toutes les gaps et les steps.

Besoin réel :
- transformer le compte rendu `strict workers / team AI / apps externes / gaps automation` en chantier parent durable ;
- consolider les gaps listés en registre canonique ;
- créer une roadmap de fermeture ;
- créer une checklist non ambiguë ;
- empêcher le closeout tant que les gaps ne sont pas réellement fermés ;
- garder la continuité locale dans `docs/chantiers/<GO_ID>/` ;
- ajouter une entrée courte dans `docs/index/inbox/`.

## 4_MASTER_PROJECT_PLAN

Plan maître validé :

1. Ouvrir un parent unique pour combler tous les gaps d'automatisation.
2. Garder le parent en documentation canonique de contrôle, pas en chantier d'implémentation directe.
3. Décomposer chaque gap en preuves attendues, steps, gates et livrables.
4. Ouvrir ensuite des GO enfants dédiés pour chaque groupe de gaps :
   - capacité et permissions ;
   - strict workers runtime ;
   - team AI manager / spécialistes / mémoire ;
   - contrats apps externes ;
   - observability ledger ;
   - HITL gates ;
   - sécurité / secrets ;
   - CI / scheduler ;
   - signal chain dry-run ;
   - LocalCMS cockpit.
5. Ne jamais fermer le parent si un seul gap reste en `OPEN`, `PARTIAL`, `HYPOTHESIS`, `DRAFT_ONLY` ou `NO_EVIDENCE`.
6. Utiliser le parent comme contrôle de convergence jusqu'au statut `ALL_GAPS_CLOSED_WITH_EVIDENCE`.

## 5_GO_PLAN

GO enfants dérivés recommandés :

| Ordre | GO enfant recommandé | Objectif |
|---:|---|---|
| 1 | `GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01` | Matrice capacités / surfaces / permissions / gates. |
| 2 | `GO_STRICT_WORKERS_RUNTIME_RUNNER_READONLY_01` | Runner strict worker read-only réel et verrouillé. |
| 3 | `GO_AI_TEAM_HANDOFF_MEMORY_POLICY_01` | Rôles, manager, spécialistes, mémoire, handoffs. |
| 4 | `GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01` | Contrats Airtable / ClickUp / Botpress / Sheets / Telegram / Drive / Gmail / Calendar. |
| 5 | `GO_AUTOMATION_OBSERVABILITY_LEDGER_01` | Ledger global des actions automatisées. |
| 6 | `GO_HITL_APPROVAL_GATES_01` | Pipeline propose/review/approve/execute/verify/log. |
| 7 | `GO_AUTOMATION_SECURITY_SECRETS_PERMISSIONS_01` | Secrets, scopes OAuth, kill switch, permissions. |
| 8 | `GO_CI_SCHEDULER_AUTOMATION_STABILITY_01` | CI, scheduler, smoke, retry, status. |
| 9 | `GO_SIGNAL_CHAIN_DRY_RUN_AUTOMATION_01` | Screening / signals / journalisation sans live trade. |
| 10 | `GO_LOCALCMS_AUTOMATION_COCKPIT_01` | Cockpit visuel d'état, contrôle et reprise. |

## 6_FINAL_TARGET

Le parent ne peut atteindre son livrable final que lorsque :

- chaque gap du registre est fermé ;
- chaque fermeture est appuyée par une preuve vérifiable ;
- chaque surface externe a un contrat ;
- chaque worker a un rôle et une permission bornée ;
- le système peut exécuter en read-only, draft, write-gated selon une promotion explicite ;
- les actions sont journalisées dans un ledger ;
- les erreurs ont un mode recovery ;
- l'humain garde le contrôle sur les actions sensibles ;
- les signaux trading restent en dry-run / journalisation tant que le live trading n'est pas validé par un GO séparé ;
- un closeout final peut prouver `ALL_GAPS_CLOSED_WITH_EVIDENCE`.

## 7_CANONICAL_STATE

État canonique courant :

- `strict workers` : socle doc + registry + job packet read-only validés en `DRAFT_ONLY`, mais pas promus runtime.
- `team AI` : parent d'architecture existant, mais architecture concrète / MVP / handoffs non implémentés.
- `apps externes` : surfaces identifiées comme bridges/cockpits, mais contrats communs manquants.
- `automation` : observation, journalisation, dispatch, dry-run et draft possibles ; écriture réelle non validée.
- `source of truth` : encore à figer entre repo, DB, LocalCMS, Sheets, Airtable, ClickUp, Telegram.
- `observability` : ledger central absent.
- `HITL` : philosophie présente, pipeline généralisé manquant.
- `security` : politique à consolider avant write-gated.
- `CI/scheduler` : à stabiliser.
- `signal trading` : doit rester watch/dry-run/journalisation sans exécution ordre.

NEXT_GO immédiat :
- ouvrir le GO enfant `GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01`.

## 8_VALIDATED_PLAN

Étapes validées pour cette phase d'ouverture :

1. Créer le parent `GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01`.
2. Créer une fiche initiale indépendante de la session.
3. Créer un registre des gaps.
4. Créer une roadmap d'exécution.
5. Créer une checklist maître.
6. Créer une politique de non-closeout.
7. Créer un état branche local au chantier.
8. Créer une entrée inbox courte.
9. Ne pas modifier les index globaux lourds à cette ouverture.
10. Laisser l'implémentation aux GO enfants.

## 9_SELECTED_SOLUTION

Approche retenue :

- Parent documentaire de contrôle.
- Gaps fermés par preuves, pas par intention.
- GO enfants pour l'implémentation.
- Promotion progressive :
  - `READ_ONLY`
  - `DRAFT_ONLY`
  - `PATCH_DRAFT`
  - `WRITE_GATED`
  - `PASS_WITH_EVIDENCE`
- Closeout interdit tant que la checklist maître n'est pas complète.

## 10_SELECTED_SETUP

Structure documentaire retenue :

```text
docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/
  00_INITIAL_PROJECT_DOC.md
  10_GAPS_REGISTER.md
  20_EXECUTION_ROADMAP.md
  30_CHECKLIST_MASTER.md
  40_NO_CLOSEOUT_POLICY.md
  BRANCH_STATE.md

docs/index/inbox/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01.md
```

Branche recommandée :

```text
go/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
```

## 11_KEY_DECISIONS

- Ce parent couvre tous les gaps d'automatisation listés dans le compte rendu validé.
- Le master target est la fermeture réelle de tous les gaps.
- Le parent ne doit pas être fermé sur base documentaire seulement.
- Les apps externes sont des bridges, pas des sources de vérité autonomes.
- Le trading live reste hors scope jusqu'à validation séparée.
- Les strict workers restent `DRAFT_ONLY` tant qu'un runner runtime n'est pas prouvé.
- Team AI reste conceptuelle tant que manager, spécialistes, mémoire et handoffs ne sont pas implémentés.
- Les gros index globaux ne sont pas modifiés dans cette ouverture.

## 12_INVARIANTS

- Ne pas fermer ce parent avant `ALL_GAPS_CLOSED_WITH_EVIDENCE`.
- Ne pas transformer une hypothèse en fait.
- Ne pas promouvoir `DRAFT_ONLY` en `PASS` sans preuve.
- Ne pas donner de droit write à un worker sans gate explicite.
- Ne pas laisser une app externe déclencher une action destructive.
- Ne pas confondre cockpit, source de vérité et runtime.
- Ne pas activer live trading depuis ce parent.
- Ne pas modifier le runtime dans ce parent documentaire.
- Ne pas élargir les index globaux sans justification explicite.

## 13_ESTABLISHED

- Le besoin utilisateur est validé : ouvrir un parent jusqu'à fermeture complète des gaps.
- Les gaps à couvrir viennent du compte rendu validé.
- Le socle strict workers existe mais reste insuffisant pour automatisation complète.
- Le parent team AI existe mais reste à concrétiser.
- Les apps externes doivent être contractualisées.
- La prochaine étape logique est la matrice de capacité.

## 14_HYPOTHESIS

- Une architecture OpenClaw + strict workers + team AI + app bridges peut combler tous les gaps.
- LocalCMS peut devenir le cockpit principal.
- Un ledger central peut suffire à auditer et rejouer les actions.
- Les apps externes peuvent rester en mode bridge sans devenir sources de vérité.
- La promotion progressive read-only/draft/write-gated est le chemin le plus sûr.

## 15_REMAINING_GAP

Voir `10_GAPS_REGISTER.md`.

Résumé des familles de gaps :

1. Matrice de capacité manquante.
2. Strict workers non promus runtime.
3. Team AI encore conceptuelle.
4. Apps externes sans contrat commun.
5. Source of truth non figée.
6. Observability ledger absent.
7. Gates HITL incomplets.
8. Sécurité / secrets / permissions à verrouiller.
9. CI / scheduler non stabilisés.
10. Signal trading limité volontairement au dry-run.
11. Cockpit LocalCMS non connecté à toutes les surfaces.
12. Recovery / rollback / reprise non généralisés.

## 16_TODO

Actions immédiates :

1. Publier ce parent sur branche dédiée.
2. Vérifier que le dossier chantier et l'entrée inbox existent.
3. Ouvrir le GO enfant de matrice de capacité.
4. Remplir la matrice actor/surface/permission/gate/log.
5. Pour chaque gap, ouvrir un GO enfant ou rattacher à un GO existant.
6. Marquer chaque item checklist avec statut `OPEN`, `PARTIAL`, `PASS_WITH_EVIDENCE`.
7. Refuser tout closeout tant que la checklist n'est pas complète.

## 17_RESUME_POINT

Reprendre depuis `7_CANONICAL_STATE`, rappeler `1_MASTER_TARGET`, `2_INITIAL_PROJECT_DOC`, `4_MASTER_PROJECT_PLAN`, puis replacer `5_GO_PLAN` et `6_FINAL_TARGET`.

Action de reprise opérationnelle :

```text
Ouvrir ou reprendre GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01.
Ne pas fermer GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01.
Mettre à jour 30_CHECKLIST_MASTER.md seulement avec preuves concrètes.
```

## 18_TO_DOCUMENT

TAGS :
- `1_MASTER_TARGET`
- `2_INITIAL_PROJECT_DOC`
- `3_INITIAL_NEED`
- `4_MASTER_PROJECT_PLAN`
- `5_GO_PLAN`
- `6_FINAL_TARGET`
- `7_CANONICAL_STATE`
- `8_VALIDATED_PLAN`
- `9_SELECTED_SOLUTION`
- `10_SELECTED_SETUP`
- `11_KEY_DECISIONS`
- `12_INVARIANTS`
- `13_ESTABLISHED`
- `14_HYPOTHESIS`
- `15_REMAINING_GAP`
- `16_TODO`
- `17_RESUME_POINT`

Blocs à extraire :
- `AUTOMATION_GAPS_PARENT_MASTER_TARGET`
- `AUTOMATION_GAPS_PARENT_NO_CLOSEOUT`
- `AUTOMATION_GAPS_PARENT_CANONICAL_STATE`
- `AUTOMATION_GAPS_PARENT_NEXT_GO`

## 19_TO_REMEMBER

MEM_CANDIDATE:
- `AUTOMATION_GAPS_PARENT_OPEN_UNTIL_ALL_CLOSED` : le parent `GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01` doit rester ouvert tant que tous les gaps d'automatisation ne sont pas comblés avec preuve.

SAVE_MEMORY:
- Aucun enregistrement durable automatique demandé ici.
