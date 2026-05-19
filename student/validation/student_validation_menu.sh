#!/usr/bin/env bash
# ============================================================
# STUDENT VALIDATION — MENU INTERACTIF
# student_validation_menu.sh
# ============================================================
# Mission  : GO_STUDENT_LIVE_VALIDATION_PACK_01
# Date     : 2026-03-20
#
# Menu interactif pour lancer les vérifications du pack
# validation student depuis un terminal.
#
# Usage : bash /opt/trading/student/validation/student_validation_menu.sh
# ============================================================

ROOT="/opt/trading/student"
VAL_DIR="$ROOT/validation"

RED='\033[0;31m'
GRN='\033[0;32m'
YEL='\033[1;33m'
BLU='\033[0;34m'
CYA='\033[0;36m'
RST='\033[0m'

clear_screen() {
  printf '\033[2J\033[H'
}

header() {
  clear_screen
  echo -e "${CYA}╔══════════════════════════════════════════════════════════╗${RST}"
  echo -e "${CYA}║         STUDENT VALIDATION PACK — MENU PRINCIPAL         ║${RST}"
  echo -e "${CYA}║  opt-trading / sot/mainline — GO_STUDENT_LIVE_VAL_01     ║${RST}"
  echo -e "${CYA}╚══════════════════════════════════════════════════════════╝${RST}"
  echo ""
}

pause() {
  echo ""
  echo -e "${YEL}Appuyer sur Entrée pour continuer...${RST}"
  read -r
}

menu_principal() {
  header
  echo -e "  ${BLU}1)${RST}  Validation live complète"
  echo -e "  ${BLU}2)${RST}  Validation live complète + auto-repair"
  echo -e "  ${BLU}3)${RST}  Vérifier les raccourcis uniquement"
  echo -e "  ${BLU}4)${RST}  Sanity check structurel"
  echo -e "  ${BLU}5)${RST}  Afficher l'état du pack"
  echo -e "  ${BLU}6)${RST}  Lancer sanity-student (entrypoint canonique)"
  echo -e "  ${BLU}7)${RST}  Lancer cmd-student status"
  echo -e "  ${BLU}8)${RST}  Lancer cmd-deepseek_student show-paths"
  echo -e "  ${BLU}9)${RST}  Réparer les raccourcis (install_shortcuts.sh)"
  echo ""
  echo -e "  ${RED}q)${RST}  Quitter"
  echo ""
  echo -ne "  Choix : "
  read -r choice

  case "$choice" in
    1)
      header
      echo -e "${CYA}── Validation live complète ────────────────────────────────${RST}"
      echo ""
      bash "$VAL_DIR/validate_student_live.sh" || true
      pause
      ;;
    2)
      header
      echo -e "${CYA}── Validation live + auto-repair ───────────────────────────${RST}"
      echo ""
      bash "$VAL_DIR/validate_student_live.sh" --repair || true
      pause
      ;;
    3)
      header
      bash "$VAL_DIR/student_validation_cmd.sh" shortcuts || true
      pause
      ;;
    4)
      header
      bash "$VAL_DIR/student_validation_sanity_check.sh" || true
      pause
      ;;
    5)
      header
      bash "$VAL_DIR/student_validation_cmd.sh" status || true
      pause
      ;;
    6)
      header
      echo -e "${CYA}── sanity-student ──────────────────────────────────────────${RST}"
      echo ""
      if command -v sanity-student &>/dev/null; then
        sanity-student || true
      else
        echo -e "${RED}sanity-student non trouvé dans PATH${RST}"
      fi
      pause
      ;;
    7)
      header
      echo -e "${CYA}── cmd-student status ──────────────────────────────────────${RST}"
      echo ""
      if command -v cmd-student &>/dev/null; then
        cmd-student status || true
      else
        echo -e "${RED}cmd-student non trouvé dans PATH${RST}"
      fi
      pause
      ;;
    8)
      header
      echo -e "${CYA}── cmd-deepseek_student show-paths ─────────────────────────${RST}"
      echo ""
      if command -v cmd-deepseek_student &>/dev/null; then
        cmd-deepseek_student show-paths || true
      else
        echo -e "${RED}cmd-deepseek_student non trouvé dans PATH${RST}"
      fi
      pause
      ;;
    9)
      header
      echo -e "${CYA}── Réparation des raccourcis ───────────────────────────────${RST}"
      echo ""
      echo -e "${YEL}Lancement de : bash $ROOT/bin/install_shortcuts.sh${RST}"
      echo ""
      bash "$ROOT/bin/install_shortcuts.sh" || true
      echo ""
      echo -e "${GRN}Réparation terminée.${RST}"
      pause
      ;;
    q|Q)
      echo ""
      exit 0
      ;;
    *)
      echo -e "${RED}Choix invalide.${RST}"
      sleep 1
      ;;
  esac
}

# ── Boucle principale ───────────────────────────────────────
while true; do
  menu_principal
done
