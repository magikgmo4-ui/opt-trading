---
doc_id: DEV_CONTRACTS_V1
doc_type: dev_operational_contracts
repo: opt-trading
status: active
version: v1
updated_at: 2026-06-15
---

# DEV_CONTRACTS — Contrats opérationnels de développement

Règles non-négociables pour agents IA opérant sur un mount Windows/Linux.

---

## CONTRACT_01 — Safe Rewrite : écriture sûre sur mount Windows/Linux

### Problème

Mount local Windows (`C:\Users\ghost\opt-trading\`) / Linux (`/sessions/.../mnt/opt-trading/`).

Quand Edit/Write tool Windows modifie un fichier :
- Le mount Linux ne met pas toujours à jour le mtime Linux.
- Python vérifie la validité du .pyc via le mtime dans le header pyc.
- Si mtime Linux source == mtime .pyc -> cache valide -> Python charge l'ANCIEN bytecode.

Incidents 2026-06-15 : spcx_composite_score.py tronqué chargé depuis cache pyc.
Résultat : tests passant/échouant sur versions incohérentes du code.

### Règle officielle

Pour toute réécriture complète d'un fichier Python/JSON/YAML critique :

  NE PAS utiliser Edit/Write tool Windows pour réécritures complètes.
  UTILISER bash heredoc + touch + suppression __pycache__.

### Protocole (3 étapes)

Étape 1 — Écriture via bash heredoc
  cat > path/to/file.py << 'EOF'
  # contenu complet
  EOF

Étape 2 — Touch explicite
  touch path/to/file.py

Étape 3 — Purge __pycache__ (Python uniquement)
  find "$(dirname path/to/file.py)" -name "*.pyc" -path "*__pycache__*" -delete 2>/dev/null || true

### Script utilitaire

scripts/safe_rewrite.sh automatise ces 3 étapes.

### Quand appliquer

| Situation | Action |
|-----------|--------|
| Réécriture complète .py | Obligatoire : heredoc + touch + purge pyc |
| Réécriture complète .json/.yaml | Obligatoire : heredoc + touch |
| Patch partiel Edit tool | Acceptable + touch + vérification |
| Nouveau fichier Write tool | Ajouter touch après création |

---

## Historique incidents

| Date | Fichier | Symptôme | Fix |
|------|---------|----------|-----|
| 2026-06-15 | spcx_composite_score.py | Tronqué, ancien .pyc chargé (poids incorrects) | Heredoc bash |
| 2026-06-15 | spcx_score_reader.py | Tronqué + stray a, mtime non mis à jour | Heredoc bash |
| 2026-06-15 | producers.json | Corrompu après Edit tool Windows | Heredoc bash |

Voir aussi : scripts/safe_rewrite.sh
