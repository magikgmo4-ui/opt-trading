---
doc_id: GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01_MIGRATION_PLAN
doc_type: migration_plan
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_migration_plan
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - strategy
  - migration
  - engines
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01/01_MIGRATION_PLAN.md
point_de_reprise: "Plan pas-à-pas pour la migration des 4 engines vers modules/strategy/."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_STRATEGY_CLUSTER_01/00_CADRAGE.md
---

# 01_MIGRATION_PLAN

## 1_PLAN_PAS_A_PAS

### Étape 1 — Créer la structure cible

```bash
mkdir -p modules/strategy/{decision,execution,position,portfolio}
```

### Étape 2 — Migrer decision_engine → modules/strategy/decision/

```bash
# Backup
cp -r modules/decision_engine _archive/legacy_modules/decision_engine/

# Migrer
mv modules/decision_engine/app        modules/strategy/decision/app
mv modules/decision_engine/config     modules/strategy/decision/config
mv modules/decision_engine/scripts    modules/strategy/decision/scripts
mv modules/decision_engine/README.md  modules/strategy/decision/README.md
mv modules/decision_engine/__init__.py modules/strategy/decision/__init__.py

# Nettoyer l'ancien répertoire (déjà vidé)
rmdir modules/decision_engine
```

### Étape 3 — Migrer execution_engine → modules/strategy/execution/

```bash
cp -r modules/execution_engine _archive/legacy_modules/execution_engine/

mv modules/execution_engine/app        modules/strategy/execution/app
mv modules/execution_engine/adapters   modules/strategy/execution/adapters
mv modules/execution_engine/config     modules/strategy/execution/config
mv modules/execution_engine/scripts    modules/strategy/execution/scripts
mv modules/execution_engine/README.md  modules/strategy/execution/README.md
mv modules/execution_engine/executor.py modules/strategy/execution/executor.py
mv modules/execution_engine/__init__.py modules/strategy/execution/__init__.py

rmdir modules/execution_engine
```

### Étape 4 — Migrer position_engine → modules/strategy/position/

```bash
cp -r modules/position_engine _archive/legacy_modules/position_engine/

mv modules/position_engine/app               modules/strategy/position/app
mv modules/position_engine/config            modules/strategy/position/config
mv modules/position_engine/scripts           modules/strategy/position/scripts
mv modules/position_engine/README.md         modules/strategy/position/README.md
mv modules/position_engine/models.py         modules/strategy/position/models.py
mv modules/position_engine/position_manager.py modules/strategy/position/position_manager.py
mv modules/position_engine/storage.py        modules/strategy/position/storage.py
mv modules/position_engine/__init__.py       modules/strategy/position/__init__.py

rmdir modules/position_engine
```

### Étape 5 — Migrer portfolio_engine → modules/strategy/portfolio/

```bash
cp -r modules/portfolio_engine _archive/legacy_modules/portfolio_engine/

mv modules/portfolio_engine/app        modules/strategy/portfolio/app
mv modules/portfolio_engine/config     modules/strategy/portfolio/config
mv modules/portfolio_engine/scripts    modules/strategy/portfolio/scripts
mv modules/portfolio_engine/README.md  modules/strategy/portfolio/README.md
mv modules/portfolio_engine/__init__.py modules/strategy/portfolio/__init__.py

rmdir modules/portfolio_engine
```

### Étape 6 — Créer le README unifié

Créer `modules/strategy/README.md` :

```markdown
# Strategy Pipeline

Pipeline de stratégie data-driven : décision → exécution → position → portefeuille.

## Architecture

decision/   → Évalue les signaux et prend des décisions (strategy_logic.py)
execution/  → Traduit les décisions en plans d'exécution (adapters/paper.py)
position/   → Gère l'état des positions (models.py, storage.py)
portfolio/  → Agrège en vue portefeuille consolidée

## Flux

[Signaux] → decision/ → decision_output.json
                     → execution/ → execution_plan.json
                                  → position/ → position_state.json
                                              → portfolio/ → portfolio_view.json

## Usage

Chaque sous-module est indépendant. Voir le README de chaque sous-module.
Communication inter-module par fichiers JSON, pas d'imports Python croisés.
```

### Étape 7 — Mettre à jour les imports internes

Rechercher les références aux anciens chemins et les mettre à jour :

```bash
# Chercher les imports référençant les anciens chemins
rg "modules\.(decision_engine|execution_engine|position_engine|portfolio_engine)" modules/strategy/ modules/ scripts/ docs/

# Remplacer :
#   modules.decision_engine    → modules.strategy.decision
#   modules.execution_engine   → modules.strategy.execution
#   modules.position_engine    → modules.strategy.position
#   modules.portfolio_engine   → modules.strategy.portfolio
```

Fichiers impactés (liste vérifiée) :

```text
modules/strategy/execution/executor.py :
  from modules.execution_engine.adapters.paper import PaperAdapter
  → from modules.strategy.execution.adapters.paper import PaperAdapter

modules/strategy/position/position_manager.py :
  from modules.position_engine.models import Position
  → from modules.strategy.position.models import Position
  from modules.position_engine.storage import load_positions
  → from modules.strategy.position.storage import load_positions
  from modules.position_engine.storage import save_positions
  → from modules.strategy.position.storage import save_positions
```

Scripts shell à mettre à jour (références aux chemins d'exécution) :

```text
modules/strategy/decision/scripts/cmd.sh
modules/strategy/decision/scripts/menu.sh
modules/strategy/execution/scripts/cmd.sh
modules/strategy/execution/scripts/execution_engine_cmd.sh
modules/strategy/execution/scripts/execution_engine_menu.sh
modules/strategy/position/scripts/cmd.sh
modules/strategy/position/scripts/position_engine_cmd.sh
modules/strategy/position/scripts/position_engine_menu.sh
modules/strategy/portfolio/scripts/cmd.sh
```

Dans chaque script, remplacer le chemin de l'ancien module par le nouveau.

### Étape 8 — Nettoyer les références externes

```bash
# Chercher TOUTES les références aux anciens chemins dans le repo
rg "decision_engine|execution_engine|position_engine|portfolio_engine" \
   --type-add 'code:*.py' --type-add 'doc:*.md' --type-add 'sh:*.sh' \
   -t code -t doc -t sh \
   modules/ docs/ scripts/ registry/

# Mettre à jour chaque occurrence
```

## 2_VERIFICATION_POST_MIGRATION

```bash
# Vérifier que les anciens répertoires n'existent plus
ls modules/decision_engine modules/execution_engine modules/position_engine modules/portfolio_engine 2>&1
# Attendu : "No such file or directory" × 4

# Vérifier que la nouvelle structure existe
ls modules/strategy/decision modules/strategy/execution modules/strategy/position modules/strategy/portfolio

# Vérifier que les backups existent
ls _archive/legacy_modules/decision_engine _archive/legacy_modules/execution_engine _archive/legacy_modules/position_engine _archive/legacy_modules/portfolio_engine
```

## 3_IMPACT

```text
Fichiers déplacés      : ~50 (code + configs + scripts + READMEs)
Imports Python à fixer : 3 (executor.py:1, position_manager.py:2)
Scripts shell à fixer  : ~9
Réfs docs à mettre à jour : à vérifier après rg
Réfs registry à vérifier  : machines_registry.yaml, modules_registry.yaml
```

## 4_GO_PROMPT — Exécution

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /home/fantome/opt-trading

# Étape 1
mkdir -p modules/strategy/{decision,execution,position,portfolio}
mkdir -p _archive/legacy_modules

# Étape 2 à 5 (backups)
for mod in decision_engine execution_engine position_engine portfolio_engine; do
  cp -r modules/$mod _archive/legacy_modules/$mod
done

# Migration des fichiers
mv modules/decision_engine/app modules/decision_engine/config modules/decision_engine/scripts modules/decision_engine/README.md modules/decision_engine/__init__.py modules/strategy/decision/
mv modules/execution_engine/app modules/execution_engine/adapters modules/execution_engine/config modules/execution_engine/scripts modules/execution_engine/README.md modules/execution_engine/executor.py modules/execution_engine/__init__.py modules/strategy/execution/
mv modules/position_engine/app modules/position_engine/config modules/position_engine/scripts modules/position_engine/README.md modules/position_engine/models.py modules/position_engine/position_manager.py modules/position_engine/storage.py modules/position_engine/__init__.py modules/strategy/position/
mv modules/portfolio_engine/app modules/portfolio_engine/config modules/portfolio_engine/scripts modules/portfolio_engine/README.md modules/portfolio_engine/__init__.py modules/strategy/portfolio/

# Nettoyer les répertoires vides
rmdir modules/decision_engine modules/execution_engine modules/position_engine modules/portfolio_engine

# Étape 6 — Créer le README unifié
cat > modules/strategy/README.md <<'READMEEOF'
# Strategy Pipeline

Pipeline de stratégie data-driven : décision → exécution → position → portefeuille.

## Architecture

| Étages | Rôle |
|--------|------|
| decision/ | Évalue les signaux et prend des décisions (strategy_logic.py) |
| execution/ | Traduit les décisions en plans d'exécution (adapters/paper.py) |
| position/ | Gère l'état des positions (models.py, storage.py) |
| portfolio/ | Agrège en vue portefeuille consolidée |

## Flux JSON

```
[Signaux] → decision/ → execution/ → position/ → portfolio/
```

Chaque étage lit le JSON de l'étage précédent et produit son propre JSON.
Aucun import Python croisé entre les étages.

## Usage

Chaque sous-module est indépendant. Voir le README.md de chaque sous-module.
READMEEOF

# Étape 7 — Fixer les imports Python
sed -i 's/modules\.execution_engine\.adapters\.paper/modules.strategy.execution.adapters.paper/g' modules/strategy/execution/executor.py
sed -i 's/modules\.position_engine\./modules.strategy.position./g' modules/strategy/position/position_manager.py

# Étape 8 — Mettre à jour les scripts shell
find modules/strategy/ -name "*.sh" -exec sed -i 's/modules\.decision_engine/modules.strategy.decision/g' {} +
find modules/strategy/ -name "*.sh" -exec sed -i 's/modules\.execution_engine/modules.strategy.execution/g' {} +
find modules/strategy/ -name "*.sh" -exec sed -i 's/modules\.position_engine/modules.strategy.position/g' {} +
find modules/strategy/ -name "*.sh" -exec sed -i 's/modules\.portfolio_engine/modules.strategy.portfolio/g' {} +

# Vérification
echo "=== Vérification anciens répertoires ==="
ls -d modules/decision_engine modules/execution_engine modules/position_engine modules/portfolio_engine 2>&1 || true
echo "=== Vérification nouvelle structure ==="
ls -d modules/strategy/decision modules/strategy/execution modules/strategy/position modules/strategy/portfolio
echo "=== Vérification backups ==="
ls -d _archive/legacy_modules/decision_engine _archive/legacy_modules/execution_engine _archive/legacy_modules/position_engine _archive/legacy_modules/portfolio_engine

echo "Migration terminée."
```

## 17_RESUME_POINT

```text
Plan de migration en 8 étapes, entièrement scripté.
4 modules → modules/strategy/{decision,execution,position,portfolio}
3 imports Python à fixer, ~9 scripts shell.
Backups dans _archive/ avant toute opération.
```
