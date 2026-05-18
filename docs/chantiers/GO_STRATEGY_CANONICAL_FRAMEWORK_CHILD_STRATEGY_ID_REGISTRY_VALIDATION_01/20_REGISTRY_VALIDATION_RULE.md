---
go_id: GO_STRATEGY_CANONICAL_FRAMEWORK_CHILD_STRATEGY_ID_REGISTRY_VALIDATION_01
doc_type: validation_rule
repo: opt-trading
status: open
surface: doc-only
created_at: 2026-05-18
---

# 20_REGISTRY_VALIDATION_RULE

## Règle de validation strategy_id vs registry

---

## 1_REGLE

```text
Tout strategy_id utilisé dans le pipeline DOIT figurer dans
95_STRATEGY_REGISTRY.md.

Les exceptions documentées (tests, legacy) sont tolérées en mode WARNING_ONLY.
```

---

## 2_MODE_INITIAL

Mode : **WARNING_ONLY**

Comportement :

```text
- Détecter tout strategy_id inconnu
- Afficher un WARNING avec la surface, le fichier, la valeur
- Ne pas bloquer l'exécution
- Ne pas modifier les fichiers source
- Code retour 0 si warning, 1 si erreur de lecture registry
```

Raison du mode warning :

```text
7 valeurs test-only non registrées existent dans les tests.
Un hard-fail bloquerait les tests sans bénéfice immédiat.
Le mode warning permet l'audit sans casse.
```

---

## 3_MODE_FUTUR_RECOMMANDÉ

Après ce GO, validation envisageable :

```text
Phase 1 (ce GO)  : WARNING_ONLY — détection + rapport
Phase 2 (futur)  : CI CHECK — warning dans CI sans bloquer
Phase 3 (futur)  : HARD_FAIL — blocage CI pour strategy_id inconnu en production
Phase 4 (futur)  : GIT_HOOK — pre-commit validation
```

---

## 4_LIMITES

```text
- Le validateur lit la registry Markdown, pas de base de données
- Ne valide pas le contenu des events, seulement les string
- Ne remplace pas un schéma JSON structuré
- Ne bloque pas le runtime
- Ne couvre pas les strategy_id générés dynamiquement (aucun identifié)
```
