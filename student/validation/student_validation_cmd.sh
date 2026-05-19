#!/usr/bin/env bash
# ============================================================
# STUDENT VALIDATION — CMD DISPATCHER
# student_validation_cmd.sh
# ============================================================
# Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
# Date     : 2026-03-20
#
# Usage : student_validation_cmd.sh <commande> [options]
#
# Commandes disponibles :
#   run           — lancer la validation live complète
#   run --repair  — lancer la validation avec auto-repair
#   shortcuts     — vérifier uniquement les raccourcis
#   sanity        — lancer le sanity check structurel
#   status        — afficher l'état du pack validation
#   help          — afficher cette aide
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

usage() {
  echo -e "${CYA}student_validation_cmd — Dispatcher du pack validation student${RST}"
  echo ""
  echo "Usage : student_validation_cmd.sh <commande> [options]"
  echo ""
  echo "Commandes :"
  echo "  run           Lancer la validation live complète"
  echo "  run --repair  Lancer la validation + auto-repair si erreurs"
  echo "  shortcuts     Vérifier uniquement les 9 raccourcis globaux"
  echo "  sanity        Lancer le sanity check structurel"
  echo "  status        Afficher l'état du pack validation"
  echo "  help          Afficher cette aide"
  echo ""
  echo "Exemples :"
  echo "  bash $VAL_DIR/student_validation_cmd.sh run"
  echo "  bash $VAL_DIR/student_validation_cmd.sh run --repair"
  echo "  bash $VAL_DIR/student_validation_cmd.sh shortcuts"
}

cmd_status() {
  echo -e "${CYA}── État du pack validation student ────────────────────────${RST}"
  echo -e "  Root        : $ROOT"
  echo -e "  Val dir     : $VAL_DIR"
  echo ""
  local files=(
    "validate_student_live.sh"
    "student_validation_cmd.sh"
    "student_validation_menu.sh"
    "student_validation_sanity_check.sh"
    "RUNBOOK.md"
    "HANDOFF.md"
  )
  for f in "${files[@]}"; do
    if [[ -f "$VAL_DIR/$f" ]]; then
      echo -e "  ${GRN}[PRÉSENT]${RST}  $f"
    else
      echo -e "  ${RED}[ABSENT]${RST}   $f"
    fi
  done
  echo ""
  echo -e "  Raccourcis installés (/usr/local/bin) :"
  local shortcuts=(menu-deepseek_hub cmd-deepseek_hub sanity-deepseek_hub
                   menu-deepseek_student cmd-deepseek_student sanity-deepseek_student
                   menu-student cmd-student sanity-student)
  for s in "${shortcuts[@]}"; do
    if [[ -L "/usr/local/bin/$s" ]]; then
      local tgt
      tgt=$(readlink -f "/usr/local/bin/$s" 2>/dev/null || echo "?")
      echo -e "    ${GRN}[LN]${RST}  $s → $tgt"
    else
      echo -e "    ${RED}[XX]${RST}  $s — absent"
    fi
  done
}

cmd_shortcuts_only() {
  echo -e "${CYA}── Vérification raccourcis uniquement ──────────────────────${RST}"
  local shortcuts=(
    "menu-deepseek_hub:$ROOT/scripts/deepseek_hub/deepseek_hub_menu.sh"
    "cmd-deepseek_hub:$ROOT/scripts/deepseek_hub/deepseek_hub_cmd.sh"
    "sanity-deepseek_hub:$ROOT/scripts/deepseek_hub/sanity_check_deepseek_hub.sh"
    "menu-deepseek_student:$ROOT/scripts/wrappers/deepseek_student_menu.sh"
    "cmd-deepseek_student:$ROOT/scripts/wrappers/deepseek_student_cmd.sh"
    "sanity-deepseek_student:$ROOT/scripts/wrappers/deepseek_student_sanity_check.sh"
    "menu-student:$ROOT/scripts/student_menu.sh"
    "cmd-student:$ROOT/scripts/student_cmd.sh"
    "sanity-student:$ROOT/scripts/student_sanity_check.sh"
  )
  local errors=0
  for entry in "${shortcuts[@]}"; do
    local name="${entry%%:*}"
    local expected="${entry##*:}"
    local link="/usr/local/bin/$name"
    if [[ ! -L "$link" ]]; then
      echo -e "  ${RED}[FAIL]${RST} $name — lien absent"
      errors=$((errors + 1))
    else
      local actual
      actual=$(readlink -f "$link" 2>/dev/null || echo "ERR")
      if [[ "$actual" == "$expected" ]]; then
        echo -e "  ${GRN}[OK]${RST}   $name → OK"
      else
        echo -e "  ${RED}[FAIL]${RST} $name"
        echo -e "         attendu : $expected"
        echo -e "         obtenu  : $actual"
        errors=$((errors + 1))
      fi
    fi
  done
  echo ""
  if [[ "$errors" -eq 0 ]]; then
    echo -e "  ${GRN}✓ Tous les raccourcis sont conformes.${RST}"
  else
    echo -e "  ${RED}✗ $errors erreur(s) détectée(s).${RST}"
    echo -e "  ${YEL}Réparation : bash $ROOT/bin/install_shortcuts.sh${RST}"
    return 1
  fi
}

# ── Dispatch ────────────────────────────────────────────────

CMD="${1:-help}"

case "$CMD" in
  run)
    shift || true
    bash "$VAL_DIR/validate_student_live.sh" "$@"
    ;;
  shortcuts)
    cmd_shortcuts_only
    ;;
  sanity)
    bash "$VAL_DIR/student_validation_sanity_check.sh"
    ;;
  status)
    cmd_status
    ;;
  help|--help|-h)
    usage
    ;;
  *)
    echo -e "${RED}Commande inconnue : $CMD${RST}"
    echo ""
    usage
    exit 1
    ;;
esac
