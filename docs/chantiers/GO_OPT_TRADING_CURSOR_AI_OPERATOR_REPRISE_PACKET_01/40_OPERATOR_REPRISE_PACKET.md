---
doc_id: GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01_40_OPERATOR_REPRISE_PACKET
doc_type: chantier/operator_reprise_packet
repo: opt-trading
machine: cursor-ai
status: active
links:
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
  - bundles/claude-artifacts/REPRISE_TEMPLATE.md
  - bundles/OPERATOR_FLOW.md
---

# 40_OPERATOR_REPRISE_PACKET

Fiche operationnelle autonome de reprise operateur cursor-ai.

## Point de redemarrage

```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
# Verifier HEAD : doit contenir PR #208
git log --oneline -1
# Attendu : 03fe829 ou descendant
```

## Quoi lire et dans quel ordre

### Ordre de lecture recommande

1. **Routage machine** : `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md`
   - Bloc CURSOR_AI : ce qui est actif, ferme, blocked.

2. **Plan parent** : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_PARENT_OPERATIONAL_PLAN_01/`
   - `80_NEXT_GO_SEQUENCE.md` — ordre recommande.
   - `70_ADMIN_TRADING_GATE.md` — conditions gate.

3. **Pack Claude artifacts** : `bundles/claude-artifacts/`
   - `README.md` — survol du pack.
   - `PROMPT_TEMPLATES.md` — 5 templates de prompts.
   - `REPRISE_TEMPLATE.md` — template de fiche de reprise.
   - `NO_COMMIT_RULES.md` — regles de securite.

4. **Bundles workflow** : `bundles/`
   - `ACTIVE_WORKFLOW.md` — definition du workflow.
   - `BUNDLE_TYPES.md` — 7 types de bundles.
   - `OPERATOR_FLOW.md` — flux 8 etapes.
   - `NO_RUNTIME_NO_SENSITIVE_RULES.md` — limites.

5. **Pre-admin gate** : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_ALERT_WEBHOOK_PRE_ADMIN_GATE_SPEC_01/`
   - `20_PRE_ADMIN_GATE_REQUIREMENTS.md` — prerequis.
   - `40_VALIDATION_MATRIX.md` — 12 checks.
   - `60_OPEN_ADMIN_TRADING_CRITERIA.md` — criteres d'ouverture.

6. **Ce packet** : `docs/chantiers/GO_OPT_TRADING_CURSOR_AI_OPERATOR_REPRISE_PACKET_01/`
   - `40_OPERATOR_REPRISE_PACKET.md` — ce fichier.
   - `50_NEXT_GO_OPTIONS.md` — options prochaines.

## Quels fichiers utiliser pour les prompts

| Situation | Fichier a utiliser |
| --- | --- |
| Reprendre un GO existant | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 1 |
| Review avant merge | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 2 |
| Merger un GO doc-only | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 3 |
| Verifier no-runtime | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 4 |
| Produire handoff IDE | `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 5 |
| Creer fiche de reprise | `bundles/claude-artifacts/REPRISE_TEMPLATE.md` |
| Creer un bundle | `bundles/OPERATOR_FLOW.md` |
| Verifier avant commit | `bundles/NO_RUNTIME_NO_SENSITIVE_RULES.md` |

## Quoi ne pas faire

- Ne pas ouvrir admin-trading sans la phrase "chantier pour admin-trading".
- Ne pas modifier de fichiers hors `docs/` et `bundles/`.
- Ne pas committer de secrets, .env, tokens, payloads reels.
- Ne pas marquer alert_webhook comme ferme.
- Ne pas marquer Bundles produit comme ferme.
- Ne pas toucher systemd, webhook_server.py, risk engine.

## Commandes de reprise

```bash
# Sync
git fetch origin --prune && git checkout sot/mainline && git pull --rebase origin sot/mainline

# Creer branche pour un nouveau GO
git checkout -b go/GO_<ID>

# Verifier diff avant commit
git diff --cached --name-only | grep -vE "^(docs/|bundles/)"  # doit etre vide

# Verifier secrets
git diff --cached | grep -iE "(password|secret|token|key=|api_key|\.env)"

# PR
gh pr create --title "docs: <message>" --base sot/mainline --head go/GO_<ID>
gh pr merge <NUM> --merge --delete-branch
```

## Conventions GO

- Branche : `go/GO_OPT_TRADING_CURSOR_AI_<DESCRIPTION>_<XX>`
- Commit : `docs: <message court>`
- PR : verifier diff → gh pr create → gh pr merge
- Inbox : toujours creer `docs/index/inbox/GO_<ID>.md`

## Sequence terminee

Positions 1-4 de la sequence cursor-ai executees. Voir `50_NEXT_GO_OPTIONS.md` pour les suites possibles.

## RISKS

- À qualifier.
