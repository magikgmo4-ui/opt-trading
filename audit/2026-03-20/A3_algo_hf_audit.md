# ALGO_HF — AUDIT DE QUALIFICATION CANONIQUE

```
Date     : 2026-03-20
Mission  : GO_ALGO_HF_AUDIT_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ — qualification canonique consolidée avec preuves live sur `db-layer`
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
| Repo sur GitHub | **PRÉSUMÉ CONFIRMÉ INDIRECTEMENT** — remote Git observé sur db-layer : `git@github.com:magikgmo4-ui/algo_hf.git` |
| Code path sur db-layer | **ÉTABLI** — `/home/ghost/dev/nouveau-systeme` |
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

### 3.2 Processus Python sur port 9100 (PROUVÉ)

Source : snapshot db-layer — ligne 188.

```
tcp   LISTEN 0   2048   0.0.0.0:9100   0.0.0.0:*   users:(("python",pid=1541,fd=6))
```

Interprétation : la passe live a confirmé l'association service ↔ processus ↔ port : `algo-hf-api.service` exécute `python -c "from algo_hf.api.run import main; main()"` et Uvicorn écoute sur `0.0.0.0:9100`.

Note : le port 9100 est conventionnellement utilisé par le `node_exporter` Prometheus. Cependant, `node_exporter` est un binaire Go, pas Python. Un processus Python sur ce port est donc atypique et pointe vers une application custom — vraisemblablement `algo-hf-api.service`.

### 3.3 Présence de `/opt/trading/` sur db-layer (PROUVÉ)

Source : snapshot db-layer — section `[paths check]`.

```
--- /opt/trading
missing
--- /opt/trading/scripts
missing
--- /opt/trading/modules
missing
```

La passe live a montré que `/opt/trading/` est présent sur `db-layer` en `sot/mainline`, mais aucun module `algo_hf` ou `hf_trading` n'y a été observé.

**Conséquence directe** : le code de `algo-hf-api` ne provient pas du repo `opt-trading` observé sur `db-layer`. Le chemin réel prouvé est `/home/ghost/dev/nouveau-systeme`.

### 3.4 `/usr/local/bin` sur db-layer (PROUVÉ)

Source : snapshot db-layer — section `[paths check]`.

```
/usr/local/bin/
  menu   (1220 bytes, créé le 2026-02-22)
```

Un seul script `menu` est présent — pas de shortcut `algo-hf-api` dans le PATH global. Le service est donc lancé par systemd directement depuis son chemin d'installation propre, non exposé via shortcut global.

### 3.5 Repo Git prouvé sur db-layer

Preuves live observées sur `db-layer` :

```text
Chemin  : /home/ghost/dev/nouveau-systeme
Branche : main
Remote  : origin git@github.com:magikgmo4-ui/algo_hf.git
```

Le remote Git permet de confirmer indirectement un repo GitHub pertinent pour `algo_hf`.
La relation avec un repo `hf_trading` reste non prouvée.

### 3.6 Service systemd et chemin de code (PROUVÉS)

Preuves live observées sur `db-layer` :

```text
FragmentPath=/etc/systemd/system/algo-hf-api.service
WorkingDirectory=/home/ghost/dev/nouveau-systeme
EnvironmentFile=/home/ghost/dev/nouveau-systeme/.env
ExecStart=/home/ghost/dev/nouveau-systeme/scripts/commandes/api_service.sh
python -c "from algo_hf.api.run import main; main()"
Uvicorn running on http://0.0.0.0:9100
```

---

## 4. ÉTABLI / À CONFIRMER

| Item | État |
|---|---|
| `algo-hf-api.service` actif sur db-layer | ÉTABLI (snapshot 2026-02-26) |
| Description systemd : "algo_hf API (FastAPI webhook)" | ÉTABLI |
| Processus Python sur port 9100 sur db-layer | ÉTABLI |
| `algo_hf` absent de `opt-trading` (modules, docs, scripts) | ÉTABLI |
| `/opt/trading/` présent sur db-layer, sans module `algo_hf` observé | ÉTABLI |
| Repo `algo_hf` visible sur GitHub | ÉTABLI INDIRECTEMENT — remote `git@github.com:magikgmo4-ui/algo_hf.git` observé |
| Repo `algo_hf` cloné localement sur cursor-ai | NON ÉTABLI — absent de `C:\Users\ghost\` |
| Repo `algo_hf` cloné localement sur db-layer | ÉTABLI — `/home/ghost/dev/nouveau-systeme` |
| Chemin du code `algo-hf-api` sur db-layer | ÉTABLI — `/home/ghost/dev/nouveau-systeme` |
| Association formelle processus ↔ algo-hf-api.service | ÉTABLI |
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
        port   : 9100 prouvé (Uvicorn en écoute)
        code   : `/home/ghost/dev/nouveau-systeme`
```

### Ce qui est désormais prouvé

Le service `algo-hf-api.service` lance du code Python depuis `/home/ghost/dev/nouveau-systeme`, avec import `algo_hf.api.run` et remote Git `git@github.com:magikgmo4-ui/algo_hf.git`.

### Ce qui n'est pas établi

- La relation entre `algo_hf` (workstream/repo) et `hf_trading` (autre repo mentionné) n'est pas documentée.
- Le contenu fonctionnel détaillé du workstream n'est pas qualifié dans cette passe.

---

## 6. DÉCISION DE CLASSIFICATION

Sur la base des éléments terrain disponibles :

| Attribut | Décision |
|---|---|
| Nature | workstream/projet **séparé** de `opt-trading` |
| Déploiement runtime | service actif sur `db-layer` |
| Repo Git | séparé, observé sur db-layer, remote GitHub prouvé indirectement |
| Intégration dans `opt-trading` | NON — aucune trace dans modules, docs, scripts |
| Statut dans le portefeuille | QUALIFIÉ — service runtime et chemin code prouvés ; relation `hf_trading` non prouvée |

---

## 7. LIMITES DE CETTE PASSE

- **Pas de repo local** sur cursor-ai — aucun clone `algo_hf` accessible en lecture terrain.
- **GitHub non exploré via API dédiée** — seul le remote Git observé sur db-layer permet une confirmation indirecte.
- **Relation `algo_hf` ↔ `hf_trading`** — ces deux workstreams sont listés séparément dans le kanban PM mais leur relation (sous-projets du même ensemble ? repos distincts ?) n'est pas documentée.

---

## 8. POINT DE REPRISE

```
GO_ALGO_HF_DEEP_AUDIT_01 → LIVRÉ

Ce qui est établi :
  ✓ algo-hf-api.service actif sur db-layer
  ✓ nature : FastAPI webhook (description systemd)
  ✓ chemin de code prouvé : /home/ghost/dev/nouveau-systeme
  ✓ repo Git local prouvé sur db-layer — branche `main`
  ✓ remote Git prouvé : git@github.com:magikgmo4-ui/algo_hf.git
  ✓ algo_hf absent de opt-trading comme module observé
  ✓ classification : workstream/projet séparé, service runtime sur db-layer

Ce qui reste conditionné à une passe ultérieure :
  → qualifier la relation algo_hf ↔ hf_trading
  → qualifier le contenu fonctionnel du workstream si besoin portefeuille

Prochain point logique :
  consolidation PM/kanban post-audit
```
