---
doc_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01_INIT
doc_type: initial_project_doc
parent_go: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
repo: opt-trading
go_id: GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
status: open
created_at: 2026-05-30
---

# 00_INITIAL_PROJECT_DOC — Child Extraction

## 1_MASTER_TARGET

Transformer les 77 sources OpenClaw cartographiées dans le parent en une bibliothèque
`docs/openclaw/` exploitable : index cross-surfaces, fiches modules, index chantiers,
synthèse hermes/governance.

## 2_PARENT

```
GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01
docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/00_CADRAGE_PARENT.md
docs/chantiers/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_PARENT_01/01_SOURCE_CARTOGRAPHY.md
```

Lifecycle parent : open — ne pas fermer.

## 3_SCOPE

Ce child se limite à :

- Créer `docs/openclaw/` et sa structure (INDEX + sous-répertoires)
- Produire 1 fiche par module runtime (9 fiches)
- Produire les index chantiers (19), hermes (10), governance (2)
- 0 runtime modifié
- Sources : `sot/mainline` uniquement (bundle sandbox inaccessible)

## 4_DELIVERABLES

| Fichier | Contenu |
| --- | --- |
| `docs/openclaw/INDEX.md` | Master cross-surface registry |
| `docs/openclaw/modules/INDEX.md` | Table des 9 modules runtime |
| `docs/openclaw/modules/<module>.md` | Fiche opérateur par module (9) |
| `docs/openclaw/chantiers/INDEX.md` | Table des 19 chantiers avec statut |
| `docs/openclaw/hermes/INDEX.md` | Table des 10 docs Hermes + statut obsolescence |
| `docs/openclaw/governance/INDEX.md` | Synthèse TARGET_CANON + PROJECT_CARD_01 |

## 5_INVARIANTS

- Doc-only — 0 ligne de code modifiée
- Repo seul = source canonique (pas de bundle externe)
- Classification stricte par surface — pas de mélange
- PR gated obligatoire pour tout commit
- Ne pas modifier les index globaux
- Ne pas fermer le parent

## 6_ACCEPTANCE_CRITERIA

```
docs/openclaw/INDEX.md existe et pointe vers les 4 sections
9 fiches modules produites avec rôle + chemin + scripts connus
19 chantiers indexés avec statut connu
10 docs hermes indexés avec note obsolescence si applicable
2 docs governance référencés
20_ACCEPTANCE_REPORT.md rédigé et validé opérateur
```

## 17_RESUME_POINT

```
Branch: go/GO_OPENCLAW_DBLAYER_DOCS_RESEARCH_LIBRARY_CHILD_EXTRACTION_01
Etape courante: structure docs/openclaw/ créée, fiches modules à remplir
Prochain: lire chaque module runtime pour enrichir les fiches
```
