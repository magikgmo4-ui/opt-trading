---
doc_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01_CADRAGE
doc_type: chantier_cadrage
repo: opt-trading
project: opt-trading
module: continuity
go_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
status: active
lifecycle_stage: cadrage
topic_keys:
  - opt-trading
  - continuity
  - indexes
  - reprise
  - governance
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/next/NEXT_GO_CANDIDATES.md
---

# 00_cadrage — GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01

## Classification
**patch local — doc-only — réalignement continuité index**

## Rôle recommandé
**Architecte continuité documentaire + mainteneur repo**

---

## Besoin initial
Réaligner la continuité documentaire sur `sot/mainline` lorsque les index dérivent :
- divergence entre `GO_INDEX` / `ACTIVE_STREAMS` / `REPRISE` / `NEXT_GO_CANDIDATES`
- coexistence de sources concurrentes pour `NEXT_GO_CANDIDATES`
- propagation incomplète de la règle closeout PASS ⇒ dossier clos pour la continuité active

---

## Cible finale
Disposer d’une couche `docs/index/*` cohérente, repo-first, sans contradictions :
- `docs/index/GO_INDEX.md` = index des chantiers parents actifs (et sections explicites hors actif si conservées)
- `docs/index/ACTIVE_STREAMS.md` = flux réellement actifs / ouverts / bloqués (sans PASS)
- `docs/index/REPRISE.md` = support opératoire (pas une seconde source concurrente)
- `docs/index/NEXT_GO_CANDIDATES.md` = matrice par parent actif (1 parent actif → 1 next GO primaire)
- `docs/next/NEXT_GO_CANDIDATES.md` = déclassé (stub/redirect explicite)

---

## Contraintes
- doc-only uniquement
- patchs ciblés, gap-only
- pas de refactor code
- pas de doublon de chantier parent ou local
- ne pas réappliquer un patch déjà absorbé

---

## Plan validé (PHASE 1)
LOT 1 — continuité index :
- réaligner `GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`
- réécrire `docs/index/NEXT_GO_CANDIDATES.md` en matrice par parent actif
- déclasser `docs/next/NEXT_GO_CANDIDATES.md`
- propager la règle closeout PASS ⇒ dossier clos

LOT 2 — retrait du journal et réalignement continuité :
- retirer `journal.md`, `journal/` et `modules/journal_de_bord/` comme surfaces opératoires obsolètes
- conserver uniquement les extractions de continuité utiles dans `docs/governance/HUMAN_*`
- réaligner les docs canoniques et les scripts encore branchés sur le journal

---

## REPRISE
Point de reprise local :
- `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md`
