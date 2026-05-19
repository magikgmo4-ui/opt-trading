#!/usr/bin/env bash
# Génère le bundle ZIP final UI productization.
# Le ZIP est exclu de git (*.zip dans .gitignore) — artefact local uniquement.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT="$ROOT/dist/GO_OPT_TRADING_UI_PRODUCT_FINAL_BUNDLE_01.zip"

mkdir -p "$ROOT/dist"
rm -f "$OUT"

zip -r "$OUT" \
  docs/chantiers/GO_OPT_TRADING_UI_PRODUCTIZATION_MAPPING_AND_KANBAN_01/ \
  docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_PRODUCT_SHELL_REVIEW_01/ \
  docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_STATE_BADGES_HARDENING_01/ \
  docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_INFORMATION_ARCHITECTURE_01/ \
  docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_ACTION_PANEL_01/ \
  docs/chantiers/GO_OPT_TRADING_DESKPRO_UI_ERROR_DIAGNOSTICS_PANEL_01/ \
  docs/chantiers/GO_OPT_TRADING_LOCALCMS_UI_BRIDGE_LINKS_01/ \
  docs/chantiers/GO_OPT_TRADING_UI_VISUAL_REGRESSION_SMOKE_01/ \
  docs/chantiers/GO_OPT_TRADING_UI_HUMAN_ACCEPTANCE_REVIEW_01/ \
  docs/screenshots/ \
  -x "*/secrets/*" -x "*/.env" -x "*/tmp/*" -x "*/__pycache__/*" \
  -q

SHA=$(sha256sum "$OUT" | awk '{print $1}')
echo "Bundle: $OUT"
echo "Size  : $(du -sh "$OUT" | cut -f1)"
echo "SHA256: $SHA"
