# 40_FINAL_CROSSWALK_MATRIX

## 1_MASTER_TARGET

Figer la matrice finale de recroisement entre les deux branches stocks :

- go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01
- go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01

## 7_CANONICAL_STATE

| Couche | Branche | Rôle canonique |
|---|---|---|
| Watchlist | go/GO_OPT_TRADING_TRADING_PARENT_AI_SPACE_WATCHLIST_01 | Dataset / tickers publics / classification / scoring futur |
| Market structure | go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01 | Thèse top-down SpaceX / supply chain / parabolic growth |
| Crosswalk student | go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01 | Recroisement documentaire et décisions d'alignement |

## 13_ESTABLISHED

| Sujet | Décision |
|---|---|
| LUNR | Aligné entre watchlist et market-structure |
| FLY | MARKET_STRUCTURE_ONLY pour l'instant |
| RKLB | Proxy public principal SpaceX / spatial public |
| ASTS | Spatial télécom asymétrique |
| PL | Données satellite / observation terrestre |
| AMD / NVDA | Couche compute IA |
| Watchlist | Ne pas modifier sans besoin dataset explicite |
| Market-structure | Porte les thèses sectorielles et comparaisons SpaceX |
| Student | Machine opératrice du recroisement, sans runtime Ollama |

## Matrice tickers

| Ticker / Acteur | Watchlist | Market-structure | Statut crosswalk |
|---|---:|---:|---|
| SpaceX | Non coté / référence externe | Oui | Moteur sectoriel top-down |
| RKLB | Oui | Oui | Aligné |
| FLY | Non | Oui | MARKET_STRUCTURE_ONLY |
| ASTS | Oui | Oui | Aligné |
| PL | Oui | Oui | Aligné |
| LUNR | Oui | Oui | Aligné après Patch 1 |
| AMD | Oui | Oui | Aligné |
| NVDA | Oui | Oui | Aligné |
| PLTR | Oui | Indirect | Pont IA + gouvernement + défense |
| BKSY | Oui | Non central | Dataset watchlist |
| MDA.TO | Oui | Non central | Dataset watchlist |

## 14_HYPOTHESIS

FLY pourra entrer dans la watchlist uniquement si une passe ultérieure valide explicitement :

- statut coté / investissable ;
- liquidité ;
- revenus comparables ;
- backlog ;
- contrats gouvernementaux ;
- dilution ;
- risque d'exécution.

## 15_REMAINING_GAP

| Gap | Action |
|---|---|
| Push branche student | À faire si non poussé |
| Patch LUNR market-structure | Fait localement, commit f8638520 |
| Patch FLY decision student | Fait localement, commit bd0bcd0a |
| Matrice finale | Présent document |
| Closeout student crosswalk | Prochain patch |
| PR éventuelle | Après push / vérification finale |

## 16_TODO

1. Vérifier que les trois commits locaux sont présents :
   - 4333c501 crosswalk opening ;
   - f8638520 LUNR market-structure ;
   - bd0bcd0a FLY decision.
2. Vérifier l'état Git des deux branches :
   - go/GO_OPT_TRADING_MACHINE_STUDENT_PARENT_STOCK_SPACE_AI_CROSSWALK_01 ;
   - go/GO_STOCK_SPACE_AI_MARKET_STRUCTURE_PARENT_01.
3. Préparer closeout du chantier student.
4. Préparer PR ou paquet de PR selon état des branches.

## 17_RESUME_POINT

Le recroisement est stabilisé.

Prochain mouvement :
- créer closeout student crosswalk ;
- pousser les branches non poussées ;
- préparer PR documentaire sans toucher aux index globaux.
