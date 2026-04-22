---
doc_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01_DECISIONS
doc_type: chantier_decisions
repo: opt-trading
project: opt-trading
module: continuity
go_id: GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01
status: active
lifecycle_stage: decisions
topic_keys:
  - opt-trading
  - continuity
  - indexes
  - reprise
  - next
surface: chantier
source_kind: canonical
updated_at: 2026-04-22
links:
  - docs/index/GO_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/REPRISE.md
  - docs/index/NEXT_GO_CANDIDATES.md
---

# 03_decisions — GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01

## D1 — Méthode canonique de reprise (repo-first, multi-parent)
Séquence canonique :
1. lire `docs/index/GO_INDEX.md` comme index des chantiers parents actifs
2. choisir un chantier parent actif
3. lire `docs/index/NEXT_GO_CANDIDATES.md` pour l’entrée de ce parent
4. descendre vers le chantier local canonique associé (si applicable)
5. utiliser `docs/index/REPRISE.md` uniquement comme support opératoire

Règles :
- ne pas modéliser la reprise comme un inventaire plat
- interdire toute seconde source de vérité concurrente à `docs/index/*`
- éviter tout doublon parent / local pour couvrir un même besoin

## D2 — Survivant canonique de NEXT_GO_CANDIDATES
Le survivant canonique est :
- `docs/index/NEXT_GO_CANDIDATES.md`

## D3 — Déclassification de docs/next/NEXT_GO_CANDIDATES.md
`docs/next/NEXT_GO_CANDIDATES.md` doit devenir :
- un stub/redirect explicite vers `docs/index/NEXT_GO_CANDIDATES.md`
- et ne plus être utilisé comme source canonique

## D4 — Règle closeout PASS ⇒ dossier clos pour la continuité active
Si un dossier chantier possède un `90_closeout.md` avec `status: pass` :
- le dossier est considéré clos pour la continuité active
- il ne doit pas apparaître dans `ACTIVE_STREAMS` comme flux actif

## D5 — Parent actif PHASE 1 (non-doublon)
`GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` est assumé comme :
- le parent opératoire ciblé pour PHASE 1 (LOT 1 continuité index + LOT 2 hiérarchie journal)
- un nouveau parent actif canonique pour la continuité locale `opt-trading`

Non-doublon confirmé :
- ce parent ne duplique pas un “parent continuity index” existant
- les chantiers `GO_UNIFORM_CONTINUITY_*` existants sont des pilotes/hardening déjà clos (PASS) ou des références ; ils ne portent pas ce rôle opératoire PHASE 1

## D6 — Sweep HUMAN_CONTINUITY_* (report explicite)
Accepté pour PHASE 1 :
- patch minimal sur `docs/governance/HUMAN_CONTINUITY_CANON_USAGE.md`

Report (non exécuté maintenant) :
- sweep global `docs/governance/HUMAN_CONTINUITY_*` non exécuté en PHASE 1
- arbitrage conservé ouvert, à reprendre en PHASE 2 ou via une phase dédiée ultérieure

## D7 — Arbitrage final du bundle GO_INDEX_ALIGNMENT_IDE_BUNDLE
Décisions retenues :
- `GO_OPT_TRADING_GO_INDEX_CANONICAL_ALIGNMENT_01` est absorbé par `GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01` ; aucun nouveau parent canonique n’est ouvert
- `GO_OPT_TRADING_GO_INDEX_METADATA_COMPLETION_01` est absorbé en gap-only dans le parent de réalignement d’index si des métadonnées restent réellement incomplètes
- `GO_OPT_TRADING_GO_INDEX_PRE_TABLE_NORMALIZATION_01` est écarté canoniquement : la continuité locale ne retient pas de file séparée “avant tableau” dans `docs/index/*`
- `GO_OPT_TRADING_GO_INDEX_DERIVED_FAMILY_VIEW_01` est absorbé autrement par les surfaces déjà retenues pour les lectures dérivées de famille : audit famille + `docs/status/*`
- les notions `SURFACE_DOCUMENTAIRE_NON_CHANTIER` et “repère dérivé non canonique” sont ancrées comme règles de lecture, sans créer de nouvelle couche d’exécution autonome
- le closeout du sujet bundle est porté par `91_bundle_closeout_go_index_alignment.md` dans ce chantier absorbant

Justification :
- éviter l’ouverture rétroactive d’un GO nominal doublon
- conserver une seule chaîne canonique de continuité pour l’alignement d’index
- ancrer la règle utile, sans importer toute la taxonomie transitoire du bundle

## REPRISE
Point de reprise unique :
- `docs/chantiers/GO_OPT_TRADING_CONTINUITY_INDEX_REALIGNMENT_01/02_journal_technique.md`
