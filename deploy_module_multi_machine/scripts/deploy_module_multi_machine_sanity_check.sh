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
import shutil
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
build_bundle = ns["build_bundle"]
make_remote_lock_path = ns["make_remote_lock_path"]
make_run_id = ns["make_run_id"]

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
    cleanup_stale_lock=False,
    lock_stale_after_seconds=3600,
)
plan = Deployer(registry, args).build_plan()
targets = [machine.ssh_target for machine in plan.targets]
expected = ["student@192.168.0.103", "ghost@192.168.0.100"]
if targets != expected:
    raise SystemExit(f"unexpected targets resolved: {targets}")

deployer = Deployer(registry, args)
run_id_one = make_run_id()
run_id_two = make_run_id()
if run_id_one == run_id_two:
    raise SystemExit("run_id collision detected")
lock_path = make_remote_lock_path("/opt/trading/example_module")
if not lock_path.startswith("/tmp/deploy_module_multi_machine_locks/"):
    raise SystemExit(f"unexpected lock path: {lock_path}")
script = deployer._build_remote_install_script(
    run_id="RIDTEST",
    remote_install="/opt/trading/example_module",
    remote_tmp="/tmp/example_module.tar.gz",
    backup_dir="/opt/trading/example_module.bak/ts",
    sanity_cmd="/opt/trading/example_module/scripts/sanity_check.sh",
    keep_tmp=False,
    no_backup=False,
)
if "then;" in script:
    raise SystemExit("unexpected 'then;' sequence in generated remote script")
if '/tmp/deploy_stage.${RUN_ID}.XXXXXX' not in script:
    raise SystemExit("missing run-scoped staging prefix")
subprocess.run(["bash", "-n"], input=script, text=True, check=True)
ssh_cmd = build_ssh_command("student@192.168.0.103", ["bash", "-lc", script])
if ssh_cmd[:2] != ["ssh", "student@192.168.0.103"] or len(ssh_cmd) != 3:
    raise SystemExit(f"unexpected ssh command layout: {ssh_cmd}")
if not ssh_cmd[2].startswith("bash -lc "):
    raise SystemExit(f"unexpected ssh remote command: {ssh_cmd[2]}")
bundle_path = build_bundle(module_dir, "RIDTEST")
if "RIDTEST" not in bundle_path.name:
    raise SystemExit(f"bundle path is not run-scoped: {bundle_path}")
shutil.rmtree(bundle_path.parent)
lock_acquire_script = deployer._build_remote_lock_acquire_script(lock_path=lock_path, run_id="RIDTEST")
subprocess.run(["bash", "-n"], input=lock_acquire_script, text=True, check=True)
lock_release_script = deployer._build_remote_lock_release_script(lock_path=lock_path, run_id="RIDTEST")
subprocess.run(["bash", "-n"], input=lock_release_script, text=True, check=True)
lock_inspect_script = deployer._build_remote_lock_inspect_script(lock_path=lock_path, stale_after_seconds=3600)
subprocess.run(["bash", "-n"], input=lock_inspect_script, text=True, check=True)
lock_cleanup_script = deployer._build_remote_lock_cleanup_script(lock_path=lock_path, stale_after_seconds=3600)
subprocess.run(["bash", "-n"], input=lock_cleanup_script, text=True, check=True)
post_script = deployer._build_remote_post_install_script(
    remote_install="/opt/trading/example_module",
    post_install_script="/opt/trading/example_module/scripts/install_module.sh",
)
subprocess.run(["bash", "-n"], input=post_script, text=True, check=True)
preflight_script = deployer._build_remote_preflight_script()
subprocess.run(["bash", "-n"], input=preflight_script, text=True, check=True)
print("Smoke deploy syntax OK")
PY

"$CMD" deploy --module-name deploy_module_multi_machine --source-dir "$MODULE_DIR" --targets student,db-layer --dry-run --post-install >/dev/null
"$CMD" preflight --module-name module_contextuals_shell --source-dir /opt/trading/modules/module_contextuals_shell --targets student,db-layer --lock-stale-after-seconds 3600 >/dev/null

echo "PASS: deploy_module_multi_machine sanity OK"
