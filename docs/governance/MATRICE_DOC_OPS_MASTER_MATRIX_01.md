---
doc_id: OPT_TRADING_MATRICE_DOC_OPS_MASTER_MATRIX_01
doc_type: governance_master_matrix
repo: opt-trading
project: opt-trading
module:
go_id: GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01
status: reference
lifecycle_stage: governance
topic_keys:
  - opt-trading
  - matrice_doc_ops
  - governance
  - master_matrix
  - continuity
  - naming
  - frontmatter
  - git
surface: governance
source_kind: canonical
reference_canonique_principale: docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md
point_de_reprise: "Regle d'entree obligatoire - creation GO / chantier / target"
updated_at: 2026-05-23
links:
  - docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md
  - docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01_MASTER_PROJECT_PLAN_CREATION_RULE_01.md
  - docs/governance/PRODUCT_FINAL_SURFACE_REGISTRY_01.md
  - docs/governance/BUNDLE_TARGET_AND_MASTER_TARGET_METHOD_01.md
  - docs/governance/SESSION_PATCH_TRANSPORT_METHOD_01.md
  - docs/governance/MATRICE_GOUVERNANTE_V2.md
  - docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md
  - docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md
  - docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md
  - docs/governance/DOC_LAYERS.md
  - docs/governance/SESSION_DOCUMENTATION_GATE.md
  - docs/governance/REPO_ROLE.md
  - docs/governance/REPO_ROOT_POLICY.md
  - docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md
  - docs/architecture/REPO_SURFACES_MAP.md
  - docs/index/GO_INDEX.md
  - docs/index/REPRISE.md
  - docs/index/ACTIVE_STREAMS.md
  - docs/index/NEXT_GO_CANDIDATES.md
  - docs/index/BRANCH_STATE.md
  - docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/01_cadrage_parent.md
---

# MATRICE_DOC_OPS_MASTER_MATRIX_01

## Regle d'entree obligatoire - creation GO / chantier / target

Cette matrice est la source souveraine a relire avant toute ouverture de GO,
chantier, bundle, patch, zip, PR ou fermeture parent dans `opt-trading`.

Les extensions, bundles, target cards, patches et index detaillent ou transportent
la decision. Ils ne remplacent pas cette regle d'entree.

### Chaine canonique de lecture

```text
PF_*
-> 1_MASTER_TARGET
-> 4_MASTER_PROJECT_PLAN
-> GO_PARENT / parent de continuite
-> GO_CHILD / child / bundle
-> 6_FINAL_TARGET / BUNDLE_TARGET
-> NEXT_GO / CLOSE_GATE
```

### Creation minimale obligatoire

Tout nouveau GO ou chantier doit declarer, avant execution :

```yaml
GO_ID: <GO_...>
GO_STRUCTURAL_ROLE: GO_CHILD | GO_CHILD_ATTACHED_TO_PARENT | GO_PARENT | GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN | GO_MASTER_PROJECT_PLAN
PF_ID: <PF_* | null>
MASTER_TARGET_ID: <MT_* | MASTER_TARGET_* | null>
MASTER_PROJECT_PLAN_ID: <MPP_* | null>
PARENT_GO_ID: <GO_* | null>
NEXT_ATTACH_TARGET: <required if GO_CHILD or GO_PARENT is not attached>
6_FINAL_TARGET: <current phase target>
BUNDLE_TARGET: <target of the bundle, if transport/bundle is required>
TRANSPORT_MODE: none | patch_only | bundle_patch | bundle_patch_zip
CLOSE_GATE_MASTER_TARGET: pending | validated | not_applicable
```

### Alias documentaire initial

Dans les échanges conversationnels et les blocs de continuité, `2_INITIAL_PROJECT_DOC`
désigne le rôle logique du document initial transporteur du projet ou du plan.

Dans le repo, le fichier canonique correspondant est :

`00_INITIAL_PROJECT_DOC.md`

Règle d’équivalence :

`2_INITIAL_PROJECT_DOC = tag logique conversationnel`
`00_INITIAL_PROJECT_DOC.md = fichier canonique repo`

Le tag logique ne remplace jamais le fichier repo. Toute ouverture de chantier
doit matérialiser ou référencer le fichier canonique `00_INITIAL_PROJECT_DOC.md`
dans `docs/chantiers/<GO_ID>/` ou dans le bundle concerné si le transport est
déportable.


### Roles structurels canoniques

Les seuls `GO_STRUCTURAL_ROLE` autorises sont :

```text
GO_CHILD
GO_CHILD_ATTACHED_TO_PARENT
GO_PARENT
GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN
GO_MASTER_PROJECT_PLAN
```

`GO_ORPHAN` n'est pas un role canonique.

Un `GO_CHILD` non encore rattache doit avoir `NEXT_ATTACH_TARGET`.
Un `GO_PARENT` non encore rattache doit avoir `NEXT_ATTACH_TARGET`.

### Rattachement obligatoire

1. Un `GO_CHILD_ATTACHED_TO_PARENT` doit pointer vers `PARENT_GO_ID`.
2. Un `GO_PARENT_ATTACHED_TO_MASTER_PROJECT_PLAN` doit pointer vers `MASTER_PROJECT_PLAN_ID`.
3. Un `GO_MASTER_PROJECT_PLAN` doit pointer vers `PF_ID` et `1_MASTER_TARGET`.
4. Un support, tool, machine, transport ou autre surface non-produit ne flotte pas seul : il doit avoir un parent de continuite ou un rattachement explicite a un `4_MASTER_PROJECT_PLAN`.
5. Si le rattachement n'est pas encore prouve, `NEXT_ATTACH_TARGET` est obligatoire et le GO ne peut pas etre ferme comme livre.

### Target et transport

`6_FINAL_TARGET` decrit la cible de phase courante.

`BUNDLE_TARGET` decrit le livrable concret du bundle courant seulement si un
bundle, un patch, un zip, une execution IDE, une autre machine ou un depot manuel
est requis.

Le champ `TRANSPORT_MODE` gouverne les artefacts a produire :

| TRANSPORT_MODE | Usage | Artefacts attendus |
|---|---|---|
| `none` | modification directe deja gouvernee par le repo ou lecture seule | aucun artefact de transport obligatoire |
| `patch_only` | demande explicite de patch ou doc-only simple | `.patch` uniquement ; ne pas appliquer sans demande explicite |
| `bundle_patch` | bundle documente sans zip requis | `TARGETS.md`, `target_card.json`, `.patch` canonique |
| `bundle_patch_zip` | IDE, autre machine, depot manuel, operateur local ou execution deportee | bundle deportable, `.patch` canonique, `.zip` transportable |

### PATCH_DEFAULT_RULE

Quand l'utilisateur demande simplement `patch`, produire le `.patch` avant toute
application directe.

Par defaut, `patch` ne signifie pas : appliquer, commit, push, ouvrir PR,
modifier runtime ou fermer parent.

### Ouverture chantier et zip

Quand un plan est valide et qu'un chantier est ouvert, les artefacts de transport
dependent de `TRANSPORT_MODE`.

Si l'execution est deportee vers IDE, autre machine, depot manuel, operateur local
ou environnement non directement modifie par la session, le chantier doit prevoir :

```text
00_INITIAL_PROJECT_DOC
TARGETS.md
target_card.json
bundle deportable
.patch canonique
.zip transportable
```

Si le lot est doc-only direct GitHub ou lecture seule, le `.zip` n'est pas
obligatoire. Le `.patch` canonique peut suffire selon le scope.

### Fermeture et close gate

Un child, bundle, patch, commit ou PR ne ferme jamais un parent.

Un parent ne peut etre ferme que si :

```text
PF_* prouve utilisable
+ 1_MASTER_TARGET atteint
+ 4_MASTER_PROJECT_PLAN complete ou explicitement declasse
+ CLOSE_GATE_MASTER_TARGET valide
```

Sinon, produire `NEXT_GO` ou documenter `REMAINING_GAP`.

### Notes de precedence

Les formulations de type `PLAN_VALIDE_CHAIN` sont des supports operatoires
derives. Elles ne sont pas la source souveraine. En cas de divergence, cette
matrice maitre prime.

## Objet

Fixer la matrice maitre finale unique de gouvernance pour `opt-trading`.

Cette matrice devient la surface canonique souveraine pour relire ensemble :
- le role reel du repo
- la continuite produit
- les parents / sous-GO / GO simples
- les plans de travail rattaches aux GO
- le nommage
- le frontmatter
- le placement documentaire
- le support Git
- l'ouverture / fermeture / propagation

Elle fusionne le canon deja publie.
Elle ne lance pas encore le lot d'alignement / deduplication / reclassement des surfaces proches.

---

## Corpus canonique recroise

Le present document recroise explicitement :
- `docs/governance/MATRICE_DOC_OPS_MASTER_PLAN_01.md`
- `docs/governance/MATRICE_GOUVERNANTE_V2.md`
- `docs/governance/MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md`
- `docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md`
- `docs/governance/DOC_LAYERS.md`
- `docs/governance/SESSION_DOCUMENTATION_GATE.md`
- `docs/governance/REPO_ROLE.md`
- `docs/governance/REPO_ROOT_POLICY.md`
- `docs/governance/GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01.md`
- `docs/architecture/REPO_SURFACES_MAP.md`
- `docs/index/GO_INDEX.md`
- `docs/index/REPRISE.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/BRANCH_STATE.md`

Verification complementaire `docs/` effectuee sur les surfaces proches non souveraines :
- `docs/next/NEXT_GO_CANDIDATES.md`
- `docs/product_targets/*`
- `docs/ot/project_cards/*`
- `docs/status/*`
- `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md`

Regle de lecture :
- ces surfaces proches peuvent aider a la reprise ou a la qualification
- elles ne montent pas au-dessus du canon maitre fixe ici

---

## Partie 1 - Autorite / couches / hierarchie

### 1.1 Role du repo

`opt-trading` est le repo canonique principal du perimetre pour :
- l'execution reelle
- la structure durable des modules
- les wrappers operatoires
- les closeouts techniques lies a l'etat reel du repo
- la continuite locale
- la compaction derivee via `memory_bricks`

`opt-trading` n'est pas, a lui seul :
- la seule couche documentaire du systeme entier
- le repo maitre de gouvernance transverse inter-repos
- le repo consumer principal de lecture UI

### 1.2 Regle d'arbitrage

Ordre d'arbitrage retenu :
1. etat reel prouve du repo, du dossier, de la branche et des artefacts
2. presente matrice maitre
3. annexes canoniques stables
4. surfaces operatoires canoniques
5. dossiers chantier
6. derives / compaction / registry / supports extraits
7. archives et historiques

Effet :
- la realite prouvee arbitre les contradictions
- la matrice maitre gouverne la lecture documentaire
- les surfaces inferieures peuvent illustrer ou operer, pas gouverner a la place du maitre

### 1.3 Hierarchie canonique retenue

`canon maitre`
- `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`

`canon stable annexe`
- `MATRICE_GOUVERNANTE_V2`
- `MATRICE_GOUVERNANTE_METADATA_DERIVATION_01`
- `PRODUCT_CONTINUITY_HIERARCHY_01`
- `AUDIT_CONTINUITE_PRODUIT_OPT_TRADING`
- `DOC_LAYERS`
- `SESSION_DOCUMENTATION_GATE`
- `REPO_ROLE`
- `REPO_ROOT_POLICY`
- `GIT_BRANCH_HOUSEKEEPING_WORKFLOW_01`
- `REPO_SURFACES_MAP`

`operatoire canonique`
- `docs/index/GO_INDEX.md`
- `docs/index/NEXT_GO_CANDIDATES.md`
- `docs/index/ACTIVE_STREAMS.md`
- `docs/index/REPRISE.md`
- `docs/index/BRANCH_STATE.md` pour la seule surface branches

`chantier canonique`
- `docs/chantiers/<GO_...>/`

`derive / compaction / support`
- `memory_bricks`
- `search_tags`
- registry derive
- `docs/governance/HUMAN_*`

`archive / historique`
- `docs/ot/closings/*`
- `_archive/`

### 1.4 Articulation gouvernance / chantier / continuite / compaction / branche

- la gouvernance fixe les regles stables
- le chantier porte un lot borne et ses preuves locales
- la continuite expose l'etat courant et la suite naturelle
- la compaction derive de surfaces stabilisees et ne remplace ni le canon ni le chantier
- la branche est un support Git d'isolement et de revue, jamais la source de la trajectoire produit

### 1.5 Regles anti-concurrence

- `GO_INDEX.md` reste la verite canonique de liste
- `REPRISE.md` n'est pas une seconde verite de liste
- `BRANCH_STATE.md` ne gouverne que la surface branches
- aucun derive metadata, tag ou registry ne remplace un objet canonique
- aucun dossier chantier ne remplace une matrice de gouvernance
- aucune synthese laterale ne concurrence le present document

---

## Partie 2 - Continuite produit globale

### 2.1 Champs directeurs obligatoires

La lecture produit globale doit toujours pouvoir retrouver :
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`
- `plan_macro_valide`
- `jalons_clos`
- `etat_global_courant`
- `gap_global_restant`
- `suite_logique`

Regles :
- un GO local sert cette lecture ; il ne la remplace pas
- si un produit n'est pas centre de gravite, il se rattache a une famille de soutien ou a la couche methode / transmission
- un support Git n'est jamais un substitut a ces champs

### 2.2 Centres de gravite produit retenus

#### Desk Pro

- `produit_centre` : `Desk Pro`
- `famille_produit` : surface operateur / multi-machine / desk
- `intention_produit` : fournir un cockpit paper trading exploitable, multi-machine, relachable et gouverne
- `produit_final_voulu` : surface operateur coherente, avec entrypoints clairs, release stable, export `/shared`, consultation cross-machine et preparation d'une future ingestion `db-layer`
- `plan_macro_valide` : clarifier les entrypoints reels, stabiliser doctrine et wrappers, fiabiliser la release, prouver le flux `admin-trading -> /shared -> student/db-layer`, preparer l'aval d'ingestion
- `jalons_clos` : hierarchie operateur fixee ; references release consolidees ; contrat source minimal pour l'ingestion `db-layer` documente
- `etat_global_courant` : cockpit et runbooks existent ; la chaine source / export / consultation est lisible ; la gouvernance wrappers est posee
- `gap_global_restant` : la vision finale reste eclatee entre plusieurs surfaces ; l'ingestion reelle cote `db-layer` n'est pas encore faite
- `suite_logique` : produire une synthese produit canonique unifiee Desk Pro ou ouvrir un lot borne d'ingestion future si le besoin redevient actif

#### Trading Dual Stack V1

- `produit_centre` : `Trading Dual Stack V1`
- `famille_produit` : trading / dual-stack / realtime borne
- `intention_produit` : eviter deux chaines divergentes et garder un noyau commun LAB + REALTIME
- `produit_final_voulu` : framework trading unique, a validation disciplinee, avec journaux exploitables et noyau commun `frame / strategy / execution / analytics`
- `plan_macro_valide` : V1 etroite `XAUUSD` / `America/Montreal` / `18:00` / `00:00`, LAB + REALTIME borne a observation puis validation, full auto hors perimetre
- `jalons_clos` : schemas V1 ; chaine LAB ; comparator ; chaine REALTIME minimale ; closeout REALTIME V1
- `etat_global_courant` : V1 close et canonique, mais volontairement bornee
- `gap_global_restant` : pas de broker, pas d'ordre reel, pas d'autotrading, pas de nouvelle phase justifiee a ce stade
- `suite_logique` : ne rouvrir que depuis un besoin reel et un nouveau GO explicite, pas par inertie documentaire

#### Bot Vision

- `produit_centre` : `Bot Vision`
- `famille_produit` : vision / pipeline artefacts / desk support
- `intention_produit` : transformer des captures en artefacts exploitables sans dependance fragile a une seule plateforme
- `produit_final_voulu` : pipeline vision cross-platform ou un provider headless browser unifie `bot_vision` entre Windows et Linux et alimente des artefacts Desk Pro exploitables
- `plan_macro_valide` : `vision_bot` pour la reception / traitement ; `bot_vision_step2` pour interaction Telegram + `/analyze` + artefacts Desk Pro ; direction de maturite = sortir d'une dependance forte a ShareX / Windows-only
- `jalons_clos` : modules presents ; contrat input/output de base etabli ; chaine partielle mais reelle
- `etat_global_courant` : pipeline utilisable localement, mais la cible cross-platform finale n'est pas encore completement figee
- `gap_global_restant` : le plan final headless browser cross-platform reste a revalider repo-first
- `suite_logique` : clarifier la cible produit finale Bot Vision et mesurer l'ecart exact avec le pipeline actuel avant tout lot technique majeur

### 2.3 Regles de lecture produit

- produit d'abord
- parent ensuite
- GO local ensuite
- support Git ensuite seulement

Interdits :
- lire un GO technique comme finalite produit
- reconstruire le produit depuis une branche
- remplacer l'etat produit par un index operatoire

---

## Partie 3 - Produits / groupes / familles

### 3.1 Couche methode / transmission

La couche transverse de methode et de transmission reste visible comme socle :
- methode uniforme + couche humaine
- `SESSION_DOCUMENTATION_GATE`
- continuite locale `docs/index/*`
- compaction derivee `memory_bricks`

Cette couche garantit la transmission.
Elle ne devient pas a elle seule un produit final.

### 3.2 Centres de gravite produit

Les centres de gravite a garder lisibles comme priorite produit sont :
- `Desk Pro`
- `Trading Dual Stack V1`
- `Bot Vision`

### 3.3 Familles de soutien

Les familles de soutien a conserver dans la lecture globale sont :
- `webhook`
- `perf`
- `quant`
- `collectors`
- `LocalCMS`
- `openclaw / agents / prompt factory`
- `satellites machines`

Ces familles restent visibles parce qu'elles servent la trajectoire produit globale ou la transmission du systeme.
Elles ne remplacent pas les centres de gravite.

### 3.4 Satellites

Dans `satellites machines`, la lecture minimale garde visibles :
- `admin-trading`
- `student`
- `db-layer`
- les surfaces operateur locales quand elles portent une preuve de reprise ou d'execution

### 3.5 Regle de rattachement global

Chaque parent, sous-GO ou GO simple doit pouvoir etre lu a travers :
1. un centre de gravite produit, ou
2. une famille de soutien, ou
3. la couche methode / transmission si le lot est purement gouvernance / continuite

Si plusieurs rattachements existent :
- un rattachement principal doit etre explicite
- les rattachements secondaires restent descriptifs et non souverains

---

## Partie 4 - Parent / sous-GO / GO simple

### 4.1 Parent prouve ou GO simple

Un parent n'existe que s'il est prouve dans le repo.

Sources de preuve recevables :
- dossier parent reel sous `docs/chantiers/`
- ligne canonique correspondante dans `GO_INDEX.md`
- document d'ouverture parent ou matrice canonique qui le reference explicitement

Si aucun parent n'est prouve :
- le GO est lu comme GO simple
- `GO_INDEX.md` peut normaliser `PARENT = CHANTIER`

#### 4.1.1 Parents ouverts explicitement prouves sur la ligne courante

Sur la ligne courante `opt-trading`, les parents suivants sont explicitement prouves et doivent rester lisibles dans la lecture canonique :

- `GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01` : prouve par la presente matrice, `GO_INDEX.md` et `docs/chantiers/GO_OPT_TRADING_MATRICE_DOC_OPS_PARENT_01/`
- `GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01` : prouve par `GO_INDEX.md`, `docs/index/ACTIVE_STREAMS.md`, `docs/index/REPRISE.md` et `docs/chantiers/GO_OPT_TRADING_MULTI_AGENTS_CANON_PARENT_01/`
- `GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01` : prouve par `GO_INDEX.md` et `docs/chantiers/GO_OPT_TRADING_AI_TEAM_ARCHITECTURE_PARENT_01/`

### 4.2 Sous-GO prouve ou non

Un sous-GO n'existe que s'il est prouve.

Regles :
- un sous-GO herite du flux du parent par defaut
- un sous-GO sert un objectif local borne
- un sous-GO ne ferme pas implicitement le parent
- si aucun sous-GO n'est prouve, `GO_INDEX.md` peut normaliser `SOUS_CHANTIER = —`

### 4.3 Role du GO local

Le GO local sert a :
- ouvrir un lot borne
- produire une preuve locale
- viser une cible locale
- fermer proprement un sous-ensemble de travail

Le GO local ne sert pas a :
- redefinir seul la trajectoire produit
- porter la verite de liste a la place de `GO_INDEX.md`
- imposer une doctrine Git generale

### 4.4 Rattachement a la trajectoire produit

Tout parent, sous-GO ou GO simple doit expliciter :
- `objectif_local`
- `cible_locale`
- `rattachement_parent` ou absence prouvee de parent
- `effet_attendu_sur_la_trajectoire_produit`

### 4.5 Propagation a l'ouverture et a la fermeture

- l'ouverture doit rendre visible la structure retenue
- la fermeture doit propager son effet vers les surfaces de continuite adequates
- aucune structure ne doit rester seulement dans un dossier local sans reflet canonique

---

## Partie 5 - Plans de travail et rattachement des chantiers

### 5.1 Regle generale

Un chantier sert un produit, une famille de soutien ou la methode de transmission.
Il ne devient pas la finalite du projet.

### 5.2 Parent et phase macro

Un parent sert une phase macro quand il :
- traverse plusieurs surfaces
- couvre plusieurs sessions ou plusieurs lots bornes
- exige une direction unique produit -> structure -> GO -> Git
- porte un besoin de fusion ou de stabilisation qui depasse un GO local unique

### 5.3 GO local et cible locale

Un GO local sert une cible locale sans devenir la finalite du projet.

Il doit rester borne par :
- un besoin initial
- une cible finale locale
- un plan valide
- un etat etabli
- un gap restant
- un next step lisible

### 5.4 Surfaces de rattachement

- `GO_INDEX.md` : verite de liste des parents, GO simples et sous-entrees retenues
- `NEXT_GO_CANDIDATES.md` : next GO primaire par parent actif
- `ACTIVE_STREAMS.md` : flux reellement actifs ou bloques
- `REPRISE.md` : support de pilotage, non souverain pour la liste

### 5.5 Regle de non-deraillement

Un lot technique est autorise si, et seulement si :
- il reste rattache a une cible produit ou a une phase macro prouvee
- il ne remplace pas la lecture globale par son detail local
- il ne transforme pas un support Git en finalite documentaire

---

## Partie 6 - Nommage canonique

### 6.1 Forme retenue

La regle canonique de nommage est :

`GO_<SCOPE>_<PRODUCT_OR_SURFACE>_<ROLE>_<OBJECT>_<NN>`

### 6.2 Sens des segments

| Segment | Regle |
| --- | --- |
| `SCOPE` | scope stable du lot, en uppercase, sans taxonomie opportuniste |
| `PRODUCT_OR_SURFACE` | produit, famille ou surface deja stabilise(e) par le canon produit ou la carte de surfaces |
| `ROLE` | role borne et lisible ; `PARENT` et `CHILD` ont un sens structurel reel |
| `OBJECT` | objet local du lot, borne et non inflationniste |
| `NN` | suffixe final obligatoire, au moins deux chiffres, pour distinguer serie, iteration ou reouverture |

### 6.3 Role reel de `PARENT` / `CHILD`

- `PARENT` n'est autorise que si un parent reel est prouve
- `CHILD` n'est autorise que si un sous-GO reel est prouve
- l'absence de `PARENT` ou `CHILD` ne suffit pas, a elle seule, a prouver une structure
- aucun nom ne doit raconter une structure non prouvee

### 6.4 Regles de stabilite

- tokens uppercase et separes par `_`
- pas de role decoratif qui singe une structure
- pas de campagne retroactive massive sans GO dedie
- si le `PRODUCT_OR_SURFACE` n'est pas encore canonise, il doit l'etre avant d'ouvrir un nouveau nom stable

### 6.5 Relation avec les branches

Quand une branche dediee est justifiee, le support Git recommande est :
- `go/<GO_ID>` pour une branche parent ou GO dedie

Le nom de branche ne prouve pas a lui seul la structure.
Il doit rester aligne sur le dossier chantier, `go_id`, `GO_INDEX` et la structure reelle.

---

## Partie 7 - Frontmatter noyau + enrichi

### 7.1 Noyau obligatoire

Le noyau frontmatter minimal a viser pour tout document canonique nouveau ou reeligne est :

| Champ | Statut | Role |
| --- | --- | --- |
| `doc_id` | obligatoire | identifiant stable |
| `doc_type` | obligatoire | type documentaire canonique |
| `repo` | obligatoire | repo porteur |
| `project` | obligatoire | projet local |
| `module` | obligatoire meme si vide | rattachement technique ou thematique |
| `go_id` | obligatoire si le document sert un GO ou un parent | rattachement de flux |
| `status` | obligatoire | statut documentaire |
| `lifecycle_stage` | obligatoire | stade de vie |
| `topic_keys` | obligatoire | recroisement stable |
| `surface` | obligatoire | surface documentaire |
| `source_kind` | obligatoire | canonique / derive / deprecated / autre statut justifie |
| `updated_at` | obligatoire | date de mise a jour |
| `links` | obligatoire | liens de reprise ou de preuve |

Recommandes selon le role :
- `reference_canonique_principale`
- `point_de_reprise`

### 7.2 Frontmatter enrichi

Le frontmatter enrichi ne vient qu'apres le noyau.
Il reste subordonne a `MATRICE_GOUVERNANTE_METADATA_DERIVATION_01.md`.

Champs enrichissables seulement si prouvables :
- `chantier_parent`
- `sous_chantier`
- `intention_parent`
- `cible_finale_parent`
- `objectif_local_go`
- `cible_locale_go`
- `produit_centre`
- `famille_produit`
- `intention_produit`
- `produit_final_voulu`
- `plan_macro_valide`
- `jalons_clos`
- `etat_global_courant`
- `gap_global_restant`
- `suite_logique`
- `reference_canonique_principale`
- `point_de_reprise`

### 7.3 Regles de preuve

- aucun champ enrichi sans source canonique identifiable
- aucun champ structurel invente pour completer un vide
- aucun support Git deduit si non prouve
- aucun etat produit deduit depuis un index ou un tag

### 7.4 Alignement nom du GO / frontmatter / GO_INDEX / branche / structure reelle

L'alignement structurel attendu est :
1. structure reelle prouvee dans le repo
2. dossier chantier et document d'ouverture
3. `go_id` et frontmatter
4. ligne correspondante dans `GO_INDEX.md`
5. branche dediee si elle existe

Si un ecart subsiste :
- il doit etre documente comme incoherence
- il ne doit pas etre masque par `search_tags`, registry derive ou renommage implicite

### 7.5 Tags et derives

- le frontmatter prime sur les tags
- `topic_keys` priment sur `search_tags`
- `search_tags` restent legers et derives
- aucun derive metadata ne monte au-dessus du frontmatter canonique

---

## Partie 8 - Placement / indexation / docs vs registry

### 8.1 Regle de placement

| Objet | Surface canonique | Indexation minimale | Ce que l'objet ne doit pas devenir |
| --- | --- | --- | --- |
| matrice maitre / regle souveraine | `docs/governance/` | `docs/INDEX.md` | un simple support operatoire |
| annexe stable de gouvernance | `docs/governance/` | `docs/INDEX.md` | une seconde matrice maitre |
| carte humaine de surfaces | `docs/architecture/` | `docs/INDEX.md` | un registry machine-readable |
| parent / GO simple / sous-GO | `docs/chantiers/<GO_...>/` | `docs/index/GO_INDEX.md` | un index transversal |
| next par parent actif | `docs/index/NEXT_GO_CANDIDATES.md` | interne a la surface | une seconde verite de liste |
| flux actifs | `docs/index/ACTIVE_STREAMS.md` | interne a la surface | une matrice de gouvernance |
| reprise operatoire | `docs/index/REPRISE.md` | interne a la surface | une verite de liste ou une doctrine complete |
| etat branches | `docs/index/BRANCH_STATE.md` | interne a la surface | la doctrine generale du chantier |
| registry machine-readable | `registry/*` | `registry/meta_index.yaml` | une source souveraine de structure |
| resultats extraits de continuite | `docs/governance/HUMAN_*` | `docs/INDEX.md` | une surface de pilotage ou de liste |
| racine repo | racine + `REPO_ROOT_POLICY.md` | categorie documentee si objet durable | un depot opportuniste non qualifie |
| bundle déportable / patch / archive de transport | `bundles/<GO_ID>/` | `docs/index/inbox/<GO_ID>.md` | une source de vérité parallèle au chantier |
 
### 8.2 Frontieres minimales

- `docs/governance/` : regles stables et souveraines
- `docs/architecture/` : cartes humaines et vues de structure
- `docs/index/` : surfaces actives de continuite
- `docs/chantiers/` : dossiers de lots bornes
- `registry/*` : supports machine-readable derives
- `docs/governance/HUMAN_*` : resultats extraits de continuite, conserves comme references
- racine repo : seulement les objets a valeur d'entree, d'execution, de compatibilite ou d'arbitrage documente

### 8.3 Surfaces proches pertinentes mais non souveraines

Restent pertinentes mais non souveraines pour la presente matrice :
- `docs/product_targets/*` : utile pour des cibles produit speciales, mais statut encore `A_REVALIDER` / `PARTIEL` sur certains axes
- `docs/ot/project_cards/*` : fiches compactes de reprise produit, pas canon maitre
- `docs/status/*` : fiches famille / statut, pas matrice globale
- `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md` : snapshot ponctuel, pas regle stable
- `docs/next/NEXT_GO_CANDIDATES.md` : stub de redirection deprecated, non source canonique

### 8.4 Continuité locale des parents et indexation différée

Pour tout nouveau chantier parent, la continuité courante doit être conservée prioritairement dans :

`docs/chantiers/<GO_PARENT>/`

Le dossier parent porte le cadrage, le plan ou état courant, les décisions locales, les gaps, les TODO et le point de reprise.

Une entrée courte atomique doit être créée dans :

`docs/index/inbox/<GO_PARENT>.md`

Cette entrée sert de tampon d'agrégation future.

Les index globaux ne doivent pas être modifiés à chaque micro-avancement. Ils sont modifiés seulement si :
- le parent devient officiellement actif dans la liste globale ;
- le parent est fermé ;
- le statut global change ;
- le next GO global change ;
- un batch explicite d'agrégation d'index est ouvert ;
- un arbitrage branche significatif l'exige.

Effet :
- chaque parent reste autonome pour la reprise ;
- les gros index globaux restent lisibles ;
- l'agrégation globale devient un acte séparé et contrôlé ;
- `docs/index/inbox/` évite de remplacer les index globaux par un journal de session.

---

## Partie 9 - Trunk / branche parent / branche enfant / exceptions

### 9.1 Quand `sot/mainline` reste autorise

`sot/mainline` reste le support Git par defaut pour :
- un GO simple ou un parent doc-only borne
- une passe sans besoin d'isolement fort
- un lot qui ne justifie ni review separee ni travail parallele reel

### 9.2 Quand un parent passe sur branche dediee

Une branche parent dediee est autorisable si au moins une condition forte est vraie :
- isolement documentaire ou technique structurant
- revue separee necessaire
- lot multi-session ou multi-lot qui merite un support propre
- travail multi-machine ou multi-surface reel
- besoin d'eviter de polluer `sot/mainline` pendant une passe structurante

### 9.3 Quand un sous-GO herite

Par defaut :
- le sous-GO herite du support Git du parent
- il n'ouvre pas sa propre branche si le parent suffit

### 9.4 Quand une branche enfant est autorisable

Une branche enfant n'est recevable qu'en exception motivee :
- isolement technique fort
- revue separee reellement necessaire
- travail parallele reel avec risque de collision
- stabilisation locale d'une surface ou d'une machine distincte
- besoin temporaire borne

Interdits :
- pas de doctrine `1 GO = 1 branche`
- pas de branche decorative
- pas de branche creee pour compenser un manque de structure documentaire

### 9.5 Fermer un sous-GO sans fermer le parent

Fermer un sous-GO implique :
- closeout local explicite
- maintien ou mise a jour du parent
- propagation vers `GO_INDEX.md`, `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` si necessaire
- decision explicite sur le sort de la branche enfant si elle existe

### 9.6 Fermer un parent et sa branche

Fermer un parent implique :
- closeout parent explicite
- sortie ou reclassification dans les surfaces actives
- mise a jour de la continuite produit si l'etat global change
- decision explicite sur le sort de la branche parent

Si une branche dediee existe encore, `BRANCH_STATE.md` doit etre aligne dans le lot qui arbitre son statut.

---

## Partie 10 - Ouverture / fermeture / propagation / closeout

### 10.1 Ouverture parent

L'ouverture d'un parent doit figer au minimum :
- besoin initial
- cible finale
- plan valide
- etat etabli courant
- gap restant
- next step
- rattachement produit ou methode
- support Git seulement s'il est prouve ou necessaire

Propagation minimale d'ouverture :
- dossier chantier parent ;
- entrée atomique `docs/index/inbox/<GO_PARENT>.md` ;
- `GO_INDEX.md` seulement si le parent doit entrer immédiatement dans la liste globale ;
- `NEXT_GO_CANDIDATES.md` seulement si le parent devient priorite active globale ;
- `ACTIVE_STREAMS.md` seulement si le flux devient reellement actif globalement ;
- `REPRISE.md` seulement si un point de pilotage global est necessaire ;
- `BRANCH_STATE.md` seulement si une branche dediee significative est ouverte ou arbitree.

#### 10.1.1 Standard bundle + .patch + .zip

Tout GO produisant un artefact transportable (patch, archive, bundle déportable)
doit suivre le format canonique :

- `.patch` = artefact canonique d'échange Git, autoporteur, source unique de vérité
- `.zip` = sidecar optionnel réservé aux charges lourdes, temporaires ou hors repo (transport IDE externe, transfert multi-machine, artefacts binaires). Le `.zip` ne remplace pas le bundle source.
- bundle source = `bundles/<GO_ID>/` = structure opérable complète : TARGETS.md, target_card.json, patches/, README_BUNDLE.md
- chantier source = `docs/chantiers/<GO_ID>/` = documentation du lot
- entrée courte = `docs/index/inbox/<GO_ID>.md` = tampon d'agrégation
- le patch est archivé sous `bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch`
- aucun `.patch` racine n'est commité

Chaîne complète :

```text
plan validé
→ GO_ID
→ docs/chantiers/<GO_ID>/00_INITIAL_PROJECT_DOC.md
→ docs/index/inbox/<GO_ID>.md
→ bundles/<GO_ID>/README_BUNDLE.md
→ bundles/<GO_ID>/TARGETS.md
→ bundles/<GO_ID>/bundle_meta/target_card.json
→ bundles/<GO_ID>/patches/<YYYYMMDD>_<GO_ID>_<slug>.patch
→ .zip de transport si utile
→ IDE lit EXEMPLE_MATRICE_APPLICATION_PATCH.md
→ git apply --check + git apply + validation + commit + push + PR/review
→ évaluation target
→ évaluation master_target
→ prochain bundle ou batch index global
```

Protocole .zip racine temporaire :
- dépôt temporaire à la racine repo ;
- extraction depuis la racine ;
- déplacement vers `bundles/<GO_ID>/` si le zip contient un bundle ;
- application depuis le contenu extrait ;
- suppression du .zip racine ;
- interdiction de committer le .zip racine ;
- si le zip contient un patch, archivage du patch sous `bundles/<GO_ID>/patches/`.

Règle standard :
- `.zip` = transport temporaire uniquement
- racine repo = zone de dépôt temporaire seulement
- extraction = obligatoire avant toute opération
- application = depuis contenu extrait, jamais depuis le zip
- suppression = obligatoire avant commit
- source canonique = `bundles/<GO_ID>/` (pas le zip, pas la racine)

### 10.2 Ouverture sous-GO

L'ouverture d'un sous-GO doit figer :
- parent prouve
- objectif local
- cible locale
- heritage Git par defaut ou exception motivee

Propagation minimale :
- dossier ou preuve de sous-GO
- `GO_INDEX.md`
- surfaces actives si le sous-GO change la priorite ou le point de reprise

### 10.3 Fermeture sous-GO

La fermeture d'un sous-GO exige :
- closeout local explicite
- mise a jour du parent
- propagation vers `GO_INDEX.md`
- propagation vers `NEXT_GO_CANDIDATES.md`, `ACTIVE_STREAMS.md`, `REPRISE.md` si le prochain geste change
- propagation vers la continuite produit si le sous-GO modifie l'etat du produit ou du plan macro

### 10.4 Fermeture parent

La fermeture d'un parent exige :
- closeout parent explicite
- retrait ou reclassement du parent dans les surfaces actives
- mise a jour du plan produit ou de la trajectoire si le parent avait une incidence structurante
- decision explicite sur la branche parent si elle existe

### 10.5 Regle de propagation

Ce qui est cree, renomme, reclassifie, rerattache, clos ou reouvert doit etre reflete dans le meme lot documentaire sur les surfaces canoniques adequates.

Propagation minimale a retenir :
- `GO_INDEX.md` pour la liste
- `NEXT_GO_CANDIDATES.md` pour le prochain geste par parent actif
- `ACTIVE_STREAMS.md` pour l'actif reel
- `REPRISE.md` pour la reprise operatoire
- surfaces produit si l'etat global change

La propagation globale n'est pas obligatoire pour chaque micro-avancement local.

Par défaut, les évolutions locales restent dans le dossier parent `docs/chantiers/<GO_PARENT>/`.

L'entrée `docs/index/inbox/<GO_PARENT>.md` sert de trace courte en attente d'un batch d'agrégation.

Les index globaux sont réservés aux changements structurels, aux fermetures, aux ouvertures significatives, aux changements de statut global, aux changements de next GO global et aux batchs d'agrégation.

### 10.6 Registre des niveaux de cible (TARGET_LEVEL_REGISTRY)

Six noms utiles, quatre niveaux de cible/livrable :

| Niveau | Nom | Fonction exacte | Est-ce une target ? |
| -----: | ----------------------- | ----------------------------------------------------------------- | ------------------- |
| L0 | `1_MASTER_TARGET` | Produit final utilisable, opérationnel, vérifiable et livrable | Oui, target suprême |
| L1 | `4_MASTER_PROJECT_PLAN` | Plan complet des livrables requis pour atteindre le produit final | Non, checklist de fermeture |
| L2 | `6_FINAL_TARGET` | Résultat attendu de la phase actuelle | Oui |
| L3 | `BUNDLE_TARGET` | Livrable concret du bundle / patch / zip | Oui |
| L4 | `GO_ID` | Unité d'exécution traçable | Oui, mais comme véhicule d'exécution |
| L5 | `NEXT_GO` | Prochain pas si la target supérieure n'est pas atteinte | Non, mécanisme de continuité |

Définitions canoniques :

```text
1_MASTER_TARGET    = produit final utilisable
4_MASTER_PROJECT_PLAN = liste des livrables obligatoires pour produire ce résultat final
6_FINAL_TARGET     = objectif de la phase courante
BUNDLE_TARGET      = résultat concret attendu du bundle transportable
GO_ID              = chantier ou sous-chantier nommé pour produire une partie du résultat
NEXT_GO            = suite obligatoire si le MASTER_TARGET n'est pas encore atteint
```

Hiérarchie canonique :

```text
1_MASTER_TARGET
  -> 4_MASTER_PROJECT_PLAN
    -> 6_FINAL_TARGET
      -> BUNDLE_TARGET
        -> GO_ID
          -> NEXT_GO
```

### 10.7 Porte de fermeture du MASTER_TARGET (CLOSE_GATE_MASTER_TARGET)

Un chantier parent ne peut pas être fermé parce qu'un GO, patch, bundle ou PR est terminé.

Il peut être fermé seulement si :

```text
1. Le MASTER_TARGET est atteint comme produit final utilisable.
2. Les livrables du MASTER_PROJECT_PLAN sont complétés ou explicitement déclassés.
3. Le produit peut être testé, utilisé ou repris.
4. Les gaps restants ne bloquent pas l'usage réel.
5. Sinon, créer NEXT_GO.
```

Invariants associés :

```text
MASTER_TARGET = produit final utilisable, pas intention générale.
MASTER_PROJECT_PLAN = checklist de fermeture du produit final.
GO_ID = unité d'exécution, pas preuve de produit fini.
PR mergée ≠ MASTER_TARGET atteint.
Bundle livré ≠ chantier parent fermé.
Si le MASTER_TARGET n'est pas atteint, il faut NEXT_GO ou REMAINING_GAP.
```

---

## Partie 11 - Invariants / interdits

- pas de doublon souverain
- pas de derive metadata au-dessus du canon
- pas de GO technique lu comme finalite produit
- pas de support Git eleve au-dessus de la trajectoire produit
- pas de parent suppose pour completer artificiellement la structure
- pas de sous-GO suppose pour habiller un lot local
- pas de `REPRISE.md` promu au rang de verite de liste
- pas de `BRANCH_STATE.md` promu au rang de doctrine generale
- pas de chantier qui remplace une matrice de gouvernance
- pas d'index qui absorbe un closeout
- pas de registry derive qui requalifie un objet source
- pas de `search_tags` qui compensent une contradiction reelle
- pas de surface locale de naming non publiee elevee au-dessus du canon publie
- pas de lot d'alignement physique avant que la presente matrice existe
- pas de `.patch` orphelin non archivé dans `bundles/<GO_ID>/patches/`
- pas de `.zip` promu au rang de source canonique (le `.zip` transporte, il ne remplace pas le bundle)
- pas de bundle sans chantier associé (`docs/chantiers/<GO_ID>/`)
- pas de bundle sans entrée courte (`docs/index/inbox/<GO_ID>.md`)
- pas de .zip racine conservé après extraction
- pas d'extraction .zip vers une surface non canonique sans justification explicite

---

## Partie 12 - Conditions de reouverture / lot suivant

### 12.1 Regle de reouverture

La reouverture d'un lot sur cette matrice n'est recevable que si l'un des cas suivants est vrai :
- contradiction canonique reelle observee contre le present document
- changement produit majeur qui invalide la lecture actuelle
- nouvelle structure parent / sous-GO prouvee dans le repo
- nouvelle doctrine Git ou frontmatter deja stabilisee ailleurs dans le canon

Une reouverture n'est pas recevable pour :
- refaire une synthese laterale
- contourner la matrice maitre
- lancer un lot technique sans rattachement produit ou methode

### 12.2 Lot suivant obligatoire

Le lot suivant n'est pas :
- la redaction d'une nouvelle synthese
- la recreation d'une seconde matrice

Le lot suivant est :
- l'alignement / deduplication / reclassement des surfaces proches a partir de la presente matrice maitre

### 12.3 Doublons ou incoherences identifies mais non traites dans ce lot

- `docs/next/NEXT_GO_CANDIDATES.md` reste un doublon de nom conserve comme stub de compatibilite
- `docs/product_targets/GO_PRODUCT_TARGET_CANONIZATION_01_DECISION.md` et `docs/product_targets/RUNTIME_TO_TARGET_MAPPING.md` restent utiles mais non souverains tant que leurs zones `A_REVALIDER` / `PARTIEL` ne sont pas requalifiees
- `docs/ot/project_cards/*` restent des fiches compactes de reprise produit et non une couche maitre
- `docs/status/*` restent des supports de famille et non une lecture globale souveraine
- `docs/architecture/PROJECT_SNAPSHOT_GLOBAL_2026-04-18.md` reste un snapshot ponctuel et non une regle stable
- `docs/governance/PRODUCT_CONTINUITY_HIERARCHY_01.md` reste pertinent mais son noyau frontmatter n'est pas encore realigne sur la convention cible
- l'alignement complet des surfaces proches avec la presente matrice est reporte au lot suivant et non execute ici

---

## Verdict de lot

Le verdict retenu pour ce lot est :
- la matrice maitre finale existe desormais comme document canonique unique
- aucun lot de deduplication / reclassement des surfaces proches n'a encore ete execute
- la suite logique devient l'alignement des surfaces proches sans doublon a partir du present maitre

## RISKS

- À qualifier.
