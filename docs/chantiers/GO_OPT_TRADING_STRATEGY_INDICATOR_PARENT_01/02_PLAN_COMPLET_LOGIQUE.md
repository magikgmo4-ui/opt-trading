---
doc_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01_PLAN_COMPLET_LOGIQUE
doc_type: chantier_logical_plan
repo: opt-trading
project: opt-trading
module: strategy_indicator
go_id: GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
status: draft
lifecycle_stage: planning
topic_keys:
  - opt-trading
  - strategy_indicator
  - macro_indicator
  - oil_macro
  - plan
surface: chantier
source_kind: canonical
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
point_de_reprise: "Section 17_RESUME_POINT"
updated_at: 2026-04-30
links:
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/01_MASTER_PLAN.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/01_SPEC.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/02_RULES.md
  - docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/REPRISE.md
---

# PLAN COMPLET LOGIQUE — Strategy / Indicator Parent

## 1_MASTER_TARGET

Construire une couche durable d'indicateurs de contexte trading pour `opt-trading`, capable de qualifier les regimes de marche avant toute decision tactique.

Le premier indicateur traite dans ce parent est le signal macro oil.

## 2_INITIAL_PROJECT_DOC

Document initial parent :

`docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/00_CADRAGE.md`

Ce document fixe :
- le parent strategy / indicator ;
- le premier child oil macro ;
- la phase initiale documentaire ;
- l'invariant : aucun runtime modifie dans l'ouverture.

## 3_INITIAL_NEED

Creer un chantier parent strategie / indicateur, puis ouvrir le premier sous-chantier sur l'indicateur oil macro afin de transformer les signaux petroliers en filtre de contexte exploitable pour crypto / desk / probabilities / OpenClaw.

## 4_MASTER_PROJECT_PLAN

### Direction generale

Les indicateurs ne doivent pas devenir des ordres automatiques. Ils doivent servir a qualifier le regime de marche :

- `risk-on supportive` ;
- `neutral range` ;
- `risk-off pressure` ;
- `event spike unstable`.

### Axes majeurs

1. `INDICATOR_CANON` : definir la place canonique des indicateurs dans la gouvernance trading.
2. `OIL_MACRO` : formaliser le premier indicateur oil macro.
3. `DATA_SCHEMA` : definir un format machine-readable minimal.
4. `BACKTEST_LITE` : tester manuellement ou semi-automatiquement les seuils sur cas historiques.
5. `INTEGRATION` : connecter plus tard vers desk / probabilities / OpenClaw sans casser les modules existants.

## 5_GO_PLAN

### Parent ouvert

`GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01`

Role : gouvernance locale et consolidation strategy / indicator.

### Child initial ouvert

`GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01`

Role : cadrage, specification et ruleset initial de l'indicateur oil macro.

### Next GO candidat

`GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_SCHEMA_02`

Role attendu : quantifier les seuils et definir l'output machine-readable.

## 6_FINAL_TARGET

Etat cible du parent avant fermeture :

- parent documente ;
- child oil macro documente ;
- regles V1 posees ;
- gaps explicites ;
- point de reprise stable ;
- aucune ambiguite entre hypothese, etabli et TODO ;
- aucune modification runtime implicite.

## 7_CANONICAL_STATE

Etat valide a la creation de ce document :

- branche dediee : `go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` ;
- parent docs cree ;
- child oil macro cree ;
- inbox atomique creee ;
- aucun code runtime modifie ;
- phase actuelle : cadrage / planification documentaire.

## 8_VALIDATED_PLAN

### Phase A — Stabilisation documentaire actuelle

1. Verifier la branche et le diff reel.
2. Corriger les frontmatters accidentels si presents.
3. Rebaser localement sur `origin/sot/mainline` avant PR / merge.
4. Conserver le parent en `KEEP_ACTIVE` jusqu'a closeout.

### Phase B — Specification oil macro

1. Verrouiller les inputs minimaux : WTI, Brent, DXY, BTC, SPX.
2. Definir les seuils daily / 3d / 5d.
3. Definir les classes de sortie.
4. Ajouter les cas d'invalidation : news spike, donnees manquantes, DXY contradictoire.

### Phase C — Schema machine-readable

1. Creer un schema JSON minimal.
2. Definir les champs : `indicator_id`, `timestamp`, `source`, `oil_move_1d`, `oil_move_3d`, `dxy_context`, `regime`, `confidence`, `notes`.
3. Garder le schema sans execution automatique.

### Phase D — Backtest lite / validation

1. Selectionner 10 a 30 cas historiques.
2. Classer les regimes oil.
3. Comparer reaction BTC / SPX / DXY.
4. Documenter les faux positifs.
5. Ajuster les seuils sans sur-optimisation.

### Phase E — Integration future

1. `desk` : affichage du regime courant.
2. `probabilities` : filtre de pondération du biais risk-on / risk-off.
3. `OpenClaw` : contexte d'ingestion, pas droit d'execution autonome.
4. `logging` : journaliser signal + reaction marche.

## 9_SELECTED_SOLUTION

Approche retenue : couche indicateur documentaire puis schema, avant toute integration runtime.

Raison : eviter d'introduire un signal macro mal calibre dans les surfaces de trading existantes.

## 10_SELECTED_SETUP

Structure canonique retenue :

```text
docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01/
  00_CADRAGE.md
  01_MASTER_PLAN.md
  02_PLAN_COMPLET_LOGIQUE.md
  BRANCH_STATE.md

docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01/
  00_CADRAGE.md
  01_SPEC.md
  02_RULES.md
  03_TODO.md
  REPRISE.md

docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md
```

## 11_KEY_DECISIONS

- Oil est un indicateur de contexte, pas un signal d'entree autonome.
- Le parent strategy / indicator est la surface de consolidation.
- Le child oil macro est le premier chantier concret.
- Le prochain travail doit porter sur schema + seuils, pas sur runtime.
- Toute integration desk / probabilities / OpenClaw demande un GO distinct.

## 12_INVARIANTS

- Pas d'autotrading base uniquement sur oil.
- Pas de refonte globale.
- Pas de modification runtime pendant le cadrage.
- Pas de signal sans source et timestamp.
- Pas de conclusion forte si DXY / BTC / SPX contredisent le regime oil.
- Les hypotheses restent distinctes des etablis.

## 13_ESTABLISHED

- Le parent est ouvert.
- Le child oil macro est ouvert.
- Les fichiers de cadrage / spec / rules / todo / reprise existent.
- Le signal oil est classe comme filtre macro.
- Le chantier est documentaire a ce stade.

## 14_HYPOTHESIS

- Une hausse rapide oil + DXY fort peut signaler un regime defavorable crypto.
- Une baisse oil + DXY faible peut soutenir un regime risk-on.
- Les seuils 1d / 3d / 5d suffiront peut-etre pour une V1 simple.
- Une fenetre de cooldown apres spike news est probablement necessaire.

## 15_REMAINING_GAP

- Branche a realigner sur `origin/sot/mainline` avant PR / merge.
- Deux frontmatters signales precedemment peuvent contenir un espace initial devant `doc_type`.
- Seuils quantitatifs non valides.
- Sources de donnees non choisies.
- Schema machine-readable non cree.
- Backtest lite non execute.
- Integration runtime non ouverte.

## 16_TODO

### TODO immediate a la reprise

1. Fetch + checkout de la branche.
2. Rebase sur `origin/sot/mainline`.
3. Corriger les frontmatters si necessaire.
4. Verifier le diff.
5. Ajouter eventuellement un closeout de phase documentaire.

### TODO fonctionnel prochain GO

1. Ouvrir `GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_SCHEMA_02`.
2. Definir le schema JSON.
3. Choisir les seuils V1.
4. Tester manuellement quelques cas.
5. Documenter PASS / FAIL.

## 17_RESUME_POINT

Reprise operationnelle :

```bash
git fetch --all --prune
git checkout go/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01
git rebase origin/sot/mainline
grep -R " doc_type:" docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01 docs/chantiers/GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01 docs/index/inbox/GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01.md
```

Puis :

- corriger ` doc_type:` en `doc_type:` si present ;
- relire `02_PLAN_COMPLET_LOGIQUE.md` ;
- repartir sur `GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_SCHEMA_02`.

## 18_TO_DOCUMENT

- `OIL_MACRO_SCHEMA_V1`
- `OIL_MACRO_THRESHOLDS_V1`
- `OIL_MACRO_BACKTEST_LITE_01`
- `STRATEGY_INDICATOR_PARENT_CLOSEOUT_01`

## 19_TO_REMEMBER

- `GO_OPT_TRADING_STRATEGY_INDICATOR_PARENT_01` = parent strategy / indicator.
- `GO_OPT_TRADING_STRATEGY_INDICATOR_OIL_MACRO_01` = premier child.
- Oil = filtre de contexte macro, pas signal d'execution.
- Prochain GO logique = schema + seuils, pas runtime.
