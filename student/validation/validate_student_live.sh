#!/usr/bin/env bash
# ============================================================
# STUDENT — VALIDATION LIVE
# validate_student_live.sh
# ============================================================
# Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
# Date     : 2026-03-20
# Pivot    : opt-trading / sot/mainline
# Machine  : machine Linux cible où /opt/trading/student est effectivement déployé
#
# Ce script effectue la validation live du sous-projet student.
# Il vérifie :
#   1. Les 9 raccourcis globaux (readlink -f)
#   2. Le raccourci critique cmd-deepseek_student (RISQUE ÉLEVÉ)
#   3. Les callers legacy (item 5 LEGACY_CALLERS_INVENTORY)
#   4. Les entrypoints canoniques fonctionnels
#
# Usage : bash /opt/trading/student/validation/validate_student_live.sh [--repair]
# ============================================================

set -euo pipefail

ROOT="/opt/trading/student"
BIN_DIR="/usr/local/bin"
REPAIR=0

for arg in "$@"; do
  [[ "$arg" == "--repair" ]] && REPAIR=1
done

# ── Couleurs ────────────────────────────────────────────────
RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[1;33m'
BLU='\033[0;34m'
CYA='\033[0;36m'
RST='\033[0m'

OK="${GRN}[OK]${RST}"
FAIL="${RED}[FAIL]${RST}"
WARN="${YEL}[WARN]${RST}"
INFO="${BLU}[INFO]${RST}"

ERRORS=0
WARNINGS=0

banner() {
  echo -e "\n${CYA}══════════════════════════════════════════════════════════${RST}"
  echo -e "${CYA}  $1${RST}"
  echo -e "${CYA}══════════════════════════════════════════════════════════${RST}"
}

check_shortcut() {
  local name="$1"
  local expected_target="$2"
  local is_critical="${3:-0}"

  local link_path="$BIN_DIR/$name"

  if [[ ! -L "$link_path" ]]; then
    if [[ "$is_critical" == "1" ]]; then
      echo -e "  ${FAIL} $name — lien absent (CRITIQUE)"
      ERRORS=$((ERRORS + 1))
    else
      echo -e "  ${FAIL} $name — lien absent"
      ERRORS=$((ERRORS + 1))
    fi
    return
  fi

  local actual
  actual=$(readlink -f "$link_path" 2>/dev/null || echo "ERREUR_READLINK")

  if [[ "$actual" == "$expected_target" ]]; then
    if [[ "$is_critical" == "1" ]]; then
      echo -e "  ${OK} $name → $actual  ${YEL}[CRITIQUE — OK]${RST}"
    else
      echo -e "  ${OK} $name → $actual"
    fi
  else
    if [[ "$is_critical" == "1" ]]; then
      echo -e "  ${FAIL} $name"
      echo -e "       attendu : $expected_target"
      echo -e "       obtenu  : $actual  ${RED}[CRITIQUE — MAUVAISE CIBLE]${RST}"
      ERRORS=$((ERRORS + 1))
    else
      echo -e "  ${FAIL} $name"
      echo -e "       attendu : $expected_target"
      echo -e "       obtenu  : $actual"
      ERRORS=$((ERRORS + 1))
    fi
  fi

  # Vérifier que la cible existe réellement
  if [[ ! -f "$actual" ]]; then
    echo -e "  ${WARN} $name — cible introuvable sur disque : $actual"
    WARNINGS=$((WARNINGS + 1))
  fi
}

# ════════════════════════════════════════════════════════════
banner "1. VÉRIFICATION DES 9 RACCOURCIS GLOBAUX"
# ════════════════════════════════════════════════════════════

echo -e "\n${INFO} Groupe deepseek_hub :"
check_shortcut "menu-deepseek_hub"   "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh"        0
check_shortcut "cmd-deepseek_hub"    "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"          0
check_shortcut "sanity-deepseek_hub" "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" 0

echo -e "\n${INFO} Groupe deepseek_student :"
check_shortcut "menu-deepseek_student"   "$ROOT/scripts/wrappers/deepseek_student_menu.sh"          0
check_shortcut "cmd-deepseek_student"    "$ROOT/scripts/wrappers/deepseek_student_cmd.sh"           1
check_shortcut "sanity-deepseek_student" "$ROOT/scripts/wrappers/deepseek_student_sanity_check.sh"  0

echo -e "\n${INFO} Groupe student :"
check_shortcut "menu-student"   "$ROOT/scripts/student_menu.sh"          0
check_shortcut "cmd-student"    "$ROOT/scripts/student_cmd.sh"            0
check_shortcut "sanity-student" "$ROOT/scripts/student_sanity_check.sh"   0

# ════════════════════════════════════════════════════════════
banner "2. VÉRIFICATION RACCOURCI CRITIQUE : cmd-deepseek_student"
# ════════════════════════════════════════════════════════════

CRITICAL_LINK="$BIN_DIR/cmd-deepseek_student"
CRITICAL_EXPECTED="$ROOT/scripts/wrappers/deepseek_student_cmd.sh"

echo ""
if [[ -L "$CRITICAL_LINK" ]]; then
  CRITICAL_ACTUAL=$(readlink -f "$CRITICAL_LINK" 2>/dev/null || echo "ERREUR")
  echo -e "  readlink -f $CRITICAL_LINK"
  echo -e "  → $CRITICAL_ACTUAL"
  if [[ "$CRITICAL_ACTUAL" == "$CRITICAL_EXPECTED" ]]; then
    echo -e "  ${OK} Raccourci critique conforme."
  else
    echo -e "  ${FAIL} Raccourci critique NON CONFORME."
    echo -e "  ${RED}  RISQUE : pointe vers $CRITICAL_ACTUAL au lieu de $CRITICAL_EXPECTED${RST}"
    echo -e "  ${YEL}  Réparation : bash $ROOT/bin/install_shortcuts.sh${RST}"
    ERRORS=$((ERRORS + 1))
  fi
else
  echo -e "  ${FAIL} Lien $CRITICAL_LINK absent."
  ERRORS=$((ERRORS + 1))
fi

# ════════════════════════════════════════════════════════════
banner "3. VÉRIFICATION CALLERS LEGACY (ITEM 5)"
# ════════════════════════════════════════════════════════════

echo ""
DEEPSEEK_HUB_CMD="$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"
DEEPSEEK_HUB_SANITY="$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh"

# 3a — deepseek_hub_cmd.sh appelle cmd-deepseek_student
echo -e "${INFO} deepseek_hub_cmd.sh — vérification appel alias-based (cmd-deepseek_student) :"
if [[ -f "$DEEPSEEK_HUB_CMD" ]]; then
  if grep -q "cmd-deepseek_student" "$DEEPSEEK_HUB_CMD" 2>/dev/null; then
    echo -e "  ${OK} deepseek_hub_cmd.sh contient 'cmd-deepseek_student' — fallback alias présent"
  else
    echo -e "  ${WARN} deepseek_hub_cmd.sh ne contient pas 'cmd-deepseek_student' — vérifier manuellement"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  echo -e "  ${FAIL} $DEEPSEEK_HUB_CMD — fichier introuvable"
  ERRORS=$((ERRORS + 1))
fi

# 3b — sanity_check_deepseek_hub.sh vérifie présence cmd-deepseek_student
echo -e "\n${INFO} sanity_check_deepseek_hub.sh — vérification check présence cmd-deepseek_student :"
if [[ -f "$DEEPSEEK_HUB_SANITY" ]]; then
  if grep -q "cmd-deepseek_student" "$DEEPSEEK_HUB_SANITY" 2>/dev/null; then
    echo -e "  ${OK} sanity_check_deepseek_hub.sh référence 'cmd-deepseek_student' — check présence actif"
  else
    echo -e "  ${WARN} sanity_check_deepseek_hub.sh ne référence pas 'cmd-deepseek_student' — vérifier manuellement"
    WARNINGS=$((WARNINGS + 1))
  fi
else
  echo -e "  ${FAIL} $DEEPSEEK_HUB_SANITY — fichier introuvable"
  ERRORS=$((ERRORS + 1))
fi

# ════════════════════════════════════════════════════════════
banner "4. VÉRIFICATION ENTRYPOINTS CANONIQUES"
# ════════════════════════════════════════════════════════════

echo ""
run_check() {
  local label="$1"
  local cmd="$2"
  echo -e "${INFO} $label"
  echo -e "  Commande : $cmd"
  if eval "$cmd" > /tmp/student_val_out 2>&1; then
    echo -e "  ${OK} Exécution réussie (exit 0)"
    head -5 /tmp/student_val_out | sed 's/^/  | /'
  else
    local exit_code=$?
    echo -e "  ${WARN} Exit code : $exit_code"
    head -5 /tmp/student_val_out | sed 's/^/  | /'
    WARNINGS=$((WARNINGS + 1))
  fi
  echo ""
}

# sanity-student
if command -v sanity-student &>/dev/null; then
  run_check "sanity-student (check structure globale)" "sanity-student"
else
  echo -e "  ${FAIL} sanity-student : commande non trouvée dans PATH"
  ERRORS=$((ERRORS + 1))
fi

# cmd-student status
if command -v cmd-student &>/dev/null; then
  run_check "cmd-student status" "cmd-student status"
else
  echo -e "  ${FAIL} cmd-student : commande non trouvée dans PATH"
  ERRORS=$((ERRORS + 1))
fi

# cmd-deepseek_student show-paths
if command -v cmd-deepseek_student &>/dev/null; then
  run_check "cmd-deepseek_student show-paths" "cmd-deepseek_student show-paths"
else
  echo -e "  ${FAIL} cmd-deepseek_student : commande non trouvée dans PATH"
  ERRORS=$((ERRORS + 1))
fi

# ════════════════════════════════════════════════════════════
banner "5. VÉRIFICATION STRUCTURE RÉPERTOIRE student/"
# ════════════════════════════════════════════════════════════

echo ""
check_path() {
  local p="$1"
  local label="${2:-$1}"
  if [[ -e "$p" ]]; then
    echo -e "  ${OK} $label"
  else
    echo -e "  ${FAIL} $label — ABSENT"
    ERRORS=$((ERRORS + 1))
  fi
}

check_path "$ROOT/scripts/student_menu.sh"                           "scripts/student_menu.sh"
check_path "$ROOT/scripts/student_cmd.sh"                            "scripts/student_cmd.sh"
check_path "$ROOT/scripts/student_sanity_check.sh"                   "scripts/student_sanity_check.sh"
check_path "$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh"         "scripts/deepseek_hub/deepseek_hub_menu.sh"
check_path "$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"          "scripts/deepseek_hub/deepseek_hub_cmd.sh"
check_path "$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh" "scripts/deepseek_hub/sanity_check_deepseek_hub.sh"
check_path "$ROOT/scripts/wrappers/deepseek_student_menu.sh"         "scripts/wrappers/deepseek_student_menu.sh"
check_path "$ROOT/scripts/wrappers/deepseek_student_cmd.sh"          "scripts/wrappers/deepseek_student_cmd.sh"
check_path "$ROOT/scripts/wrappers/deepseek_student_sanity_check.sh" "scripts/wrappers/deepseek_student_sanity_check.sh"
check_path "$ROOT/bin/install_shortcuts.sh"                          "bin/install_shortcuts.sh"
check_path "$ROOT/config/shortcut_map.env"                           "config/shortcut_map.env"

# ════════════════════════════════════════════════════════════
banner "6. RÉSUMÉ"
# ════════════════════════════════════════════════════════════

echo ""
if [[ "$ERRORS" -eq 0 && "$WARNINGS" -eq 0 ]]; then
  echo -e "  ${GRN}✓ VALIDATION RÉUSSIE — 0 erreur, 0 avertissement${RST}"
elif [[ "$ERRORS" -eq 0 ]]; then
  echo -e "  ${YEL}⚠ VALIDATION PARTIELLE — 0 erreur, $WARNINGS avertissement(s)${RST}"
else
  echo -e "  ${RED}✗ VALIDATION ÉCHOUÉE — $ERRORS erreur(s), $WARNINGS avertissement(s)${RST}"
fi

echo ""
if [[ "$ERRORS" -gt 0 ]]; then
  echo -e "${INFO} Réparation des raccourcis :"
  echo -e "  bash $ROOT/bin/install_shortcuts.sh"
  echo -e "  → puis relancer : bash $ROOT/validation/validate_student_live.sh"
  echo ""
fi

# ── Auto-repair si --repair passé ───────────────────────────
if [[ "$REPAIR" -eq 1 && "$ERRORS" -gt 0 ]]; then
  echo -e "${YEL}[--repair] Lancement de install_shortcuts.sh ...${RST}"
  bash "$ROOT/bin/install_shortcuts.sh"
  echo -e "${GRN}Réparation appliquée. Relancer la validation sans --repair pour vérifier.${RST}"
fi

[[ "$ERRORS" -eq 0 ]]
