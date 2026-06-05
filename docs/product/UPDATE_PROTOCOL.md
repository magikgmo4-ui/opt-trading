---
doc_id: OPT_TRADING_PRODUCT_UPDATE_PROTOCOL
doc_type: update_protocol
repo: opt-trading
status: canonical
lifecycle_stage: product_usage
source_kind: canonical
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_PARENT_01/04_UPDATE_PROTOCOL_AFTER_PR.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/01_USAGE_VIEW.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_USAGE_VIEW_01/02_NEXT_GO_BY_PRODUCT.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/01_UPDATE_MATRIX_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/02_STATUS_PROMOTION_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/03_OPENCLAW_WORKER_ORCHESTRATION_RULES.md
  - docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/04_PR_CHECKLIST.md
  - docs/product/PRODUCT_USAGE_MATRIX.md
  - docs/product/PRODUCT_USAGE_ATLAS.md
---

# Update Protocol

## Quand mettre a jour cette couche

Mettre a jour cette couche apres toute PR significative qui :
- change le mode d'usage d'un produit ;
- ferme un gap ;
- ouvre un nouveau gap ;
- fournit un closeout de preuve ;
- ajoute ou retire un guide ;
- change un interdit live.

## Procedure canonique

1. Lire le closeout, le diff et les preuves repo.
2. Identifier les produits touches.
3. Recalculer la `usage_view` de chaque produit touche avec la precedence prudente.
4. Mettre a jour la lecture rapide et la matrice detaillee dans `PRODUCT_USAGE_MATRIX.md`.
5. Mettre a jour `PRODUCT_USAGE_ATLAS.md`.
6. Mettre a jour le guide associe si l'usage autorise change.
7. Mettre a jour `FINAL_TARGET_GAPS.md`.
8. Mettre a jour `PRODUCT_USAGE_GRAPH.mmd` si la carte change.
9. Verifier que le langage ne surevalue pas le produit.

## Precedence prudente de lecture

```text
FORBIDDEN_LIVE
> SIMULATED_ONLY
> DOC_ONLY
> USABLE_LIMITED
> USABLE_NOW
```

## Buckets a maintenir

- `USABLE_NOW`
- `USABLE_LIMITED`
- `DOC_ONLY`
- `SIMULATED_ONLY`
- `FORBIDDEN_LIVE`

## Sous-types

### DOC_ONLY
- `DOC_ONLY_REFERENCE` — documentation de reference pure
- `DOC_ONLY_INITIAL_PROJECT` — plan pose, pas de code verifie
- `DOC_ONLY_IMPLEMENTATION_READY` — documentation complete, implementation autorisee
- `DOC_ONLY_BLOCKED_BY_DEPENDENCY` — bloque par un autre produit

### SIMULATED_ONLY
- `SIMULATED_ONLY_TEST` — smoke test uniquement
- `SIMULATED_ONLY_BACKTEST` — backtest sur donnees historiques
- `SIMULATED_ONLY_IMPLEMENTATION_READY` — tests passes, pret pour usage reel

### USABLE_LIMITED
- `USABLE_LIMITED_CONSTRAINED` — utilisable avec limites documentees
- `USABLE_LIMITED_NEEDS_EXTERNAL` — depend de services externes
- `USABLE_LIMITED_PARTIAL_MODULE` — partiellement operationnel

### USABLE_NOW
- `USABLE_NOW_FULL` — produit fini, preuves completes
- `USABLE_NOW_MONITORED` — produit fini avec surveillance continue

### FORBIDDEN_LIVE
- `FORBIDDEN_LIVE_ACTIVE_DEVELOPMENT` — interdit live, en developpement

## Matrice de transition

```text
Promotion autorisee uniquement avec preuve minimale :
  DOC_ONLY → SIMULATED_ONLY : closeout de test PASS + logs + captures
  SIMULATED_ONLY → USABLE_LIMITED : 1+ session d'usage reel documentee
  USABLE_LIMITED → USABLE_NOW : toutes limites levees + 5+ sessions sans echec
  FORBIDDEN_LIVE → autre : closeout complet + revue securite + decision operateur
```

## Promotions interdites sans preuve supplementaire

- `DOC_ONLY` -> `USABLE_NOW`
- `SIMULATED_ONLY` -> `USABLE_NOW`
- `DOC_ONLY_REFERENCE` -> `USABLE_NOW`
- `SIMULATED_PASS` -> `PRODUCT_FINISHED`
- `NOT_USABLE_YET` -> `USABLE_LIMITED`
- `FORBIDDEN_LIVE` -> tout autre (sans revue complete)

## Anti-regles

```text
A1. PASS chantier ≠ USABLE_NOW
A2. Un guide ecrit ≠ usage reel prouve
A3. Un closeout documentaire ≠ preuve d'usage
A4. OpenClaw qui lance un script ≠ produit fini
A5. Une app externe qui fonctionne = projection, pas canon
A6. Un worker qui tourne en simulation ≠ utilisable en reel
A7. Un backtest PASS ≠ strategie live
A8. Une PR mergee ≠ promotion automatique
```

## Graphe de confiance

```text
Niveau 1 (source canonique) : Chantiers GO_*, closeouts, preuves repo
Niveau 2 (lecture structuree) : MATRIX, ATLAS, GAPS, GRAPH
Niveau 3 (usage documente)   : Guides, UPDATE_PROTOCOL, Checklist
Niveau 4 (projection)        : OpenClaw, workers, apps externes
Niveau 5 (non canonique)     : Chat, commentaires, logs non verifies
```

## Checklist rapide apres PR

1. Lire closeout + diff
2. Identifier produits affectes
3. Recalculer bucket + sous-type
4. Mettre a jour MATRIX → ATLAS → GAPS → Guide → GRAPH (dans cet ordre)
5. Verifier anti-regles A1-A8
6. Commiter avec reference a la PR source

Voir la checklist complete : `docs/chantiers/GO_OPT_TRADING_PRODUCT_USAGE_ATLAS_CHILD_UPDATE_PROTOCOL_01/04_PR_CHECKLIST.md`

## Questions de controle

Avant de sauvegarder la mise a jour, verifier :
- Est-ce que PASS chantier est en train d'etre confondu avec produit fini ?
- Est-ce qu'une app externe est en train d'etre promue au rang de source canonique ?
- Est-ce qu'un guide live a ete ajoute pour une surface non validee ?
- Est-ce que la `usage_view` retenue est bien la lecture la plus prudente ?
- Est-ce que chaque gap pointe encore vers un NEXT_GO ?
- Est-ce que le sous-type est correctement attribue ?
- Est-ce qu'OpenClaw ou un worker est traite comme source canonique ?

## Point de reprise

```text
docs/product/PRODUCT_USAGE_MATRIX.md
```

## RISKS

- À qualifier.
