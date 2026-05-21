---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_EXECUTION_ROADMAP
doc_type: execution_roadmap
repo: opt-trading
project: opt-trading
module: automation
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: parent_gap_control
topic_keys:
  - roadmap
  - automation
  - gap_closure
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/20_EXECUTION_ROADMAP.md
point_de_reprise: "PHASE_01_CAPABILITY_MATRIX"
updated_at: 2026-05-20
---

# 20_EXECUTION_ROADMAP — steps de fermeture des gaps

## Objectif

Transformer la liste des gaps en séquence d'exécution contrôlée. Chaque phase doit produire des preuves, pas seulement des intentions.

---

## PHASE_00_PARENT_OPENING — ouverture documentaire

### Cible

Créer le parent et figer la doctrine de non-fermeture.

### Livrables

- `00_INITIAL_PROJECT_DOC.md`
- `10_GAPS_REGISTER.md`
- `20_EXECUTION_ROADMAP.md`
- `30_CHECKLIST_MASTER.md`
- `40_NO_CLOSEOUT_POLICY.md`
- `BRANCH_STATE.md`
- `docs/index/inbox/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01.md`

### Critère de sortie

Le chantier est découvrable et indépendant de la session.

---

## PHASE_01_CAPABILITY_MATRIX

### Cible

Définir les capacités exactes par acteur/surface/action/gate/log.

### Steps

1. Créer `GO_OPENCLAW_AI_TEAM_AUTOMATION_CAPABILITY_MATRIX_01`.
2. Lister acteurs.
3. Lister surfaces.
4. Définir permissions.
5. Définir gates.
6. Définir logs.
7. Définir rollback.
8. Valider sur scénarios.

### Critère de sortie

Matrice complète, versionnée, reliée à tous les gaps.

---

## PHASE_02_STRICT_WORKERS_RUNTIME_READONLY

### Cible

Passer des strict workers de `DRAFT_ONLY` à runner read-only prouvé.

### Steps

1. Créer runner read-only.
2. Parser job packets.
3. Appliquer no-write guard.
4. Émettre output JSON.
5. Logger dans ledger ou fichier temporaire.
6. Tester smoke.
7. Documenter preuve.

### Critère de sortie

Un strict worker peut exécuter un job read-only sans modifier repo/runtime.

---

## PHASE_03_TEAM_AI_CORE

### Cible

Rendre l'équipe AI concrète.

### Steps

1. Définir manager.
2. Définir spécialistes.
3. Définir handoff packet.
4. Définir memory broker.
5. Définir task router.
6. Définir validation humaine.
7. Tester scénario complet sans write.

### Critère de sortie

Un scénario multi-agent produit un résultat auditably dry-run.

---

## PHASE_04_EXTERNAL_APP_BRIDGES

### Cible

Contractualiser toutes les apps externes.

### Apps minimum

- Airtable
- ClickUp / Asana
- Botpress
- Google Sheets
- Telegram
- Gmail
- Calendar
- Drive
- Figma
- LocalCMS

### Critère de sortie

Chaque app possède un `APP_BRIDGE_CONTRACT` et une place dans la matrice.

---

## PHASE_05_SOURCE_OF_TRUTH_AND_LEDGER

### Cible

Éliminer la duplication non contrôlée.

### Steps

1. Source of truth matrix.
2. Ledger schema.
3. Writer unique.
4. Event examples.
5. Replay/audit.
6. LocalCMS read view.

### Critère de sortie

Toute action automatisée a un événement traçable.

---

## PHASE_06_HITL_SECURITY

### Cible

Encadrer toute écriture ou mutation.

### Steps

1. Approval packet.
2. Dual confirm.
3. Forbidden actions.
4. Secrets policy.
5. OAuth scopes.
6. Kill switch.
7. Tests anti-secret.

### Critère de sortie

Aucune mutation sensible ne peut passer sans gate.

---

## PHASE_07_CI_SCHEDULER_STATUS

### Cible

Stabiliser smoke, scheduler, alerting et status.

### Steps

1. CI smoke.
2. Scheduler.
3. Retry.
4. Dead-letter.
5. Status JSON.
6. Telegram/LocalCMS notification.

### Critère de sortie

Le système sait dire automatiquement : OK, FAIL, BLOCKED, NEEDS_HUMAN.

---

## PHASE_08_SIGNAL_CHAIN_DRY_RUN

### Cible

Automatiser le screening/trading lab sans ordre live.

### Steps

1. Signal schema.
2. Sources.
3. Recroisement.
4. Journal.
5. Backtest.
6. Alert.
7. Dry-run only guard.
8. Evidence report.

### Critère de sortie

La chaîne produit des alertes et statistiques sans exécution d'ordre.

---

## PHASE_09_LOCALCMS_COCKPIT

### Cible

Créer la surface opérateur.

### Steps

1. Automation overview.
2. Worker state.
3. Queue state.
4. Approvals.
5. Ledger.
6. Signals.
7. Safe buttons.
8. Kill switch.

### Critère de sortie

L'opérateur voit l'état, approuve, bloque et reprend sans agir directement dans chaque app.

---

## PHASE_10_PARENT_CLOSEOUT_ALLOWED_ONLY_IF_COMPLETE

### Cible

Fermer seulement si tout est prouvé.

### Conditions

- Tous les gaps `PASS_WITH_EVIDENCE`.
- Tous les GO enfants clos ou explicitement transférés.
- Tous les risques restants acceptés.
- Aucun `DRAFT_ONLY` masqué en `PASS`.
- Aucun live trading activé par erreur.
- Checklist complète.

### Critère de sortie

Créer seulement alors `90_CLOSEOUT.md`.
