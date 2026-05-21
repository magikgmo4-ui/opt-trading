---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_GAPS_REGISTER
doc_type: gaps_register
repo: opt-trading
project: opt-trading
module: automation
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: parent_gap_control
topic_keys:
  - automation_gaps
  - strict_workers
  - ai_team
  - external_apps
  - observability
  - hitl
  - security
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/10_GAPS_REGISTER.md
point_de_reprise: "GAP_01_CAPABILITY_MATRIX"
updated_at: 2026-05-20
---

# 10_GAPS_REGISTER — registre complet des gaps

## Statuts autorisés

```text
OPEN = non traité
PARTIAL = traité partiellement, preuve insuffisante
DRAFT_ONLY = documenté ou simulé, pas opérationnel
PASS_WITH_EVIDENCE = fermé avec preuve vérifiable
BLOCKED = bloqué avec raison
OUT_OF_SCOPE = exclu explicitement du parent
```

Un gap ne peut passer à `PASS_WITH_EVIDENCE` que si :
- le livrable attendu existe ;
- les tests ou preuves sont disponibles ;
- les invariants de sécurité sont respectés ;
- la checklist associée est complète ;
- le parent peut citer le chemin exact des preuves.

---

## GAP_01_CAPABILITY_MATRIX — Matrice de capacité manquante

### Problème

Le système ne possède pas encore une matrice canonique qui définit clairement :

```text
QUI peut faire QUOI
SUR QUELLE SURFACE
AVEC QUEL DROIT
SOUS QUEL GATE
AVEC QUEL LOG
AVEC QUEL ROLLBACK
```

### Risque

Sans matrice, un worker, une app externe ou un agent peut confondre :
- lecture ;
- draft ;
- patch ;
- write-gated ;
- runtime ;
- notification ;
- exécution destructive.

### Livrable attendu

`GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01`

Doit produire une matrice avec :

| Champ | Attendu |
|---|---|
| actor_id | humain, OpenClaw, strict_worker, team_ai_manager, specialist_worker, app_bridge |
| surface_id | repo, tmux, Telegram, TradingView, Airtable, ClickUp, Botpress, Sheets, LocalCMS, DeskPro |
| permission | read, draft, patch_draft, write_gated, forbidden |
| gate | none, dry_run, human_approve, dual_confirm |
| log_required | true/false |
| rollback_required | true/false |
| evidence_ref | chemin ou artefact |
| status | OPEN/PARTIAL/PASS_WITH_EVIDENCE |

### Steps

1. Recenser tous les acteurs.
2. Recenser toutes les surfaces.
3. Définir les permissions par surface.
4. Définir les actions interdites.
5. Définir les gates.
6. Définir les logs requis.
7. Définir rollback/recovery.
8. Tester la matrice sur 3 scénarios :
   - read-only signal ;
   - draft patch repo ;
   - app external write gated.
9. Valider `PASS_WITH_EVIDENCE`.

---

## GAP_02_STRICT_WORKERS_RUNTIME — Strict workers non promus runtime

### Problème

Le socle strict workers existe en `DRAFT_ONLY`, mais pas comme runtime verrouillé.

### Risque

Confusion entre smoke documenté et exécution réelle.

### Livrables attendus

- runner read-only réel ;
- job queue ou folder queue ;
- job state machine ;
- output schema ;
- retry policy ;
- no-mutation guard ;
- logs ;
- smoke re-exécutable ;
- verdict de promotion contrôlée.

### Steps

1. Créer runner read-only isolé.
2. Valider input schema job packet.
3. Bloquer mutations par défaut.
4. Ajouter mode `--dry-run`.
5. Ajouter sortie JSON normalisée.
6. Ajouter logs par job.
7. Ajouter test fixture read-only.
8. Exécuter smoke réel.
9. Documenter preuve.
10. Garder `PATCH_DRAFT` hors scope jusqu'au GO suivant.

---

## GAP_03_TEAM_AI_CONCRETE_ARCHITECTURE — Team AI encore conceptuelle

### Problème

Le parent team AI existe, mais l'architecture concrète n'est pas encore livrée.

### Manques

- manager agent ;
- specialist workers ;
- memory broker ;
- handoff protocol ;
- shared context ;
- task router ;
- validation humaine ;
- failure mode ;
- artefacts inter-agents ;
- mode reprise.

### Livrables attendus

- diagramme actor/role/handoff ;
- protocole de handoff ;
- policy mémoire ;
- registry rôles ;
- exemples de tâches ;
- failure modes ;
- preuve dry-run.

### Steps

1. Définir rôles minimum.
2. Définir manager agent.
3. Définir spécialistes.
4. Définir mémoire partagée.
5. Définir handoff packet.
6. Définir task router.
7. Définir human validation gate.
8. Tester scénario multi-agent non destructif.
9. Documenter preuve.

---

## GAP_04_EXTERNAL_APPS_CONTRACTS — Apps externes sans contrat commun

### Problème

Airtable, ClickUp, Botpress, Sheets, Telegram, Gmail, Calendar, Drive, Figma et LocalCMS n'ont pas encore de contrat commun de bridge.

### Risque

Chaque app devient une intégration isolée, avec des permissions et logs incohérents.

### Contrat attendu

```text
APP_BRIDGE_CONTRACT:
- app_id
- purpose
- source_of_truth_rank
- allowed_reads
- allowed_writes
- forbidden_actions
- required_env_vars
- dry_run_mode
- approval_gate
- audit_log
- rollback_or_compensating_action
- evidence_ref
```

### Steps

1. Créer template de contrat.
2. Remplir contrat pour Airtable.
3. Remplir contrat pour ClickUp.
4. Remplir contrat pour Botpress.
5. Remplir contrat pour Google Sheets.
6. Remplir contrat pour Telegram.
7. Remplir contrat pour Gmail/Calendar/Drive.
8. Remplir contrat pour LocalCMS.
9. Valider toutes les actions interdites.
10. Relier chaque contrat à la matrice de capacité.

---

## GAP_05_SOURCE_OF_TRUTH — Source of truth non figée

### Problème

Le système peut dupliquer les états entre repo, DB, LocalCMS, Sheets, Airtable, ClickUp et Telegram.

### Décision attendue

| Domaine | Source canonique à figer |
|---|---|
| Plan projet | repo `docs/chantiers` |
| État runtime | DB ou ledger runtime |
| Journal trading | DB + export Sheets ou Sheets contrôlé |
| Backtests | DB + artefacts repo/export |
| Tâches humaines | ClickUp/Asana ou repo, à décider |
| Mémoire projet | Repo KG + docs |
| Cockpit visuel | LocalCMS |
| Notifications | Telegram |
| Evidence | repo + artefacts immuables |

### Steps

1. Lister tous les domaines d'état.
2. Choisir source canonique par domaine.
3. Définir sources dérivées.
4. Définir règles de synchronisation.
5. Définir conflits.
6. Définir stratégie de récupération.
7. Documenter verdict.

---

## GAP_06_OBSERVABILITY_LEDGER — Ledger global absent

### Problème

Aucune table/fichier global n'a encore été fixé pour tracer toutes les actions automatisées.

### Schéma minimal attendu

```json
{
  "event_id": "...",
  "timestamp": "...",
  "actor": "...",
  "worker_id": "...",
  "app_surface": "...",
  "input_ref": "...",
  "action_type": "...",
  "dry_run": true,
  "approval_status": "...",
  "output_ref": "...",
  "error": null,
  "rollback_ref": null
}
```

### Steps

1. Définir schema.
2. Définir stockage initial.
3. Définir writer unique.
4. Définir read API.
5. Définir export LocalCMS.
6. Définir alert Telegram.
7. Tester 3 événements.
8. Valider replay/audit.

---

## GAP_07_HITL_GATES — Gates humains incomplets

### Problème

Le pipeline de validation humaine n'est pas encore généralisé.

### Pipeline attendu

```text
PROPOSE → REVIEW → APPROVE → EXECUTE → VERIFY → LOG → CLOSEOUT
```

### Steps

1. Définir `proposal_packet`.
2. Définir `approval_packet`.
3. Définir `execution_packet`.
4. Définir `verification_packet`.
5. Définir qui peut approuver.
6. Définir actions dual-confirm.
7. Tester un write-gated non destructif.
8. Documenter preuve.

---

## GAP_08_SECURITY_SECRETS_PERMISSIONS — Sécurité / secrets / permissions

### Problème

Les permissions multi-apps et secrets ne sont pas encore stabilisés dans une doctrine complète.

### Invariants attendus

- aucun token dans repo ;
- aucun `.env` publié ;
- scopes minimaux ;
- séparation read/write ;
- rotation des clés ;
- audit des appels externes ;
- commandes destructives interdites depuis mobile/bouton tactile ;
- kill switch global ;
- deny-by-default.

### Steps

1. Inventorier secrets requis.
2. Définir stockage.
3. Définir rotation.
4. Définir scopes par app.
5. Définir kill switch.
6. Définir forbidden actions.
7. Ajouter tests anti-secret.
8. Documenter preuve.

---

## GAP_09_CI_SCHEDULER_STABILITY — CI / scheduler non stabilisés

### Problème

La stabilisation CI/scheduler/smoke n'est pas encore complète.

### Livrables attendus

- workflow CI minimal ;
- smoke read-only ;
- job retry ;
- status report ;
- failure ingestion ;
- alerting ;
- scheduler local ou GitHub Actions ;
- preuve d'exécution.

### Steps

1. Recenser workflows existants.
2. Définir smoke critique.
3. Définir scheduler.
4. Ajouter retry policy.
5. Ajouter status summary.
6. Relier au ledger.
7. Relier alert Telegram/LocalCMS.
8. Valider.

---

## GAP_10_SIGNAL_CHAIN_DRY_RUN — Signal trading limité volontairement

### Problème

La chaîne signal peut être automatisée, mais ne doit pas exécuter d'ordre live sans GO séparé.

### Autorisé

```text
WATCH
OBSERVE
INVALIDATED
PERF_UPDATE
GATE_BLOCKED
DRY_RUN
JOURNALIZE
BACKTEST
SCREEN
ALERT
```

### Interdit sans GO séparé

```text
BUY
SELL
LONG NOW
SHORT NOW
EXECUTE
ORDER SENT
BYPASS RISK ENGINE
LIVE ORDER
```

### Steps

1. Formaliser signal schema.
2. Formaliser journal schema.
3. Définir sources : TradingView, Telegram, screenshots, Coinglass, sheets, DB.
4. Définir recroisement.
5. Définir invalidation.
6. Définir dry-run.
7. Définir stats/backtest.
8. Définir alert.
9. Tester sans ordre live.
10. Documenter preuve.

---

## GAP_11_LOCALCMS_COCKPIT — Cockpit LocalCMS incomplet

### Problème

LocalCMS peut devenir le hub, mais les connexions automation ne sont pas encore complètes.

### Livrables attendus

- page automation state ;
- page workers ;
- page jobs ;
- page signal chain ;
- page approvals ;
- page ledger ;
- liens repo/GO ;
- boutons safe only ;
- kill switch visible.

### Steps

1. Définir écrans.
2. Définir données consommées.
3. Définir actions autorisées.
4. Interdire actions destructives.
5. Brancher ledger read-only.
6. Brancher queue read-only.
7. Brancher approvals.
8. Tester cockpit read-only.

---

## GAP_12_RECOVERY_ROLLBACK_REPRISE — Recovery non généralisé

### Problème

Les modes de reprise et rollback ne sont pas uniformes sur tous les workers/apps.

### Livrables attendus

- recovery policy ;
- rollback policy ;
- retry policy ;
- stuck job policy ;
- orphan branch policy ;
- failed app call policy ;
- replay from ledger ;
- human escalation.

### Steps

1. Définir classes d'échec.
2. Définir recovery par classe.
3. Définir rollback par action.
4. Définir stuck job.
5. Définir dead-letter queue.
6. Définir escalation humaine.
7. Tester échec contrôlé.
8. Documenter preuve.

---

## Synthèse de fermeture autorisée

Le parent peut seulement être fermé quand les 12 gaps sont en :

```text
PASS_WITH_EVIDENCE
```

Toute autre fermeture est interdite.
