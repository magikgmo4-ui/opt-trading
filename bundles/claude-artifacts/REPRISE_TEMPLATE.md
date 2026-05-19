---
doc_id: BUNDLE_CLAUDE_ARTIFACTS_REPRISE_TEMPLATE
doc_type: bundle/reprise_template
repo: opt-trading
machine: cursor-ai
status: active
lifecycle_stage: operator_pack
links:
  - bundles/claude-artifacts/README.md
  - bundles/claude-artifacts/PROMPT_TEMPLATES.md
---

# REPRISE_TEMPLATE — Claude Artifacts Operator Pack

Template standard pour fiche de reprise operateur cursor-ai.

## Template

```text
# REPRISE — <GO_ID>

## 7_CANONICAL_STATE

Machine actuelle : cursor-ai.

Etat valide :
<inserer les verifications effectuees>

## 13_ESTABLISHED

<inserer les faits etablis>

## 14_HYPOTHESIS

<inserer les hypotheses non verifiees>

## 15_REMAINING_GAP

<inserer les gaps restants>

## 16_TODO

| Priorite | Action | Statut |
| --- | --- | --- |
| P0 | <action critique> | pending |
| P1 | <action importante> | pending |
| P2 | <action non bloquante> | pending |

## 17_RESUME_POINT

Point de reprise :
- Branche : <branche>
- Dernier commit : <hash>
- Prochaine action : <action>
- Prochain GO recommande : <GO_ID>

Commandes de reprise :
```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
<commandes supplementaires>
```
```
