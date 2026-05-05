---
doc_id: BUNDLE_CLAUDE_ARTIFACTS_PROMPT_TEMPLATES
doc_type: bundle/prompt_templates
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_pack
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/claude-artifacts/NO_COMMIT_RULES.md
---

# PROMPT_TEMPLATES — Claude Artifacts Operator Pack

Templates de prompts standard pour operateur cursor-ai.

## Template 1 — Prompt de reprise

```text
GO_REPRISE_<GO_ID>

ROLE
Tu es worker doc-ops pour opt-trading.
Tu reprends le GO <GO_ID> depuis son dernier point de reprise.

REPO
- Repo canonique : C:\Users\ghost\opt-trading
- Branche canonique : sot/mainline
- Machine actuelle : cursor-ai

ETAT VALIDE
- <inserer etat valide>

OBJECTIF
<inserer objectif>

A NE PAS FAIRE
- Ne pas ouvrir admin-trading.
- Ne pas modifier runtime.
- Ne pas committer secrets, .env, tokens ou outputs sensibles.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas marquer Bundles produit comme ferme.

ETAPES
1. Verifier Git :
   git status --short --branch
   git branch --show-current
   git log --oneline -10

2. Synchroniser :
   git fetch origin --prune
   git checkout sot/mainline
   git pull --rebase origin sot/mainline

3. Creer la branche :
   git checkout -b go/<GO_ID>

4. <inserer etapes specifiques>

5. Verifier le diff :
   git status --short --branch
   git diff --stat
   git diff --name-only

6. Commit :
   git add <fichiers>
   git commit -m "docs: <message>"

7. Push :
   git push -u origin go/<GO_ID>

VERDICT PASS SI
- <inserer criteres de PASS>
```

## Template 2 — Prompt de review

```text
GO_REVIEW_<GO_ID>

ROLE
Tu es reviewer doc-ops pour opt-trading.
Tu revises le GO <GO_ID> avant merge.

REPO
- Repo canonique : C:\Users\ghost\opt-trading
- Branche source : go/<GO_ID>
- Branche cible : sot/mainline
- Machine actuelle : cursor-ai

OBJECTIF
Verifier que le contenu du GO <GO_ID> est conforme aux invariants avant merge.

VERIFICATIONS OBLIGATOIRES
- [ ] Doc-only (pas de runtime)
- [ ] Aucun admin-trading ouvert
- [ ] Aucun secret / .env / token
- [ ] alert_webhook non marque comme ferme
- [ ] Bundles produit non marque comme ferme
- [ ] Fichiers crees conformes a la spec

VERDICT
PASS si toutes les verifications sont OK.
FAIL avec raison explicite sinon.
```

## Template 3 — Prompt de merge doc-only

```text
GO_MERGE_<GO_ID>

ROLE
Tu es worker doc-ops pour opt-trading.
Tu merger la PR du GO <GO_ID> dans sot/mainline.

REPO
- Repo canonique : C:\Users\ghost\opt-trading
- Branche source : go/<GO_ID>
- Branche cible : sot/mainline
- Machine actuelle : cursor-ai

OBJECTIF
Merger la PR dans sot/mainline en verifiant la conformite.

ETAPES
1. Ouvrir PR :
   gh pr create --title "<titre>" --body "<body>" --base sot/mainline --head go/<GO_ID>

2. Verifier diff :
   - doc-only
   - aucun runtime
   - aucun admin-trading
   - aucun secret

3. Merger :
   gh pr merge <PR_NUM> --merge --delete-branch

4. Sync local :
   git fetch origin --prune
   git checkout sot/mainline
   git pull --rebase origin sot/mainline

VERDICT PASS SI
- PR mergee
- Branche source supprimee
- sot/mainline synced localement
```

## Template 4 — Prompt de no-runtime safety check

```text
SAFETY_CHECK_<GO_ID>

ROLE
Tu es safety checker pour opt-trading.
Tu verifies que le GO <GO_ID> ne contient aucune modification runtime.

REPO
- Repo canonique : C:\Users\ghost\opt-trading
- Machine actuelle : cursor-ai

VERIFICATIONS
- [ ] Aucun fichier dans modules/ modifie (hors docs/)
- [ ] Aucun fichier dans scripts/ modifie (hors docs/)
- [ ] Aucun systemd / service / timer
- [ ] Aucun webhook serveur
- [ ] Aucun risk engine
- [ ] Aucun .env / secrets / tokens
- [ ] Aucun output live sensible

COMMANDE DE VERIFICATION
git diff sot/mainline...go/<GO_ID> --stat
git diff sot/mainline...go/<GO_ID> --name-only | grep -v "^docs/" | grep -v "^bundles/"

VERDICT
PASS si tous les fichiers modifies sont dans docs/ ou bundles/.
FAIL si des fichiers runtime, systemd, webhook, risk engine ou secrets sont touches.
```

## Template 5 — Prompt de handoff IDE

```text
GO_HANDOFF_<GO_ID>

ROLE
Tu es worker handoff pour opt-trading.
Tu produis le handoff IDE du GO <GO_ID> pour reprise par un operateur.

OBJECTIF
Produire un point de reprise clair et executable.

CONTENU OBLIGATOIRE
1. Machine actuelle et branche de travail
2. Etat valide (canonical state)
3. Dernier commit / PR merge
4. Fichiers crees / modifies
5. Invariants respectes
6. Prochain GO recommande
7. Commandes de reprise

FORMAT
- 7_CANONICAL_STATE
- 13_ESTABLISHED
- 15_REMAINING_GAP
- 16_TODO
- 17_RESUME_POINT
```
