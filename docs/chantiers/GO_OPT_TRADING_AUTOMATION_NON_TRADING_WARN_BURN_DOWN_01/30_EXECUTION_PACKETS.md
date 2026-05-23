# 30_EXECUTION_PACKETS

## Packet P0-01 : .env permissions

**WARN #2** — `.env` world-readable (0o644)

### Actions
1. Vérifier permissions actuelles : `stat -c %a .env`
2. Corriger : `chmod 600 .env`
3. Vérifier qu'aucun autre fichier sensible (`credentials.json`, `*.pem`, `*_key*`) n'est world-readable
4. Ajouter `.env` à `.gitignore` si pas déjà présent
5. Vérifier qu'aucun commit avec `.env` n'existe dans l'historique

### Evidence
- Output de `stat -c %a .env` avant/après
- Audit des permissions des fichiers sensibles

---

## Packet P1-01 : Registry drift AI-team

**WARN #3, #4** — `REVIEW_DRAFT` / `CLOSEOUT_DRAFT` absents de `tasks.index.json`

### Actions
1. Localiser `tasks.index.json` dans le repo
2. Vérifier les capabilities déclarées dans le code (orchestration contract)
3. Ajouter les entrées manquantes ou déclasser les capabilities du contrat
4. Vérifier la cohérence contractuelle

### Evidence
- Diff du fichier registry
- Vérification croisée code ↔ registry

---

## Packet P1-02 : Sources handoff manquantes

**WARN #5, #6** — `handoff_bricks.py` / `handoff_renderer.py` `.pyc` only

### Actions
1. Localiser les `.pyc` dans le repo
2. Vérifier l'utilisation réelle de ces modules
3. Restaurer les sources `.py` ou documenter la suppression volontaire

### Evidence
- Localisation des fichiers
- Décision documentée

---

## Packet P1-03 : Gmail/Calendar/Drive (RÉSOLU)

**WARN #9, #10, #11, #13** — Bridges non implémentés + canary absents

### Décision HITL
- **Gmail (#9)** → RETIRÉ du périmètre actif. Contrat historique conservé dans `20_BRIDGE_CONTRACTS.md`.
- **Calendar (#10)** → RETIRÉ du périmètre actif. Contrat historique conservé.
- **Drive (#11)** → CONSERVÉ comme surface active. Canary packet créé.
- **Canaries (#13)** → Gmail/Calendar : aucun canary requis (retirés). Drive : canary packet créé.

### Actions exécutées
1. Inventaire des références : grep complet — gmail/calendar/drive absents de l'enum `requested_app` du contrat d'orchestration, aucun module runtime, aucune variable d'env
2. Décision HITL documentée : retrait Gmail/Calendar, conservation Drive
3. Drive canary packet créé : `scripts/ai/workers/job_packets/GO_DRIVE_CANARY_PACKET_01.json`

### Opérations Drive canary
| ID | Type | Description | Readback | Rollback |
|----|------|-------------|----------|----------|
| drive-read-folder-health | READ_ONLY | Lire métadonnées dossier Drive | Oui | N/A |
| drive-upload-report-canary | WRITE_GATED | Upload fichier .canary.txt non destructif | Oui | Manuelle HITL |
| drive-readback-verify | READ_ONLY | Vérifier contenu du canary après upload | Oui | N/A |
| drive-compensation-path | READ_ONLY | Instructions rollback manuel | N/A | Documenté |

### État Drive
- Mode : WRITE_GATED
- Credentials requis : `GOOGLE_DRIVE_CREDENTIALS`, `GOOGLE_DRIVE_FOLDER_ID`
- Packet prêt à exécution (bloqué par credentials uniquement)
- Non destructif : pas de delete, pas de modif permissions, pas de modif fichiers existants

---

## Packet P1-04 : KG repo index entries

**WARN #12** — 3 index entries sans bricks

### Actions
1. Localiser l'index KG concerné
2. Identifier les 3 entrées sans implémentation
3. Implémenter les bricks stubs ou retirer les entrées

### Evidence
- Localisation et contenu de l'index
- Corrections apportées

---

## Packet P2-01 : FastAPI venv

**WARN #7** — FastAPI absent du venv cible

### Actions
1. Vérifier la dépendance réelle dans le code
2. Vérifier si `uvicorn` est présent
3. Documenter la stratégie runtime (install fastapi ou utiliser uvicorn seul)

### Evidence
- Vérification du requirements.txt / pyproject.toml
- Décision documentée

---

## Packet P2-02 : Kill switch widget

**WARN #8** — Absence de kill switch dans LocalCMS

### Actions
1. Vérifier le template LocalCMS actuel
2. Proposer un emplacement pour le widget
3. Créer une proposition HITL avec maquette textuelle

### Evidence
- Proposition documentée
- Emplacement identifié

---

## Packet P3-01 : Strict worker E2E (RÉSOLU)

**WARN #1** — strict-worker-readonly-smoke en PRECHECK_PASS seulement

### Actions exécutées
1. Test E2E read-only conçu : `scripts/ai/tests/g05_strict_worker_e2e_readonly.py`
2. Exécuté avec succès — verdict **PASS**
3. Rapport produit : `reports/ai/strict_worker_e2e_readonly.json`

### Résultat
| Check | Statut |
|-------|--------|
| denied_commands scan | returncode 0 (PASS) |
| secret leak check | PASS — 0 credentials leaks |
| output schema check | PASS — 0 issues |
| readonly contract validation | PASS — 4/4 checks |
| existing scans (x2) | PASS — both returncode 0 |
| **Synthèse** | **3/3 checks PASS — VERDICT PASS** |

### Preuve read-only
- 0 git write (add/commit/push/rebase/merge)
- 0 secret leak (api_key/token/password)
- 0 forbidden write to runtime dirs
