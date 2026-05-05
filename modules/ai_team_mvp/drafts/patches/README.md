# AI Team MVP — Patches (PATCH_DRAFT)

Dossier de sortie autorise pour les propositions de patch (PATCH_DRAFT).

Contrat :
- Les fichiers ici sont des PROPOSITIONS, jamais appliquees automatiquement.
- Aucune modification du fichier cible n'est faite par le runner.
- Validation humaine (Gatekeeper) obligatoire avant toute application manuelle.
- Format : Markdown avec section PATCH_PROPOSAL en diff-like.

Format de nommage : `<task_id>_<timestamp>.md`

Exemple : `analyzer_patch_draft_smoke_01_20260505_130000.md`

## Application manuelle (apres validation humaine)

1. Lire la proposition dans ce dossier.
2. Verifier la section PATCH_PROPOSAL.
3. Appliquer manuellement les changements (editeur, pas `git apply`).
4. Commiter manuellement apres revue.
