---
doc_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
status: draft_for_user_validation
lifecycle_stage: parent_opening_draft
topic_keys:
  - opt-trading
  - trading
  - btc
  - coin-m
  - accumulation
  - short-engine
  - math-base
  - risk-invariants
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
point_de_reprise: "Valider ou corriger le cadrage initial ci-dessous avant tout worker, backtest ou code d'execution."
updated_at: 2026-05-06
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01.md
---

# GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01

## 1_MASTER_TARGET

Construire une base mathematique et documentaire canonique pour un moteur d'accumulation BTC : DCA spot, marge COIN-M, shorts COIN-M servant a profiter des baisses sans vendre les BTC accumules, simulation par variables, invariants, bornes reelles, worker calculateur, correcteur et optimiseur.

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial du chantier parent.

Statut : `draft_for_user_validation`.

Regle : aucune execution reelle, aucun worker, aucun backtest et aucun trade live ne sont autorises depuis ce document tant que la validation utilisateur n'est pas explicite.

## 3_INITIAL_NEED

Documenter integralement la reponse de cadrage precedente comme base de validation pour un chantier parent dedie.

Demande utilisateur source :

> commence par une branche dedier , chantier parent, documente la derniere reponse en entier je valide

## 4_MASTER_PROJECT_PLAN

Le chantier doit suivre l'ordre suivant :

1. deposer toutes les variables ;
2. poser les relations mathematiques ;
3. comparer les methodes viables en usage reel ;
4. definir les bornes et garde-fous lies au reel ;
5. prevoir un worker calculateur ;
6. prevoir un correcteur / validateur ;
7. prevoir un optimiseur mathematique ;
8. chercher les invariants toujours vrais ;
9. viser l'accumulation BTC optimale sous contraintes.

## 6_FINAL_TARGET

Cible de phase actuelle : obtenir une fiche parent validee avant toute implementation.

Aucune recommandation de trade n'est figee ici. Le document sert de base conceptuelle et mathematique.

## 7_CANONICAL_STATE — Reponse precedente documentee en entier

Tu ne decris pas seulement une grille. Tu decris un **algorithme d'accumulation BTC avec moteur short COIN-M**.

Objectif central :

```text
Accumuler du BTC dans les deux sens du marche
sans vendre le BTC accumule
en utilisant les shorts pour capter les baisses
et le DCA/transfert pour renforcer la marge COIN-M.
```

Le short n'est donc pas un hedge principal. Son role est :

```text
profiter de la baisse sans vendre les BTC
```

---

## 13_ESTABLISHED — Toujours vrais du systeme

### Toujours vrai 1 — Le BTC accumule ne doit pas etre vendu

```text
BTC spot accumule = stock strategique
```

Il ne sert pas a prendre profit directement. Le profit vient plutot de :

```text
short COIN-M gagnant quand BTC baisse
funding positif eventuel
reallocation controlee vers marge
DCA quand le prix descend
```

### Toujours vrai 2 — Le short doit rester survivable si BTC monte

Le short peut etre perdant si BTC monte. Le systeme est viable seulement si :

```text
la perte latente du short reste absorbable par la marge COIN-M
```

Sur futures, si la maintenance margin n'est plus respectee, la liquidation devient possible. Le modele doit donc suivre maintenance margin, margin ratio et distance de liquidation.

### Toujours vrai 3 — COIN-M = logique BTC, pas seulement USD

Les contrats COIN-M sont marges en crypto ; pour BTCUSD COIN-M, le BTC sert de base de marge et de calcul PnL. Certains contrats COIN-M BTCUSD representent typiquement une valeur fixe en USD selon les specifications d'exchange.

Donc le modele doit suivre deux valeurs en meme temps :

```text
BTC reel detenu
valeur USD du BTC detenu
```

---

## 3_INITIAL_NEED — Besoin exact maintenant

Construire une base mathematique complete avant toute strategie :

```text
1. deposer toutes les variables
2. definir les relations entre variables
3. comparer les methodes viables
4. poser les bornes reelles
5. creer un worker de calcul
6. creer un correcteur / validateur
7. viser les invariants d'accumulation BTC optimale
```

---

## 4_MASTER_PROJECT_PLAN — Architecture mathematique

### Bloc A — Etat du systeme

```text
P_t = prix BTC au temps t
S_t = BTC spot accumule
U_t = reserve USDT disponible pour DCA
M_t = marge COIN-M en BTC
M_usd_t = valeur USD de la marge COIN-M
Q_t = taille totale short ouverte
E_t = prix moyen d'entree short
PnL_t = PnL latent short
R_t = PnL realise short
F_t = funding paye ou recu
MR_t = margin ratio
Liq_t = prix de liquidation estime
D_t = distance de liquidation
```

### Bloc B — Variables de decision

```text
z = distance d'echelonnement
x = frequence / cadence / cooldown
y = montant DCA brut
r = ratio de transfert spot -> COIN-M
b = montant transfere spot -> COIN-M
a = marge ajoutee au COIN-M
c = nouvelle marge totale COIN-M
g = oscillation prix utilisee comme signal
q = taille short ajoutee
tp = prise de profit short
```

### Bloc C — Relations fondamentales

```text
b = y * r
a ≈ b converti en BTC puis valorise au prix courant
c = ancienne marge + a + PnL - funding - frais
```

Mais en COIN-M, il faut garder la version BTC :

```text
BTC_achete = y / P_t
BTC_transfere_COINM = b / P_t
BTC_conserve_spot = (y - b) / P_t
```

---

## 9_SELECTED_SOLUTION — These de fonctionnement

### These centrale

```text
Le systeme cherche a augmenter le stock net de BTC
en utilisant une combinaison :
- DCA spot
- transfert partiel vers COIN-M
- shorts espaces sur hausse
- prises de profit short sur baisse
- reinjection controlee des gains
```

Le short est ajoute quand BTC monte suffisamment :

```text
g_hausse = + seuil %
=> ajout short
```

Le short prend profit quand BTC baisse suffisamment :

```text
g_baisse = - seuil %
=> TP partiel ou total
```

Exemple conceptuel :

```text
BTC monte de +g %
-> ajouter short espace

BTC baisse de -g %
-> prendre profit sur une partie du short

profit realise
-> reste en capital systeme
-> renforce accumulation ou marge
```

---

## 13_ESTABLISHED — Correction importante

Cette phrase est vraie seulement sous condition :

> si le prix monte, le DCA renforce la marge et le profit monte aussi.

Correction :

```text
si BTC monte :
- le BTC spot accumule gagne en valeur
- la marge COIN-M en BTC gagne en valeur USD
- mais les shorts ouverts perdent
```

Donc la hausse est bonne seulement si :

```text
gain spot + renfort marge > perte latente short
```

Ce n'est pas automatique.

La vraie formule est :

```text
Net_t = valeur BTC spot + valeur marge COIN-M + PnL short - funding - frais
```

---

## 12_INVARIANTS — Contraintes de surete

### Invariant 1 — Pas de liquidation imminente

```text
D_t = distance liquidation
D_t doit toujours rester > seuil_min
```

Exemple de garde-fou :

```text
si distance liquidation < seuil_min :
    bloquer nouveaux shorts
    autoriser seulement renfort marge ou reduction risque
```

### Invariant 2 — Pas de vente du BTC stock

```text
S_t ne diminue jamais par decision strategique
```

Exception uniquement a documenter :

```text
urgence liquidation / panne systeme / liquidation forcee
```

### Invariant 3 — Pas de short dense pres du prix

Tu as raison : l'echelonnement des shorts doit etre **plus distance** que le DCA.

Donc :

```text
z_short > z_dca
```

Exemple conceptuel :

```text
DCA tous les 0,5 %
short tous les 1,0 % ou 1,5 %
```

Le short doit capter des zones significatives, pas scalper chaque bruit.

### Invariant 4 — Le TP short doit liberer du free trade

Principe :

```text
premier TP rembourse une partie du risque
reste du short devient plus libre
```

Exemple logique :

```text
TP1 = 50 % du short
TP2 = 25 %
runner = 25 %
```

Mais le systeme doit tester plusieurs variantes.

---

## 14_HYPOTHESIS — Hypotheses a comparer

### H1 — Short grid large + DCA fin

```text
z_short large
z_dca plus serre
```

But :

```text
accumuler souvent
shorter seulement les exces haussiers
```

### H2 — Oscillation pure `g`

```text
si hausse de g % depuis dernier pivot -> short
si baisse de g % depuis dernier short -> TP
```

But :

```text
profiter des oscillations sans predire la tendance
```

### H3 — Volatilite adaptative

```text
z = fonction de l'ATR / volatilite recente
```

But :

```text
ne pas utiliser le meme ecartement en marche calme et violent
```

### H4 — Renfort marge dynamique

```text
r augmente quand risque liquidation augmente
r diminue quand marge est confortable
```

But :

```text
preserver le BTC spot quand tout va bien
renforcer COIN-M quand le risque augmente
```

### H5 — TP progressif des shorts

```text
TP partiel sur baisse
pas de fermeture totale obligatoire
```

But :

```text
prendre du profit sans perdre toute exposition baissiere
```

---

## 15_REMAINING_GAP — Variables manquantes a deposer

Il manque encore ces variables :

| Variable | Role |
|---|---|
| `z_short` | distance entre ajouts de shorts |
| `z_dca` | distance entre achats DCA |
| `g_up` | % hausse qui autorise short |
| `g_down` | % baisse qui autorise TP |
| `tp1` | prise de profit initiale |
| `tp2` | prise de profit secondaire |
| `runner` | portion short gardee |
| `r_min` | transfert minimal vers COIN-M |
| `r_max` | transfert maximal vers COIN-M |
| `D_min` | distance liquidation minimale |
| `MR_max` | margin ratio maximal autorise |
| `Q_max` | exposition short maximale |
| `S_min_growth` | croissance minimale BTC attendue |
| `U_floor` | reserve USDT minimale |
| `M_floor` | marge COIN-M minimale |
| `funding_limit` | funding defavorable maximal |

Le funding doit etre signe : un funding positif fait normalement payer les longs aux shorts ; un funding negatif fait payer les shorts aux longs. Le funding est un flux periodique entre longs et shorts, calcule sur la valeur notionnelle de la position.

---

## 5_GO_PLAN — Methodes de comparaison viables

### Methode 1 — Simulation historique

Tester le systeme sur des donnees BTC passees :

```text
marche haussier
marche baissier
range
crash
pump violent
haute volatilite
basse volatilite
```

### Methode 2 — Stress tests extremes

Meme principe qu'un test industriel critique :

```text
BTC +5 % rapide
BTC +10 % rapide
BTC +20 % rapide
BTC -5 % rapide
BTC -20 % rapide
range violent avec meches
funding defavorable prolonge
liquidite faible
spread eleve
```

### Methode 3 — Monte Carlo

Creer des milliers de trajectoires synthetiques :

```text
hausse lente
baisse lente
oscillation
cassure
retour violent
gap
volatilite compressee puis expansion
```

### Methode 4 — Comparaison des politiques

Comparer plusieurs politiques :

```text
policy_A = z fixe
policy_B = z adaptatif volatilite
policy_C = short large + DCA serre
policy_D = TP 50/25/25
policy_E = transfert marge dynamique
```

### Methode 5 — Pareto frontier

Chercher les configurations qui maximisent :

```text
BTC accumule final
profit short realise
survie sans liquidation
faible drawdown
faible consommation USDT
```

Et eliminer les configurations dominees.

---

## 6_FINAL_TARGET — Definition correcte de optimal

Optimal ne veut pas dire maximum profit brut.

Dans ton systeme, optimal veut dire :

```text
maximiser l'accumulation BTC
sous contrainte de non-liquidation
sous contrainte de non-vente du BTC spot
sous contrainte de marge reelle
sous contrainte de funding/frais/slippage
```

Formule conceptuelle :

```text
max BTC_total_final
```

Sous contraintes :

```text
S_t ne diminue pas
D_t > D_min
MR_t < MR_max
Q_t < Q_max
U_t >= U_floor
M_t >= M_floor
funding_loss <= funding_limit
```

---

## 10_SELECTED_SETUP — Architecture worker / correcteur

### Worker 1 — Calculateur

Role :

```text
prend les parametres
simule chaque tick / bougie / niveau
calcule marge, PnL, funding, liquidation, BTC accumule
```

Entrees :

```text
prix BTC
funding
contrat
capital initial
z_short
z_dca
x
y
r
tp
g_up
g_down
```

Sorties :

```text
BTC accumule
PnL short realise
PnL latent
marge COIN-M
distance liquidation
drawdown
nombre de shorts
etat risque
```

### Worker 2 — Correcteur

Role :

```text
refuser les configurations irrealistes
detecter les doubles comptes
tester les invariants
signaler les conflits
```

Exemples de refus :

```text
BTC spot diminue
short ajoute trop pres du prix
distance liquidation trop faible
exposition short grossit sans limite
r > 100 %
DCA consomme plus que la reserve
funding ignore
contrat minimal non respecte
```

### Worker 3 — Mathematicien / Optimiseur

Role :

```text
tester plusieurs politiques
trouver les bornes robustes
chercher les zones optimales
classer les configurations
```

Methodes :

```text
grid search
random search
Monte Carlo
stress tests
Pareto frontier
walk-forward testing
```

---

## 16_TODO — Prochaine etape propre

Creer le document initial :

```text
GO_BTC_COINM_ACCUMULATION_SHORT_ENGINE_MATH_BASE_01
```

Contenu :

```text
1. these
2. toujours vrais
3. variables d'etat
4. variables de decision
5. formules
6. invariants
7. hypotheses de methodes
8. garde-fous reels
9. worker calculateur
10. worker correcteur
11. worker optimiseur
12. protocoles de stress test
```

---

## 17_RESUME_POINT

```text
Le systeme vise une accumulation BTC optimale.
Le BTC spot accumule ne doit pas etre vendu.
Le short COIN-M sert a profiter des baisses sans vendre le BTC.
Les shorts doivent etre espaces et survivables.
Le DCA peut renforcer la marge via transfert spot -> COIN-M.
La hausse BTC augmente la valeur du stock BTC et de la marge BTC, mais fait perdre les shorts.
La baisse BTC fait gagner les shorts et permet DCA, mais reduit la valeur USD du collateral BTC.
Le modele doit etre teste comme un systeme critique : variables, bornes, invariants, stress tests, worker calculateur, correcteur, optimiseur.
```

## 18_TO_DOCUMENT

TAGS a extraire :

```text
1_MASTER_TARGET
3_INITIAL_NEED
4_MASTER_PROJECT_PLAN
6_FINAL_TARGET
7_CANONICAL_STATE
9_SELECTED_SOLUTION
12_INVARIANTS
13_ESTABLISHED
14_HYPOTHESIS
15_REMAINING_GAP
16_TODO
17_RESUME_POINT
```

## 19_TO_REMEMBER

```text
MEM_CANDIDATE:
Projet conceptuel BTC COIN-M accumulation engine :
objectif = accumulation BTC optimale sans vendre le BTC spot ;
short COIN-M = moteur de profit sur baisse, non hedge principal ;
DCA + transfert spot vers COIN-M = renfort dynamique de marge ;
modele a construire par variables, invariants, stress tests, worker calculateur, correcteur et optimiseur.
```

---

## 8_VALIDATED_PLAN

En attente de validation utilisateur.

Avant validation, les seuls gestes autorises sont :

```text
- corriger le vocabulaire ;
- completer les variables ;
- corriger les invariants ;
- ajouter les bornes reelles ;
- refuser explicitement toute hypothese dangereuse ;
- documenter les conflits.
```

## 11_KEY_DECISIONS

```text
- branche dediee : go/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
- chantier parent : GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
- surface canonique : TRADING
- role : PARENT
- objet : BTC_COINM_ACCUMULATION_ENGINE
- statut : draft_for_user_validation
```

## 12_INVARIANTS — Parent

```text
- Pas de vente du BTC spot accumule dans le modele strategique normal.
- Pas d'execution live depuis ce document.
- Pas de worker sans validation du document initial.
- Pas d'ouverture de sous-GO avant validation du parent.
- Pas de transformation du short en hedge principal sans correction explicite.
- Toute configuration doit rester testable par simulation et correcteur.
```

## 14_HYPOTHESIS — Parent

```text
- Le moteur peut optimiser l'accumulation BTC sous contrainte de non-liquidation.
- Les shorts espaces sur hausse + TP sur baisse peuvent produire du capital sans vendre le stock BTC.
- Un ratio dynamique de transfert spot -> COIN-M peut ameliorer la survivabilite.
- La politique optimale devra etre trouvee par stress tests, Monte Carlo et comparaison Pareto.
```

## 15_REMAINING_GAP — Parent

```text
- Exchange exact et contrat exact.
- Taille minimale contrat.
- Formule precise de PnL inverse COIN-M.
- Formule precise liquidation/maintenance selon exchange.
- Donnees funding historiques.
- Definition finale de z_short, z_dca, g_up, g_down, tp.
- Seuils D_min, MR_max, Q_max, U_floor, M_floor.
```

## 16_TODO — Parent

```text
1. Validation utilisateur du present document.
2. Correction du nommage si le rattachement produit doit etre autre que TRADING.
3. Creation eventuelle d'un document 02_variables_bounds.md.
4. Creation eventuelle d'un document 03_worker_spec.md.
5. Creation eventuelle d'un correcteur d'invariants, uniquement apres validation.
```

## 17_RESUME_POINT — Parent

Reprendre ici : document parent cree, statut `draft_for_user_validation`, attente validation ou corrections utilisateur.

## RISKS

- À qualifier.
