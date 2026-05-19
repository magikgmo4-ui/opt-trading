---
doc_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01_CONSOLIDATION_MAP
doc_type: consolidation_map
repo: opt-trading
project: opt-trading
module: product
go_id: GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01
status: draft_for_review
lifecycle_stage: child_consolidation_map
parent_go_id: GO_OPT_TRADING_AUDIT_ORPHAN_MODULES_01
topic_keys:
  - opt-trading
  - consolidation
  - ui
  - desk-pro
  - migration
surface: product
source_kind: canonical_draft
reference_canonique_principale: docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/02_UI_CONSOLIDATION_MAP.md
point_de_reprise: "Plan de migration pas-à-pas des 5 composants vers modules/desk_pro/."
updated_at: 2026-05-07
links:
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/00_CADRAGE.md
  - docs/chantiers/GO_OPT_TRADING_CONSOLIDATION_UI_CLUSTER_01/01_UI_CLUSTER_INVENTORY.md
---

# 02_UI_CONSOLIDATION_MAP

## 1_PLAN_PAS_A_PAS

### Étape 1 — Backup des modules sources

```bash
cd /home/fantome/opt-trading
mkdir -p _archive/legacy_modules

for mod in desk_pro_runner desk_pro_orchestrator desk_pro_dashboard market_scanner ui_registry_msi; do
  cp -r modules/$mod _archive/legacy_modules/$mod
done
```

### Étape 2 — Migrer desk_pro_runner → modules/desk_pro/runner/

```bash
mv modules/desk_pro_runner modules/desk_pro/runner
```

### Étape 3 — Migrer desk_pro_orchestrator → modules/desk_pro/orchestrator/

```bash
mv modules/desk_pro_orchestrator modules/desk_pro/orchestrator
```

### Étape 4 — Migrer desk_pro_dashboard → modules/desk_pro/dashboard/

```bash
mv modules/desk_pro_dashboard modules/desk_pro/dashboard
```

### Étape 5 — Migrer market_scanner → modules/desk_pro/scanner/

```bash
mv modules/market_scanner modules/desk_pro/scanner
```

### Étape 6 — Migrer ui_registry_msi → modules/desk_pro/registry/

```bash
mv modules/ui_registry_msi modules/desk_pro/registry
```

### Étape 7 — Fixer les imports string dans desk_pro_runner

```bash
# Fichier : modules/desk_pro/runner/app/desk_pro_runner.py

sed -i 's|modules\.desk_pro_orchestrator\.app\.desk_pro_orchestrator|modules.desk_pro.orchestrator.app.desk_pro_orchestrator|g' \
  modules/desk_pro/runner/app/desk_pro_runner.py

sed -i 's|modules\.desk_pro_dashboard\.app\.desk_pro_dashboard|modules.desk_pro.dashboard.app.desk_pro_dashboard|g' \
  modules/desk_pro/runner/app/desk_pro_runner.py
```

### Étape 8 — Fixer les imports string dans desk_pro_orchestrator

```bash
# Fichier : modules/desk_pro/orchestrator/app/desk_pro_orchestrator.py

sed -i 's|modules\.market_scanner\.app\.market_scanner|modules.desk_pro.scanner.app.market_scanner|g' \
  modules/desk_pro/orchestrator/app/desk_pro_orchestrator.py
```

### Étape 9 — Mettre à jour les scripts shell

```bash
# Tous les scripts shell dans les modules migrés
find modules/desk_pro/runner/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_runner|modules.desk_pro.runner|g' {} +
find modules/desk_pro/orchestrator/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_orchestrator|modules.desk_pro.orchestrator|g' {} +
find modules/desk_pro/dashboard/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_dashboard|modules.desk_pro.dashboard|g' {} +
find modules/desk_pro/scanner/scripts -name "*.sh" -exec sed -i 's|modules\.market_scanner|modules.desk_pro.scanner|g' {} +
find modules/desk_pro/registry/scripts -name "*.sh" -exec sed -i 's|modules\.ui_registry_msi|modules.desk_pro.registry|g' {} +
```

### Étape 10 — Mettre à jour le registre YAML

```yaml
# Fichier : registry/ui_surfaces_registry.yaml

# Remplacer les anciens chemins :
#   module: desk_pro_dashboard  → module: desk_pro.dashboard
#   module: desk_pro_runner     → module: desk_pro.runner
#   module: market_scanner      → module: desk_pro.scanner
```

```bash
sed -i 's|module: desk_pro_dashboard|module: desk_pro.dashboard|g' registry/ui_surfaces_registry.yaml
sed -i 's|module: desk_pro_runner|module: desk_pro.runner|g' registry/ui_surfaces_registry.yaml
sed -i 's|module: market_scanner|module: desk_pro.scanner|g' registry/ui_surfaces_registry.yaml
```

### Étape 11 — Mettre à jour le registre modules

```yaml
# Fichier : registry/modules_registry.yaml
```

```bash
sed -i 's|modules/desk_pro_runner|modules/desk_pro/runner|g' registry/modules_registry.yaml
sed -i 's|modules/desk_pro_orchestrator|modules/desk_pro/orchestrator|g' registry/modules_registry.yaml
sed -i 's|modules/desk_pro_dashboard|modules/desk_pro/dashboard|g' registry/modules_registry.yaml
sed -i 's|modules/market_scanner|modules/desk_pro/scanner|g' registry/modules_registry.yaml
sed -i 's|modules/ui_registry_msi|modules/desk_pro/registry|g' registry/modules_registry.yaml
```

### Étape 12 — Mettre à jour le README du hub

```bash
# Remplacer modules/desk_pro/README.md avec la documentation unifiée
```

### Étape 13 — Scanner les références résiduelles

```bash
rg "desk_pro_runner|desk_pro_orchestrator|desk_pro_dashboard|market_scanner|ui_registry_msi" \
   --type-add 'code:*.py' --type-add 'yaml:*.yaml' --type-add 'doc:*.md' \
   -t code -t yaml -t doc \
   modules/ docs/ registry/ scripts/ 2>/dev/null | grep -v "_archive/" | grep -v "docs/chantiers/" | grep -v ".git/"
```

Corriger toute référence restante pointant vers les anciens chemins.

### Étape 14 — Vérification

```bash
# Vérifier que les anciens répertoires n'existent plus
ls -d modules/desk_pro_runner modules/desk_pro_orchestrator modules/desk_pro_dashboard modules/market_scanner modules/ui_registry_msi 2>&1
# Attendu : "No such file or directory" × 5

# Vérifier la nouvelle structure
ls -d modules/desk_pro/runner modules/desk_pro/orchestrator modules/desk_pro/dashboard modules/desk_pro/scanner modules/desk_pro/registry
# Attendu : 5 répertoires listés

# Vérifier les backups
ls -d _archive/legacy_modules/desk_pro_runner _archive/legacy_modules/desk_pro_orchestrator _archive/legacy_modules/desk_pro_dashboard _archive/legacy_modules/market_scanner _archive/legacy_modules/ui_registry_msi
# Attendu : 5 répertoires listés
```

## 2_IMPACT_GLOBAL

```text
Modules déplacés     : 5
Fichiers déplacés    : ~35
Imports string fixés : 3 (runner:2, orchestrator:1)
Scripts shell fixés  : ~15
Registres mis à jour : 2 (ui_surfaces_registry.yaml, modules_registry.yaml)
README hub mis à jour: 1
```

## 3_SCRIPT_COMPLET

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

cd /home/fantome/opt-trading

# Backup
mkdir -p _archive/legacy_modules
for mod in desk_pro_runner desk_pro_orchestrator desk_pro_dashboard market_scanner ui_registry_msi; do
  echo "Backup $mod..."
  cp -r modules/$mod _archive/legacy_modules/$mod
done

# Migration
mv modules/desk_pro_runner modules/desk_pro/runner
mv modules/desk_pro_orchestrator modules/desk_pro/orchestrator
mv modules/desk_pro_dashboard modules/desk_pro/dashboard
mv modules/market_scanner modules/desk_pro/scanner
mv modules/ui_registry_msi modules/desk_pro/registry

# Fix imports string (Python)
sed -i 's|modules\.desk_pro_orchestrator\.app\.desk_pro_orchestrator|modules.desk_pro.orchestrator.app.desk_pro_orchestrator|g' modules/desk_pro/runner/app/desk_pro_runner.py
sed -i 's|modules\.desk_pro_dashboard\.app\.desk_pro_dashboard|modules.desk_pro.dashboard.app.desk_pro_dashboard|g' modules/desk_pro/runner/app/desk_pro_runner.py
sed -i 's|modules\.market_scanner\.app\.market_scanner|modules.desk_pro.scanner.app.market_scanner|g' modules/desk_pro/orchestrator/app/desk_pro_orchestrator.py

# Fix scripts shell
find modules/desk_pro/runner/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_runner|modules.desk_pro.runner|g' {} +
find modules/desk_pro/orchestrator/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_orchestrator|modules.desk_pro.orchestrator|g' {} +
find modules/desk_pro/dashboard/scripts -name "*.sh" -exec sed -i 's|modules\.desk_pro_dashboard|modules.desk_pro.dashboard|g' {} +
find modules/desk_pro/scanner/scripts -name "*.sh" -exec sed -i 's|modules\.market_scanner|modules.desk_pro.scanner|g' {} +
find modules/desk_pro/registry/scripts -name "*.sh" -exec sed -i 's|modules\.ui_registry_msi|modules.desk_pro.registry|g' {} +

# Fix registries
sed -i 's|module: desk_pro_dashboard|module: desk_pro.dashboard|g' registry/ui_surfaces_registry.yaml
sed -i 's|module: desk_pro_runner|module: desk_pro.runner|g' registry/ui_surfaces_registry.yaml
sed -i 's|module: market_scanner|module: desk_pro.scanner|g' registry/ui_surfaces_registry.yaml

echo "=== Vérification ==="
ls -d modules/desk_pro/runner modules/desk_pro/orchestrator modules/desk_pro/dashboard modules/desk_pro/scanner modules/desk_pro/registry
echo "Migration UI terminée."
```

## 17_RESUME_POINT

```text
Plan 14 étapes, entièrement scripté.
5 modules → modules/desk_pro/{runner,orchestrator,dashboard,scanner,registry}
3 imports string à fixer, ~15 scripts shell, 2 registres YAML.
Backups dans _archive/ avant toute opération.
Le hub desk_pro existant n'est pas déplacé.
```
