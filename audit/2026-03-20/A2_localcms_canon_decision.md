# LOCALCMS — DÉCISION CANONIQUE

```
Date     : 2026-03-20
Mission  : GO_LOCALCMS_CANON_DECISION_01
Pivot    : opt-trading / sot/mainline (ce document ne modifie pas opt-trading)
Statut   : LIVRÉ — décision de lecture/pilotage fixée, structure réelle documentée
```

---

## 1. STATUT CANONIQUE DE LOCALCMS

`localcms` est un **projet séparé** de `opt-trading`.

| Attribut | Valeur |
|---|---|
| Nature | repo Git indépendant — NON intégré à `opt-trading` |
| Repo canonique | `C:\Users\ghost\localcms\` (clone local Windows) |
| Sandbox de travail | `C:\Users\ghost\project-localcms\localcms\` |
| Branches actives | 2 branches complémentaires (voir §2) |
| Branches remote | `origin/feature/localcms-shared-explorer-cms-installer-v1` + `origin/tools/localcms-dev-host` |
| Décision de fusion dans `opt-trading` | NON — maintenu séparé |

---

## 2. TOPOLOGIE DES BRANCHES — ÉTAT RÉEL

Le repo `localcms` contient exactement **2 branches** avec une topologie **linéaire** :

```
826a67a  Add Shared Explorer V1 and CMS Installer V1 branch-ready bundle
   ↓
6bbe56a  reintroduce explorer/installer nav entries + fix webhook template
   ↓
28ac50a  fix nav paths (remove spurious space after /)
   ↓
67c0bab  remove duplicate const declarations (typeList/typeIcons/typeLabels)
   ↓
023a636  add canonical reprise pack (docs/claude)
   ↓
ef94833  add host FastAPI sandbox arbitrage doc
   ↓
d26f07f  record validated host sandbox decision and reprise update
         ← feature/localcms-shared-explorer-cms-installer-v1  (branche produit)
   ↓
54da71f  add executable dev host branch files
         ← tools/localcms-dev-host  (surcouche dev host)
```

**Ces deux branches ne sont pas concurrentes. Elles sont séquentielles et complémentaires.**

`tools/localcms-dev-host` est **1 commit en avance** sur `feature/...` et en est une extension directe.

---

## 3. RÔLE DE `feature/localcms-shared-explorer-cms-installer-v1`

### Rôle

**Base produit du CMS** — contient les deux modules fonctionnels et le frontend patché.

### Contenu prouvé (terrain)

| Composant | Fichier | Statut |
|---|---|---|
| Frontend SPA | `localcms-v5.html` | ÉTABLI — 3 corrections appliquées (nav entries, nav paths, duplicate const) |
| M1 Shared Explorer — Frontend | `modules/shared-explorer.js` (602 lignes) | ÉTABLI — validé live sandbox |
| M1 Shared Explorer — Backend | `api/shared_explorer.py` (311 lignes, 4 endpoints GET) | ÉTABLI — lecture seule, realpath sécurisé |
| M2 CMS Installer — Frontend | `modules/cms-installer.js` (364 lignes) | ÉTABLI — install live prouvée |
| M2 CMS Installer — Backend | `api/cms_installer.py` (460 lignes) | ÉTABLI — install hello-mod-v1.0.0.zip réussie |
| Tests M1 | `tests/shared-explorer.test.js` (13 tests) + `smoke.js` (6 smokes) | ÉTABLI |
| Tests M2 | `tests/cms-installer.test.js` (210 tests) + `smoke.js` (260 smokes) | ÉTABLI |
| Pipeline d'intégration | `tests/integration_test_pipeline.py` | ÉTABLI |
| Documentation module | `docs/module/` — PATCH_V5_M1.txt, PATCH_V5_M2.txt, README_M1.md, README_M2.md | présent |
| Pack de reprise | `docs/claude/` — 11 fichiers dont `02_etabli_localcms.txt`, `04_reprise_localcms.txt` | présent |

### Corrections déjà appliquées dans cette branche

| ID | Commit | Fichier | Action |
|---|---|---|---|
| CORR-1 | `6bbe56a` | `localcms-v5.html` | Ajout entrées nav shared_explorer + cms_installer ; fix bug template string webhook |
| CORR-2 | `28ac50a` | `localcms-v5.html` | Correction paths nav `'/ explorer'` → `'/explorer'`, `'/ installer'` → `'/installer'` |
| CORR-3 | `67c0bab` | `localcms-v5.html` | Suppression 12 lignes doublons const (typeList/typeIcons/typeLabels) dans 3 IIFEs |

### Règles à préserver

- ne pas ajouter d'endpoint écriture dans `shared_explorer.py`
- ne pas casser MOD_SHARED_EXPLORER V1
- tout patch futur sur `localcms-v5.html` : minimal, ciblé, diff vérifié avant commit
- conserver `realpath + relative_to()` dans `_resolve_safe()`

---

## 4. RÔLE DE `tools/localcms-dev-host`

### Rôle

**Surcouche d'hébergement local** — ajoute l'outillage de lancement du serveur de développement FastAPI au-dessus de la base produit.

### Contenu additionnel (1 commit au-dessus de `feature/...`)

| Fichier | Description |
|---|---|
| `main.py` | FastAPI app (V101) — monte les routers M1 (`/api/shared/*`) et M2 (`/api/installer/*`) + sert le frontend statique |
| `requirements.txt` | fastapi ≥ 0.111, uvicorn ≥ 0.29, pydantic ≥ 2.0, aiofiles ≥ 23.0 |
| `run.sh` | Lanceur Linux/macOS — `uvicorn main:app --host 0.0.0.0 --port 8000 --reload` |
| `run.bat` | Lanceur Windows — même commande |

### Décision d'arbitrage déjà validée (doc interne 2026-03-18)

L'arbitrage `00_arbitrage_HOST_DEV_SANDBOX.txt` (commit `ef94833`) a fixé :

- **Classe** : B — outillage durable séparé
- **Forme** : versionner les fichiers host dans `tools/localcms-dev-host` distinctement de la branche feature
- **Raison** : ne pas mélanger outillage de dev et évolutions du front-end SPA
- **Validé** par l'opérateur le 2026-03-18

Cette décision est antérieure à la présente passe. Elle est ici reprise et figée dans le bundle d'audit.

---

## 5. DÉCISION DE LECTURE ET PILOTAGE

### Décision retenue

```
localcms = projet séparé, 2 branches complémentaires, pilotage autonome.

Ne pas traiter ces branches comme concurrentes.
Ne pas traiter tools/localcms-dev-host comme une base produit autonome.
Ne pas fusionner localcms dans opt-trading.
```

### Règle de lecture

| Question | Réponse |
|---|---|
| Quelle branche est la base produit ? | `feature/localcms-shared-explorer-cms-installer-v1` |
| Quelle branche contient le host de dev ? | `tools/localcms-dev-host` (superset de feature) |
| Ces deux branches sont-elles concurrentes ? | NON — séquentielles, `tools/...` étend `feature/...` |
| Peut-on promouvoir `tools/...` comme nouvelle base ? | Pas dans cette passe — décision déférée |
| Faut-il merger les deux ? | Pas dans cette passe — décision déférée |
| Faut-il créer une branche `main` ou `develop` ? | Pas dans cette passe — décision déférée |

### Copies locales

| Chemin | Rôle |
|---|---|
| `C:\Users\ghost\localcms\` | Clone canonique — branche courante : `feature/...` |
| `C:\Users\ghost\project-localcms\localcms\` | Sandbox de travail |
| `Desktop/github/localcms-feature-*/` | Snapshot statique de la branche feature (archive) |
| `Desktop/github/localcms-tools-*/` | Snapshot statique de la branche tools (archive) |

---

## 6. ÉTABLI / À CONFIRMER

| Item | État |
|---|---|
| `localcms` = projet séparé de `opt-trading` | ÉTABLI |
| 2 branches actives : `feature/...` + `tools/...` | ÉTABLI |
| Topologie linéaire (tools est 1 commit en avance sur feature) | ÉTABLI |
| M1 (Shared Explorer V1) — validé live sandbox | ÉTABLI |
| M2 (CMS Installer V1) — install live prouvée | ÉTABLI |
| 3 corrections appliquées sur `localcms-v5.html` | ÉTABLI |
| Arbitrage host FastAPI validé opérateur (2026-03-18) | ÉTABLI |
| `feature/...` = base produit | ÉTABLI |
| `tools/...` = surcouche dev host | ÉTABLI |
| Décision de merge / consolidation de branches | À CONFIRMER — déférée, hors passe documentaire |
| Promotion de `tools/...` comme nouvelle baseline | À CONFIRMER — hors passe |
| Prochain chantier produit localcms (M3, M4...) | À CONFIRMER — hors périmètre passe |
| Artefact virtiofs sur `localcms-v5.html` (lock .git/index) | CONNU / se résorbe au prochain git pull/checkout Windows |

---

## 7. LIMITES DE CETTE PASSE

- Aucun accès runtime live au serveur FastAPI (port 8000).
- L'état actuel du sandbox `project-localcms/localcms/` vs le clone canonique `localcms/` n'est pas audité dans cette passe (divergences potentielles non prouvées, hors périmètre).
- Les sessions Claude précédentes (M1–M4 dans `docs/claude/`) contiennent des états intermédiaires qui ne sont pas rejoués ici.
- Le contenu des dossiers `Downloads/claude/localcms_*` (archives de sessions) n'a pas été relu — leur contenu est antérieur aux commits actuels.

---

## 8. POINT DE REPRISE

```
GO_LOCALCMS_CANON_DECISION_01 → LIVRÉ

Ce qui est établi :
  ✓ localcms = projet séparé, repo autonome, NON intégré à opt-trading
  ✓ 2 branches complémentaires (feature = base produit, tools = surcouche dev host)
  ✓ topologie linéaire prouvée (git log --graph)
  ✓ M1 + M2 établis et validés
  ✓ arbitrage host host (2026-03-18) repris et figé dans l'audit

Ce qui reste conditionné à une passe ultérieure :
  → décision de merge / consolidation branches
  → décision sur baseline future (tools comme nouvelle base ?)
  → reprise du développement CMS (M3, M4+)

Prochain chantier portefeuille recommandé :
  GO_ALGO_HF_AUDIT_01
  → qualifier workstream algo_hf / lien avec db-layer (algo-hf-api.service actif)
  → ou GO_OPENCLAW_CANONICAL_REENTRY_01 selon priorité PM
```
