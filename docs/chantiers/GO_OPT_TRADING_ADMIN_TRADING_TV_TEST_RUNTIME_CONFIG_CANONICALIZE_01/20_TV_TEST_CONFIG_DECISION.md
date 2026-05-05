---
doc_id: GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01_20_DECISION
doc_type: chantier/decision
repo: opt-trading
branch: go/GO_OPT_TRADING_ADMIN_TRADING_TV_TEST_RUNTIME_CONFIG_CANONICALIZE_01
machine: admin-trading
status: active
lifecycle_stage: config_canonicalize
---

# 20_TV_TEST_CONFIG_DECISION — Decision de canonicalisation

## Options evaluees

### Option 1 : Fichier example dans `state/`

`state/risk_config.example.json` avec les valeurs safe.

**Rejetee** : `state/` est entierement dans `.gitignore`. Tout fichier
dans ce repertoire est ignore par git. Un `git add -f` contournerait
la regle mais cree une exception non voulue.

### Option 2 : Fichier example hors `state/`

Ex: `config_examples/risk_config.example.json` a la racine.

**Rejetee** : Aucun precedent de dossier `config_examples/` dans le repo.
Les `.example` existants sont dans les dossiers de modules ou a la racine
(`.env.example`). `risk_config.json` est un fichier de state runtime,
pas un fichier de config de module.

### Option 3 : Documenter le pattern dans le chantier

Le pattern canonique est documente dans `30_SAFE_CONFIG_PATTERN.md`.
Aucun fichier example cree dans le repo. La config reste runtime locale.

### Option 4 : Ajouter TV_TEST dans le code (hardcode default)

Modifier `webhook_server.py` pour que `load_risk_config()` fournisse un
fallback safe pour `TV_TEST` quand l'entree est absente.

**Rejetee** : Modification de code runtime non necessaire. La config
runtime est le mecanisme prevu. Le code est deja correct.

## Decision

**Option 3 retenue** : Documenter le pattern canonique dans ce chantier.

### Justification

1. La config est locale a admin-trading, comme prevu par `.gitignore`
2. Le pattern est simple (5 lignes JSON, valeurs safe par defaut)
3. Aucune modification de `.gitignore` ni de code
4. Le pattern est reproductible : tout operateur peut recreer la config
5. La documentation dans `30_SAFE_CONFIG_PATTERN.md` sert de reference canonique

### Consequences

- Aucun nouveau fichier dans le repo (hors chantier docs)
- La config `TV_TEST` reste runtime locale
- Le pattern est documente et reproductible
- Si un jour le repo doit fournir un fichier example, le pattern est deja la
