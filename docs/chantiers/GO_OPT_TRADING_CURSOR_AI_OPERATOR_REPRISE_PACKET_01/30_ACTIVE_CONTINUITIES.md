---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01_30_ACTIVE_CONTINUITIES
doc_type: chantier/active_continuities
repo: opt-trading
machine: cursor-ai
status: active
links:
  - docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md
---

# 30_ACTIVE_CONTINUITIES

Continuites actives cote cursor-ai apres la sequence positions 1-3.

## alert_webhook — ACTIVE_CONTINUITY

| Element | Statut |
| --- | --- |
| Statut global | ACTIVE_CONTINUITY |
| Template JSON | Integre, flags securite actifs |
| Application | Non fermee |
| Endpoint production | Non connecte |
| Alerte reelle | Jamais declenchee depuis cursor-ai |
| Pre-admin gate spec | Documentee (GO position 3) |

**A ne pas faire** :
- Ne pas marquer comme ferme.
- Ne pas connecter a un endpoint de production.
- Ne pas declencher d'alerte reelle.

## Bundles — Workflow actif

| Element | Statut |
| --- | --- |
| Statut produit | APPLICATION_DOCUMENTED, non ferme |
| Statut workflow | ACTIF (GO position 2) |
| Pack Claude artifacts | Integre |
| Methode de creation | Documentee (8 etapes) |
| Types de bundles | 7 types documentes |

**A ne pas faire** :
- Ne pas marquer le produit Bundles comme ferme.
- Ne pas creer de bundle admin-trading sans demande explicite.
- Ne pas injecter de secrets ou payloads reels.

## Admin-trading gate — Fermee

| Element | Statut |
| --- | --- |
| Statut | FERME, NON OUVERT |
| Phrase d'activation | "chantier pour admin-trading" |
| Criteres documentes | 5 criteres (GO position 3) |
| Branches admin-trading | Existent mais non touchees par cursor-ai |

**A ne pas faire** :
- Ne pas ouvrir sans la phrase d'activation.
- Ne pas contourner la pre-admin gate spec.

## Map machine

| Machine | Role | Etat |
| --- | --- | --- |
| cursor-ai | Preparation, documentation, packaging, gate | ACTIF |
| admin-trading | Runtime, services, execution | FERME |
| student | Lab, Ollama, tests | SEPARE |
| db-layer | OpenClaw, backend, data | SEPARE |

Voir `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`.

## RISKS

- À qualifier.
