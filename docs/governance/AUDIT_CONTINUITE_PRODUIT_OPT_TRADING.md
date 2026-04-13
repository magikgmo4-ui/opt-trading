# AUDIT CONTINUITE PRODUIT — OPT-TRADING

## 1. COUCHE 0 — SOCLE TRANSVERSE

| Element | Role | Pourquoi au socle transverse | Etat |
|---|---|---|---|
| Methode uniforme + couche humaine | gouvernance / continuite | fixe comment conserver et transmettre l'etat, la trajectoire produit et la reprise | ETABLI |
| memory_bricks | compaction derivee | fixe comment compacter sans remplacer la doc longue ni creer une memoire concurrente | ETABLI |

### Methode uniforme + couche humaine
- besoin initial : eviter qu'une continuite correcte garde l'etat technique mais perde plan valide, but final et logique humaine
- objectif vise : une continuite capable de transmettre etat + trajectoire produit + reprise utile
- preuves : `docs/chantiers/GO_OPT_TRADING_JOURNAL_FULL_READING_03/00_cadrage.md`, `docs/governance/HUMAN_FOUNDATIONS_CONTINUITY.md`, `docs/governance/HUMAN_CONTINUITY_METHOD.md`, `journal.md` notes `note5001`, `note5010`, `note5011`
- etat : gouvernance, couche humaine, lecture journal et hierarchie de reprise posees
- gap : application encore incomplete projet par projet

### memory_bricks
- besoin initial : compacter sans perdre contexte ni creer memoire concurrente
- objectif vise : compaction derivee, tracable, utile a la reprise, fondee sur docs stabilisees
- preuves : `docs/governance/MEMORY_BRICKS_MAPPING.md`, `docs/governance/REPO_ROLE.md`, `docs/chantiers/GO_OPT_TRADING_CHANTIER_PILOTE_MEMORY_BRICKS_01/90_closeout.md`
- etat : role canonique et pilote documentaire PASS etablis
- gap : derivation reguliere depuis trajectoires produit stabilisees encore non systematique

## 2. ANNEAU A — PRODUITS PRIORITAIRES

| Projet | Besoin initial | Objectif final vise | Etat obtenu | Gap principal | Prochain GO |
|---|---|---|---|---|---|
| Desk Pro | depasser UI/modules isoles et obtenir un cockpit operateur exploitable | cockpit paper trading multi-machine, pilote sur `admin-trading`, exporte vers `/shared`, consultable sur `student`, preparant l'ingestion future `db-layer` | runbooks, hierarchie operateur, flux run/export et contrat multi-machine etablis | vision finale unifiee encore eclatee ; ingestion reelle cote `db-layer` non faite | synthese canonique Desk Pro ou lot ingestion future `/shared` |
| Trading Dual Stack V1 | eviter lab d'un cote et live de l'autre | framework trading unique avec meme noyau LAB/REALTIME, trader discipline, validation avant autonomie, journalisation exploitable | schemas, config V1, chaine LAB, comparator, chaine REALTIME minimale et closeout canonique etablis | V1 close mais bornee, sans broker, sans ordre reel, sans auto-trading | uniquement si besoin reel, depuis `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01` |
| Bot Vision | transformer des captures en analyse exploitable sans workflow fragile ni dependance trop forte a une plateforme | un pipeline vision cross-platform ou un provider headless browser unifie `bot_vision` entre Windows et Linux sans dependre de ShareX, afin de produire des artefacts Desk Pro exploitables | modules presents, contrat input/output de base repo-source, chaine partielle mais reelle | cible cross-platform finale non materialisee comme spec canonique retrouvee | clarifier repo-source la cible produit finale Bot Vision et mesurer l'ecart exact |

### Desk Pro
- besoin initial : depasser UI/modules isoles ; obtenir un cockpit operateur reellement exploitable
- objectif final vise : cockpit paper trading multi-machine, pilote sur `admin-trading`, exporte vers `/shared`, consultable sur `student`, preparant ingestion future `db-layer`
- plan valide : hierarchie canonique des surfaces ; runs logges/rejouables ; dashboard + journal + export ; partage `/shared` ; distribution des usages par machine
- etat obtenu : entree operateur canonique ; flux run/export repo-source ; contrat de consultation multi-machine ; procedure release/tag
- preuves : `docs/admin_trading_desk_pro_runbook.md`, `docs/student_desk_pro_runbook.md`, `docs/db_layer_desk_pro_runbook.md`, `docs/desk_pro_release_ops_runbook.md`
- gap : vision finale unifiee encore eclatee entre runbooks, modules et journal ; ingestion reelle cote `db-layer` non faite
- prochain GO : synthese canonique Desk Pro ou lot ingestion future `/shared`

### Trading Dual Stack V1
- besoin initial : eviter lab d'un cote et live de l'autre
- objectif final vise : framework trading unique, LAB et REALTIME avec meme noyau, trader discipline, validation avant autonomie, journalisation exploitable
- plan valide : LAB + REAL-TIME ; noyau commun `frame / strategy / execution / analytics` ; V1 etroite `XAUUSD` / `America/Montreal` / `18:00` / `00:00` ; REALTIME borne a observation puis validation ; full auto hors perimetre
- etat obtenu : schemas, config V1, chaine LAB, comparator, chaine REALTIME minimale ; REALTIME V1 close repo/canonique
- preuves : `docs/ot/trading/00_TRADING_DUAL_STACK_LAB_REALTIME_V1.md`, `docs/ot/trading/02_TRADING_DUAL_STACK_CORE_SPEC_V1.md`, `docs/ot/trading/INDEX.md`, `docs/ot/trading/21_TRADING_REALTIME_V1_CLOSEOUT_01.md`
- gap : V1 close mais bornee ; sans broker ; sans ordre reel ; sans auto-trading
- prochain GO : uniquement si besoin reel, depuis `GO_OT_TRADING_REALTIME_V1_CHAIN_CLOSED_01`

### Bot Vision
- besoin initial : transformer des captures en analyse exploitable ; eviter un workflow fragile et trop dependant d'une plateforme
- objectif final vise : un pipeline vision cross-platform ou un provider headless browser unifie `bot_vision` entre Windows et Linux sans dependre de ShareX, afin de produire des artefacts Desk Pro exploitables
- plan valide : `vision_bot` = reception / traitement de captures ; `bot_vision_step2` = interaction Telegram + `/analyze` + artefacts Desk Pro ; direction de maturite = sortir d'une dependance forte a ShareX / Windows-only et stabiliser une chaine vision unifiee
- etat obtenu : modules existants ; contrat input/output de base repo-source ; chaine partielle mais reelle
- preuves : `modules/vision_bot/README.md`, `modules/bot_vision_step2/README.md`
- gap restant : ETABLI : le pipeline actuel Bot Vision existe et repose encore sur Windows / ShareX / SFTP cote capture ; A REVALIDER : la cible finale headless browser cross-platform n'est pas encore retrouvee comme spec canonique explicite figee dans le repo
- prochain GO : clarifier repo-source la cible produit finale Bot Vision ; mesurer l'ecart exact entre pipeline actuel et pipeline cross-platform vise

## 3. ANNEAU B — REGISTRE COURT DES PROJETS STRUCTURANTS

| Projet | Statut | Pourquoi il reste dans la continuite | Pourquoi il n'est pas prioritaire ici | Point de reprise minimal |
|---|---|---|---|---|
| webhook | ETABLI | point d'entree runtime central de la chaine signaux | mieux lu comme brique structurante au service de la trajectoire produit globale | recroiser runtime signaux avec Desk Pro / trading |
| perf | ETABLI | couche monitor-only claire, utile a la discipline trading et au desk | partiellement absorbe par Desk Pro | etat `/perf` + recroisement avec flux Desk |
| quant | ETABLI | fondation historique de la logique recherche avant execution | moins central aujourd'hui que Desk Pro / trading dual stack | journal canon fevrier + lot lecture journal |
| LocalCMS | ETABLI | vrai produit consumer structure, utile a la continuite inter-repos | hors centre du repo canonique `opt-trading` dans cette passe | role consumer + continuite locale `localcms` |
| Student | ETABLI | role machine durable de consultation et reprise | traite ici comme satellite machine de Desk Pro | `docs/student_desk_pro_runbook.md` |
| db-layer | PARTIEL | role machine durable et futur aval d'ingestion | satellite machine de Desk Pro, produit futur incomplet | `docs/db_layer_desk_pro_runbook.md` |
| collector family | ETABLI | vraie famille transverse avec doctrine claire | moins prioritaire que les 3 centres produit retenus | `GO_COLLECTORS_MIGRATION_MAP_01` |
| Trae / agents / prompt factory / registry | ETABLI | programme transverse reel de structuration/documentation | en arriere-plan par rapport aux produits prioritaires de cette passe | `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md` |
| surface operateur | ETABLI | couche transverse utile pour usage reel et reprise | sous-jacente a Desk Pro plutot que produit autonome prioritaire | `menu-ops_menu_hub` + runbooks machine |
| openclaw | A REVALIDER | role repo transverse important ; cockpit operateur local repo-prouve ; policy provider/modele prouvee | produit OpenClaw global complet encore non verrouille | `modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md`, `modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md`, `modules/model_provider_openclaw/README.md` |
| llm_wiki_minimal | PARTIEL | sas de pre-consolidation explicitement etabli | role surtout transverse, pas produit fort d'`opt-trading` | `docs/governance/REPO_ROLE.md` |
| hf_trading | PARTIEL | repo conforme utile pour extension future | bootstrap trop leger pour peser dans l'anneau A | bootstrap conforme, pas de lot metier etabli |
| Antigravity | PARTIEL | chantier specialise reel, historiquement utile | peripherique au centre de gravite produit actuel | relecture dediee des closings/notes Antigravity |

## 4. CONCLUSION OPERATOIRE

- cadre clarifie en 3 niveaux :
  - Couche 0 — Socle transverse
  - Anneau A — Produits prioritaires
  - Anneau B — Registre court
- ce decoupage repond mieux au probleme de continuite produit
- suite la plus utile :
  1. figer une synthese produit canonique pour Desk Pro
  2. figer une synthese produit canonique pour Trading Dual Stack V1
  3. clarifier repo-source la cible produit finale de Bot Vision
  4. deriver ensuite seulement les memory_bricks depuis ces syntheses stabilisees
