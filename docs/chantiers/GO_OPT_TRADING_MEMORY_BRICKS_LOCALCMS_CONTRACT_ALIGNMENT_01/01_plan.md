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

Produire la matrice canon vs consumer et figer le contrat minimal cible.

---

## Étapes

1. Lire le canon `opt-trading`
   - lire `SPEC_MEMORY_BRICKS_API_V2_READONLY.md`
   - lire `MEMORY_BRICKS_MAPPING.md`
   - noter les champs exposés, les types, les endpoints définis

2. Lire la surface consumer `LocalCMS`
   - identifier les appels effectifs à `memory_bricks`
   - identifier les champs réellement consommés
   - identifier le mode actuel : fichier local ou HTTP

3. Produire la matrice d'alignement
   - colonne producer : ce que `opt-trading` expose ou prévoit
   - colonne consumer : ce que `LocalCMS` consomme réellement
   - statut par champ : aligné / écart / à décider

4. Décider le contrat minimal
   - format de liste retenu
   - champs obligatoires
   - champs optionnels
   - stratégie de fallback

5. Ordonner les GO suivants
   - GO_2 producer impl
   - GO_3 consumer adopt
   - GO_4 transition hardening

---

## Livrables

- matrice de contrat (`02_journal_technique.md` ou section dédiée)
- décisions figées (`03_decisions.md`)
- point de reprise mis à jour
- séquence GO suivants validée
