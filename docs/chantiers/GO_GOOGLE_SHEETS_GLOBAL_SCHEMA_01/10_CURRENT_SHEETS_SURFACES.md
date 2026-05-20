---
doc_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01_CURRENT_SHEETS_SURFACES
doc_type: inventory
repo: opt-trading
go_id: GO_GOOGLE_SHEETS_GLOBAL_SCHEMA_01
status: reference
source_kind: canonical
updated_at: 2026-05-19
---

# 10_CURRENT_SHEETS_SURFACES - État actuel (repo)

## Surfaces existantes

| Surface | Preuve | Rôle | Statut |
| --- | --- | --- | --- |
| Daily session controlled sync | `scripts/sheets/sync_daily_session.py` | map journal daily → 1 row Sheets | PRESENT (dry-run default) |
| Tests sync daily session | `tests/e2e/test_sync_daily_session.py` | valider invariants (no write par défaut) | PRESENT |
| Scheduler hook | `scripts/schedule/daily_session.sh` | exécute sync en dry-run (ou controlled-write flag) | PRESENT |
| Mapping stratégie (doc-only) | `docs/chantiers/GO_STRATEGY_CANONICAL_FRAMEWORK_PARENT_01/85_GOOGLE_SHEETS_EXPORT_MAPPING.md` | propose tabs stratégie | PRESENT (doc-only) |

## Limitations actuelles

- le script daily session écrit sur `sheet1` (premier onglet) uniquement
- pas de schéma global partagé (noms tabs et colonnes) pour:
  - strategy_events / perf / registry
  - routing events taxonomisés
- pas de writer transverse réutilisable (hors daily session)

## Conclusion

Une surface Sheets existe déjà et est sûre (dry-run par défaut), mais elle ne suffit pas pour le produit total. Le schéma global doit être fixé avant d’étendre l’écriture à d’autres tabs.

## Validation locale executee

Commande relancee dans cette passe :

```powershell
python -m pytest tests\e2e\test_sync_daily_session.py -q
```

Resultat observe :

```text
26 passed
```

## Ancrage umbrella

- `MASTER_TARGET` : contribuer au produit final total via Google Sheets comme consumer transverse
- `Kanban bundle` : reste la reference principale
- `Prochain item Kanban` : `GO_TELEGRAM_LATENCY_BACKTEST_01`
- `Gaps encore ouverts` : schema tabs 2-5 sans writer, controlled-write toujours borne, single-writer encore absent
