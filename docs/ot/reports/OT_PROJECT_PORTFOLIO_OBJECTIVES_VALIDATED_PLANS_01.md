# OT_PROJECT_PORTFOLIO_OBJECTIVES_VALIDATED_PLANS_01

Date: 2026-04-13

## 1. Objet

Figer dans le repo une vue d’ensemble transversale des projets, briques et modules principaux, en séparant explicitement:
- l’objectif final retenu;
- le plan validé reconstitué;
- l’état établi;
- la lacune documentaire restante.

Cette note répond à une lacune récurrente constatée en séance: beaucoup de chantiers disposent de patches, closings, runbooks ou PRs, mais pas d’une fiche compacte unique résumant **but final + plan validé + état établi + reprise**.

## 2. Règle de lecture

Cette note distingue volontairement 3 niveaux:

1. **ETABLI / repo-verifiable**  
   Ce qui est directement appuyé par les artefacts GitHub, docs, README, scripts ou PRs.

2. **PLAN VALIDE RECONSTITUE**  
   Ce qui a été présenté, retenu et poursuivi comme fil logique de travail, mais qui n’est pas toujours figé dans une doc source unique. Cette couche peut donc agréger repo + mémoire de continuité + formulation validée en séance.

3. **LACUNE DOC**  
   Ce qui manque encore pour qu’un lecteur retrouve le chantier sans devoir relire plusieurs closings, rapports ou conversations.

## 3. Vue d’ensemble portefeuille

---

## 3.1 `opt-trading` — plateforme principale

### A. Desk Pro

**Objectif final retenu**

Construire une surface opérateur multi-machine cohérente, gouvernée et relâchable, avec entrypoints propres, wrappers maîtrisés, runbooks de release cohérents et chaîne d’export/consultation claire.

**ETABLI**

- Une note dédiée formalise la distinction entre GO global de sélection, missions candidates Desk Pro et chantiers DEV `fantome`.
- Les missions candidates repo-sourcees sont explicites:
  - gouvernance wrappers admin;
  - drill release ops;
  - drill shared export consumption;
  - inventaire installateurs/wrappers;
  - consolidation des références release;
  - préparation ingestion `db-layer`.

**PLAN VALIDE RECONSTITUE**

1. Nettoyer la surface opérateur et les entrypoints.
2. Recaler doctrine, wrappers et documentation.
3. Stabiliser la release et ses preuves.
4. Prouver le flux inter-machines via `/shared`.
5. Préparer ensuite la couche de consultation / ingestion enrichie côté `db-layer`.

**LACUNE DOC**

Il manque encore une fiche produit courte unique expliquant Desk Pro comme programme global, au-delà des missions candidates et des closings locaux.

---

### B. SimEx Bitget Bridge

**Objectif final retenu**

Avoir un runner SimEx Bitget durable, relançable automatiquement, avec contrat runtime stable, compatibilité legacy conservée et comportement propre sur fautes upstream.

**ETABLI**

- Le module est documenté comme module durable pour le runner SimEx Bitget.
- Le contrat runtime `SIMEX_UNITS_V1` est fixé.
- La compat legacy minimale est conservée.
- Les fautes upstream sont classifiées et loggées de façon compacte.
- Les erreurs de fetch / candles insuffisantes n’explosent plus en traceback massif et laissent le timer relancer naturellement le runner.

**PLAN VALIDE RECONSTITUE**

1. Sortir SimEx du script ad hoc vers un module durable.
2. Préserver le contrat métier et la compat opérateur.
3. Poser wrappers, sanity et menu.
4. Déployer sur `admin-trading` avec service/timer.
5. Durcir progressivement le runtime réel sur fautes réseau/upstream.
6. Garder Perf et logique signal hors refactor large.

**LACUNE DOC**

Le but du module est bien documenté, mais la séquence complète de maturation (module durable -> déploiement -> hardening -> closeout runtime) reste dispersée.

---

### C. OpenClaw dans `opt-trading`

**Objectif final retenu**

Fixer OpenClaw, dans `opt-trading`, comme cockpit opérateur local sur `db-layer`, centré sur l’installation, la configuration, la gateway locale, le diagnostic et l’export de preuves.

**ETABLI**

- Le projet cible réel est borné comme cockpit opérateur local sur `db-layer`.
- La chaîne cible documentée est: install -> config -> gateway -> configure -> doctor -> evidence -> policy.
- Les usages utiles prouvés couvrent menu, policy provider/model, validation config, doctor, gateway tmux et export de preuves.
- Le non-périmètre est explicite: pas de serving exposé, pas de cloud GPU actif, pas de runtime multi-machine généralisé, pas de migration runtime déjà décidée vers un autre repo.

**PLAN VALIDE RECONSTITUE**

1. Documenter le périmètre réel.
2. Arrêter les extrapolations produit non prouvées.
3. Outiller proprement le poste opérateur local.
4. Fiabiliser lecture config, gateway, doctor et evidence.
5. N’ouvrir un chantier plus large que sur besoin opératoire réel.

**LACUNE DOC**

Le périmètre est déjà mieux borné que sur beaucoup d’autres chantiers, mais il manque encore une feuille de route compacte des prochains niveaux de maturité explicitement exclus ou permis.

---

### D. `validated_prompt_factory`

**Objectif final retenu**

Servir d’usine à prompts validés: transformer une synthèse validée en prompt final réutilisable dans le bon mode d’usage.

**ETABLI**

- Le repo contient audits, reports, closings, hardening et adoption autour du module.
- Le module a été traité comme brique durable à wrappers/sanity/menu, avec focus sur usage réel et qualité documentaire.

**PLAN VALIDE RECONSTITUE**

1. Prendre de la matière déjà validée.
2. La convertir en prompt final exploitable.
3. Supporter plusieurs modes de sortie selon l’usage.
4. Rendre la brique découvrable et opérable.
5. Durcir ensuite l’adoption réelle et les wrappers.

**LACUNE DOC**

Il manque une fiche produit courte explicitant la place exacte du module dans la chaîne humaine/machine globale.

---

### E. `module_contextuals_shell`

**Objectif final retenu**

Servir de socle partagé pour déclarer, découvrir, afficher et router les actions contextuelles des futurs modules shell.

**ETABLI**

- Le module est documenté comme socle partagé pour tous les futurs modules shell.
- Il standardise l’usage de fichiers `.ctx`, la lecture robuste, les menus dynamiques et le routage des actions.
- Il est pensé comme fondation pour un menu global capable de scanner les contextuals des modules.

**PLAN VALIDE RECONSTITUE**

1. Éviter de recoder la couche menu/dispatch dans chaque module.
2. Passer à une logique déclarative d’actions shell.
3. Préparer un index global d’actions par scanning des modules.
4. Réduire le coût d’intégration des futurs modules shell.

**LACUNE DOC**

La cible architecturale est claire, mais la feuille d’adoption effective par les autres modules reste peu figée.

---

### F. Chaîne analytique trading (`risk_engine`, `derivatives_collector`, `derivatives_analyzer`, `probability_engine`)

**Objectif final retenu**

Constituer une chaîne d’analyse et d’aide à la décision séparant collecte, calcul risque, lecture des dérivés, analyse et probabilité, avec contrats de sortie stables.

**ETABLI**

- Cette note n’a pas pour objet de relire ici chaque fichier de cette chaîne.
- En continuité, la cible fonctionnelle retenue est cohérente: séparation collecte/analyse/probabilité/risque et durcissement progressif des contrats.

**PLAN VALIDE RECONSTITUE**

1. Séparer collecte, calcul, analyse et probabilité.
2. Stabiliser les payloads et contrats machine-readables.
3. Durcir les sémantiques avant élargissement de périmètre.
4. Préserver les formats déjà acceptés quand ils servent d’interface.
5. Ajouter tests et verrouillage sémantique avant extension fonctionnelle.

**LACUNE DOC**

Cette famille manque d’une vue produit unique expliquant clairement la finalité de la chaîne entière et le rôle final de chaque brique dans un même document.

---

### G. Bot Vision / ingestion desk

**Objectif final retenu**

Transformer des captures ou snapshots visuels en entrée desk structurée, puis en analyse exploitable côté trading/desk.

**ETABLI**

- La chaîne opérationnelle connue passe par capture, transit, bridge, ingestion puis fichier `latest` exploitable côté desk.
- Le cœur de la logique retenue est une source structurée de snapshot, puis consommation analytique.

**PLAN VALIDE RECONSTITUE**

1. Obtenir une capture opératoire simple.
2. Fiabiliser la chaîne de transit.
3. Atomiser l’ingestion vers une source structurée unique.
4. Fournir un `latest snapshot` stable.
5. Brancher ensuite l’analyse desk.

**LACUNE DOC**

Le fil produit global reste moins bien figé que la mécanique runtime ou les diagnostics machines.

---

### H. Journal extractor / journalisation structurée

**Objectif final retenu**

Créer une brique durable d’extraction et segmentation de journal, pour transformer un journal brut en matière exploitable par étapes ultérieures.

**ETABLI**

- Le chantier a été poursuivi comme module durable avec bootstrap, normalisation d’input et segmentation.

**PLAN VALIDE RECONSTITUE**

1. Sortir l’extraction du bricolage manuel.
2. Normaliser les entrées.
3. Segmenter proprement.
4. Rendre la chaîne réutilisable par d’autres passes d’analyse.
5. Enrichir seulement ensuite API, exports ou usages dérivés.

**LACUNE DOC**

Le plan vit surtout dans les lots/patches et moins dans une fiche produit compacte.

---

## 3.2 `localcms`

**Objectif final retenu**

Faire de `localcms` une surface locale modulable combinant:
- Shared Explorer lecture seule sur `/shared`;
- CMS Installer par bundles zip contrôlés;
- Memory View en lecture.

**ETABLI**

- `MOD_SHARED_EXPLORER V1` est établi comme module frontend + endpoints FastAPI lecture seule.
- Les protections sont fixées: `realpath`, blocage symlinks sortants, path traversal, `.env`, preview bornée.
- `MOD_CMS_INSTALLER V1` est établi avec pipeline contrôlé: Scan -> Inspect -> Precheck -> Backup -> Staging -> Validate -> Install -> Post-check -> Finalize.
- Le format bundle et les contraintes de sécurité sont fixés.
- Le merge V1 réunit explicitement Shared Explorer + CMS Installer + Memory View.

**PLAN VALIDE RECONSTITUE**

1. M1: Shared Explorer V1.
2. M2: CMS Installer V1.
3. M3: enrichissement viewer / memory bricks / briques suivantes.
4. Garder le tout local, borné, testable, sans casser le runtime existant.
5. Intégrer par patch minimal dans la surface LocalCMS existante.

**LACUNE DOC**

`localcms` est mieux servi que la moyenne, mais il manque encore une vue portefeuille unique résumant la progression M1 -> M2 -> M3 -> suites.

---

## 3.3 Repo `openclaw`

**Objectif final retenu (reconstitue)**

Disposer, si nécessaire, d’un repo proprement dédié à OpenClaw lorsque la séparation deviendra utile et justifiée par le périmètre réel.

**ETABLI**

- Le repo existe.
- À ce stade, la matière la plus structurée reste toutefois portée dans `opt-trading` pour le périmètre opérationnel effectivement documenté.

**PLAN VALIDE RECONSTITUE**

1. Documenter et stabiliser d’abord le périmètre réel dans `opt-trading`.
2. Éviter d’inventer une migration avant besoin avéré.
3. Préparer une séparation repo dédiée seulement si l’autonomie produit devient réelle.

**LACUNE DOC**

Le repo dédié n’embarque pas encore, à lui seul, une vision produit aussi complète que celle reconstruite autour des modules OpenClaw déjà présents dans `opt-trading`.

---

## 3.4 Autres repos visibles (`Magikgmo`, `hf_trading`, `algo_hf`, `Llm-wiki`, `Llm-wiki-minimal`)

**Objectif de cette note**

Ne pas surinterpréter des repos pour lesquels cette passe n’a pas établi une matière suffisante.

**ETABLI**

- Ces repos existent dans GitHub.
- Cette note ne dispose pas ici d’assez de matière validée pour figer un plan produit comparable à `opt-trading` ou `localcms`.

**PLAN VALIDE RECONSTITUE**

Non figé à ce stade.

**LACUNE DOC**

Il manque encore une première passe de qualification produit par repo avant de pouvoir résumer leur objectif final et leur plan validé.

---

## 4. Constat transversal retenu

La lacune majeure n’est pas l’absence d’artefacts de travail.

La lacune majeure est l’absence fréquente, pour un chantier donné, d’une fiche courte unique du type:
- objet;
- but final;
- plan validé;
- état établi;
- non établi;
- reprise.

Conséquence: on retrouve les preuves, closings et patches, mais moins facilement **le récit de finalité et la séquence validée**.

## 5. Correctif de méthode retenu

Pour les prochains chantiers structurés, prévoir en plus des closings une fiche compacte de gel du plan validé.

Format recommandé:

```text
PROJECT_CARD
- Objet
- But final
- Plan validé
- Établi
- Non établi
- Reprise
```

## 6. Priorités de rattrapage documentaire

Ordre de valeur recommandé pour figer les plans validés déjà poursuivis:
1. Desk Pro
2. chaîne analytique trading
3. Bot Vision / ingestion desk
4. Journal extractor
5. OpenClaw
6. validated_prompt_factory
7. module_contextuals_shell
8. LocalCMS (si l’on veut une vue programme unique; M1/M2 sont déjà mieux fixés que la moyenne)

## 7. ETABLI

- Une vue portefeuille transversale est désormais figée dans le repo.
- La séparation entre **objectif final**, **plan validé reconstitué** et **lacune documentaire** est explicitement documentée.
- La lacune prioritaire est elle-même formalisée comme sujet documentaire de premier niveau.

## 8. TODO

- Décliner cette logique en fiches `PROJECT_CARD` par gros chantier.
- Commencer par Desk Pro, puis chaîne analytique trading.

## 9. REPRISE

Point de reprise recommandé:
`GO_PROJECT_CARDS_FREEZE_01`

Première fiche à produire:
`PROJECT_CARD_DESKPRO_01`

## 10. MEM_CANDIDATE

Utile à mémoriser seulement sur demande explicite:
- la lacune documentaire structurante porte moins sur les preuves que sur l’absence d’une fiche compacte "but final + plan validé + établi + reprise" par chantier.
