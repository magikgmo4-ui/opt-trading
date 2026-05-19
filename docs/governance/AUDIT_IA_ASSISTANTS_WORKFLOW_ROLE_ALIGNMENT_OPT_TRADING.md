# AUDIT — IA / IDE / WORKFLOW ROLE ALIGNMENT — OPT-TRADING

## LECTURE CANONIQUE

- lire cet audit apres `docs/governance/MATRICE_DOC_OPS_MASTER_MATRIX_01.md`
- garder `docs/governance/MATRICE_GOUVERNANTE_V2.md` comme annexe stable secondaire seulement si un recroisement est utile
- ne pas utiliser cet audit a la place des surfaces souveraines ou des index actifs

## Besoin initial
- Éviter les confusions (assistant externe vs produit vs repo transverse vs IDE vs machine) qui cassent la continuité et le scope des missions.

## Objectif final visé
- Disposer d’une cartographie compacte et opposable du **rôle workflow canonique** des entrées IA/IDE/couples outil-produit, repo-sourcée, sans ouvrir de patch runtime.

## Plan validé
- Lire les audits de gouvernance + entrypoints Trae déjà fixés.
- Pour chaque entrée demandée, ne citer que des preuves repo-sourcées (docs/README/runbooks/modules) ; journal = secondaire.
- Produire : tableau exécutif + fiches courtes (nature, rôle workflow, limites, confusion, point d’entrée canonique) + statut (ETABLI/PARTIEL/A_REVALIDER).

## État établi
- La structure canonique de continuité est déjà injectée dans les templates et entrypoints Trae (docs OT Trae + starter pack).
- Les audits produit et thématiques existent et servent de sources de vérité secondaires/complémentaires à cet audit (ne pas les remplacer).

## Gap
- Les rôles workflow des assistants / IDE / couples outil-produit restaient mélangés ou implicites, et certains noms forts sont surpromis malgré des preuves repo limitées.

## Prochain GO
> GO_IA_ASSISTANTS_WORKFLOW_ROLE_ALIGNMENT_01

---

## 1. Objet
- Ce document ne remplace ni l’audit maître de continuité produit ([AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md)) ni la coupe thématique multi-IA ([AUDIT_THEMATIQUE_MULTI_IA_IDE_AGENTS_SPACES_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_THEMATIQUE_MULTI_IA_IDE_AGENTS_SPACES_OPT_TRADING.md)).
- Il fixe le **rôle workflow canonique** des assistants / IDE / couples outil-produit listés, avec séparation explicite :
  - rôle machine
  - rôle IA / IDE
  - rôle repo / produit
  - rôle workflow
  - limites / hors-scope

## 2. Règle de lecture (opposable)
Pour chaque entrée ci-dessous :
- **Nature** : IA / IDE / repo transverse / produit / assistant externe / bridge borné.
- **Rôle workflow canonique** : à quoi sert cette entrée dans le workflow (cadrage/exécution/validation/production d’artefacts).
- **Ce que ce n’est pas** : anti-confusions explicites.
- **Point d’entrée canonique** : chemin repo ou commande wrapper/menu/cmd documentée.
- **Limites / hors-scope** : ce que l’entrée ne doit pas faire.
- **Statut** : ETABLI (preuves claires), PARTIEL (preuve locale + cible finale non figée), A_REVALIDER (preuves insuffisantes ou absentes).

## 3. Tableau exécutif

| Entrée | Nature | Rôle workflow canonique | Ce que ce n’est pas | Point d’entrée canonique | Statut |
|---|---|---|---|---|---|
| Trae | Couche workflow (doc opposable) | Gouverner missions (cadrage → exécution → review → close), continuité, gates, points de reprise | Produit métier principal ; runtime/agents actifs par défaut | [docs/ot/trae/OT_TRAE_SESSION_REPRISE.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_TRAE_SESSION_REPRISE.md) + [00_mission_start_guide.md](file:///c:/Users/ghost/opt-trading/docs/master_pack/mission_starter_pack/00_mission_start_guide.md) | ETABLI |
| ChatGPT | Assistant externe | Cadrage/synthèse/validation conversationnelle, entrée “session” dans des prompts validés | Source de vérité repo-native ; workflow opposable autonome | [validated_prompt_factory/README.md](file:///c:/Users/ghost/opt-trading/modules/validated_prompt_factory/README.md) | PARTIEL |
| Claude / LocalCMS | Assistant externe + produit (hors repo) | Claude : exécution/doc ponctuelle ; LocalCMS : produit consumer distinct (référencé) | Confondre l’assistant et le produit ; promouvoir LocalCMS comme produit central d’opt-trading | [AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md) (registre) | PARTIEL |
| OpenClaw / Hermes | Repo transverse + bridge borné | OpenClaw : cockpit opérateur local + policy provider/modèles ; Hermes : axe expérimental de génération avec bridge borné vers OpenClaw | Un “produit unique général” ; fusion Hermes→OpenClaw sans borne | OpenClaw : [GO_OPENCLAW_CHAIN_03.md](file:///c:/Users/ghost/opt-trading/modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md) ; Hermes : [docs/hermes/00_overview.md](file:///c:/Users/ghost/opt-trading/docs/hermes/00_overview.md) + [generate.sh](file:///c:/Users/ghost/opt-trading/tools/hermes_bridge/generate.sh) | OpenClaw ETABLI / Hermes PARTIEL |
| DeepSeek / Ollama | IA locale + hub opérateur | IA locale (student) avec hub d’unification, séparation thinking/response, surface opérateur | Cible finale déjà close ; substitution du runtime sans mission dédiée | [deepseek_hub/README.md](file:///c:/Users/ghost/opt-trading/modules/deepseek_hub/README.md) + [student_deepseek_runbook.md](file:///c:/Users/ghost/opt-trading/docs/student_deepseek_runbook.md) | PARTIEL |
| Antigravity / Gemini | Axe spécialisé + assistant (à prouver) | Antigravity : chantier spécialisé (référencé), à recontextualiser ; Gemini : non prouvé repo-sourcé dans ce repo | Surpromouvoir sans preuve ; confondre “outil/IDE” et “assistant” | Antigravity : audits gouvernance (références) ; Gemini : N/A | Antigravity PARTIEL / Gemini A_REVALIDER |
| MiMoPro | Nom fort (à revalider) | Ne pas surpromouvoir : distinguer ligne spécialisée prouvée (mimo_open_observer) vs “MiMoPro” produit global | Confondre “MiMoPro” et “mimo_open_observer” ; étendre en produit global sans preuve | [mimo_open_observer/README.md](file:///c:/Users/ghost/opt-trading/modules/mimo_open_observer/README.md) + [MIMO_V2_PRO_FREE_CLOSEOUT.md](file:///c:/Users/ghost/opt-trading/student/docs/MIMO_V2_PRO_FREE_CLOSEOUT.md) | A_REVALIDER |

## 4. Fiches courtes par entrée

### 4.1 Trae
- **Nature** : couche de workflow opposable (doc repo-sourcée).
- **Rôle workflow canonique** : imposer un cadre mission clair (cadrage → exécution → review → close), avec continuité (besoin/objectif/plan/état/gap/GO).
- **Rôle repo / produit** : structure documentaire OT Trae (décisions, entrypoints, checklists) ; starter pack mission projet.
- **Rôle machine** : N/A (doc-only).
- **Ce que ce n’est pas** :
  - un produit métier principal (Desk Pro / Trading Dual Stack / etc.)
  - une plateforme d’agents runtime active par défaut
- **Point d’entrée canonique** :
  - [OT_TRAE_SESSION_REPRISE.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/OT_TRAE_SESSION_REPRISE.md)
  - [docs/ot/trae/README.md](file:///c:/Users/ghost/opt-trading/docs/ot/trae/README.md)
  - [12_ORCHESTRATOR_ENTRYPOINT_V1.txt](file:///c:/Users/ghost/opt-trading/docs/ot/trae/12_ORCHESTRATOR_ENTRYPOINT_V1.txt)
- **Confusions à éviter** : Trae (workflow) ≠ runtime ≠ agents V1 ≠ produit métier.
- **Statut** : ETABLI (preuves doc OT + audits).
- **Point de reprise minimal** : reprendre via l’entrypoint Trae, cadrer la mission, puis appliquer le GO indiqué par kanban/closing.

### 4.2 ChatGPT
- **Nature** : assistant externe (conversationnel).
- **Rôle workflow canonique** : cadrage/synthèse/validation ; support de génération contrôlée via “session” dans un module repo (pas source de vérité).
- **Rôle repo / produit** : encapsulé/consommé via un module repo-sourcé quand besoin (ex: génération de prompts validés).
- **Rôle machine** : N/A (sauf capture journaling si appliqué).
- **Ce que ce n’est pas** :
  - une source de vérité repo-native
  - un workflow opposable à lui seul
- **Point d’entrée canonique** : [validated_prompt_factory/README.md](file:///c:/Users/ghost/opt-trading/modules/validated_prompt_factory/README.md) (mode “chatgpt_session”).
- **Confusions à éviter** : ChatGPT (assistant externe) ≠ Trae (workflow) ≠ module repo.
- **Statut** : PARTIEL (preuve via module + journal secondaire ; pas de rôle “canonique global” au-delà).
- **Point de reprise minimal** : passer par une mission cadrée Trae si on veut industrialiser/figer un usage.

### 4.3 Claude / LocalCMS
- **Nature** :
  - Claude : assistant externe.
  - LocalCMS : produit consumer distinct (référencé dans opt-trading, mais non présent comme repo ici).
- **Rôle workflow canonique** :
  - Claude : exécution/doc ponctuelle quand explicitement cadrée (pas de promotion automatique).
  - LocalCMS : rappeler qu’il existe comme produit séparé ; opt-trading ne doit pas l’absorber sans preuve.
- **Rôle repo / produit** : LocalCMS est hors du repo opt-trading ; ici on ne garde qu’une référence de continuité.
- **Rôle machine** : N/A dans ce repo.
- **Ce que ce n’est pas** :
  - Claude ≠ LocalCMS
  - LocalCMS ≠ produit central d’opt-trading
- **Point d’entrée canonique (repo-sourcé)** : registre LocalCMS dans [AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md).
- **Confusions à éviter** : “assistant externe” ≠ “produit consumer” ≠ “repo transverse”.
- **Statut** : PARTIEL (preuve de rôle conceptuel uniquement dans ce repo ; entrypoint du produit hors périmètre).
- **Point de reprise minimal** : si besoin, pointer explicitement vers le repo LocalCMS et son entrypoint interne (hors scope de ce document).

### 4.4 OpenClaw / Hermes

#### OpenClaw
- **Nature** : couche transverse (cockpit opérateur local + gouvernance provider/modèles) dans opt-trading.
- **Rôle workflow canonique** : offrir une surface opérateur bornée + une policy provider/modèle centralisée pour éviter que les scripts/agents choisissent arbitrairement.
- **Rôle repo / produit** : modules et docs dans `modules/menu_openclaw/` et `modules/model_provider_openclaw/`.
- **Rôle machine** : principalement local (surface opérateur), avec portabilité bornée selon usages.
- **Ce que ce n’est pas** : un “produit global unique” qui remplace Desk Pro / trading ; une normalisation implicite de toutes les couches IA.
- **Point d’entrée canonique** :
  - [GO_OPENCLAW_CHAIN_03.md](file:///c:/Users/ghost/opt-trading/modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md)
  - [model_provider_openclaw/README.md](file:///c:/Users/ghost/opt-trading/modules/model_provider_openclaw/README.md)
- **Confusions à éviter** : OpenClaw (cockpit/policy) ≠ Hermes (bridge expérimental).
- **Statut** : ETABLI (preuves modules/docs).

#### Hermes
- **Nature** : axe expérimental + bridge borné vers OpenClaw.
- **Rôle workflow canonique** : générer des scripts/artefacts encadrés (horodatés + logs), consommables par une exécution bornée ; ne pas se présenter comme “système central”.
- **Rôle repo / produit** : docs Hermes + outil de génération dans `tools/hermes_bridge/`.
- **Rôle machine** : N/A (outil local, doc-only ici).
- **Ce que ce n’est pas** : un assistant générique ; une plateforme d’exécution non gouvernée.
- **Point d’entrée canonique** :
  - [docs/hermes/00_overview.md](file:///c:/Users/ghost/opt-trading/docs/hermes/00_overview.md)
  - [tools/hermes_bridge/generate.sh](file:///c:/Users/ghost/opt-trading/tools/hermes_bridge/generate.sh)
- **Statut** : PARTIEL (bridge borné prouvé, mais rôle volontairement non généralisé).

### 4.5 DeepSeek / Ollama
- **Nature** : IA locale (Ollama + modèles) + surfaces opérateur + hub d’unification.
- **Rôle workflow canonique** : fournir une IA locale exploitable (notamment sur machine student) avec séparation thinking/response et une surface opérateur unifiée via hub.
- **Rôle repo / produit** : `modules/deepseek_hub/` formalise le hub ; runbooks documentent les entrypoints côté machine.
- **Rôle machine** : fortement lié à `student` (runtime actuel) ; multi-machine = à cadrer mission par mission.
- **Ce que ce n’est pas** :
  - une cible finale déjà close (la “destination canonique finale” n’est pas verrouillée)
  - un prétexte pour patcher runtime sans mission dédiée
- **Point d’entrée canonique** :
  - [deepseek_hub/README.md](file:///c:/Users/ghost/opt-trading/modules/deepseek_hub/README.md)
  - [student_deepseek_runbook.md](file:///c:/Users/ghost/opt-trading/docs/student_deepseek_runbook.md)
- **Confusions à éviter** : runtime machine `scripts/student` ≠ module hub repo ≠ assistant externe.
- **Statut** : PARTIEL (hub prouvé, mais cible finale non figée).

### 4.6 Antigravity / Gemini
- **Antigravity**
  - **Nature** : chantier spécialisé (référencé en gouvernance).
  - **Rôle workflow canonique** : conserver comme axe périphérique documenté ; ne pas le promouvoir comme centre de gravité multi-IA sans relecture dédiée.
  - **Point d’entrée canonique (repo-sourcé)** : références gouvernance uniquement :
    - [AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_CONTINUITE_PRODUIT_OPT_TRADING.md)
    - [AUDIT_THEMATIQUE_MULTI_IA_IDE_AGENTS_SPACES_OPT_TRADING.md](file:///c:/Users/ghost/opt-trading/docs/governance/AUDIT_THEMATIQUE_MULTI_IA_IDE_AGENTS_SPACES_OPT_TRADING.md)
  - **Statut** : PARTIEL (pas d’entrypoint dédié repéré dans ce repo).
- **Gemini**
  - **Nature** : assistant/moteur externe supposé (non prouvé ici).
  - **Rôle workflow canonique** : N/A tant qu’aucune preuve repo-sourcée n’est identifiée.
  - **Point d’entrée canonique** : N/A (aucune occurrence repo).
  - **Statut** : A_REVALIDER.

### 4.7 MiMoPro
- **Nature** : nom fort à revalider ; la preuve repo-sourcée la plus solide est une **ligne spécialisée** (mimo_open_observer) + un closeout E2E “V2 Pro Free”.
- **Rôle workflow canonique** : ne pas confondre “MiMoPro” avec la ligne prouvée ; traiter “MiMoPro” comme label tant que le produit global n’est pas figé.
- **Rôle repo / produit** :
  - Ligne prouvée : [mimo_open_observer/README.md](file:///c:/Users/ghost/opt-trading/modules/mimo_open_observer/README.md)
  - Closeout E2E : [MIMO_V2_PRO_FREE_CLOSEOUT.md](file:///c:/Users/ghost/opt-trading/student/docs/MIMO_V2_PRO_FREE_CLOSEOUT.md)
- **Rôle machine** : dépend des flux trading/collecte ; non consolidé ici.
- **Ce que ce n’est pas** : une promotion automatique en produit global transverse.
- **Point d’entrée canonique** :
  - pour la ligne prouvée : `modules/mimo_open_observer/` (cmd/menu documentés dans le README)
  - pour “MiMoPro” : closeout E2E ci-dessus (pas d’entrypoint unique consolidé)
- **Confusions à éviter** : MiMoPro (nom fort) ≠ mimo_open_observer (ligne spécialisée prouvée).
- **Statut** : A_REVALIDER (nom fort non verrouillé comme produit global).

## 5. Conclusion opératoire
- Rôles canoniques clarifiés :
  - Trae = workflow opposable (doc repo-sourcée) ; pas un produit métier.
  - ChatGPT/Claude = assistants externes ; utilisables mais non sources de vérité.
  - OpenClaw = couche transverse (cockpit/policy) ; Hermes = bridge expérimental borné.
  - DeepSeek/Ollama = IA locale prouvée (hub + runbooks) mais cible finale non close.
  - Antigravity = axe périphérique référencé ; Gemini = absent repo-sourcé.
  - MiMoPro = nom fort à revalider ; ne pas confondre avec la ligne mimo_open_observer prouvée.
- Confusions à éviter (rappel) : assistant externe ≠ IDE ≠ produit ≠ repo transverse ≠ machine ≠ workflow.
- Suites possibles (hors scope de ce document) :
  - Si besoin : mission dédiée “synthèse canonique OpenClaw” ou “clarification runtime DeepSeek”.
  - Si “MiMoPro” doit devenir un produit : décision repo-sourcée + entrypoint canonique consolidé.
