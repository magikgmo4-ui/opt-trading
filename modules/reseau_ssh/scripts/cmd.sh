#!/usr/bin/env bash
set -euo pipefail

RESEAU_SSH_ENTRY_SOURCE="${BASH_SOURCE[0]}"
RESEAU_SSH_SOURCE_PATH="${BASH_SOURCE[0]}"
while [ -L "$RESEAU_SSH_SOURCE_PATH" ]; do
  RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
  RESEAU_SSH_SOURCE_PATH="$(readlink "$RESEAU_SSH_SOURCE_PATH")"
  case "$RESEAU_SSH_SOURCE_PATH" in
    /*) ;;
    *) RESEAU_SSH_SOURCE_PATH="$RESEAU_SSH_SOURCE_DIR/$RESEAU_SSH_SOURCE_PATH" ;;
  esac
done
RESEAU_SSH_SOURCE_DIR="$(cd "$(dirname "$RESEAU_SSH_SOURCE_PATH")" && pwd -P)"
# shellcheck source=./_reseau_ssh_common.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_common.sh"
# shellcheck source=./_reseau_ssh_baseline.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_baseline.sh"
# shellcheck source=./_reseau_ssh_transition.sh
source "$RESEAU_SSH_SOURCE_DIR/_reseau_ssh_transition.sh"

cmd="${1:-help}"
shift || true

case "$cmd" in
  info|path)
    reseau_ssh_print_info
    ;;
  readme)
    reseau_ssh_readme
    ;;
  ls)
    (cd "$RESEAU_SSH_MODULE_DIR" && find . -maxdepth 3 -type f | sed 's#^\./##' | sort) | sed -n '1,240p'
    ;;
  menu)
    exec bash "$RESEAU_SSH_TOP_MENU" "$@"
    ;;
  sanity)
    exec bash "$RESEAU_SSH_TOP_SANITY" "$@"
    ;;
  wg-install|wg-genkeys|wg-showpub|wg-render|wg-render-windows|wg-apply|wg-up|wg-down|wg-status|fw-dry-run|fw-apply)
    reseau_ssh_require_exec "$RESEAU_SSH_IMPL_CMD"
    exec bash "$RESEAU_SSH_IMPL_CMD" "$cmd" "$@"
    ;;
  wg-show)
    echo "INFO: wg-show is deprecated; delegating to wg-status." >&2
    reseau_ssh_require_exec "$RESEAU_SSH_IMPL_CMD"
    exec bash "$RESEAU_SSH_IMPL_CMD" wg-status "$@"
    ;;
  bootstrap|ssh-hardening-safe|ssh-lockdown)
    echo "INFO: $cmd is handled by the canonical reseau_ssh facade." >&2
    case "$cmd" in
      bootstrap) reseau_ssh_transition_bootstrap "$@" ;;
      ssh-hardening-safe) reseau_ssh_transition_ssh_hardening_safe "$@" ;;
      ssh-lockdown) reseau_ssh_transition_ssh_lockdown "$@" ;;
    esac
    ;;
  wg-server-init|wg-client-init|wg-add-peer)
    cat >&2 <<EOF
ERROR: $cmd has been removed from the canonical facade.
Use the canonical workflow instead:
  cmd-reseau_ssh wg-genkeys
  cmd-reseau_ssh wg-render
  cmd-reseau_ssh wg-apply
  cmd-reseau_ssh wg-up
  cmd-reseau_ssh wg-status

If you explicitly need the legacy compat backend, call it directly:
  restore it from:
  $RESEAU_SSH_ARCHIVE_RUNTIME_DIR
EOF
    exit 2
    ;;
  baseline-dry-run)
    reseau_ssh_baseline_apply_linux "$@"
    ;;
  baseline-apply)
    reseau_ssh_baseline_apply_linux --apply "$@"
    ;;
  baseline-hostname)
    reseau_ssh_baseline_apply_hostname "$@"
    ;;
  baseline-sanity)
    reseau_ssh_baseline_sanity "$@"
    ;;
  baseline-show-hosts)
    reseau_ssh_baseline_show_hosts "$@"
    ;;
  baseline-show-ssh)
    reseau_ssh_baseline_show_ssh "$@"
    ;;
  help|-h|--help|"")
    cat <<'EOF'
cmd-reseau_ssh <command> [args]

Canonical facade:
  info | path
  readme
  ls
  menu
  sanity

Step 2 implementation:
  wg-install
  wg-genkeys
  wg-showpub
  wg-render
  wg-render-windows
  wg-apply
  wg-up
  wg-down
  wg-status
  fw-dry-run
  fw-apply

Canonical SSH bootstrap / hardening:
  bootstrap
  ssh-hardening-safe
  ssh-lockdown
  wg-show               # deprecated alias to wg-status

Baseline compat (step1b):
  baseline-dry-run
  baseline-apply
  baseline-hostname <admin-trading|db-layer|student>
  baseline-sanity
  baseline-show-hosts
  baseline-show-ssh
EOF
    ;;
  *)
    echo "ERROR: unknown command: $cmd" >&2
    exit 1
    ;;
esac
