---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
status: validated
lifecycle_stage: child_opening_plan
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitcoin
  - gold
  - xauusd
  - bitget
  - coin-futures
  - formulas
  - compatibility
  - no-duplicate-coding
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
point_de_reprise: "Valider ce document initial avant de lancer 01_formulas_compat_review.md ou tout sous-chantier suivant."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
  - docs/index/inbox/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01.md
---

# GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

## 1_MASTER_TARGET

Créer une stratégie robuste d’accumulation Bitcoin + Gold, en réutilisant l’existant opt-trading, sans double codage, sans double module, sans double UI, sans backtest prématuré, sans live.

## 2_INITIAL_PROJECT_DOC

Ce document est le transporteur initial validé pour ouvrir le child de review formules / compatibilité.

Il documente intégralement les deux réponses qui ont précédé la validation utilisateur :

1. la décision `FORMULAS REVIEW` avant `BACKTEST_DATA_PREP` ;
2. l’élargissement de l’objectif final vers une stratégie robuste d’accumulation `Bitcoin + Gold`.

Statut : `draft_for_user_validation`.

Règle : aucun sous-chantier opérationnel, aucun worker, aucun backtest, aucune connexion exchange et aucune UI nouvelle ne sont autorisés avant validation explicite de ce document.

## 3_INITIAL_NEED

Demande utilisateur source :

```text
prend les 2 derniere reponses et documente l'integral je valide et ensuite on lance les sous chantiers , fixe dabord un plan precis
```

Validation utilisateur du plan :

```text
valider
```

## 4_MASTER_PROJECT_PLAN

Ordre strict :

1. ouvrir ce document initial ;
2. y copier intégralement les deux réponses de cadrage ;
3. figer l’objectif final `stratégie robuste accumulation Bitcoin + Gold` ;
4. statuer les invariants anti-double-codage ;
5. valider ce document ;
6. ouvrir ensuite seulement `01_formulas_compat_review.md` ;
7. ne pas ouvrir `BACKTEST_DATA_PREP` tant que la review formules n’est pas PASS ;
8. cadrer Gold/XAUUSD séparément, sans mélanger les formules BTC et Gold.

---

# COPIE INTÉGRALE — RÉPONSE 1

## VERDICT

```text
Choix recommandé : FORMULAS REVIEW d’abord.
Backtest data prep ensuite seulement.
```

Raison : le backtest dépend des formules Bitget figées. Sans `qty_to_notional_fn`, PnL inverse, funding signé et liquidation/cross margin, un backtest produirait des résultats non fiables.

## 13_ESTABLISHED

PR #235 est bien mergée dans `sot/mainline`, avec `merged=true`, `closed`, merge commit `64dc0d70`, et les 5 fichiers documentaires du parent.

Sur l’existant repo :

| Surface existante | Rôle à réutiliser |
|---|---|
| `modules/trading_lab_v1` | squelette LAB existant, mais pas encore backtest réel ; ne pas recréer un second lab/backtest. |
| `modules/desk_pro_runner` | point d’entrée opérateur déjà capable de piloter orchestration, dashboard, export JSON/HTML. |
| `modules/probability_engine` | moteur analytique existant avec features, score long/short, contexte derivatives, sortie JSON. |
| `docs/ui_indexation/01_ui_registry_modules.md` | registre UI déjà établi : `ops_menu_hub`, `desk_pro_dashboard`, `desk_pro_runner`, `probability_engine`, `risk_engine`, `market_scanner`, etc. |

## 5_GO_PLAN — Child recommandé

```text
GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
```

Parent :

```text
GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
```

Objectif strict :

```text
Figer les formules Bitget et leur compatibilité avec les surfaces existantes,
sans créer de nouveau module, sans nouveau backtest, sans nouvelle UI.
```

## 12_INVARIANTS — Anti-double-codage

```text
- Ne pas créer un nouveau module si trading_lab_v1, probability_engine, risk_engine, desk_pro_runner ou desk_pro_dashboard peuvent être étendus/adaptés.
- Ne pas créer une nouvelle UI : passer par ops_menu_hub / desk_pro_dashboard / desk_pro_runner.
- Ne pas créer un second moteur de probabilité : réutiliser probability_engine si un score analytique est requis.
- Ne pas créer un second lab/backtest : préparer l’intégration future via trading_lab_v1.
- Ne pas connecter Bitget live.
- Ne pas exécuter de backtest.
- Ne pas écrire de worker runtime.
- Produire seulement une review de compatibilité + contrats de fonctions.
```

## 6_FINAL_TARGET — Ce que le child doit produire

Créer un document :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
```

Contenu attendu :

```text
1. Inventaire des surfaces existantes à réutiliser.
2. Mapping formule → module existant.
3. Fonctions Bitget à figer.
4. Contrats d’entrée/sortie JSON.
5. Gaps qui bloquent backtest.
6. Décision : extension existante ou nouveau composant interdit.
7. Préparation du child suivant : BACKTEST_DATA_PREP.
```

## Mapping proposé

| Besoin BTC COIN-M | Réutilisation attendue | Interdit |
|---|---|---|
| Formules Bitget | doc `04_math_formulas.md` + nouveau review doc | coder directement |
| Backtest futur | `modules/trading_lab_v1` | créer `btc_backtester` séparé |
| Sortie opérateur/UI | `desk_pro_runner` / `desk_pro_dashboard` | créer nouvelle UI |
| Score / résumé analytique | `probability_engine` si score requis | créer second probability engine |
| Risque/liquidation | `risk_engine` si présent/compatible, sinon contrat d’adapter | dupliquer risk logic |
| Menu opérateur | `ops_menu_hub` | nouveau menu isolé |

## GO_PROMPT — Ouvrir le child review

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /opt/trading
git fetch origin

git checkout sot/mainline
git pull --rebase origin sot/mainline

git checkout -b go/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

mkdir -p docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

cat > docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md <<'EOF'
---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01_FORMULAS_COMPAT_REVIEW
doc_type: formulas_compat_review
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
status: draft
lifecycle_stage: child_opening_review
topic_keys:
  - opt-trading
  - trading
  - btc
  - bitget
  - coin-futures
  - formulas
  - compatibility
  - no-duplicate-coding
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
point_de_reprise: "Review formules Bitget et compatibilité avec modules existants avant backtest data prep."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
---

# 01_formulas_compat_review

## 1_MASTER_TARGET

Figer les formules Bitget BTC COIN-FUTURES et leur compatibilité avec l’existant sans double codage, sans nouveau module, sans nouveau backtest et sans nouvelle UI.

## 4_MASTER_PROJECT_PLAN

1. Relire les docs parent 01/02/03/04.
2. Inventorier les surfaces existantes.
3. Mapper chaque besoin vers un module existant.
4. Figer les formules Bitget encore UNKNOWN.
5. Définir les contrats JSON d’entrée/sortie.
6. Refuser toute duplication.
7. Préparer seulement ensuite BACKTEST_DATA_PREP.

## 12_INVARIANTS

```text
- ne pas créer de nouveau module si une surface existante peut être adaptée
- ne pas créer de nouvelle UI
- ne pas créer de second backtest engine
- ne pas créer de second probability/risk engine
- pas de connexion exchange
- pas d’exécution live
- pas de backtest réel
- documentation + contrats uniquement
```

## 15_REMAINING_GAP

```text
- qty_to_notional_fn Bitget
- notional_to_qty_fn Bitget
- PnL inverse COIN-M
- liquidation / maintenance cross margin
- funding historique requis avant backtest
- mapping final vers trading_lab_v1 / desk_pro / probability_engine / risk_engine
```

## 16_TODO

```text
1. Compléter l’inventaire existant.
2. Définir le mapping besoin -> module existant.
3. Définir les fonctions mathématiques à figer.
4. Définir les contrats JSON.
5. Lister explicitement les interdits de duplication.
6. Produire verdict PASS/PATCH_REQUIRED/FAIL.
```

## 17_RESUME_POINT

Child ouvert pour review de compatibilité formules.
Ne pas ouvrir BACKTEST_DATA_PREP tant que ce review n’est pas PASS.
EOF

git add docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
git commit -m "docs: open BTC COIN-M formulas compatibility review"

git status --short --branch --untracked-files=no
git diff --stat origin/sot/mainline...HEAD
```

## 17_RESUME_POINT

```text
PR #235 mergée.
Parent BTC COIN-M canonique présent sur sot/mainline.
Suite correcte : child FORMULAS_COMPAT_REVIEW.
BACKTEST_DATA_PREP attendra.
Règle forte : réutiliser trading_lab_v1, desk_pro_runner/dashboard, probability_engine/risk_engine si compatibles.
Pas de double module, pas de double fonction, pas de double UI.
```

---

# COPIE INTÉGRALE — RÉPONSE 2

## 13_ESTABLISHED — Plan validé

```text
PLAN = VALIDÉ
Suite = FORMULAS_COMPAT_REVIEW avant BACKTEST_DATA_PREP
Règle = compatibilité avec existant, zéro double codage
Objectif final global = stratégie robuste d’accumulation Bitcoin + Gold
```

## Correction canonique à intégrer

Le parent actuel reste :

```text
GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01
```

Mais l’objectif produit plus large doit être statué comme :

```text
Stratégie robuste d’accumulation Bitcoin + Gold
```

Donc on distingue :

| Niveau | Rôle |
|---|---|
| Parent BTC COIN-M actuel | Premier chantier mathématique sur accumulation BTC via Bitget COIN-FUTURES |
| Objectif final produit | Stratégie robuste d’accumulation multi-actifs : Bitcoin + Gold |
| Gold | À rattacher à l’existant XAUUSD / Trading Dual Stack / Trading Lab, sans créer une deuxième architecture |
| BTC | À rattacher au parent BTC COIN-M validé |
| UI | Desk Pro / dashboard / ops_menu_hub existants |
| Lab/backtest | `trading_lab_v1`, pas nouveau moteur |

## 6_FINAL_TARGET — Formulation canonique

À ajouter dans le child `FORMULAS_COMPAT_REVIEW` :

```text
L’objectif final du programme n’est pas seulement un moteur BTC COIN-M.
L’objectif final est une stratégie robuste d’accumulation Bitcoin + Gold.

Bitcoin :
- accumulation BTC long terme ;
- short COIN-M comme moteur de profit sur baisse sans vendre le BTC accumulé ;
- DCA + renfort de marge selon règles mathématiques.

Gold :
- accumulation / exposition robuste sur l’or ;
- rattachement prioritaire à l’existant XAUUSD / Trading Dual Stack / Trading Lab ;
- pas de double architecture ;
- les règles Gold devront être traitées dans un child séparé ou un parent global si le périmètre dépasse BTC.

La logique commune est :
- robustesse ;
- accumulation ;
- non-liquidation ;
- simulation ;
- validation par formules ;
- backtest seulement après bornes ;
- intégration UI par surfaces existantes.
```

## 12_INVARIANTS — À ajouter

```text
- Le chantier BTC ne doit pas enfermer le programme final dans BTC seulement.
- L’objectif final est Bitcoin + Gold.
- Le Gold ne doit pas être codé dans un nouveau module isolé si XAUUSD / Trading Lab / Desk Pro peuvent servir.
- BTC et Gold peuvent partager une couche stratégie, mais les formules produit/contrat restent séparées.
- Pas de double UI.
- Pas de double backtest engine.
- Pas de double risk/probability engine.
```

## Décision structurante

Je recommande cette hiérarchie :

```text
1. Objectif produit global :
   STRATEGIE_ROBUSTE_ACCUMULATION_BTC_GOLD

2. Parent courant :
   BTC COIN-M accumulation engine

3. Child courant :
   formulas compatibility review

4. Child futur probable :
   BTC COIN-M backtest data prep

5. Chantier Gold futur :
   GOLD / XAUUSD accumulation model review
```

Ne pas mélanger tout de suite Gold dans les formules BTC. Il faut seulement **statuer l’objectif final global** maintenant, puis garder BTC et Gold séparés au niveau formules.

## GO_PROMPT — Ajouter l’objectif final au child

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /opt/trading
git fetch origin

git checkout sot/mainline
git pull --rebase origin sot/mainline

git checkout -b go/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

mkdir -p docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01

cat > docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md <<'EOF'
---
doc_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01_FORMULAS_COMPAT_REVIEW
doc_type: formulas_compat_review
repo: opt-trading
project: opt-trading
module: trading
go_id: GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01
status: draft
lifecycle_stage: child_opening_review
topic_keys:
  - opt-trading
  - trading
  - bitcoin
  - gold
  - btc
  - bitget
  - coin-futures
  - xauusd
  - formulas
  - compatibility
  - no-duplicate-coding
surface: trading
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
point_de_reprise: "Review formules Bitget et compatibilité avec modules existants avant backtest data prep. Objectif final global : stratégie robuste accumulation Bitcoin + Gold."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/01_initial_project_doc.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/02_variables_bounds.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/03_worker_spec.md
  - docs/chantiers/GO_OPT_TRADING_TRADING_PARENT_BTC_COINM_ACCUMULATION_ENGINE_01/04_math_formulas.md
  - modules/trading_lab_v1/docs/ETABLI.txt
  - modules/desk_pro_runner/app/desk_pro_runner.py
  - modules/probability_engine/app/probability_engine.py
  - docs/ui_indexation/01_ui_registry_modules.md
---

# 01_formulas_compat_review

## 1_MASTER_TARGET

Figer les formules Bitget BTC COIN-FUTURES et leur compatibilité avec l’existant sans double codage, sans nouveau module, sans nouveau backtest et sans nouvelle UI.

Objectif final global du programme :

```text
stratégie robuste d’accumulation Bitcoin + Gold
```

## 6_FINAL_TARGET

Le chantier courant vise seulement la compatibilité des formules BTC COIN-M.

Le programme final vise une stratégie robuste multi-actifs :

```text
Bitcoin :
- accumulation BTC long terme
- short COIN-M comme moteur de profit sur baisse sans vendre le BTC accumulé
- DCA + renfort de marge selon règles mathématiques

Gold :
- accumulation / exposition robuste sur l’or
- rattachement prioritaire à l’existant XAUUSD / Trading Dual Stack / Trading Lab
- aucun nouveau module isolé sans preuve de nécessité
```

## 12_INVARIANTS

```text
- ne pas créer de nouveau module si une surface existante peut être adaptée
- ne pas créer de nouvelle UI
- ne pas créer de second backtest engine
- ne pas créer de second probability/risk engine
- pas de connexion exchange
- pas d’exécution live
- pas de backtest réel
- documentation + contrats uniquement
- objectif final global = stratégie robuste accumulation Bitcoin + Gold
- BTC et Gold partagent une direction produit, mais gardent des formules séparées
```

## 15_REMAINING_GAP

```text
- qty_to_notional_fn Bitget
- notional_to_qty_fn Bitget
- PnL inverse COIN-M
- liquidation / maintenance cross margin
- funding historique requis avant backtest
- mapping final vers trading_lab_v1 / desk_pro / probability_engine / risk_engine
- cadrage Gold/XAUUSD futur à ouvrir séparément après verrouillage BTC
```

## 16_TODO

```text
1. Compléter l’inventaire existant.
2. Définir le mapping besoin -> module existant.
3. Définir les fonctions mathématiques BTC à figer.
4. Définir les contrats JSON.
5. Lister explicitement les interdits de duplication.
6. Statuer l’intégration future Gold/XAUUSD sans l’implémenter ici.
7. Produire verdict PASS/PATCH_REQUIRED/FAIL.
```

## 17_RESUME_POINT

Child ouvert pour review de compatibilité formules.

Objectif final statué :

```text
stratégie robuste d’accumulation Bitcoin + Gold
```

Ne pas ouvrir BACKTEST_DATA_PREP tant que ce review n’est pas PASS.
EOF

git add docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/01_formulas_compat_review.md
git commit -m "docs: open BTC COIN-M formulas compatibility review"

git status --short --branch --untracked-files=no
git diff --stat origin/sot/mainline...HEAD
```

## 17_RESUME_POINT

```text
Plan validé.
Objectif final à statuer dans le child :
stratégie robuste accumulation Bitcoin + Gold.
Le child reste BTC formulas compat review.
Gold/XAUUSD est reconnu comme cible finale produit, mais non implémenté dans ce child.
```

---

# PLAN PRÉCIS VALIDÉ

## 6_FINAL_TARGET

Objectif final global :

```text
STRATEGIE_ROBUSTE_ACCUMULATION_BITCOIN_GOLD
```

Traduction produit :

```text
Bitcoin : accumulation BTC long terme, Bitget COIN-FUTURES, short comme moteur de profit sur baisse sans vente du BTC spot.
Gold : accumulation / exposition robuste XAUUSD, via surfaces Trading Dual Stack / Trading Lab / Desk Pro existantes.
```

## 8_VALIDATED_PLAN

1. `00_INITIAL_PROJECT_DOC.md` — présent document, validation du plan et copie intégrale des deux réponses.
2. `01_formulas_compat_review.md` — review formules BTC Bitget + compatibilité modules existants.
3. `GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_BACKTEST_DATA_PREP_01` — seulement après PASS du child FORMULAS_COMPAT_REVIEW complet.
4. `GO_OPT_TRADING_TRADING_CHILD_GOLD_XAUUSD_ACCUMULATION_COMPAT_REVIEW_01` — cadrage Gold séparé, sans double architecture.
5. `GO_OPT_TRADING_TRADING_CHILD_BTC_GOLD_STRATEGY_UNIFICATION_REVIEW_01` — uniquement après BTC + Gold cadrés.

## 10_SELECTED_SETUP — Réutilisation obligatoire

| Besoin | Surface existante à privilégier | Interdit |
|---|---|---|
| Backtest futur | `modules/trading_lab_v1` | créer un second backtest engine |
| UI / opérateur | `desk_pro_runner`, `desk_pro_dashboard`, `ops_menu_hub` | créer nouvelle UI |
| Score / analyse | `probability_engine` | créer second moteur de probabilité |
| Risque | `risk_engine` si compatible | dupliquer liquidation/risk logic |
| Dashboard | `desk_pro_dashboard` | interface séparée |
| Menu | `ops_menu_hub` | menu isolé |
| Gold/XAUUSD | Trading Dual Stack / Trading Lab | architecture parallèle |

## 12_INVARIANTS

```text
- objectif final = stratégie robuste accumulation Bitcoin + Gold
- BTC et Gold partagent une direction produit, mais pas forcément les mêmes formules
- BTC COIN-M reste un chantier spécialisé
- Gold/XAUUSD sera cadré séparément
- pas de double codage
- pas de double module
- pas de double UI
- pas de second backtest engine
- pas de second probability engine
- pas de worker runtime avant validation formules
- pas de backtest avant data prep
- pas de live / ordre réel
```

## 15_REMAINING_GAP

```text
- valider ce document initial
- ouvrir FORMULAS_COMPAT_REVIEW
- figer les formules Bitget
- préparer BACKTEST_DATA_PREP ensuite
- cadrer Gold/XAUUSD séparément
- unifier BTC + Gold seulement après preuves
```

## 16_TODO

```text
1. Commit + push du présent document.
2. Validation utilisateur.
3. Ensuite seulement créer 01_formulas_compat_review.md.
4. Après PASS du child FORMULAS_COMPAT_REVIEW complet, ouvrir backtest data prep.
5. Gold/XAUUSD : child séparé, non inclus dans les formules BTC.
```

## GAP_INDEXATION

Ce lot ouvre un child documentaire sur branche dédiée. Les index globaux (`GO_INDEX`, `ACTIVE_STREAMS`, `REPRISE`, `BRANCH_STATE`) ne sont pas modifiés dans ce commit initial afin d'éviter un élargissement prématuré. La trace canonique de reprise est locale dans :

```text
docs/chantiers/GO_OPT_TRADING_TRADING_CHILD_BTC_COINM_FORMULAS_COMPAT_REVIEW_01/00_INITIAL_PROJECT_DOC.md
```

Indexation globale à traiter seulement si le child devient actif après validation.

## 17_RESUME_POINT

```text
PR #235 mergée.
Parent BTC COIN-M présent sur sot/mainline.
Child FORMULAS_COMPAT_REVIEW ouvert en plan initial.
Objectif final global statué : stratégie robuste accumulation Bitcoin + Gold.
Aucun sous-chantier opérationnel lancé.
Prochaine action : validation utilisateur du présent document, puis ouverture 01_formulas_compat_review.md.
```

## RISKS

- À qualifier.
