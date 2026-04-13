# AUDIT THEMATIQUE — MULTI IA / IDE / AGENTS / SPACES — OPT-TRADING

- ce document ne remplace pas l'audit maitre de continuite produit
- il constitue une coupe thematique parallele
- la Couche 0 transverse reste heritee du cadre maitre :
  - methode uniforme + couche humaine
  - memory_bricks
- Rattachement : depend du cadre maitre de continuite produit, ne le remplace pas

## Tableau executif Anneau A

| Projet | Besoin initial | Objectif final vise | Etat obtenu | Gap principal | Prochain GO |
|---|---|---|---|---|---|
| Trae | structurer le travail assiste IA sans derive entre workflow, kanban, regles, agents et runtime | une couche Trae gouvernee et opposable, ou les missions IA multi-etapes sont reprises proprement sans ambiguite | socle pre-V1 gele, decisions canoniques produites, reprise canonique en place | encore pre-V1, agents/skills non ouverts comme couche runtime active | `GO_OT_TRAE_AGENTS_V1_OPEN_01` si selection explicite |
| OpenClaw | sortir la gouvernance transverse et borner agents/providers/modeles hors du canon execution `opt-trading` | une couche OpenClaw avec politique provider/modele centralisee, gouvernee et bornee | role repo transverse etabli ; cockpit operateur local partiellement reconstruit ; `model_provider_openclaw` prouve | produit OpenClaw global encore peu verrouille | audit/synthese OpenClaw ou lot provider policy V1 |
| Hugging Face | exposer certaines surfaces sans deplacer la source de verite hors du repo canonique | une couche Hugging Face de publication propre avec portail public, tools prives, MCP public, assets publics | `portal_static` documente, surfaces nommees, publication target only explicite | peu de preuve d'usage bout-en-bout, chronologie produit limitee | audit publication Hugging Face ou cadrage d'usage des surfaces |
| DeepSeek / Ollama local | avoir une IA locale exploitable sans dependance exclusive aux APIs externes, avec separation thinking / response | un hub DeepSeek / Ollama local stable, menu unifie, thinking/response pilotables, logs et artefacts lisibles | `scripts/student` = runtime canonique actuel, `deepseek_hub` = hub reel d'unification, `deepseek-student` = surface operateur | cible finale unique non figee ; `deepseek_hub` reste candidat d'unification le plus fort | audit runtime DeepSeek / clarification runtime canonique |

### Trae
- besoin : structurer le travail assiste IA sans derive entre workflow, kanban, regles, agents et runtime
- objectif final : couche Trae gouvernee et opposable ; missions IA multi-etapes reprises proprement sans ambiguite
- plan : socle pre-V1 documente ; gel `Rules / Agents / Skills / MCP Policy` sans surpromesse ; decisions / closings / reprise / alignement kanban ; `Rules V1` doc-only avant toute ouverture ulterieure
- etat : `validated_prompt_factory` clos ; `trae_module_validator` actif formalise ; Trae pre-V1 acte ; `Rules V1` ouvert doc-only ; reprise canonique Trae en place
- preuves : `docs/ot/trae/README.md`, `docs/ot/trae/OT_TRAE_SESSION_REPRISE.md`, `docs/ot/kanban/opt_trading_kanban_source_of_truth.md`, `docs/ot/trae/OT_TRAE_PRE_V1_CLOSEOUT_STATUS_DECISION_01.md`
- gap : pas encore de plateforme agents active au-dela du pre-V1 gele
- prochain GO : `GO_OT_TRAE_AGENTS_V1_OPEN_01` si selection explicite

### OpenClaw
- besoin : sortir la gouvernance transverse et borner agents/providers/modeles hors du canon execution `opt-trading`
- objectif final : couche OpenClaw avec politique provider/modele centralisee, gouvernee et bornee
- plan : `openclaw` = repo de gouvernance transverse ; `opt-trading` = cockpit operateur local borne + politique provider/modele
- etat : role transverse fixe ; cockpit operateur local partiellement reconstruit ; `model_provider_openclaw` present ; providers/modeles autorises ; matrice agent -> modele/fallback ; regle : aucun agent ne choisit directement son provider/modele
- preuves : `modules/menu_openclaw/docs/GO_OPENCLAW_CHAIN_03.md`, `modules/menu_openclaw/docs/GO_OPENCLAW_USAGE_EXAMPLES_09.md`, `modules/model_provider_openclaw/README.md`
- gap : produit OpenClaw global complet pas encore verrouille
- prochain GO : audit/synthese OpenClaw ou lot provider policy V1

### Hugging Face
- besoin : exposer certaines surfaces sans deplacer la source de verite hors du repo canonique
- objectif final : couche Hugging Face de publication propre avec portail public, tools prives, MCP public, assets publics
- plan : `opt-trading/sot/mainline` reste source de verite ; Hugging Face = publication target only ; separation portail public / tools prives / MCP public / assets publics
- etat : `portal_static` documente ; surfaces Hugging Face nommees ; publication target only explicite
- preuves : `modules/hf_free_platform/spaces/portal_static/README.md`
- gap : peu de preuve d'usage bout-en-bout ; chronologie produit limitee
- prochain GO : audit publication Hugging Face ou cadrage d'usage des surfaces

### DeepSeek / Ollama local
- besoin : avoir une IA locale exploitable sans dependance exclusive aux APIs externes ; separation thinking / response
- objectif final : hub DeepSeek / Ollama local stable, menu unifie, thinking/response pilotables, logs et artefacts lisibles
- plan : installer Ollama local ; separer `deepseek_thinking` et `deepseek_response` ; preferer API HTTP a `ollama run` ; unifier via `deepseek_hub`
- etat : `scripts/student` constitue le runtime reel / canonique actuel ; `deepseek_hub` est le hub reel d'unification ; `deepseek-student` est la surface operateur reelle
- preuves : `journal.md`, `modules/deepseek_hub/README.md`
- gap : aucune cible finale unique n'est encore figee repo-sourcee ; `deepseek_hub` est le candidat d'unification le plus fort, mais la destination finale canonique n'est pas close
- prochain GO : audit runtime DeepSeek / clarification runtime canonique

## Registre court Anneau B

| Nom | Statut | Pourquoi il reste dans la continuite | Pourquoi il n'est pas prioritaire dans cette passe | Point de reprise minimal |
|---|---|---|---|---|
| Hermes | PARTIEL | vrai axe experimental de generation / memoire de travail, avec bridge borne vers OpenClaw | trop borne et explicitement non generalise pour devenir centre de gravite principal | `docs/hermes/00_overview.md`, `docs/hermes/03_bridge_openclaw.md`, `docs/hermes/HERMES_OPENCLAW_BRIDGE_CASE_01_RESULT_2026-04-09.txt` |
| Claude | PARTIEL | role reel dans le journal comme executeur documentaire, notamment pour LocalCMS | interface externe / assistant, moins couche repo-native canonique | `journal.md` passages `workflow-claude` et LocalCMS |
| ChatGPT | PARTIEL | role reel comme source de conversation capturee puis orchestrateur/validateur dans certaines sequences | interface externe / assistant, pas produit repo-natif principal | `journal/canon/JOURNAL_CANON_FULL_20260301_071931.md`, `journal.md` passages ChatGPT |
| MiMo | A REVALIDER | vraie ligne specialisee trading via `mimo_open_observer` | le nom fort du produit reste peu verrouille dans cette passe thematique | `modules/mimo_open_observer/README.md` |
| Antigravity | PARTIEL | chantier specialise reel et historiquement utile | peripherique a l'axe multi IA principal de cette passe | relecture dediee des closings/notes Antigravity |
| OpenAI | PARTIEL | fondation historique importante pour journalisation et reflexion sur agents/tool calling | backend / assistant externe plutot que produit repo-structurant actuel | `journal/canon/JOURNAL_CANON_FULL_20260301_071931.md`, `journal.md` passages OpenAI |
| llm_wiki_minimal | PARTIEL | utile comme sas de pre-consolidation autour de l'ecosysteme IA/doc | role transverse, pas produit prioritaire ici | `docs/governance/REPO_ROLE.md` |
| hf_trading | PARTIEL | extension repo utile proche de l'axe Hugging Face | bootstrap encore leger, pas assez riche pour Anneau A | `journal.md` passages bootstrap `hf_trading` |

## Conclusion operatoire

- cette coupe thematique confirme 4 centres de gravite actuels :
  - Trae
  - OpenClaw
  - Hugging Face
  - DeepSeek / Ollama local
- Anneau B conserve les autres axes utiles sans brouiller la lecture prioritaire
- suite logique :
  1. figer une synthese canonique Trae
  2. figer une synthese canonique OpenClaw
  3. clarifier la carte produit Hugging Face spaces
  4. clarifier la cible finale DeepSeek entre runtime actuel, candidat d'unification et destination canonique non figee
