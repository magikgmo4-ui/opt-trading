# ALGO_HF — AUDIT DE QUALIFICATION CANONIQUE

```
Date     : 2026-03-20
Mission  : GO_ALGO_HF_AUDIT_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ — qualification canonique produite sur la base des sources terrain disponibles
```

---

## 1. DÉFINITION / QUALIFICATION DE `algo_hf`

`algo_hf` est un **workstream/projet séparé** de `opt-trading`.

Il dispose d'un **service runtime actif** sur la machine `db-layer` :
- nom du service systemd : `algo-hf-api.service`
- description systemd : `algo_hf API (FastAPI webhook)`
- état snapshot 2026-02-26 : `loaded active running`

Ce workstream n'est **pas intégré à `opt-trading`** :
- aucun module `algo_hf` ou `hf_trading` dans `opt-trading/modules/`
- aucune référence dans `opt-trading/docs/` ou `opt-trading/scripts/`
- `/opt/trading/` est **absent** de la machine `db-layer` (paths check snapshot : "missing")

---

## 2. SUPPORT CANONIQUE DE RÉFÉRENCE

| Attribut | Valeur |
|---|---|
| Repo local sur cursor-ai | **ABSENT** — aucun clone trouvé sur `C:\Users\ghost\` |
| Repo sur GitHub | MENTIONNÉ dans les docs PM comme "visible côté GitHub" — non vérifié terrain dans cette passe |
| Code path sur db-layer | **NON ÉTABLI** — `/opt/trading/` absent sur db-layer ; chemin réel inconnu depuis les sources disponibles |
| Module dans opt-trading | **ABSENT** |
| Documentation dédiée dans opt-trading | **ABSENTE** |

Les seules preuves terrain disponibles pour cette passe proviennent :
1. du snapshot systemd de `db-layer` (2026-02-26)
2. des docs d'audit PM (`96_cross_project_inventory_kanban_archive_first.md`, `97_cross_project_master_kanban.md`, `91_cross_topology_canon.md`, `A1_runtime_surfaces_canonical_map.md`)

---

## 3. ÉLÉMENTS DE PREUVE OBSERVÉS

### 3.1 Service systemd actif (PROUVÉ)

Source : `infra_context_sanitized/machines/db-layer/snapshot/snapshot_2026-02-26T15-23-55-05-00.txt` — ligne 203.

```
algo-hf-api.service   loaded active running   algo_hf API (FastAPI webhook)
```

### 3.2 Processus Python sur port 9100 (PROUVÉ, source inconnue)

Source : snapshot db-layer — ligne 188.

```
tcp   LISTEN 0   2048   0.0.0.0:9100   0.0.0.0:*   users:(("python",pid=1541,fd=6))
```

Interprétation : un processus Python (pid=1541) écoute sur le port 9100. Il est structurellement probable que ce soit `algo-hf-api.service` (Python + FastAPI), mais aucune association formelle service ↔ port n'est prouvée dans les sources disponibles.

Note : le port 9100 est conventionnellement utilisé par le `node_exporter` Prometheus. Cependant, `node_exporter` est un binaire Go, pas Python. Un processus Python sur ce port est donc atypique et pointe vers une application custom — vraisemblablement `algo-hf-api.service`.

### 3.3 Absence de `/opt/trading/` sur db-layer (PROUVÉ)

Source : snapshot db-layer — section `[paths check]`.

```
--- /opt/trading
missing
--- /opt/trading/scripts
missing
--- /opt/trading/modules
missing
```

**Conséquence directe** : le code de `algo-hf-api` ne provient pas d'un déploiement de `opt-trading` sur db-layer. Son chemin réel sur la machine est inconnu depuis les sources disponibles.

### 3.4 `/usr/local/bin` sur db-layer (PROUVÉ)

Source : snapshot db-layer — section `[paths check]`.

```
/usr/local/bin/
  menu   (1220 bytes, créé le 2026-02-22)
```

Un seul script `menu` est présent — pas de shortcut `algo-hf-api` dans le PATH global. Le service est donc lancé par systemd directement depuis son chemin d'installation propre, non exposé via shortcut global.

### 3.5 Mention GitHub (NON PROUVÉ TERRAIN)

Sources : `96_cross_project_inventory_kanban_archive_first.md` et `97_cross_project_master_kanban.md`.

Ces docs mentionnent : "repos visibles côté GitHub" pour `algo_hf` et `hf_trading`. Cette information provient du cadrage PM (ChatGPT) et n'a pas été vérifiée par une exploration terrain dans cette passe.

---

## 4. ÉTABLI / À CONFIRMER

| Item | État |
|---|---|
| `algo-hf-api.service` actif sur db-layer | ÉTABLI (snapshot 2026-02-26) |
| Description systemd : "algo_hf API (FastAPI webhook)" | ÉTABLI |
| Processus Python sur port 9100 sur db-layer | ÉTABLI |
| `algo_hf` absent de `opt-trading` (modules, docs, scripts) | ÉTABLI |
| `/opt/trading/` absent de db-layer | ÉTABLI |
| Repo `algo_hf` visible sur GitHub | PRÉSUMÉ — mentionné par PM, non vérifié terrain |
| Repo `algo_hf` cloné localement sur cursor-ai | NON ÉTABLI — absent de `C:\Users\ghost\` |
| Chemin du code `algo-hf-api` sur db-layer | NON ÉTABLI |
| Association formelle processus pid=1541 ↔ algo-hf-api.service | NON ÉTABLI (probable mais non prouvé) |
| Relation entre `algo_hf` et `hf_trading` | NON ÉTABLI |
| Contenu fonctionnel du workstream (stratégie HF, données, dépendances) | NON ÉTABLI |

---

## 5. LIEN AVEC `db-layer` / `algo-hf-api.service`

### Ce qui est prouvé

```
db-layer (Ubuntu 24.04, 192.168.16.179)
  └── algo-hf-api.service
        état   : loaded active running (snapshot 2026-02-26)
        nature : FastAPI webhook (description systemd)
        port   : 9100 probable (Python process, non formellement lié)
        code   : chemin inconnu (hors /opt/trading/ qui est absent)
```

### Ce qui est une hypothèse forte (non prouvée)

Le nom du service (`algo-hf-api`) et sa description (`algo_hf API`) suggèrent que le code source appartient au workstream `algo_hf`. Cette relation nominale est structurellement évidente mais non confirmée par un chemin de fichier ou une trace Git dans les sources disponibles.

### Ce qui n'est pas établi

- La relation entre `algo_hf` (workstream/repo) et `hf_trading` (autre repo mentionné) n'est pas documentée.
- Le déploiement exact sur db-layer (répertoire, virtualenv, systemd unit file path) n'est pas visible depuis les sources terrain disponibles.

---

## 6. DÉCISION DE CLASSIFICATION

Sur la base des éléments terrain disponibles :

| Attribut | Décision |
|---|---|
| Nature | workstream/projet **séparé** de `opt-trading` |
| Déploiement runtime | service actif sur `db-layer` |
| Repo Git | potentiellement séparé (GitHub mentionné) — non qualifié dans cette passe |
| Intégration dans `opt-trading` | NON — aucune trace dans modules, docs, scripts |
| Statut dans le portefeuille | PARTIELLEMENT QUALIFIÉ — service runtime prouvé, source code non localisée |

---

## 7. LIMITES DE CETTE PASSE

- **Pas d'accès SSH live** à db-layer — impossible de lire le unit file systemd de `algo-hf-api.service` ou d'identifier le chemin d'installation réel.
- **Pas de repo local** sur cursor-ai — aucun clone `algo_hf` accessible en lecture terrain.
- **GitHub non exploré** — le repo GitHub mentionné par le PM n'a pas été consulté dans cette passe (pas d'accès web requis dans un audit documentaire local-only).
- **Port 9100** — l'association avec `algo-hf-api.service` est probable mais non formellement prouvée.
- **Relation `algo_hf` ↔ `hf_trading`** — ces deux workstreams sont listés séparément dans le kanban PM mais leur relation (sous-projets du même ensemble ? repos distincts ?) n'est pas documentée.

---

## 8. POINT DE REPRISE

```
GO_ALGO_HF_AUDIT_01 → LIVRÉ (passe documentaire locale)

Ce qui est établi :
  ✓ algo-hf-api.service actif sur db-layer (snapshot 2026-02-26)
  ✓ nature : FastAPI webhook (description systemd)
  ✓ algo_hf absent de opt-trading (modules, docs, scripts)
  ✓ /opt/trading/ absent de db-layer — code source algo_hf non dans opt-trading
  ✓ aucun repo local algo_hf sur cursor-ai
  ✓ classification : workstream/projet séparé, service runtime sur db-layer

Ce qui reste conditionné à une passe ultérieure :
  → GO_ALGO_HF_DEEP_AUDIT_01 (si décision PM de qualifier complètement) :
     - lire le unit file algo-hf-api.service sur db-layer (SSH live)
     - identifier le chemin de code réel sur db-layer
     - explorer le repo GitHub algo_hf
     - qualifier la relation algo_hf ↔ hf_trading
  → Ou clore à ce niveau si le workstream n'est pas prioritaire dans le portefeuille

Prochain chantier portefeuille recommandé :
  GO_OPENCLAW_CANONICAL_REENTRY_01
  → qualifier openclaw (hors bundle dans cette passe, aucune source terrain observée)
  → ou clôture formelle de la passe 2026-03-20 si PM juge le portefeuille suffisamment cadré
```
