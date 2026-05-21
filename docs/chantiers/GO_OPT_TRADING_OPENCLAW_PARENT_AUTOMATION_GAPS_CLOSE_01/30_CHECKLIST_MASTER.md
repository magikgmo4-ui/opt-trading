---
doc_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01_CHECKLIST_MASTER
doc_type: master_checklist
repo: opt-trading
project: opt-trading
module: automation
go_id: GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01
status: open
lifecycle_stage: parent_gap_control
topic_keys:
  - checklist
  - automation
  - no_closeout_until_complete
surface: docs/chantiers
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01/30_CHECKLIST_MASTER.md
point_de_reprise: "CHECKLIST_STATUS_OPEN"
updated_at: 2026-05-20
---

# 30_CHECKLIST_MASTER — checklist complète non-closeout

## Règle

Le parent `GO_OPT_TRADING_OPENCLAW_PARENT_AUTOMATION_GAPS_CLOSE_01` ne peut pas être fermé tant que chaque item n'est pas en `PASS_WITH_EVIDENCE`.

## Statut global

```text
GLOBAL_STATUS: OPEN
CLOSEOUT_ALLOWED: NO
REASON: checklist non complétée
```

---

## Checklist maître

| ID | Gap | Checklist de fermeture | Statut | Evidence required |
|---|---|---|---|---|
| G01 | Capability matrix | Acteurs listés ; surfaces listées ; permissions définies ; gates définis ; logs définis ; rollback défini ; scénarios testés | OPEN | matrice + test scenarios |
| G02 | Strict workers runtime | runner read-only ; job schema ; no-write guard ; output JSON ; logs ; smoke réel | OPEN | smoke report + artifacts |
| G03 | Team AI concrete | manager ; spécialistes ; handoff ; memory broker ; task router ; dry-run scenario | OPEN | architecture + dry-run |
| G04 | External app contracts | contrats Airtable/ClickUp/Botpress/Sheets/Telegram/Gmail/Calendar/Drive/Figma/LocalCMS | OPEN | contract docs |
| G05 | Source of truth | domaines listés ; source canonique par domaine ; conflits ; sync ; recovery | OPEN | source-of-truth matrix |
| G06 | Observability ledger | schema ; writer ; storage ; 3 events ; replay/audit ; LocalCMS read | OPEN | ledger sample + tests |
| G07 | HITL gates | propose/review/approve/execute/verify/log ; approval packet ; dual confirm | OPEN | gated action proof |
| G08 | Security/secrets | no token ; scopes ; rotation ; kill switch ; deny default ; anti-secret tests | OPEN | security report |
| G09 | CI/scheduler | smoke ; scheduler ; retry ; status ; failure ingestion ; alert | OPEN | CI/scheduler run |
| G10 | Signal chain dry-run | signal schema ; sources ; recroisement ; journal ; backtest ; dry-run guard | OPEN | dry-run report |
| G11 | LocalCMS cockpit | pages automation/workers/jobs/approvals/ledger/signals ; safe buttons ; kill switch | OPEN | screenshots or route tests |
| G12 | Recovery/rollback | error classes ; rollback policy ; dead-letter ; stuck job ; replay ; escalation | OPEN | failure drill |

---

## Sous-checklists détaillées

### G01_CAPABILITY_MATRIX

- [ ] `actors.registry` existe.
- [ ] `surfaces.registry` existe.
- [ ] permission matrix existe.
- [ ] gates matrix existe.
- [ ] forbidden actions matrix existe.
- [ ] rollback matrix existe.
- [ ] 3 scénarios sont testés.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G02_STRICT_WORKERS_RUNTIME

- [ ] runner read-only créé.
- [ ] job packet parser validé.
- [ ] no-write guard testé.
- [ ] sortie JSON normalisée.
- [ ] logs par job.
- [ ] smoke read-only exécuté.
- [ ] aucune mutation repo/runtime.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G03_TEAM_AI_CONCRETE

- [ ] manager agent défini.
- [ ] spécialistes définis.
- [ ] handoff packet défini.
- [ ] memory broker défini.
- [ ] task router défini.
- [ ] failure modes définis.
- [ ] scénario multi-agent dry-run.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G04_EXTERNAL_APP_CONTRACTS

- [ ] template `APP_BRIDGE_CONTRACT`.
- [ ] Airtable contract.
- [ ] ClickUp/Asana contract.
- [ ] Botpress contract.
- [ ] Google Sheets contract.
- [ ] Telegram contract.
- [ ] Gmail contract.
- [ ] Calendar contract.
- [ ] Drive contract.
- [ ] Figma contract.
- [ ] LocalCMS contract.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G05_SOURCE_OF_TRUTH

- [ ] domaines d'état listés.
- [ ] source canonique par domaine.
- [ ] sources dérivées.
- [ ] sync rules.
- [ ] conflict policy.
- [ ] recovery policy.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G06_LEDGER

- [ ] schema défini.
- [ ] stockage défini.
- [ ] writer défini.
- [ ] event sample.
- [ ] replay/audit validé.
- [ ] affichage cockpit prévu.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G07_HITL

- [ ] proposal packet.
- [ ] approval packet.
- [ ] execution packet.
- [ ] verification packet.
- [ ] approver roles.
- [ ] dual confirm.
- [ ] write-gated test.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G08_SECURITY

- [ ] inventory secrets.
- [ ] secret storage policy.
- [ ] OAuth scopes.
- [ ] rotation.
- [ ] kill switch.
- [ ] deny-by-default.
- [ ] anti-secret tests.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G09_CI_SCHEDULER

- [ ] workflows recensés.
- [ ] smoke critique.
- [ ] scheduler.
- [ ] retry policy.
- [ ] status summary.
- [ ] failure ingestion.
- [ ] alerting.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G10_SIGNAL_CHAIN

- [ ] signal schema.
- [ ] source adapters.
- [ ] recroisement.
- [ ] invalidation.
- [ ] dry-run guard.
- [ ] journal.
- [ ] backtest stats.
- [ ] no live order proof.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G11_LOCALCMS

- [ ] automation page.
- [ ] workers page.
- [ ] jobs page.
- [ ] approvals page.
- [ ] ledger page.
- [ ] signal page.
- [ ] safe buttons.
- [ ] kill switch visible.
- [ ] verdict `PASS_WITH_EVIDENCE`.

### G12_RECOVERY

- [ ] error classes.
- [ ] retry policy.
- [ ] rollback policy.
- [ ] dead-letter.
- [ ] stuck job handling.
- [ ] replay from ledger.
- [ ] human escalation.
- [ ] verdict `PASS_WITH_EVIDENCE`.

---

## Closeout gate

```text
IF any checklist item != PASS_WITH_EVIDENCE:
  CLOSEOUT_ALLOWED = NO
ELSE:
  CLOSEOUT_ALLOWED = YES
```
