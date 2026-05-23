---
doc_id: OPT_TRADING_GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01
doc_type: governance_rule
repo: opt-trading
project: opt-trading
module: doc_ops
go_id: GO_OPT_TRADING_DOC_OPS_METHOD_SESSION_PATCH_TRANSPORT_01
status: draft
lifecycle_stage: governance_candidate
surface: governance
source_kind: canonical_candidate
updated_at: 2026-05-21
topic_keys:
  - opt-trading
  - global_indexes
  - master_target
  - closeout
  - continuation
  - index_aggregation
reference_canonique_principale: docs/governance/GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01.md
point_de_reprise: "Section 7 - Decision tree"
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/governance/PARENT_CONTINUITY_INDEX_INBOX_METHOD_01.md
  - docs/index/GO_INDEX.md
  - docs/index/GO_CLOSED_INDEX.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/REPRISE.md
---

# GLOBAL_INDEX_UPDATE_TRIGGER_RULE_01

## 1. Objet

Fixer une règle plus nette pour savoir quand proposer ou exécuter la mise à jour des index globaux.

## 2. Index globaux concernés

```text
docs/index/GO_INDEX.md
docs/index/GO_CLOSED_INDEX.md
docs/index/ACTIVE_STREAMS.md
docs/index/NEXT_GO_CANDIDATES.md
docs/index/REPRISE.md
docs/index/BRANCH_STATE.md
```

## 3. Règle par défaut

Par défaut :

```text
continuité locale parent + docs/index/inbox/<GO_ID>.md
```

Les index globaux ne sont pas modifiés pour chaque micro-avancement.

## 4. Règle master target

Les index globaux doivent refléter les **master targets**, pas les targets internes de session ou de sous-phase.

Un target interne atteint peut fermer une tâche, un fichier, un enfant ou une phase.

Un master target atteint peut justifier une mise à jour globale si l'état est :

- terminé;
- testé;
- utilisable réellement;
- ou reclassé explicitement comme closeout/pass;
- ou porteur d'un changement de prochaine destination.

## 5. Parent fermé ≠ horizon terminé

Un parent fermé ne signifie pas automatiquement :

```text
master target complete
```

À chaque fermeture parent, relire :

- `1_MASTER_TARGET`;
- `6_FINAL_TARGET`;
- `7_CANONICAL_STATE`;
- `13_ESTABLISHED`;
- `15_REMAINING_GAP`;
- `17_RESUME_POINT`.

Puis décider :

```text
A. master target atteint réellement -> proposer batch index global
B. target interne atteint mais horizon restant -> ouvrir continuité locale / nouveau parent rattaché
C. parent fermé mais destination non claire -> créer NEXT local, pas index global
D. vrai closeout produit ou PASS -> GO_CLOSED_INDEX + retrait GO_INDEX via batch
```

## 6. Quand proposer une mise à jour globale

La session conversationnelle doit suggérer un update global quand au moins une condition forte est vraie :

- master target produit réellement atteint;
- produit fini testé et utilisable;
- passage réel `OPEN/ACTIVE` vers `CLOSED/PASS`;
- changement de priorité opératoire globale;
- changement du `next GO primaire` d'un parent actif;
- nouveau parent devient horizon principal;
- branche significative ouverte/fermée/abandonnée;
- batch d'agrégation explicitement demandé;
- divergence claire entre inbox locale et index global.

## 7. Decision tree

```text
Une action vient d'être terminée.
  |
  |-- Est-ce seulement une target interne?
  |     -> Oui: garder local parent + inbox. Ne pas modifier index global.
  |
  |-- Est-ce que le master target est atteint, testé ou utilisable réellement?
  |     -> Oui: proposer batch d'agrégation des index globaux.
  |
  |-- Est-ce un parent fermé mais l'horizon continue?
  |     -> Oui: créer un nouveau parent/GO de continuité rattaché au master target. Ne pas forcer GO_INDEX.
  |
  |-- Est-ce un vrai closeout produit ou PASS?
  |     -> Oui: proposer déplacement GO_INDEX -> GO_CLOSED_INDEX via batch.
  |
  |-- Est-ce que le next GO primaire change?
  |     -> Oui: proposer update NEXT_GO_CANDIDATES + REPRISE via batch.
  |
  |-- Sinon:
        -> local parent + inbox seulement.
```

## 8. Niveau de permission conversationnelle

La session conversationnelle peut :

- suggérer la mise à jour globale;
- préparer un patch;
- préparer un `INDEX_PATCH.md`;
- préparer un batch d'agrégation.

Elle ne doit pas modifier les index globaux sans demande explicite ou validation claire.

## 9. Formule de suggestion standard

```text
INDEX_GLOBAL_UPDATE_CANDIDATE:
Le master target semble avoir changé ou être atteint. Je recommande d'ouvrir un batch d'agrégation des index globaux plutôt que de modifier les index dans ce GO.
Surfaces candidates:
- GO_INDEX.md
- GO_CLOSED_INDEX.md
- ACTIVE_STREAMS.md
- NEXT_GO_CANDIDATES.md
- REPRISE.md
Raison:
<raison courte>
```

## 10. Anti-confusion

Ne pas confondre :

| Élément | Sens |
|---|---|
| target interne | étape locale atteinte |
| closeout fichier | document final local |
| parent fermé | lot parent terminé ou transmis |
| master target atteint | destination produit/méthode réellement atteinte |
| produit fini testé | utilisable en condition réelle |
| index global update | agrégation contrôlée, pas journal de session |

## 11. Règle opérationnelle courte

```text
Les index globaux sont mis à jour quand l'horizon change, pas quand une session avance.
```
