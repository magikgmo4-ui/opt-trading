# 10_WARN_REGISTER

Inventaire des 13 WARN issus du rollout non-trading (PR #690).

## Registre

| # | WARN | Phase | Gate | Description | Priorité |
|---|------|-------|------|-------------|----------|
| 1 | `strict-worker-readonly-smoke` | 01 | PRECHECK_PASS | strict_worker readonly smoke test passé en precheck uniquement, pas en E2E réel | P3 |
| 2 | `.env permissions 0644` | 03 | WARN | `.env` world-readable (0o644) contient `AIRTABLE_API_KEY` | P0 |
| 3 | `REVIEW_DRAFT absent de tasks.index.json` | 05 | WARN | Capability drift : capability `REVIEW_DRAFT` déclarée dans le code mais absente du registre | P1 |
| 4 | `CLOSEOUT_DRAFT absent de tasks.index.json` | 05 | WARN | Capability drift : capability `CLOSEOUT_DRAFT` déclarée dans le code mais absente du registre | P1 |
| 5 | `handoff_bricks.py source manquante` | 05 | WARN | Service handoff référencé mais seul `.pyc` présent, source `.py` absente | P1 |
| 6 | `handoff_renderer.py source manquante` | 05 | WARN | Service handoff référencé mais seul `.pyc` présent, source `.py` absente | P1 |
| 7 | `FastAPI absent dans venv cible` | 06 | WARN | `fastapi_available: false` dans le venv ; localcms conçu pour uvicorn | P2 |
| 8 | `kill switch widget absent LocalCMS` | 06 | WARN | Aucun widget d'arrêt d'urgence dans l'UI LocalCMS | P2 |
| 9 | `Gmail bridge non implémenté` | 07 | WARN | Target `gmail` déclarée mais bridge inexistant | P1 |
| 10 | `Calendar bridge non implémenté` | 07 | WARN | Target `calendar` déclarée mais bridge inexistant | P1 |
| 11 | `Drive bridge non implémenté` | 07 | WARN | Target `drive` déclarée mais bridge inexistant | P1 |
| 12 | `KG repo index entries sans bricks` | 07 | WARN | 3 entrées dans l'index sans implémentation de bricks correspondantes | P1 |
| 13 | `Gmail/Calendar/Drive canary non implémentés` | 08 | WARN | Canary tests pour gmail/calendar/drive absents | P1 |

## Statuts possibles

- `CLOSED` — corrigé et vérifié
- `DECLASSIFIED` — déterminé comme non-bloquant avec justification
- `CARRIED_FORWARD_WITH_REASON` — reporté à un futur GO avec raison documentée

## Évolution des statuts — Final

| # | WARN | Priorité | Statut | Date | Evidence |
|---|------|----------|--------|------|----------|
| 1 | `strict-worker-readonly-smoke` | P3 | **CLOSED** | 2026-05-22 | Test E2E read-only exécuté via `scripts/ai/tests/g05_strict_worker_e2e_readonly.py` ; verdict PASS ; 5 checks : denied_commands (returncode 0), secret_leak (PASS), output_schema (PASS), readonly_contract (PASS), existing_scans (PASS). Rapport : `reports/ai/strict_worker_e2e_readonly.json`. Preuve : 0 git write, 0 secret leak, 0 forbidden write. |
| 2 | `.env permissions 0644` | P0 | **CLOSED** | 2026-05-22 | `chmod 600 .env` appliqué ; `.env` déjà dans `.gitignore` (lignes 14, 37, 87) ; aucun commit historique contenant `.env` ; audit fichiers sensibles : `.secrets/` inexistant (seulement `.example`), `modules/auth/*.py` sans credentials hardcodées, `student/config/shortcut_map.env` et `modules/memory_bricks/config/defaults.env` contiennent uniquement des chemins/config non sensibles (644 acceptable) |
| 3 | `REVIEW_DRAFT absent de tasks.index.json` | P1 | **CLOSED** | 2026-05-22 | Ajouté à `scripts/ai/workers/tasks.index.json` avec autonomy_max A2, sections requises (CONTEXTE_REVUE, FICHIERS_REVUS, OBSERVATIONS, RECOMMANDATIONS, RISQUES, VERDICT_DRAFT_ONLY), preferred_workers incluant glm-5.1 et qwen3.6-plus |
| 4 | `CLOSEOUT_DRAFT absent de tasks.index.json` | P1 | **CLOSED** | 2026-05-22 | Ajouté à `scripts/ai/workers/tasks.index.json` avec autonomy_max A2, sections requises (RESUME, OBJECTIFS_ATTENTS, TRAVAUX_EFFECTUES, ECARTS, WARN_REMAINING, ARTEFACTS_PRODUITS, LEGACY, VERDICT_DRAFT_ONLY), preferred_workers incluant minimax-m2.5 et qwen3.5-plus |
| 5 | `handoff_bricks.py source manquante` | P1 | **DECLASSIFIED** | 2026-05-22 | Source `.py` supprimée de l'arbre ; `.pyc` dans `modules/memory_bricks/app/services/__pycache__/` est un artefact gitignoré ; aucune importation de `handoff_bricks` dans le codebase courant ; fonctionnalité obsolète |
| 6 | `handoff_renderer.py source manquante` | P1 | **DECLASSIFIED** | 2026-05-22 | Source `.py` supprimée de l'arbre ; `.pyc` dans `modules/memory_bricks/app/renderers/__pycache__/` est un artefact gitignoré ; aucune importation de `handoff_renderer` dans le codebase courant ; fonctionnalité obsolète |
| 7 | `FastAPI absent dans venv cible` | P2 | **DECLASSIFIED** | 2026-05-22 | `fastapi==0.129.0` et `uvicorn[standard]==0.41.0` dans `requirements.txt` ; les deux sont installés dans `venv/` ; `api_v2_server.py` les importe et les utilise ; le WARN Phase 06 était un faux positif lié à un venv de test spécifique |
| 8 | `kill switch widget absent LocalCMS` | P2 | **DECLASSIFIED** | 2026-05-22 | Le widget kill switch existe dans `registry/cockpit/automation/index.html` (lignes 21-23 nav, lignes 29-32 overview card, lignes 110-112 styles) ; l'état NORMAL est affiché ; le cockpit consomme les données LocalCMS ; l'UI opérateur est fonctionnelle |
| 9 | `Gmail bridge non implémenté` | P1 | **DECLASSIFIED** | 2026-05-22 | **Retiré du périmètre actif.** Gmail reste documenté comme contrat historique dans `GO_EXTERNAL_APPS_BRIDGE_CONTRACTS_01/20_BRIDGE_CONTRACTS.md` (lignes 134-157) mais n'est plus une surface active : (1) absent de l'enum `requested_app` dans le contrat d'orchestration, (2) aucun module runtime, (3) aucune variable d'env, (4) aucun job scheduler. Réactivation possible dans un GO dédié futur. |
| 10 | `Calendar bridge non implémenté` | P1 | **DECLASSIFIED** | 2026-05-22 | **Retiré du périmètre actif.** Même traitement que Gmail. Bridge contract lignes 159-181 conservé comme documentation historique. Aucun canary Calendar requis. |
| 11 | `Drive bridge non implémenté` | P1 | **CLOSED** | 2026-05-22 | **Drive conservé comme surface active.** Canary packet créé : `scripts/ai/workers/job_packets/GO_DRIVE_CANARY_PACKET_01.json`. 4 opérations documentées : drive-read-folder-health (READ_ONLY), drive-upload-report-canary (WRITE_GATED non destructif), drive-readback-verify (READ_ONLY), drive-compensation-path (rollback manuel HITL). Exécution blocable par absence de credentials `GOOGLE_DRIVE_CREDENTIALS`/`GOOGLE_DRIVE_FOLDER_ID` — packet prêt à exécution. |
| 12 | `KG repo index entries sans bricks` | P1 | **DECLASSIFIED** | 2026-05-22 | L'index `_state/memory_bricks/index/index_full.json` contient 3 entrées (MB-00001, MB-00002, MB-00003) qui ont toutes des fichiers bricks correspondants dans `_state/memory_bricks/bricks/`. Ratio 1:1. Le drift entre 12 entrées d'index et 3 bricks (signalé en Phase 07) a été résolu par nettoyage naturel. |
| 13 | `Gmail/Calendar/Drive canary non implémentés` | P1 | **CLOSED** | 2026-05-22 | Gmail et Calendar retirés du périmètre actif → aucun canary requis. Drive canary packet créé et documenté (cf. WARN #11). Canary Drive non destructif avec readback, ledger, rollback HITL documenté. |

## Résumé final

| Métrique | Valeur |
|----------|--------|
| Total WARN | 13 |
| CLOSED | 6 (#1, #2, #3, #4, #11, #13) |
| DECLASSIFIED | 7 (#5, #6, #7, #8, #9, #10, #12) |
| CARRIED_FORWARD | **0** |
| BLOCKED | **0** |
| Résolution | **13/13** |
