---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01_SCOPE
doc_type: smoke_scope
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_CONTRACT_COMPATIBILITY_SMOKE_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-06
---

# 10_SMOKE_SCOPE - Smoke Scope

## Ce qui est testé

| # | Test | Contrat | Résultat attendu |
| --- | --- | --- | --- |
| 1 | V0 minimal → normalize → validate | signal_event V1 | PASS |
| 2 | V0 complet → normalize → validate | signal_event V1 | PASS |
| 3 | payload_hash déterministe | signal_event V1 | PASS |
| 4 | visual_context fixture valide | visual_context V1 | PASS |
| 5 | signal_event peut référencer visual_context | signal_event ↔ visual_context | PASS |
| 6 | desk_snapshot fixture valide | desk_snapshot | PASS |
| 7 | desk_snapshot peut être joint à visual_context | desk_snapshot ↔ visual_context | PASS |
| 8 | Synthesis object contient les 3 artefacts | Desk Pro consumer | PASS |
| 9 | Join keys cohérents | cross-contract | PASS |
| 10 | Synthesis indépendant du runtime | isolation | PASS |

## Ce qui n'est pas testé

| Élément | Raison |
| --- | --- |
| Webhook réel | Invariant: pas de side effect runtime |
| Capture headless réelle | Invariant: pas de side effect runtime |
| Telegram | Invariant: pas d'envoi |
| desk_state agrégation | Nécessite relance manuelle (stale 2 mois) |
| desk_analyze OpenAI vision | Nécessite API key + images réelles |
| Desk Pro orchestrator run | Nécessite runtime complet |
| Lecture events.jsonl réel | Préféré: fixtures synthétiques pour reproductibilité |

## Pourquoi aucun runtime réel n'est appelé

Le but de ce GO est de valider la **compatibilité contractuelle** entre les artefacts, pas leur intégration runtime. Les contrats sont documentaires et les adapters sont stateless. Le smoke vérifie que :
1. Les formats sont compatibles
2. Les join keys fonctionnent
3. Un consumer Desk Pro peut contenir les 3 artefacts
4. Aucun import runtime n'est nécessaire

## Fixtures utilisées

| Fixture | Format | Source |
| --- | --- | --- |
| `signal_event_v0_minimal.json` | V0 (webhook) | Synthétique |
| `signal_event_v0_complete.json` | V0 (webhook) | Synthétique |
| `visual_context_v1_minimal.json` | V1 (contrat) | Synthétique |
| `desk_snapshot_minimal.json` | desk_snapshot | Synthétique |

## Contrats vérifiés

| Contrat | Document source | Vérifié par |
| --- | --- | --- |
| signal_event V1 | `30_SIGNAL_EVENT_CONTRACT.md` | `normalize_signal_event_v1` + `validate_signal_event_v1` |
| visual_context V1 | `30_VISUAL_CONTEXT_CONTRACT.md` | Fixture validation |
| desk_snapshot | `40_DESK_BRIDGE_COMPATIBILITY.md` | Fixture validation |
| Desk Pro synthesis | `40_CONTRACT_COMPATIBILITY_REVIEW.md` | `TestDeskProSynthesisSmoke` |
