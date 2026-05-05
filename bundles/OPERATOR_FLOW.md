---
doc_id: BUNDLES_OPERATOR_FLOW_01
doc_type: bundle/operator_flow
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: workflow_active
links:
  - bundles/ACTIVE_WORKFLOW.md
  - bundles/BUNDLE_TYPES.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
---

# OPERATOR_FLOW — Flux operateur Bundles cursor-ai

## Flux standard

### Etape 1 — Identifier source

Identifier la matiere source a packager :
- artefacts Claude / IDE ;
- docs de chantier existants ;
- templates de prompts ;
- regles de securite ;
- fiches de reprise.

### Etape 2 — Classifier bundle

Determiner le type de bundle (voir `BUNDLE_TYPES.md`) :
- reprise bundle ;
- operator pack ;
- IDE handoff bundle ;
- prompt bundle ;
- PR merge bundle ;
- closeout bundle.

### Etape 3 — Extraire contenu stable

Ne garder que le contenu stable et reproductible :
- templates (pas d'instances avec donnees reelles) ;
- regles (pas d'hypotheses non verifiees) ;
- procedures (pas de logs d'execution) ;
- invariants (pas d'etat temporaire).

### Etape 4 — Creer pack / docs

Structurer le bundle :
- `bundles/<bundle-name>/` pour les packs reutilisables ;
- `docs/chantiers/<GO_ID>/` pour les chantiers documentaires.

Inclure au minimum :
- README avec objectif et invariants ;
- Templates / prompts le cas echeant ;
- Regles no-secret / no-runtime.

### Etape 5 — Verifier no-runtime / no-secret

Checklist avant commit :
- [ ] Aucun fichier runtime (hors docs/ et bundles/)
- [ ] Aucun systemd / service / timer
- [ ] Aucun webhook serveur
- [ ] Aucun risk engine
- [ ] Aucun secret / .env / token
- [ ] Aucun output live sensible
- [ ] Aucun payload reel
- [ ] Chemins anonymises

### Etape 6 — Commit doc-only

```bash
git add bundles/<bundle-name>/ docs/chantiers/<GO_ID>/ docs/index/inbox/<GO_ID>.md
git commit -m "docs: <message>"
```

### Etape 7 — PR

```bash
gh pr create --title "<titre>" --body "<body>" --base sot/mainline --head go/<GO_ID>
gh pr merge <PR_NUM> --merge --delete-branch
```

### Etape 8 — Reprise

Sync local :
```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
```

Mettre a jour la fiche de reprise (`REPRISE_TEMPLATE.md`).

## Flux en cas d'anomalie

Si une verification echoue :
1. Documenter l'anomalie dans le GO courant.
2. Ne pas committer tant que l'anomalie n'est pas resolue.
3. Si secret detecte : revert, rotation, documentation.

## Lien avec Claude artifacts

Le pack `bundles/claude-artifacts/` fournit les templates de prompts pour chaque etape du flux :
- Template 1 (reprise) → Etape 1
- Template 4 (safety check) → Etape 5
- Template 3 (merge) → Etape 7
- Template 5 (handoff) → Etape 8
