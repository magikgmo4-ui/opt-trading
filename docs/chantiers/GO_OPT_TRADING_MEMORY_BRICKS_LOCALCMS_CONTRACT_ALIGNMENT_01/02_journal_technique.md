---
doc_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01_JOURNAL
doc_type: chantier_journal
go_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
chantier_parent: opt_trading_memory_bricks_localcms_consumer
sous_chantier: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
point_de_reprise: docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01/00_cadrage.md
status: open
updated_at: 2026-04-17
---

# GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01 — Journal technique

## Objet

Comparer le canon `memory_bricks` porté par `opt-trading` avec la surface consumer réelle déjà établie dans `LocalCMS`, puis figer le contrat minimal utile avant toute implémentation.

---

## Sources retenues

### Canon producer
- `modules/memory_bricks/docs/SPEC_MEMORY_BRICKS_API_V2_READONLY.md`
- `docs/governance/MEMORY_BRICKS_MAPPING.md`
- `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`

### Consumer réel
- consumer `memory_view` déjà ouvert et stabilisé côté `LocalCMS`
- contrat V1 réellement consommé :
  - `index/index_full.json`
  - `bricks/MB-*.md`

---

## État réel retenu

### Côté `opt-trading`
- `memory_bricks` est canonique comme forme compacte dérivée
- une spec V2 HTTP read-only existe
- cette V2 reste une spec, pas encore verrouillée par un consumer réel

### Côté `LocalCMS`
- un consumer réel existe déjà
- il consomme une forme V1 fichier
- il ne prouve pas encore le besoin complet de toute la V2 HTTP

---

## Matrice canon / consumer

| Élément | Canon `opt-trading` | Réel `LocalCMS` | Écart observé | Impact |
|---|---|---|---|---|
| Source d'état | `_state/memory_bricks` via backend V1 | export local de fichiers | oui | transition à gérer |
| Mode d'accès | HTTP V2 proposée | fichiers locaux V1 | oui | contrat à converger |
| Liste | `GET /bricks` | `index/index_full.json` | oui | shape à figer |
| Détail | `GET /bricks/{id}` | `bricks/MB-*.md` | faible | conserver markdown utile |
| Health | `GET /health` | absent | oui | facile à ajouter |
| Status | `GET /status` | absent comme surface standard | oui | utile pour diagnostic |
| Pagination | `limit/offset` proposés | non prouvés utiles | oui | peut être différée |
| Links | endpoint dédié proposé | non prouvé utile | oui | reporter |
| Find | endpoint proposé | non prouvé utile | oui | reporter |
| Indexes bruts | proposés | déjà présents en V1 fichier | partiel | optionnel |

---

## Lecture technique retenue

Le consumer `LocalCMS` ne justifie pas encore l'implémentation de toute la V2.

Le plus petit contrat utile et défendable est :
- `GET /health`
- `GET /status`
- `GET /bricks`
- `GET /bricks/{id}`

Le chemin recommandé est une transition hybride :
- conservation du fallback V1 fichier
- ouverture d'un chemin V2 HTTP minimal
- adoption progressive côté consumer

---

## Risques identifiés

- implémenter trop large sans besoin prouvé
- casser un consumer V1 déjà stable
- figer trop tôt pagination / links / search sans validation d'usage réel

---

## Recommandation

Valider un sous-ensemble minimal V2, puis découper la suite en :
1. implémentation producer minimale
2. adoption consumer
3. hardening / transition

---

## Historique des entrées

| Date | Entrée |
|---|---|
| 2026-04-17 | Ouverture du journal — cadrage non encore commencé |
| 2026-04-17 | Matrice canon / consumer remplie et lecture technique minimale retenue |
