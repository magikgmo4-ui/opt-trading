---
doc_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01_PLAN
doc_type: chantier_plan
go_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
chantier_parent: opt_trading_memory_bricks_localcms_consumer
sous_chantier: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
point_de_reprise: docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01/00_cadrage.md
status: open
updated_at: 2026-04-17
---

# GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01 — Plan

## Objet

Produire la matrice canon vs consumer, figer le contrat minimal cible, puis ordonner les GO techniques suivants sans ouvrir d'implémentation dans ce lot.

---

## Besoin initial

Comparer proprement le canon `memory_bricks` porté par `opt-trading` avec la surface consumer réellement établie dans `LocalCMS`, afin d'éviter :

- une implémentation V2 trop large
- une adoption consumer prématurée
- une rupture du chemin V1 déjà réel

---

## Cible finale

Sortir du présent GO avec :

- une matrice canon / consumer remplie
- les écarts réellement utiles explicités
- un contrat minimal V2 retenu
- une stratégie de transition figée
- la liste des GO suivants ordonnée

---

## Étapes retenues

1. Relire le canon `opt-trading`
   - `modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md`
   - `docs/governance/MEMORY_BRICKS_MAPPING.md`
   - `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`

2. Relire la surface consumer `LocalCMS`
   - consumer `memory_view` déjà établi
   - contrat V1 réellement consommé :
     - `index/index_full.json`
     - `bricks/MB-*.md`

3. Produire la matrice canon / consumer
   - mode d'accès
   - shape de liste
   - détail brique
   - status / health
   - pagination
   - links
   - find
   - indexes bruts

4. Figer les décisions minimales de contrat
   - sous-ensemble V2 retenu
   - shape JSON retenue
   - maintien ou non du fallback V1
   - stratégie de transition

5. Ordonner les GO suivants
   - implémentation producer minimale
   - adoption consumer
   - hardening / transition

6. Préparer le closeout du cadrage
   - sans fermer le lot avant validation réelle des décisions

---

## Livrables attendus

- matrice canon / consumer dans `02_journal_technique.md`
- décisions retenues dans `03_decisions.md`
- stratégie de transition explicitée
- liste ordonnée des GO suivants
- point de reprise prêt pour fermeture du GO

---

## Hors périmètre

Le présent GO n'inclut pas :

- l'implémentation FastAPI ou équivalent
- un patch runtime du module `memory_bricks`
- un patch UI `LocalCMS`
- une migration de données
- une bascule forcée du consumer vers HTTP
