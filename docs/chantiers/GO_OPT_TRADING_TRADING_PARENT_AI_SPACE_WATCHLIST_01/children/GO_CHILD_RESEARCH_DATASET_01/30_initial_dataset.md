# 30_INITIAL_DATASET

## Objectif

Créer le dataset qualitatif V1 du chantier IA + spatial + défense.

Ce fichier ne fige pas encore de prix, market caps, P/E ou revenus chiffrés. Ces données doivent être vérifiées au moment de la passe data chiffrée.

---

## Règle de lecture

- `core` : leader structurant ou actif central du thème.
- `infrastructure` : bénéficiaire indirect mais critique du cycle IA/spatial.
- `growth` : croissance forte, risque élevé, exécution clé.
- `speculative` : dossier asymétrique avec risque de dilution/exécution important.
- `defense` : exposition institutionnelle, gouvernementale ou militaire.
- `hybrid` : exposition forte à plusieurs thèmes.

---

## Dataset V1

| Priority | Ticker | Company | Category | Primary theme | Economic role | AI exposure | Space exposure | Defense exposure | Government dependency | Energy/Data center dependency | Profitability profile | Speculative level | Key catalysts | Main invalidation | Horizon | Notes |
|---:|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NVDA | NVIDIA | core / hybrid | IA | GPU, networking, AI compute stack | fort | faible indirect | moyen | moyen | fort | profitable | moyen | data centers, GPU demand, sovereign AI, inference | compression multiple, ralentissement capex IA, concurrence ASIC | moyen/long | Cœur du cycle IA. Sert de benchmark pour tout le panier IA. |
| 2 | AMD | Advanced Micro Devices | growth | IA | challenger GPU/CPU data center | fort | faible | faible/moyen | faible | fort | profitable/variable selon cycle | moyen/fort | rattrapage GPU IA, parts data center, alternative NVDA | retard compétitif, marges, adoption IA insuffisante | moyen/long | Dossier de rattrapage. Plus asymétrique que NVDA mais moins dominant. |
| 3 | AVGO | Broadcom | core / infrastructure | IA | ASIC custom, networking, infrastructure hyperscaler | fort | faible | moyen | moyen | fort | profitable | moyen | ASIC IA, networking, hyperscalers | dépendance gros clients, ralentissement commandes custom | long | Pilier IA moins narratif que NVDA, mais très stratégique. |
| 4 | RKLB | Rocket Lab | hybrid / speculative | spatial | lancement, satellites, défense, hypersonique | moyen indirect | fort | fort | fort | faible | non profitable/transition | fort | Neutron, backlog, Space Force, HASTE, contrats défense | retard Neutron, cash burn, dilution, échec cadence | long | Meilleur proxy public du thème mini-SpaceX + défense spatiale. |
| 5 | PLTR | Palantir | hybrid / growth | IA défense | logiciel IA gouvernement/défense | fort | faible/moyen indirect | fort | fort | faible | profitable | fort | AIP, contrats gouvernement, défense IA | valorisation excessive, ralentissement gouvernement/commercial | long | Pont central IA + gouvernement + défense. |
| 6 | VRT | Vertiv | infrastructure | data centers IA | power/cooling/racks data centers | fort indirect | faible | faible | faible/moyen | fort | profitable | moyen | densité compute, cooling IA, commandes data centers | ralentissement capex hyperscaler, marges, supply chain | moyen/long | Bénéficiaire clé hors semi-conducteurs. |
| 7 | MU | Micron | growth / cyclical | mémoire IA | DRAM, NAND, HBM | fort | faible | faible | faible | fort | cyclique | fort | HBM, cycle mémoire, demande IA | retournement cycle mémoire, marges, surcapacité | moyen | Levier IA important mais très cyclique. |
| 8 | ASTS | AST SpaceMobile | speculative | spatial telecom | satellite-to-phone | faible/moyen | fort | possible | moyen | faible | non profitable | extrême | commercialisation satellite-to-phone, partenariats telco | dilution, échec technique, retard déploiement | long | Asymétrie élevée, risque d’exécution majeur. |
| 9 | NOC | Northrop Grumman | defense | défense spatiale | systèmes militaires, espace, missiles | moyen indirect | fort | fort | fort | faible | profitable | faible/moyen | budgets défense, espace stratégique, missiles | pression budgets, exécution contrats | long | Défense spatiale stable, moins explosive que RKLB. |
| 10 | GEV | GE Vernova | infrastructure | énergie IA | turbines, grid, electrification | moyen indirect | faible | faible/moyen | moyen | fort | profitable/transition | moyen | demande électricité data centers, grid, turbines | cycle énergie, exécution industrielle, valorisation | long | Bénéficiaire clé de la contrainte électrique IA. |
| 11 | TSM | Taiwan Semiconductor | core | semi IA | fabrication avancée | fort indirect | faible | moyen géopolitique | moyen | fort indirect | profitable | moyen | demande GPU/ASIC, nœuds avancés | risque géopolitique Taïwan, cyclicité semi | long | Colonne vertébrale de l’écosystème IA. |
| 12 | ETN | Eaton | infrastructure | power management | distribution électrique, data centers | moyen indirect | faible | faible/moyen | faible/moyen | fort | profitable | faible/moyen | data centers, électrification, grid | marges, ralentissement commandes | long | Infrastructure IA défensive comparée à VRT. |
| 13 | PWR | Quanta Services | infrastructure | grid / construction | transmission, sous-stations, EPC | moyen indirect | faible | faible/moyen | moyen | fort | profitable | moyen | expansion réseau, data centers, interconnexions | exécution projets, coûts, cycles capex | long | Pelle-et-pioche du boom électrique. |
| 14 | LMT | Lockheed Martin | defense | défense espace | missiles, satellites, défense | faible/moyen | fort | fort | fort | faible | profitable | faible | budgets défense, espace, missiles | budget, programmes, marges | long | Défense stable, moins asymétrique. |
| 15 | LHX | L3Harris | defense / hybrid | capteurs / satellite | communications, capteurs, systèmes défense | moyen indirect | moyen/fort | fort | fort | faible | profitable | faible/moyen | satellites, capteurs, défense réseau | intégration, marges, budgets | long | Proxy institutionnel capteurs/satellites. |
| 16 | RTX | RTX | defense | défense / aéro | missiles, capteurs, défense aérienne | faible/moyen | faible/moyen | fort | fort | faible | profitable | faible | demande défense, missiles, capteurs | moteurs/aéro, marges, programmes | long | Défense plus large, moins spatial pur. |
| 17 | PL | Planet Labs | speculative / data | données spatiales | imagerie satellite, géospatial data | moyen | fort | moyen | moyen/fort | faible | non profitable/transition | fort | IA géospatiale, contrats gouvernement, data analytics | monétisation lente, concurrence, cash burn | long | Données spatiales + IA analytique, plus discret que RKLB. |
| 18 | LUNR | Intuitive Machines | speculative | lunaire / NASA | services lunaires, missions NASA | faible | fort | moyen | fort | faible | non profitable/variable | extrême | missions lunaires, contrats NASA, infrastructure lune | échec mission, dilution, calendrier | long | Dossier très spéculatif, événementiel. |
| 19 | MRVL | Marvell | infrastructure / growth | IA networking | custom silicon, networking | fort | faible | moyen | moyen | fort | variable | moyen/fort | ASIC, networking IA, hyperscalers | concurrence AVGO/NVDA, marges, exécution | long | À intégrer dans comparaison ASIC/réseau. |
| 20 | ARM | Arm Holdings | growth | architecture compute | IP CPU, edge/data center | moyen/fort | faible | faible/moyen | faible | moyen | profitable | fort | AI edge, datacenter CPU, licensing | valorisation, dépendance licensing, concurrence | long | Potentiel IA edge + data center, valorisation à surveiller. |
| 21 | ANET | Arista Networks | infrastructure | networking data center | switches, networking hyperscaler | fort indirect | faible | faible/moyen | faible | fort | profitable | moyen | AI networking, hyperscalers, Ethernet AI | ralentissement capex, concurrence | long | Bénéficiaire réseau IA propre. |
| 22 | SMCI | Super Micro Computer | speculative / infrastructure | serveurs IA | serveurs GPU IA | fort | faible | faible | faible | fort | profitable/variable | fort | serveurs IA, demande GPU | gouvernance, marges, concurrence, cyclicité | court/moyen | Très sensible au momentum et à la confiance. |
| 23 | DELL | Dell Technologies | infrastructure | serveurs IA | serveurs, enterprise AI | moyen/fort | faible | faible/moyen | faible | fort | profitable | moyen | serveurs IA, enterprise, stockage | marges faibles, concurrence | moyen/long | Moins pur mais réel bénéficiaire IA. |
| 24 | HPE | Hewlett Packard Enterprise | infrastructure | serveurs / réseau | enterprise AI, networking | moyen | faible | faible/moyen | moyen | moyen/fort | profitable | moyen | AI enterprise, networking, hybrid cloud | intégration, marges, concurrence | moyen/long | Moins explosif, à classer comme infra entreprise. |
| 25 | CEG | Constellation Energy | infrastructure | énergie IA | nucléaire / électricité | moyen indirect | faible | faible/moyen | moyen | fort | profitable | moyen | demande électricité data centers, contrats énergie | régulation, prix énergie, exécution | long | Proxy énergie IA défensif/stratégique. |
| 26 | VST | Vistra | infrastructure | énergie IA | production électrique | moyen indirect | faible | faible | faible/moyen | fort | profitable | moyen/fort | demande power data centers | prix énergie, régulation, valorisation | moyen/long | Bénéficiaire énergie plus cyclique. |
| 27 | IREN | IREN | speculative / infrastructure | AI cloud / énergie | capacité électrique, data centers IA | fort indirect | faible | faible | faible | fort | variable/non stable | extrême | contrats IA, capacité power, GPU cloud | dilution, exécution, financement, crypto legacy | court/moyen | Dossier très spéculatif lié à capacité énergie/IA. |
| 28 | APLD | Applied Digital | speculative / infrastructure | AI data centers | data centers IA | fort indirect | faible | faible | faible | fort | non profitable/variable | extrême | data centers, hosting GPU, énergie | financement, dilution, exécution | court/moyen | Très sensible aux annonces et au financement. |
| 29 | BKSY | BlackSky | speculative | imagerie spatiale | imagery/intelligence satellite | moyen | fort | moyen/fort | fort | faible | non profitable/transition | extrême | contrats gouvernement, géospatial intelligence | cash burn, concurrence, faible échelle | long | Petit dossier spatial data très risqué. |
| 30 | MDA.TO | MDA Space | defense / spatial | spatial Canada | satellites, robotique spatiale | moyen indirect | fort | moyen/fort | fort | faible | profitable/transition | moyen | satellites, défense, robotique, Canada | liquidité, exécution, budgets | long | Proxy spatial canadien à suivre séparément. |
| 31 | AVAV | AeroVironment | defense / hybrid | drones défense | drones, autonomy, loitering munitions | moyen/fort | faible | fort | fort | faible | profitable/variable | moyen/fort | drones, autonomie, défense moderne | budgets, concurrence, valorisation | moyen/long | Pont IA/autonomie/défense, pas spatial pur. |

---

## Classement initial leaders vs spéculatifs

### Leaders / piliers

- NVDA
- AVGO
- TSM
- NOC
- LMT
- LHX
- RTX

### Croissance agressive

- AMD
- PLTR
- VRT
- MU
- ANET
- MRVL

### Infrastructure IA / énergie

- VRT
- ETN
- GEV
- PWR
- CEG
- VST
- DELL
- HPE

### Spatial asymétrique

- RKLB
- ASTS
- PL
- LUNR
- BKSY
- MDA.TO

### Ultra spéculatifs

- ASTS
- LUNR
- BKSY
- IREN
- APLD

---

## Hypothèse de travail V1

Le thème dominant à suivre n'est pas seulement IA ou spatial séparément.

La structure à surveiller est :

`IA -> data centers -> énergie -> défense -> spatial -> satellites -> données`

Les meilleurs dossiers à analyser en priorité sont ceux qui captent plusieurs couches à la fois :

- NVDA : cerveau IA ;
- AVGO : ASIC + infrastructure ;
- PLTR : IA gouvernement/défense ;
- RKLB : lancement + satellites + défense ;
- VRT/ETN/GEV/PWR : infrastructure physique IA ;
- NOC/LHX/LMT : défense spatiale stable.

---

## Invariants dataset

- Ce dataset est qualitatif V1.
- Les chiffres financiers doivent être ajoutés seulement après vérification récente.
- Les catégories peuvent être révisées dans une passe scoring.
- Aucun ticker n'est une recommandation d'achat.
- Aucune pondération de portefeuille n'est encore définie.

---

## Prochaine étape

Créer une passe data chiffrée :

`40_verified_metrics_snapshot.md`

Objectif :

- prix actuel ;
- market cap ;
- revenus TTM ou dernier FY ;
- croissance YoY ;
- profitabilité ;
- P/E ou absence de P/E ;
- dette ;
- backlog si applicable ;
- dilution ;
- date de vérification.
