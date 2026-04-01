#!/usr/bin/env bash
set -euo pipefail

SCRIPT_PATH="$(readlink -f "${BASH_SOURCE[0]}")"
MODULE_DIR="$(cd "$(dirname "$SCRIPT_PATH")/.." && pwd)"
PYTHON_BIN="${PYTHON_BIN:-python3}"
APP="$MODULE_DIR/app/deploy_module_multi_machine.py"
CMD="$MODULE_DIR/scripts/deploy_module_multi_machine_cmd.sh"
MENU="$MODULE_DIR/scripts/deploy_module_multi_machine_menu.sh"
INSTALLER="$MODULE_DIR/scripts/install_module.sh"
FALLBACK="$MODULE_DIR/config/hosts_fallback.json"

fail() {
  echo "FAIL: $*" >&2
  exit 1
}

[ -f "$APP" ] || fail "app manquant"
[ -x "$CMD" ] || fail "cmd non executable"
[ -x "$MENU" ] || fail "menu non executable"
[ -x "$INSTALLER" ] || fail "install_module.sh non executable"
[ -f "$FALLBACK" ] || fail "hosts_fallback.json manquant"

"$PYTHON_BIN" -m py_compile "$APP"
"$CMD" status >/dev/null

"$PYTHON_BIN" - "$APP" "$MODULE_DIR" "$FALLBACK" <<'PY'
import runpy
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

app_path = Path(sys.argv[1])
module_dir = Path(sys.argv[2])
fallback = Path(sys.argv[3])
ns = runpy.run_path(str(app_path))
RegistryView = ns["RegistryView"]
Deployer = ns["Deployer"]
build_ssh_command = ns["build_ssh_command"]

registry = RegistryView(Path("/opt/trading/registry"), fallback)
args = SimpleNamespace(
    module_name="deploy_module_multi_machine",
    source_dir=str(module_dir),
    install_path=None,
    targets="student@192.168.0.103,ghost@192.168.0.100",
    sanity_relpath=None,
    dry_run=True,
    keep_tmp=False,
    no_backup=False,
    post_install=False,
)
plan = Deployer(registry, args).build_plan()
targets = [machine.ssh_target for machine in plan.targets]
expected = ["student@192.168.0.103", "ghost@192.168.0.100"]
if targets != expected:
    raise SystemExit(f"unexpected targets resolved: {targets}")

deployer = Deployer(registry, args)
script = deployer._build_remote_install_script(
    remote_install="/opt/trading/example_module",
    remote_tmp="/tmp/example_module.tar.gz",
    backup_dir="/opt/trading/example_module.bak/ts",
    sanity_cmd="/opt/trading/example_module/scripts/sanity_check.sh",
    keep_tmp=False,
    no_backup=False,
)
if "then;" in script:
    raise SystemExit("unexpected 'then;' sequence in generated remote script")
subprocess.run(["bash", "-n"], input=script, text=True, check=True)
ssh_cmd = build_ssh_command("student@192.168.0.103", ["bash", "-lc", script])
if ssh_cmd[:2] != ["ssh", "student@192.168.0.103"] or len(ssh_cmd) != 3:
    raise SystemExit(f"unexpected ssh command layout: {ssh_cmd}")
if not ssh_cmd[2].startswith("bash -lc "):
    raise SystemExit(f"unexpected ssh remote command: {ssh_cmd[2]}")
post_script = deployer._build_remote_post_install_script(
    remote_install="/opt/trading/example_module",
    post_install_script="/opt/trading/example_module/scripts/install_module.sh",
)
subprocess.run(["bash", "-n"], input=post_script, text=True, check=True)
print("Smoke deploy syntax OK")
PY

"$CMD" deploy --module-name deploy_module_multi_machine --source-dir "$MODULE_DIR" --targets student,db-layer --dry-run --post-install >/dev/null

echo "PASS: deploy_module_multi_machine sanity OK"
