---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01_CHILD_GO_OPERATING_PLAN
doc_type: operating_plan
repo: opt-trading
go_id: GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
status: active
surface: chantier
source_kind: canonical
updated_at: 2026-05-05
---

# 55_CHILD_GO_OPERATING_PLAN - admin-trading

## 1_MASTER_TARGET

Documenter le plan operatoire complet des child GO `admin-trading` dans un ordre strict, afin de valider d'abord les contrats producer/consumer `signal_event`, `visual_context` et `desk_snapshot` avant toute revue finale Desk Pro ou integration reelle.

## 2_INITIAL_PROJECT_DOC

References utilisees pour ce plan :

- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/05_VALIDATED_OPERATING_PLAN.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/50_NEXT_GO_DECISION.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/90_CLOSEOUT.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/20_RUNTIME_SERVICES_AND_PORTS.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/30_TRADING_SURFACE_MAP.md`
- `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/40_DEPENDENCIES_AND_GAPS.md`

## 3_INITIAL_NEED

Le parent review est clos en PASS, mais aucun child GO ne doit s'ouvrir avant qu'un plan documentaire explicite fixe l'ordre, les dependances et les criteres PASS/FAIL du sequenceur runtime `admin-trading`.

## 4_MASTER_PROJECT_PLAN

Le plan global retenu contient 4 child GO, dans cet ordre strict :

1. `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01`
2. `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01`
3. `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`
4. `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01`

Regle globale : chaque child GO doit fermer en PASS ou FAIL avant ouverture du suivant.

## 5_GO_PLAN

### GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01

- GO ID: `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01`
- Role: review du producer runtime `Webhook / TradingView` pour le contrat `signal_event`
- But: verifier la surface `tv-webhook`, l'ingress `TradingView -> webhook`, les points de persistance et la forme attendue de `signal_event` sans declencher de webhook reel
- Inputs: etat parent review PASS, `tv-webhook.service`, `ngrok-tv.service`, cartographie webhook deja etablie, ports 8000/4040, flux documente `TradingView -> POST /tv -> state/events.jsonl`
- Outputs: cartographie webhook runtime, contrat documentaire initial `signal_event`, frontiere producer/consumer pour le diagnostic suivant et pour Desk Pro
- Criteres PASS: la surface runtime webhook est observable sans mutation; le flux d'entree, la persistance, les champs minimaux et les marqueurs de fraicheur de `signal_event` sont documentables; aucun blocage critique n'empeche un consumer downstream de s'aligner
- Criteres FAIL: la surface webhook ne peut pas etre etablie de facon fiable; la persistance normalisee du signal reste contradictoire; le contrat minimal `signal_event` ne peut pas etre formule sans speculation
- Dependances producer/consumer: consomme un alert payload TradingView; produit un contrat `signal_event` pour `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` puis pour `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01`
- Fichiers attendus: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01/00_START.md`, `10_RUNTIME_STATE.md`, `20_SIGNAL_EVENT_CONTRACT.md`, `30_DEPENDENCIES_AND_GAPS.md`, `90_CLOSEOUT.md`
- Point de reprise: si PASS, ouvrir `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01`; si FAIL, stopper la sequence et ouvrir un GO de remediation separe seulement apres closeout

### GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01

- GO ID: `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01`
- Role: diagnostic du producer `signal_event` et validation du contrat consomme downstream
- But: verifier la forme interne, les champs fonctionnels, les erreurs attendues et la compatibilite consumer de `signal_event` sans mutation runtime
- Inputs: closeout PASS du runtime review webhook, trace documentaire du flux `POST /tv`, points de persistance evenementielle, etat perf/router/risk deja references par le parent review
- Outputs: schema documentaire `signal_event`, liste de mismatches eventuels, verdict de compatibilite producer/consumer pour Desk Pro et pour de futurs GO d'integration
- Criteres PASS: les champs fonctionnels, timestamps, symboles, moteur, direction, risque et regles de fraicheur de `signal_event` sont explicitement documentes; les consommateurs attendus peuvent etre relies a ce contrat sans ambiguite bloquante
- Criteres FAIL: schema de signal ambigu, incomplet ou contradictoire; absence de regle de fraicheur; incompatibilite bloquante entre la production webhook et la consommation downstream
- Dependances producer/consumer: depend obligatoirement de `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01`; consomme le contrat `signal_event` brut issu du webhook; produit un contrat `signal_event` valide pour la suite de sequence
- Fichiers attendus: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01/00_START.md`, `10_EVENT_PATH.md`, `20_SIGNAL_EVENT_SCHEMA.md`, `30_FAILURE_MODES.md`, `90_CLOSEOUT.md`
- Point de reprise: si PASS, ouvrir `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`; si FAIL, stopper la sequence et renvoyer vers un GO de remediation cible

### GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01

- GO ID: `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`
- Role: review du producer `Bot Vision Headless` et de la compatibilite artifact vers l'adapter `Desk Bridge`
- But: documenter le contrat `visual_context`, les artefacts de capture headless, la compatibilite `desk_bridge`, et les conditions de production de `desk_snapshot` sans restaurer ni committer le repertoire mis en quarantaine
- Inputs: etat parent review PASS, `bot-vision-headless-capture.timer`, cartographie `vision_inbox -> vision_processed -> desk_bridge`, statut `desk_bridge` RESOLVED, repertoire en quarantaine `/tmp/opt-trading-quarantine/headless_capture_20260505_171247/` explicitement hors commit
- Outputs: contrat documentaire `visual_context`, regles de nommage et de metadata artifact, frontiere `Desk Bridge -> desk_snapshot`, liste des bloqueurs restants pour la consommation Desk Pro
- Criteres PASS: le format `PNG + JSON metadata` de `visual_context` est etablissable; les regles de compatibilite artifact pour `desk_bridge` sont formulables; le passage de `visual_context` valide vers `desk_snapshot` est documente sans gap critique
- Criteres FAIL: le contrat artifact headless reste opaque; le schema `visual_context` ne peut pas etre formule; la compatibilite `Desk Bridge` vers `desk_snapshot` ne peut pas etre etablie proprement
- Dependances producer/consumer: respecte une regle de compatibilite artifact avant tout test ulterieur; produit `visual_context`; `Desk Bridge` adapte ce `visual_context` en `desk_snapshot`; le resultat sera consomme ensuite par Desk Pro
- Fichiers attendus: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01/00_START.md`, `10_CAPTURE_CHAIN.md`, `20_VISUAL_CONTEXT_CONTRACT.md`, `30_DESK_BRIDGE_COMPAT.md`, `90_CLOSEOUT.md`
- Point de reprise: si PASS, ouvrir `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01`; si FAIL, stopper la sequence et ouvrir un GO separe de remediation artifact ou bridge

### GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01

- GO ID: `GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01`
- Role: review du consumer final `Desk Pro` et synthese des contrats upstream
- But: verifier les attentes d'entree, la fraicheur, les frontieres de consommation et les sorties `Desk Pro` a partir de `signal_event`, `visual_context` et `desk_snapshot`, sans lancer d'integration reelle
- Inputs: closeouts PASS des 3 child GO precedents, etat parent review sur `/shared/desk_pro/latest/`, dernier run connu `2026-04-05`, modules et wrappers Desk Pro identifies dans la cartographie parent
- Outputs: contrat documentaire d'entree Desk Pro, verdict de fraicheur, liste des gaps restants, borne claire entre revue contractuelle et future integration reelle
- Criteres PASS: `Desk Pro` peut etre decrit comme consumer final de `signal_event + visual_context + desk_snapshot`; les contraintes de fraicheur et de donnees manquantes sont formulees; les suites reelles eventuelles sont explicitement sorties de ce GO
- Criteres FAIL: le contrat d'entree Desk Pro reste partiel; une incompatibilite bloquante subsiste entre les producteurs et le consumer; la fraicheur ou les artefacts requis ne peuvent pas etre relies de facon fiable
- Dependances producer/consumer: ne peut s'ouvrir qu'apres PASS de `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01`, `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_SIGNAL_DIAG_01` et `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01`; consomme `signal_event`, `visual_context` et `desk_snapshot`
- Fichiers attendus: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_DESK_PRO_RUNTIME_REVIEW_01/00_START.md`, `10_INPUT_CONTRACTS.md`, `20_FRESHNESS_AND_OUTPUTS.md`, `30_GAPS_AND_BLOCKERS.md`, `90_CLOSEOUT.md`
- Point de reprise: apres PASS ou FAIL, stopper la sequence; toute integration reelle, smoke global ou mutation runtime devra ouvrir un GO separe

### Matrice de compatibilite

| Surface | Role | Produit | Consomme | Format attendu | Consumer direct | Bloquant si absent |
| --- | --- | --- | --- | --- | --- | --- |
| Webhook / TradingView | Producer | `signal_event` | alert payload | JSON / event contract | Desk Pro / diagnostics | Oui |
| Bot Vision Headless | Producer | `visual_context` | chart/browser capture | PNG + JSON metadata | Desk Bridge / Desk Pro | Oui |
| Desk Bridge | Adapter | `desk_snapshot` | valid `visual_context` | JSON snapshot | Desk Pro | Oui |
| Desk Pro | Consumer | synthesis/report | `signal_event` + `visual_context` + `desk_snapshot` | latest/report contract | operator | Oui |

## 6_FINAL_TARGET

Etat final attendu apres cette sequence documentaire :

- `Webhook / TradingView` documente comme producer compatible de `signal_event`
- `Bot Vision Headless` documente comme producer compatible de `visual_context`
- `Desk Bridge` documente comme adapter/producteur compatible de `desk_snapshot`
- `Desk Pro` documente comme consumer final capable de synthetiser `signal_event + visual_context + desk_snapshot`
- aucune integration reelle, smoke global ou mutation runtime executee dans cette sequence

## 7_CANONICAL_STATE

Etat canonique retenu a l'ouverture de ce plan :

- `GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01` est clos PASS et le `HEAD` attendu est `9454396`
- la branche parent `admin-trading` a ete realignee sur `origin/sot/mainline`
- `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` est present et confirme le bloc `ADMIN_TRADING`
- `desk_bridge` est `RESOLVED`
- `GAP-01` et `GAP-03` sont `RESOLVED`
- les timers actifs documentes sont `trading-heartbeat`, `bot-vision-headless-capture` et `desk_bridge`
- `macro-xau` reste un failed non bloquant
- le worktree est propre et aucun child GO n'est ouvert
- `modules/bot_vision/headless_capture/` a ete sorti du worktree et mis en quarantaine sous `/tmp/opt-trading-quarantine/headless_capture_20260505_171247/`

## 8_VALIDATED_PLAN

Le plan valide pour la suite est le suivant :

1. Aucun child GO ne s'ouvre avant commit local de ce plan documentaire.
2. L'ordre strict est `WEBHOOK_RUNTIME_REVIEW` puis `WEBHOOK_SIGNAL_DIAG` puis `BOT_VISION_HEADLESS_PIPELINE_REVIEW` puis `DESK_PRO_RUNTIME_REVIEW`.
3. Chaque child GO doit fermer en PASS ou FAIL avant toute suite.
4. `WEBHOOK_SIGNAL_DIAG` depend de `WEBHOOK_RUNTIME_REVIEW`.
5. `BOT_VISION_HEADLESS_PIPELINE_REVIEW` depend d'une regle de compatibilite artifact entre capture headless, `visual_context` et `Desk Bridge`.
6. `DESK_PRO_RUNTIME_REVIEW` depend des contrats webhook, vision headless et `desk_bridge` deja documentes.
7. Toute integration reelle, smoke global, fix runtime ou relance service devra etre ouverte dans un GO separe apres ces reviews.
8. La priorite documentaire precedente `Desk Pro` en premier est remplacee ici par un enchainement contract-first, car le consumer final ne peut etre valide proprement sans contrats producer/consumer amont.

## 9_SELECTED_SOLUTION

Solution retenue : approche contract-first, producer/consumer.

- `Webhook / TradingView` est traite comme producer de `signal_event`
- `Bot Vision Headless` est traite comme producer de `visual_context`
- `Desk Bridge` est traite comme adapter qui transforme `visual_context` valide en `desk_snapshot`
- `Desk Pro` est retenu comme consumer final et surface de synthese, donc volontairement reporte a la fin de la sequence

## 10_SELECTED_SETUP

Setup retenu pour cette documentation :

- machine: `admin-trading`
- repo root: `/opt/trading`
- branche de travail: `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`
- base canonique reappliquee: `origin/sot/mainline`
- chantier parent: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/`
- fichier presentement cree: `docs/chantiers/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01/55_CHILD_GO_OPERATING_PLAN.md`
- repertoire hors scope Git: `/tmp/opt-trading-quarantine/headless_capture_20260505_171247/`

## 11_KEY_DECISIONS

- La branche parent reste l'unique surface de travail tant qu'aucun child GO n'est explicitement ouvert.
- Le sequenceur child GO passe en mode contract-first et ne suit plus la recommandation precedente `Desk Pro` en premier.
- `Desk Bridge` est traite comme adaptateur intermediaire, pas comme consumer terminal autonome.
- Le nom `GO_OPT_TRADING_ADMIN_TRADING_BOT_VISION_HEADLESS_PIPELINE_REVIEW_01` est retenu ici comme GO documentaire cible de sequence, sans ouvrir de branche ni restaurer le repertoire en quarantaine.
- Les sorties attendues de chaque child GO sont des contrats documentes et des verdicts PASS/FAIL, pas des mutations runtime.

## 12_INVARIANTS

Invariants a respecter pendant ce plan et pendant les child reviews qu'il ordonne :

- ne pas toucher au runtime
- ne pas start, stop, restart ou reload de service
- ne pas lire ni afficher `.env`
- ne pas declencher de webhook reel
- ne pas envoyer de Telegram
- ne pas ouvrir de child GO depuis ce document
- ne pas restaurer ni committer `modules/bot_vision/headless_capture/`
- ne pas perturber `cursor-ai`, `db-layer`, `student` ou `fantome`
- ne pas exposer de secret, token ou credential
- ne pas pousser sans ordre explicite

## 13_ESTABLISHED

Ce qui est confirme au moment de ce plan :

- branche active: `go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01`
- `HEAD` courant: `9454396 docs: update admin-trading parent review with current runtime state`
- split machine canonique present
- worktree clean
- runtime non modifie
- aucun child GO ouvert
- quarantaine etablie: `/tmp/opt-trading-quarantine/headless_capture_20260505_171247/`
- services critiques deja observes actifs: `tv-webhook`, `tv-perf`, `vision_bot`, `bot_vision_step2`, `ngrok-tv`
- `Desk Pro` a un dernier run connu en date du `2026-04-05`

## 14_HYPOTHESIS

Hypotheses a valider pendant les child GO, sans speculation hors preuve :

- le contrat `signal_event` peut etre formalise proprement a partir de la surface webhook et de sa persistance normalisee
- le contrat `visual_context` peut etre formalise a partir des artefacts headless attendus et de leurs metadata
- le contrat `desk_snapshot` peut etre formalise a partir de `Desk Bridge` et de la frontiere d'ingestion desk
- `Desk Pro` peut etre evalue comme consumer final seulement apres clarification amont des 3 contrats
- le gap de fraicheur Desk Pro restera probablement un point d'analyse meme si les contrats amont sont propres

## 15_REMAINING_GAP

Gaps restant a fermer par la sequence child GO :

- schema `signal_event`
- schema `visual_context`
- schema `desk_snapshot`
- input contract `Desk Pro`
- freshness `Desk Pro`

## 16_TODO

Prochaine action apres documentation et commit local de ce plan :

1. ouvrir `GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01`
2. ne pas ouvrir d'autre child GO avant closeout PASS ou FAIL du premier

## 17_RESUME_POINT

Point exact de reprise :

```text
GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
55_CHILD_GO_OPERATING_PLAN.md committe localement
Prochain child GO a ouvrir: GO_OPT_TRADING_ADMIN_TRADING_WEBHOOK_RUNTIME_REVIEW_01
```

Redemarrage operatoire :

```bash
cd /opt/trading
git fetch origin
git checkout go/GO_OPT_TRADING_ADMIN_TRADING_PARENT_REVIEW_01
git status --short --branch
git log --oneline -5
```

Si le commit local n'est pas encore pousse, attendre une instruction explicite de push avant toute publication distante.

## 18_TO_DOCUMENT

Blocs a reporter dans chaque child GO :

- contrat producer/consumer du GO courant
- inputs et outputs attendus
- criteres PASS et FAIL
- dependances avec le GO precedent et le suivant
- format attendu des artefacts ou evenements
- point de reprise exact et condition d'ouverture du GO suivant

## 19_TO_REMEMBER

Memory Bricks projet uniquement :

- sur `admin-trading`, la sequence child GO runtime doit suivre l'ordre `webhook runtime -> webhook signal diag -> bot vision headless pipeline -> desk pro runtime`
- `Desk Pro` ne doit pas etre valide avant documentation des contrats `signal_event`, `visual_context` et `desk_snapshot`
- toute integration reelle, smoke global ou mutation runtime doit sortir de cette sequence et ouvrir un GO dedie
