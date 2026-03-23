#!/usr/bin/env bash
# ============================================================
# STUDENT VALIDATION — SANITY CHECK STRUCTUREL
# student_validation_sanity_check.sh
# ============================================================
# Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
# Date     : 2026-03-20
#
# Sanity check statique : vérifie la présence des fichiers
# attendus du pack validation et du sous-projet student,
# sans exécuter de commandes live.
#
# Usage : bash /opt/trading/student/validation/student_validation_sanity_check.sh
# Exit 0 = structurellement conforme / Exit 1 = anomalies détectées
# ============================================================

set -euo pipefail

ROOT="/opt/trading/student"
VAL_DIR="$ROOT/validation"

RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[1;33m'
BLU='\033[0;34m'
CYA='\033[0;36m'
RST='\033[0m'

OK="${GRN}[OK]${RST}"
FAIL="${RED}[FAIL]${RST}"
WARN="${YEL}[WARN]${RST}"

ERRORS=0
WARNINGS=0

section() {
  echo -e "\n${CYA}── $1 ──────────────────────────────────────────────────────${RST}"
}

check_file() {
  local path="$1"
  local label="${2:-$path}"
  if [[ -f "$path" ]]; then
    echo -e "  ${OK}  $label"
  else
    echo -e "  ${FAIL} $label — ABSENT"
    ERRORS=$((ERRORS + 1))
  fi
}

check_exec() {
  local path="$1"
  local label="${2:-$path}"
  if [[ -f "$path" ]]; then
    if [[ -x "$path" ]]; then
      echo -e "  ${OK}  $label (exécutable)"
    else
      echo -e "  ${WARN} $label — présent mais NON exécutable"
      WARNINGS=$((WARNINGS + 1))
    fi
  else
    echo -e "  ${FAIL} $label — ABSENT"
    ERRORS=$((ERRORS + 1))
  fi
}

check_dir() {
  local path="$1"
  local label="${2:-$path}"
  if [[ -d "$path" ]]; then
    echo -e "  ${OK}  $label/"
  else
    echo -e "  ${FAIL} $label/ — ABSENT"
    ERRORS=$((ERRORS + 1))
  fi
}

check_symlink() {
  local path="$1"
  local label="${2:-$path}"
  if [[ -L "$path" ]]; then
    echo -e "  ${OK}  $label (lien symbolique)"
  else
    echo -e "  ${FAIL} $label — lien absent"
    ERRORS=$((ERRORS + 1))
  fi
}

echo -e "${CYA}STUDENT VALIDATION — SANITY CHECK STRUCTUREL${RST}"
echo -e "Date : $(date '+%Y-%m-%d %H:%M:%S')"
echo -e "Root : $ROOT"

# ─────────────────────────────────────────────────────────────
section "1. PACK VALIDATION (student/validation/)"

check_dir  "$VAL_DIR"                          "validation/"
check_exec "$VAL_DIR/validate_student_live.sh"             "validation/validate_student_live.sh"
check_exec "$VAL_DIR/student_validation_cmd.sh"            "validation/student_validation_cmd.sh"
check_exec "$VAL_DIR/student_validation_menu.sh"           "validation/student_validation_menu.sh"
check_exec "$VAL_DIR/student_validation_sanity_check.sh"   "validation/student_validation_sanity_check.sh"
check_file "$VAL_DIR/RUNBOOK.md"                           "validation/RUNBOOK.md"
check_file "$VAL_DIR/HANDOFF.md"                           "validation/HANDOFF.md"

# ─────────────────────────────────────────────────────────────
section "2. STRUCTURE student/ (répertoires principaux)"

check_dir "$ROOT/scripts"               "scripts/"
check_dir "$ROOT/scripts/deepseek_hub"  "scripts/deepseek_hub/"
check_dir "$ROOT/scripts/wrappers"      "scripts/wrappers/"
check_dir "$ROOT/bin"                   "bin/"
check_dir "$ROOT/config"                "config/"
check_dir "$ROOT/docs"                  "docs/"

# ─────────────────────────────────────────────────────────────
section "3. ENTRYPOINTS CANONIQUES (scripts sources)"

check_exec "$ROOT/scripts/student_menu.sh"                           "scripts/student_menu.sh"
check_exec "$ROOT/scripts/student_cmd.sh"                            "scripts/student_cmd.sh"
check_exec "$ROOT/scripts/student_sanity_check.sh"                   "scripts/student_sanity_check.sh"
check_exec "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh"         "scripts/deepseek_hub/deepseek_hub_menu.sh"
check_exec "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"          "scripts/deepseek_hub/deepseek_hub_cmd.sh"
check_exec "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" "scripts/deepseek_hub/sanity_check_deepseek_hub.sh"
check_exec "$ROOT/scripts/wrappers/deepseek_student_menu.sh"         "scripts/wrappers/deepseek_student_menu.sh"
check_exec "$ROOT/scripts/wrappers/deepseek_student_cmd.sh"          "scripts/wrappers/deepseek_student_cmd.sh"
check_exec "$ROOT/scripts/wrappers/deepseek_student_sanity_check.sh" "scripts/wrappers/deepseek_student_sanity_check.sh"

# ─────────────────────────────────────────────────────────────
section "4. RACCOURCIS GLOBAUX (/usr/local/bin/)"

check_symlink "/usr/local/bin/menu-deepseek_hub"    "menu-deepseek_hub"
check_symlink "/usr/local/bin/cmd-deepseek_hub"     "cmd-deepseek_hub"
check_symlink "/usr/local/bin/sanity-deepseek_hub"  "sanity-deepseek_hub"
check_symlink "/usr/local/bin/menu-deepseek_student" "menu-deepseek_student"
check_symlink "/usr/local/bin/cmd-deepseek_student"  "cmd-deepseek_student  [CRITIQUE]"
check_symlink "/usr/local/bin/sanity-deepseek_student" "sanity-deepseek_student"
check_symlink "/usr/local/bin/menu-student"         "menu-student"
check_symlink "/usr/local/bin/cmd-student"          "cmd-student"
check_symlink "/usr/local/bin/sanity-student"       "sanity-student"

# ─────────────────────────────────────────────────────────────
section "5. FICHIERS DE CONFIGURATION ET OUTILLAGE"

check_exec "$ROOT/bin/install_shortcuts.sh"    "bin/install_shortcuts.sh"
check_exec "$ROOT/bin/repair_shortcuts.sh"     "bin/repair_shortcuts.sh"
check_file "$ROOT/config/shortcut_map.env"     "config/shortcut_map.env"

# ─────────────────────────────────────────────────────────────
section "6. DOCUMENTATION INTERNE"

check_file "$ROOT/docs/LEGACY_CALLERS_INVENTORY.md" "docs/LEGACY_CALLERS_INVENTORY.md"

# ─────────────────────────────────────────────────────────────
echo ""
echo -e "${CYA}── RÉSUMÉ ──────────────────────────────────────────────────${RST}"
echo ""
if [[ "$ERRORS" -eq 0 && "$WARNINGS" -eq 0 ]]; then
  echo -e "  ${GRN}✓ SANITY OK — 0 erreur, 0 avertissement${RST}"
elif [[ "$ERRORS" -eq 0 ]]; then
  echo -e "  ${YEL}⚠ SANITY PARTIEL — 0 erreur, $WARNINGS avertissement(s)${RST}"
  echo -e "  ${YEL}  Vérifier les fichiers signalés ci-dessus.${RST}"
else
  echo -e "  ${RED}✗ SANITY ÉCHOUÉ — $ERRORS erreur(s), $WARNINGS avertissement(s)${RST}"
  echo ""
  echo -e "  Actions recommandées :"
  echo -e "  • Raccourcis manquants → bash $ROOT/bin/install_shortcuts.sh"
  echo -e "  • Fichiers non exécutables → chmod +x <fichier>"
  echo -e "  • Répertoires manquants → git checkout sot/mainline + pull"
fi
echo ""

[[ "$ERRORS" -eq 0 ]]
