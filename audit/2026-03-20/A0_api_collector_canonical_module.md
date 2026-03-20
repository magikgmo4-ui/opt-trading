# API COLLECTOR — FICHE CANONIQUE MODULE

```
Date     : 2026-03-20
Mission  : GO_API_COLLECTOR_CANONICAL_MODULE_01
Pivot    : opt-trading / sot/mainline
Statut   : LIVRÉ — module qualifié, état fonctionnel documenté, runbook minimal établi
```

---

## 1. ALIAS PM → NOM CANONIQUE RÉEL

Le kanban PM (`97_cross_project_master_kanban.md`) et la topologie (`91_cross_topology_canon.md`)
désignent ce module sous l'alias **"api collector"**.

Le nom réel dans le repo est :

```
modules/derivatives_collector
```

Ce document utilise exclusivement le nom canonique `derivatives_collector`.

---

## 2. CLASSIFICATION CANONIQUE

| Attribut | Valeur |
|---|---|
| Nom canonique | `derivatives_collector` |
| Type | **module interne** de `opt-trading` |
| Statut | PRÉSENT / FONCTIONNEL (mode mock) / ADAPTERS RÉELS À COMPLÉTER |
| Appartenance | `opt-trading/modules/derivatives_collector/` |
| Repo séparé | NON — intégré dans `sot/mainline` |
| Chaîne Desk Pro | OUI — module de la chaîne core Desk Pro |

---

## 3. RÔLE FONCTIONNEL

Le module collecte et normalise des données de marché dérivés :

- Open Interest (OI)
- Funding Rates
- Liquidations (long / short)
- Long/Short Ratios
- Volume Futures

Sources supportées :
- `mock` — générateur aléatoire (défaut, fonctionnel)
- `coinglass` — placeholder (clé API non configurée)
- `binance` — placeholder (clé API non configurée)
- `bitget` — placeholder (clé API non configurée)

Consommateurs downstream déclarés (README) :
- Risk Engine
- Strategy

---

## 4. STRUCTURE DU MODULE

```
modules/derivatives_collector/
├── app/
│   └── derivatives_collector.py     # entrypoint Python, CLI + classes
├── config/
│   └── env.example                  # template de configuration
└── scripts/
    ├── cmd.sh                       # dispatcher Bash → Python
    ├── menu.sh                      # menu interactif
    └── sanity_check.sh              # vérification de structure + exécution mock
```

---

## 5. ENTRYPOINT ET INVOCATION

### Via Bash (opérateur)

```bash
# Depuis la racine opt-trading
bash modules/derivatives_collector/scripts/cmd.sh collect
bash modules/derivatives_collector/scripts/cmd.sh status
bash modules/derivatives_collector/scripts/cmd.sh sample
bash modules/derivatives_collector/scripts/cmd.sh export
bash modules/derivatives_collector/scripts/cmd.sh sanity
```

### Via Python (direct)

```bash
# Depuis la racine opt-trading
python3 -m modules.derivatives_collector.app.derivatives_collector collect
python3 -m modules.derivatives_collector.app.derivatives_collector status
python3 -m modules.derivatives_collector.app.derivatives_collector sample
```

### Commandes disponibles

| Commande | Effet |
|---|---|
| `collect` | Collecte les données selon la source configurée |
| `status` | Affiche la configuration active (source, symboles, format, répertoire) |
| `sample` | Collecte mock forcée (test sans config) |
| `export` | Collecte + export fichier (json ou csv) |
| `menu` | Lance `menu.sh` |
| `sanity` | Lance `sanity_check.sh` (structure + exécution mock) |

---

## 6. CONFIGURATION

Fichier de config : `modules/derivatives_collector/config/.env` (à créer depuis `env.example`).

Variables d'environnement :

| Variable | Défaut | Description |
|---|---|---|
| `DATA_SOURCE` | `mock` | Source de données : mock, coinglass, binance, bitget |
| `SYMBOLS` | `BTCUSDT,ETHUSDT` | Symboles à collecter (virgule-séparés) |
| `OUTPUT_FORMAT` | `json` | Format de sortie : json ou csv |
| `OUTPUT_DIR` | `data/derivatives` | Répertoire de sortie (relatif à la racine projet) |
| `COINGLASS_API_KEY` | — | Clé API Coinglass (placeholder) |
| `BINANCE_API_KEY` | — | Clé API Binance (placeholder) |
| `BITGET_API_KEY` | — | Clé API Bitget (placeholder) |

---

## 7. ÉTAT FONCTIONNEL RÉEL

| Composant | État |
|---|---|
| Structure de fichiers | SAINE — app/, config/, scripts/ présents |
| Entrypoint `cmd.sh` | FONCTIONNEL — dispatche correctement vers Python |
| `sanity_check.sh` | FONCTIONNEL — vérifie structure + exécute mock |
| Adapter `mock` | FONCTIONNEL — génère données aléatoires cohérentes |
| Adapter `coinglass` | PLACEHOLDER — clé API non configurée, code non implémenté |
| Adapter `binance` | PLACEHOLDER — clé API non configurée, code non implémenté |
| Adapter `bitget` | PLACEHOLDER — clé API non configurée, code non implémenté |
| Export JSON | FONCTIONNEL |
| Export CSV | FONCTIONNEL |
| Shortcut global | ABSENT — pas de shortcut `/usr/local/bin/` déclaré pour ce module |
| Intégration Risk Engine | DÉCLARÉE dans README — non vérifiable depuis ce contexte |

---

## 8. LIMITES DE CETTE PASSE

- Audit purement structurel et documentaire — aucun accès runtime live.
- L'intégration réelle avec le Risk Engine et la Strategy n'est pas vérifiable sans accès à la machine d'exécution.
- Les adapters réels (Coinglass, Binance, Bitget) ne sont pas implémentés dans le code actuel — ils se rabattent tous sur le `MockAdapter`.
- Pas de shortcut global déclaré : le module n'est pas invocable via `/usr/local/bin/` contrairement à `student`.

---

## 9. RUNBOOK MINIMAL

### Prérequis

```bash
# Depuis la racine opt-trading — vérifier Python
python3 --version   # Python 3.8+ attendu

# Créer la config si absente
cp modules/derivatives_collector/config/env.example modules/derivatives_collector/config/.env
```

### Vérification rapide

```bash
# Sanity check complet
bash modules/derivatives_collector/scripts/cmd.sh sanity

# Statut de la configuration active
bash modules/derivatives_collector/scripts/cmd.sh status

# Collecte mock de test
bash modules/derivatives_collector/scripts/cmd.sh sample
```

### Collecte réelle (une fois adapter configuré)

```bash
# Éditer la config
nano modules/derivatives_collector/config/.env
# Mettre DATA_SOURCE=coinglass (ou binance, bitget)
# Renseigner la clé API correspondante

# Lancer la collecte
bash modules/derivatives_collector/scripts/cmd.sh collect
```

---

## 10. DÉCISION DE CLASSIFICATION

Ce module est classé **module interne de `opt-trading`** pour cette passe.

Conditions de reclassification en projet séparé :
- si le module développe ses propres adapters avec état persistant indépendant ;
- si une équipe ou un déploiement séparé est nécessaire ;
- si un repo indépendant est créé.

Aucune de ces conditions n'est remplie à date.

---

## 11. POINT DE REPRISE

```
GO_API_COLLECTOR_CANONICAL_MODULE_01 → LIVRÉ

Ce qui est établi :
  ✓ nom canonique : modules/derivatives_collector
  ✓ classification : module interne opt-trading / chaîne Desk Pro
  ✓ état fonctionnel : mock opérationnel, adapters réels = placeholders
  ✓ structure documentée : app/ config/ scripts/
  ✓ runbook minimal établi
  ✓ limites documentées (pas d'accès live, adapters non implémentés)

Ce qui reste conditionné à une passe ultérieure :
  → implémenter les adapters réels (Coinglass, Binance, Bitget)
  → vérifier l'intégration live avec Risk Engine / Strategy
  → décider si un shortcut global est nécessaire (/usr/local/bin/)
  → décider si la config .env doit être gérée par un secret manager

Prochain chantier portefeuille recommandé :
  GO_RUNTIME_SURFACES_CANONICAL_MAP_01
  → carte canonique minimale machine → rôle → surface active → repo associé
  → périmètre : admin-trading, db-layer, cursor-ai
```
