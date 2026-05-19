# Prompt — Cursor Agent (Gated + Institutionnel Light)

Tu appliques un workflow par Gates. Tu t’arrêtes à la fin de chaque Gate et tu demandes: **"GO ou STOP ?"**.

Règles:
- Interdiction de coder avant validation Gates 0–3.
- Interdiction d’éditer des fichiers non référencés via @File / @Folder.
- Interdiction d’inventer API/DB. Tout doit respecter @specs.md, @tasks.md, @db_schema.md, @api_contract.md.
- Backup obligatoire avant tout nouveau module ou correction (patch export + rollback).
- Pour chaque incrément, fournir:
  1) fichiers modifiés/créés
  2) résumé diff (quoi/pourquoi)
  3) commandes
  4) expected output
  5) rollback

Contexte 4 machines:
- admin-trading = repo truth + exécution
- cursor-ai = édition (Cursor)
- db-layer = DB only
- student = compute/tests
