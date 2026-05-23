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

## Packet P1-03 : Gmail/Calendar/Drive

**WARN #9, #10, #11, #13** — Bridges non implémentés + canary absents

### Actions
1. Vérifier l'état actuel : grep des références à gmail/calendar/drive dans le code
2. Vérifier si ces targets sont utilisées dans l'orchestration actuelle
3. Décision HITL : implémenter stubs ou retirer du contrat

### Evidence
- Inventaire des références
- Décision documentée

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

## Packet P3-01 : Strict worker E2E

**WARN #1** — strict-worker-readonly-smoke en PRECHECK_PASS seulement

### Actions
1. Concevoir un test E2E read-only réel
2. L'exécuter sur un worker strict
3. Documenter le résultat

### Evidence
- Script de test E2E
- Résultat d'exécution
