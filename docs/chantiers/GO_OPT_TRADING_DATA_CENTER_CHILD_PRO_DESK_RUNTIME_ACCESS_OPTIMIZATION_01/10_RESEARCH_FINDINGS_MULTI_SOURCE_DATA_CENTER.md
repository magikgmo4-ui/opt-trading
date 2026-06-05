---
doc_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01_RESEARCH_FINDINGS
doc_type: research
repo: opt-trading
go_id: GO_OPT_TRADING_DATA_CENTER_CHILD_PRO_DESK_RUNTIME_ACCESS_OPTIMIZATION_01
status: open
source_kind: canonical
created_at: 2026-06-05
links:
  - modules/data_center/registry/pro_desk_data_inventory.json
  - modules/data_center/registry/source_candidates.json
  - docs/chantiers/GO_OPT_TRADING_DATA_CENTER_CHILD_SOURCE_RELIABILITY_SCORING_01/BEST_VALUE_RESOLVER_POLICY.md
---

# 10_RESEARCH_FINDINGS_MULTI_SOURCE_DATA_CENTER

## Objet

Etat de l'art et precedents connus sur les architectures multi-source Data Center : Master Data Management (MDM), data contracts, lineage, source selection, et arbitrage de sources candidates.

## 1. Precedents industriels

### 1.1 Bloomberg Data License / B-PIPE

```text
Bloomberg gere des milliers de sources (exchanges, contributeurs, OTC).
Chaque instrument a un flux primaire + fallbacks.
Le terminal affiche la "best available price" sans exposer la source au trader.
La selection est interne, basee sur : venue priority, latency, liquidity.
```

**Ce qu'on reprend :** Data Center = arbitre interne. Consumer = ne choisit pas la source.

### 1.2 Refinitiv Elektron / TREP

```text
Refinitiv utilise un "contributor model" :
- Chaque contributor a un score de qualite
- Le "consolidated feed" fusionne les contributions redondantes
- Les consumers s'abonnent au RIC (Refinitiv Instrument Code), pas a un contributor
```

**Ce qu'on reprend :** `canonical_value.v1` = equivalent du RIC. `source_score.v1` = equivalent du contributor quality score.

### 1.3 Coinglass / Glassnode / DeFiLlama (crypto)

```text
Les agregateurs crypto gerent des dizaines d'exchanges :
- Coinglass : OI, funding, liquidations par exchange, expose un "aggregated OI"
- Glassnode : on-chain data multi-sources (nodes + APIs)
- DeFiLlama : TVL agregee par chain/protocole avec transparence des sources
```

**Ce qu'on reprend :** La transparence des sources candidates. `resolver_decision.v1` expose les alternatives rejetees.

## 2. Master Data Management (MDM)

```text
Principes MDM applicables au Data Center :

1. Golden Record : une valeur canonique par entite (symbol + data_key)
   → canonical_value.v1

2. Source of Truth : une source primaire par domaine
   → pro_desk_data_inventory.json declare le domaine (P0-P21)

3. Survivorship : regles de merge quand plusieurs sources existent
   → source_score.v1 + resolver_decision.v1

4. Lineage : tracabilite complete source → transformation → consommation
   → source_evidence.v1 + audit_lineage (P21)

5. Stewardship : qui est responsable de chaque donnee
   → producer_id + contract_class + validated_at
```

## 3. Data Contracts et Schema Validation

```text
Un data contract = promesse du producer au consumer :

{
  "contract_class": "market_metrics.v1",
  "schema": { ... },
  "freshness_sla": "max_age_seconds: 3600",
  "completeness_sla": "min_completeness: 0.8",
  "producer_id": "derivatives_collector__bitget"
}

Le Data Center enforce le contrat :
- schema_validation → dimension du source_score (poids 0.15)
- freshness check → dimension du source_score (poids 0.20)
- completeness → dimension du source_score (poids 0.15)

Si le contrat est viole, le score baisse, la source peut devenir ineligible.
```

## 4. Lineage et audit trail

```text
Trajectoire complete d'une donnee :

producer write
  → producer path (audit trail)
  → source_score evaluation (dimensions + evidence)
  → source_selector decision (resolver_decision.v1)
  → canonical_value publication (view)
  → consumer read

Chaque etape est tracee :
- producer : produced_at, producer_id, contract_class
- scoring : source_score.v1 + source_evidence.v1
- selection : resolver_decision.v1 (candidates, scores, selection_reason)
- publication : canonical_value.v1 (winning_producer, alternatives)
- consumption : consumer read timestamp + path
```

## 5. Arbitrage de sources : lecons apprises

```text
1. Ne pas cacher les alternatives.
   → resolver_decision.v1 liste TOUS les candidats, pas seulement le gagnant.

2. Ne pas figer le scoring.
   → Les poids des dimensions sont configurables par contract_class.

3. Toujours avoir un fallback.
   → Si 0 candidats eligibles, retourner la derniere valeur connue avec stale=true.

4. Mesurer avant d'optimiser.
   → Les cibles de perf (<0.1ms, ~30ms) sont des targets, pas des faits.

5. Le lineage est aussi important que la valeur.
   → Un consumer doit pouvoir auditer pourquoi une valeur a ete choisie.
```

## 6. Implications pour l'architecture runtime

```text
CE QUE LA RECHERCHE CONFIRME :

1. Les index compiles sont la bonne approche V1.
   → Bloomberg, Refinitiv, Coinglass utilisent tous des caches/indexes pre-calcules.
   → Aucun ne parse un fichier JSON complet a chaque requete.

2. Le source selector est un composant standard.
   → Tous les data aggregators ont un "resolver" ou "consolidator" interne.
   → Aucun n'expose la selection brute au consumer.

3. SQLite / base embarquee est utilise (Glassnode, Dune) mais pas pour le hot path.
   → Les requetes OLTP critiques passent par un cache memoire.
   → SQLite = option valide pour le stockage froid (history, audit, lineage).

4. La transparence des sources est un differentiateur.
   → Peu d'outils retail exposent pourquoi une valeur a ete choisie.
   → resolver_decision.v1 + canonical_value.v1 = avantage pro-desk.
```
