---
doc_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01_DECISIONS
doc_type: chantier_decisions
go_id: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
chantier_parent: opt_trading_memory_bricks_localcms_consumer
sous_chantier: GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01
point_de_reprise: docs/chantiers/GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01/00_cadrage.md
status: open
updated_at: 2026-04-17
---

# GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_CONTRACT_ALIGNMENT_01 — Décisions

## Décisions retenues

### D-01 — Repo canonique du chantier
**Retenu : `opt-trading`**

Justification :
- le canon `memory_bricks` est porté par `opt-trading`
- le chantier traite d'abord du contrat producer / consumer

### D-02 — Consumer de référence
**Retenu : `LocalCMS`**

Justification :
- consumer réel déjà existant
- surface `memory_view` déjà stabilisée

### D-03 — Contrat V2 implémenté dans ce cycle
**Retenu : sous-ensemble minimal seulement**

Sous-ensemble retenu :
- `GET /health`
- `GET /status`
- `GET /bricks`
- `GET /bricks/{id}`

### D-04 — Shape de la liste
**Retenu : envelope structurée**

Shape retenue :

```json
{
  "items": [],
  "total": 0,
  "limit": 50,
  "offset": 0
}
```

Justification :
- cohérent avec la spec V2
- plus stable qu'un array plat
- extensible sans casser le consumer

### D-05 — Pagination
**Retenu : support conservé dans le contrat, complexité non prioritaire**

Justification :
- la spec la prévoit
- le consumer réel n'a pas encore prouvé un besoin fort
- garder `limit/offset` sans en faire un sujet bloquant

### D-06 — `content_markdown`
**Retenu : oui**

Justification :
- le consumer V1 lit déjà le markdown brut des briques
- l'équivalence fonctionnelle est utile

### D-07 — Endpoint `links`
**Retenu : reporté**

Justification :
- besoin non prouvé à ce stade
- pas nécessaire pour le contrat minimal

### D-08 — Endpoint `find`
**Retenu : reporté**

Justification :
- besoin non prouvé
- sujet utile mais non minimal

### D-09 — Indexes bruts
**Retenu : optionnels / non prioritaires**

Justification :
- le consumer V1 a déjà une logique fichier
- non nécessaire pour ouvrir la V2 minimale

### D-10 — Stratégie de transition
**Retenu : hybride avec fallback V1 fichier**

Justification :
- protège le consumer existant
- permet une adoption progressive
- évite une bascule brutale

---

## Impacts

- la suite du chantier ne doit pas viser toute la V2 d'un seul bloc
- le prochain GO utile est une implémentation producer minimale
- l'adoption consumer doit venir après, avec fallback explicite
- `links`, `find` et `indexes/*` sortent du périmètre minimal

---

## GO suivants retenus

### GO suivant 1
`GO_OPT_TRADING_MEMORY_BRICKS_API_V2_MINIMAL_IMPL_01`

Objet :
- implémenter le sous-ensemble V2 minimal côté producer

### GO suivant 2
`GO_LOCALCMS_MEMORY_BRICKS_HTTP_CONSUMER_ADOPT_01`

Objet :
- faire adopter le chemin HTTP minimal côté consumer, avec fallback V1 si nécessaire

### GO suivant 3
`GO_OPT_TRADING_MEMORY_BRICKS_LOCALCMS_TRANSITION_HARDENING_01`

Objet :
- fermer la transition
- clarifier le mode principal final

---

## Historique

| Date | Décision | Statut |
|---|---|---|
| 2026-04-17 | Ouverture — aucune décision encore figée | open |
| 2026-04-17 | Contrat minimal V2, shape envelope et stratégie hybride retenus | validated |
