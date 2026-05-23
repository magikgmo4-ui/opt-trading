---
doc_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01_INITIAL_PROJECT_DOC
doc_type: initial_project_doc
go_id: GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01
status: active
updated_at: 2026-05-23
---

# 00_INITIAL_PROJECT_DOC — GO_OPENCLAW_TERMUX_MOBILE_PHASE01_SMOKE_01

## Objectif

Valider en conditions réelles le wrapper `scripts/ai/workers/openclaw_mobile_control.py` depuis une machine (Linux x64) et/ou un environnement Termux (Android). Ce chantier constitue le premier test "smoke" du contrôle mobile pour la Phase 01 non-trading.

## Portée (Scope)

- Validation du wrapper `openclaw_mobile_control.py`.
- Exécution des commandes de base : `status`, `list-jobs`, `preflight`, `run-dry`, `evidence`.
- Vérification de la production de rapports JSON dans `reports/ai/mobile_control/`.
- Vérification de l'écriture dans le ledger local via `ledger_writer.py`.
- Test de blocage pour les jobs non autorisés ou hors périmètre.

## Contraintes de sécurité

- **Non-trading only** : Aucune commande liée au trading ne doit être accessible ou exécutable.
- **Phase 01 only** : Uniquement les jobs définis dans la Phase 01.
- **No external write** : Pas d'écriture en dehors des répertoires de rapports et du ledger local.
- **No signal/trading** : Pas d'émission de signaux ou d'ordres.
- **No secrets** : Aucune manipulation de secrets ou de clés API sensibles.
- **No scheduler activation** : Pas d'activation de cron ou de services système.
- **No global index modification** : Ne pas modifier les index globaux du dépôt (sauf documentation de ce chantier).

## Critères de succès

1. Le wrapper répond correctement à toutes les commandes sur une machine de test.
2. Les rapports JSON sont générés avec les métadonnées Git correctes.
3. Le ledger local enregistre les événements `MOBILE_CONTROL`.
4. Les jobs interdits sont explicitement bloqués avec un statut `BLOCKED_WITH_REASON`.
5. Preuve d'exécution (éventuelle) sur Termux si l'environnement est disponible.

## Références

- `scripts/ai/workers/openclaw_mobile_control.py`
- `docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_RUNTIME_CONTROL_WRAPPER_01/50_IMPLEMENTATION_EVIDENCE.md`
- `docs/chantiers/GO_OPENCLAW_TERMUX_MOBILE_JOB_CONTROL_01/40_PHASE01_MOBILE_CONTROL_DRY_RUN.md`
