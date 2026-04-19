---
doc_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01_JOURNAL_TECHNIQUE
doc_type: chantier_journal_technique
repo: opt-trading
project: opt-trading
module: continuity
go_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
status: active
lifecycle_stage: journal_technique
topic_keys:
  - opt-trading
  - continuity
  - indexes
  - patch
surface: chantier
source_kind: canonical
updated_at: 2026-04-18
links:
  - docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/00_cadrage.md
  - docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/03_decisions.md
---

# 02_journal_technique — GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01

## 2026-04-18
### Étape 1 — Ouverture du chantier parent (doc-only)
- création du dossier chantier et des artefacts minimaux :
  - `00_cadrage.md`
  - `02_journal_technique.md`
  - `03_decisions.md`

### ETABLI
- le chantier parent est ouvert avec une base minimale de traçabilité

### TODO
- LOT 1 : réaligner `docs/index/*` et déclasser `docs/next/NEXT_GO_CANDIDATES.md`

### REPRISE
- poursuivre sur le sous-lot LOT 1 : correction des contradictions `ACTIVE_STREAMS` / `NEXT_GO_CANDIDATES` / closeouts PASS

### Étape 2 — Réalignement initial de continuité active (index)
- mise à jour de la continuité active pour :
  - retirer un flux PASS de `ACTIVE_STREAMS`
  - ajouter le chantier `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` aux listes actives

### ETABLI
- `ACTIVE_STREAMS` ne référence plus `GO_GITHUB_PARK_AUDIT_EXPANSION_01` comme flux actif (closeout PASS)
- `GO_INDEX` et `REPRISE` intègrent le chantier de réalignement d’index dans la liste active

### TODO
- LOT 1 (suite) : réécrire `docs/index/NEXT_GO_CANDIDATES.md` en matrice par parent actif
- LOT 1 (suite) : déclasser `docs/next/NEXT_GO_CANDIDATES.md` (stub/redirect)

### REPRISE
- poursuivre sur LOT 1 : matrice `NEXT_GO_CANDIDATES` + déclassification `docs/next/NEXT_GO_CANDIDATES.md`

### Étape 3 — Matrice NEXT_GO_CANDIDATES (parent actif → next GO)
- réécriture de `docs/index/NEXT_GO_CANDIDATES.md` en matrice :
  - suppression des références actives à un chantier PASS
  - explicitation “aucun nouveau GO” lorsque le next est une action dans le même parent

### ETABLI
- `NEXT_GO_CANDIDATES` est aligné sur `GO_INDEX` / `ACTIVE_STREAMS` / `REPRISE` (6 GO non clos)

### TODO
- LOT 1 (suite) : déclasser `docs/next/NEXT_GO_CANDIDATES.md` (stub/redirect)

### REPRISE
- poursuivre sur LOT 1 : déclassification `docs/next/NEXT_GO_CANDIDATES.md`

### Étape 4 — Déclassification de docs/next/NEXT_GO_CANDIDATES.md
- transformation en stub de redirection explicite :
  - source canonique unique : `docs/index/NEXT_GO_CANDIDATES.md`
  - statut : file kept for compatibility (non canonique)

### ETABLI
- aucune seconde source de vérité concurrente n’est maintenue sous `docs/next/` pour NEXT

### TODO
- LOT 1 (suite) : consolider les règles “PASS ⇒ clos” dans les index si d’autres cas de drift apparaissent
- LOT 2 : hiérarchie journal (brut/index/canon) + alignement `HUMAN_CONTINUITY_*`

### REPRISE
- passer au LOT 2 (hiérarchie journal) après validation du LOT 1

### Étape 5 — Hiérarchie journal (règle canonique)
- matérialisation de la hiérarchie journal dans la doc canonique minimale :
  - `journal.md` = brut vivant
  - `journal/index/*` = dérivé opératoire
  - `journal/canon/*` = archive / historique de lecture

### ETABLI
- une règle explicite existe dans `docs/governance/JOURNAL_HIERARCHY.md`
- les chantiers journal qui lisent `journal/canon/*` le qualifient explicitement comme archive

### TODO
- aligner les éventuelles références `journal/canon/*` présentées comme base active si elles existent encore

### REPRISE
- continuer LOT 2 : alignement ciblé des docs “HUMAN_CONTINUITY_*” si une divergence réelle est identifiée

### Vigilance levée — Parent actif non-doublon (avant PHASE 2)
- `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` confirmé comme parent opératoire ciblé PHASE 1
- non-doublon confirmé vis-à-vis des chantiers `GO_UNIFORM_CONTINUITY_*` (périmètre et statut différents)

### Arbitrage ouvert — Sweep HUMAN_CONTINUITY_* reporté
- accepté : patch minimal PHASE 1 sur `docs/governance/HUMAN_CONTINUITY_CANON_USAGE.md`
- reporté : sweep global `docs/governance/HUMAN_CONTINUITY_*` non exécuté à ce stade

### REPRISE (fil “HUMAN_CONTINUITY_*”)
- si reprise du sweep : partir de `docs/governance/JOURNAL_HIERARCHY.md`, puis relire `docs/governance/HUMAN_CONTINUITY_*` pour aligner uniquement les divergences réelles
