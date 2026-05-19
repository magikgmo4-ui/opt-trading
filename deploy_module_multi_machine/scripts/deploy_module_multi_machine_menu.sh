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
  read -r -p "Cibles CSV [student,db-layer]: " TARGETS_INPUT
  TARGETS="${TARGETS_INPUT:-student,db-layer}"
  EXTRA_ARGS=(--module-name "$MODULE_NAME" --source-dir "$SOURCE_DIR" --targets "$TARGETS")
}

prompt_optional_post_install() {
  POST_INSTALL_ARGS=()
  read -r -p "Activer le post-install distant si disponible ? [y/N]: " POST_INSTALL
  if [[ "${POST_INSTALL:-N}" =~ ^[Yy]$ ]]; then
    POST_INSTALL_ARGS=(--post-install)
  fi
}

while true; do
  cat <<EOF

=== deploy_module_multi_machine ===
Log: $LOG_FILE
1) Status registry / fallback
2) Lancer la sanity distante
3) Plan de déploiement (dry-run)
4) Préflight distant
5) Déployer un module
6) Déployer un module + post-install
7) Quitter
EOF
  read -r -p "Choix: " CHOICE
  case "$CHOICE" in
    1)
      run_and_log "$CMD" status
      ;;
    2)
      prompt_common_flags
      run_and_log "$CMD" sanity "${EXTRA_ARGS[@]}"
      ;;
    3)
      prompt_common_flags
      run_and_log "$CMD" plan "${EXTRA_ARGS[@]}" --dry-run
      ;;
    4)
      prompt_common_flags
      prompt_optional_post_install
      run_and_log "$CMD" preflight "${EXTRA_ARGS[@]}" "${POST_INSTALL_ARGS[@]}"
      ;;
    5)
      prompt_common_flags
      run_and_log "$CMD" deploy "${EXTRA_ARGS[@]}"
      ;;
    6)
      prompt_common_flags
      run_and_log "$CMD" deploy "${EXTRA_ARGS[@]}" --post-install
      ;;
    7)
      echo "Sortie."
      exit 0
      ;;
    *)
      echo "Choix invalide."
      ;;
  esac
done
