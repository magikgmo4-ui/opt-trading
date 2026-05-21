---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01_TERMUX_OPENCLAW_ENTRYPOINTS
doc_type: entrypoints_doc
go_id: GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01
status: open
updated_at: 2026-05-21
---

# 20_TERMUX_OPENCLAW_ENTRYPOINTS

## Objet

Definir les entrypoints cibles pour utiliser Termux/mobile comme controleur OpenClaw, sans implementation runtime dans ce GO.

## Entry pattern cible

```text
mobile/Termux
  -> openclaw mobile-control wrapper
  -> phase/job registry
  -> preflight gate
  -> job runner machine
  -> ledger/report
  -> LocalCMS snapshot
```

## Entry classes

| Classe | But | Mode initial | Gate |
|---|---|---|---|
| `status` | consulter l'etat OpenClaw/jobs | read-only | none |
| `list-jobs` | lister les jobs autorises | read-only | none |
| `preflight` | verifier si un job peut etre lance | read-only | none |
| `run-dry` | declencher un job dry-run/local-only | dry-run | phase packet |
| `evidence` | afficher les preuves d'un run | read-only | none |
| `approve` | participer a HITL | human validation | HITL |
| `block` | bloquer/stopper une action | control | safety gate |

## Entry classes exclues

| Classe | Statut | Raison |
|---|---|---|
| external write direct | excluded | necessite Phase 08 + dual confirm |
| trading/signal execution | excluded | hors scope non-trading |
| secret handling | excluded | aucune circulation mobile |
| Git destructive operations | excluded | non pertinent pour mobile-control |
| runtime mutation libre | excluded | doit passer par register + gate |

## Wrapper cible a deriver plus tard

Nom propose :

```text
openclaw_mobile_control
```

Interface conceptuelle :

```text
openclaw_mobile_control <entry_class> --phase <PHASE_ID> --job <JOB_ID> --evidence
```

Note : cette interface est volontairement conceptuelle dans ce GO doc-only. Toute implementation devra ouvrir un GO runtime separe.

## Machine routing

| Source | Destination possible | Regle |
|---|---|---|
| Termux/mobile | db-layer | controle via OpenClaw, pas execution brute |
| Termux/mobile | admin-trading | lecture/statut seulement au depart |
| Termux/mobile | local machine | dry-run local-only si allowliste |
| Termux/mobile | app externe | read-only ou HITL/write-gated plus tard |

## Evidence route

Toute execution lancee depuis mobile doit produire :

```text
reports/ai/mobile_control/<run_id>.json
ledger event
optional tmp/localcms_latest.json refresh
```

## Point de controle avant implementation

Avant toute implementation, verifier :

- PR #680 mergee ou branche explicitement choisie ;
- Phase cible identifiee ;
- job_id existe dans le registre ;
- mode compatible mobile ;
- allowed_writes local-only ou none ;
- gate present si action non read-only.
