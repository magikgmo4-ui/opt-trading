# HANDOFF — Operator Export cursor-ai

Instructions de handoff pour un nouvel operateur cursor-ai.

## Demarrage

```bash
git fetch origin --prune
git checkout sot/mainline
git pull --rebase origin sot/mainline
git log --oneline -5
```

## Etat actuel

- **Machine** : cursor-ai.
- **Dernier merge** : PR #211 (Option B — Bundles maintenance).
- **Prochain GO** : voir `50_NEXT_GO_OPTIONS.md`.
- **Admin-trading** : FERME. Phrase requise : "chantier pour admin-trading".

## Lecture prioritaire

1. `bundles/operator-export/README.md` — ce dossier.
2. `bundles/operator-export/EXPORT_MANIFEST.json` — inventaire.
3. `bundles/CURSOR_AI_OPERATOR_REPRISE_PACKET.md` — reprise rapide.
4. `docs/index/MACHINE_WORK_SPLIT_ANTI_CONFLICT_01.md` — bloc CURSOR_AI.
5. `bundles/claude-artifacts/README.md` — pack operateur.

## Actions standard

- **Creer un GO** : utiliser `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 1.
- **Merger un GO** : utiliser `bundles/claude-artifacts/PROMPT_TEMPLATES.md` > Template 3.
- **Verifier securite** : utiliser `bundles/claude-artifacts/CHECKLIST_EXECUTION.md`.

## Invariants

- Doc-only pour cursor-ai.
- Admin-trading ferme sans phrase d'activation.
- alert_webhook = ACTIVE_CONTINUITY (ne pas fermer).
- Bundles produit = non ferme.
- Runtime = non modifie.

## Reprise

Ce handoff est autonome. Un nouvel operateur peut reprendre l'etat cursor-ai sans la conversation originale.
