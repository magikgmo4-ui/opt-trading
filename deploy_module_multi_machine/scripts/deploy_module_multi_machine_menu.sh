#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
MODULE_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
CMD="$MODULE_DIR/scripts/deploy_module_multi_machine_cmd.sh"
LOG_DIR="$MODULE_DIR/logs"
mkdir -p "$LOG_DIR"
LOG_FILE="$LOG_DIR/menu_$(date +%Y%m%d_%H%M%S).log"

run_and_log() {
  echo
  echo "[RUN] $*"
  "$@" 2>&1 | tee -a "$LOG_FILE"
}

prompt_common_flags() {
  read -r -p "Nom du module cible: " MODULE_NAME
  read -r -p "Source locale (ex: /opt/trading/modules/validated_prompt_factory): " SOURCE_DIR
  read -r -p "Cibles CSV (ex: student,db-layer): " TARGETS
  EXTRA_ARGS=(--module-name "$MODULE_NAME" --source-dir "$SOURCE_DIR" --targets "$TARGETS")
}

while true; do
  cat <<EOF

=== deploy_module_multi_machine ===
Log: $LOG_FILE
1) Status registry / fallback
2) Plan de déploiement (dry-run conseillé)
3) Déployer un module
4) Lancer la sanity distante
5) Quitter
EOF
  read -r -p "Choix: " CHOICE
  case "$CHOICE" in
    1)
      run_and_log "$CMD" status
      ;;
    2)
      prompt_common_flags
      run_and_log "$CMD" plan "${EXTRA_ARGS[@]}" --dry-run
      ;;
    3)
      prompt_common_flags
      read -r -p "Dry-run seulement ? [y/N]: " DRY
      if [[ "${DRY:-N}" =~ ^[Yy]$ ]]; then
        run_and_log "$CMD" deploy "${EXTRA_ARGS[@]}" --dry-run
      else
        run_and_log "$CMD" deploy "${EXTRA_ARGS[@]}"
      fi
      ;;
    4)
      prompt_common_flags
      run_and_log "$CMD" sanity "${EXTRA_ARGS[@]}"
      ;;
    5)
      echo "Sortie."
      exit 0
      ;;
    *)
      echo "Choix invalide."
      ;;
  esac
done
