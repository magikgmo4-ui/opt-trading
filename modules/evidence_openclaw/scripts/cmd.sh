#!/usr/bin/env bash
set -euo pipefail

BASE="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

detect_workspace() {
  local tmp
  tmp="$(mktemp)"
  openclaw agents list > "$tmp"
  python3 - "$tmp" <<'PY'
import pathlib, sys
p = pathlib.Path(sys.argv[1])
lines = p.read_text().splitlines()
default_seen = False
workspace = None
for line in lines:
    s = line.strip()
    if s.startswith("- ") and "(default)" in s:
        default_seen = True
        continue
    if default_seen and s.startswith("Workspace:"):
        workspace = s.split("Workspace:", 1)[1].strip()
        break
home = pathlib.Path.home()
candidates = [
    home / ".openclaw" / "workspace-orchestrateur",
    home / ".openclaw" / "workspace",
]
if workspace:
    print(str(pathlib.Path(workspace).expanduser()))
    sys.exit(0)
for c in candidates:
    if c.exists():
        print(str(c))
        sys.exit(0)
print(str(candidates[0]))
PY
  rm -f "$tmp"
}

evidence_dir() {
  local ws
  ws="$(detect_workspace)"
  printf '%s\n' "$ws/docs_evidence/openclaw_current_state"
}

print_prompt() {
  local ev
  ev="$(evidence_dir)"
  cat <<EOF
Tu agis comme documentaliste technique OpenClaw.

Source de vérité obligatoire :
- $ev/01_doctor_status.txt
- $ev/02_configure_status.txt
- $ev/03_doctor_quick.txt
- $ev/04_workspace_context.txt

Mission :
1. lire uniquement ces fichiers,
2. en extraire uniquement les faits réellement prouvés,
3. rédiger 3 blocs texte bruts distincts :
   - ETABLI
   - RUNBOOK
   - CHANGELOG

Contraintes impératives :
- ne rien inventer
- ne pas raisonner depuis un sandbox abstrait
- ne pas parler de agent=main ou workspace-main sauf si explicitement prouvé dans ces fichiers
- ne marquer “validé” qu’un module explicitement prouvé
- inclure les modules validés si réellement prouvés
- inclure l’état réel des agents si présent
- distinguer clairement :
  - CLOSE
  - EN COURS
  - TODO
  - RISQUES / POINTS DE VIGILANCE
- format texte brut
- sortie concise, propre, exploitable
- ajouter une section finale :
  PREUVES UTILISÉES
EOF
}

run_doctor_status() {
  if command -v cmd-doctor_openclaw >/dev/null 2>&1; then
    cmd-doctor_openclaw status
  else
    echo "USER=$(whoami)"
    echo "CONFIG=$(openclaw config file 2>/dev/null || echo ~/.openclaw/openclaw.json)"
    openclaw agents list || true
  fi
}

run_configure_status() {
  if command -v cmd-configure_openclaw >/dev/null 2>&1; then
    cmd-configure_openclaw status
  else
    echo "USER=$(whoami)"
    echo "CONFIG=$(openclaw config file)"
    echo
    openclaw config validate
    echo
    openclaw agents list || true
  fi
}

run_doctor_quick() {
  if command -v cmd-doctor_openclaw >/dev/null 2>&1; then
    cmd-doctor_openclaw quick
  else
    openclaw doctor --non-interactive
    openclaw config validate
    openclaw gateway health
    openclaw gateway probe
  fi
}

export_docs() {
  local ws ev
  ws="$(detect_workspace)"
  ev="$(evidence_dir)"
  mkdir -p "$ev"
  {
    echo "USER=$(whoami)"
    echo "HOME=$HOME"
    echo "WORKSPACE=$ws"
    echo "DATE=$(date --iso-8601=seconds 2>/dev/null || date)"
    echo "HOSTNAME=$(hostname)"
  } > "$ev/04_workspace_context.txt"
  run_doctor_status > "$ev/01_doctor_status.txt"
  run_configure_status > "$ev/02_configure_status.txt"
  run_doctor_quick > "$ev/03_doctor_quick.txt"
  print_prompt > "$ev/90_PROMPT_DOCS.txt"
  echo "EVIDENCE_DIR=$ev"
  ls -lah "$ev"
}

case "${1:-help}" in
  sanity)
    "$BASE/scripts/sanity.sh"
    ;;
  detect-workspace)
    detect_workspace
    ;;
  status)
    echo "USER=$(whoami)"
    echo "WORKSPACE=$(detect_workspace)"
    echo "EVIDENCE_DIR=$(evidence_dir)"
    ;;
  export-docs)
    export_docs
    ;;
  print-doc-prompt)
    print_prompt
    ;;
  evidence-dir)
    evidence_dir
    ;;
  show-files)
    ev="$(evidence_dir)"
    ls -lah "$ev"
    ;;
  *)
    echo "Usage: cmd.sh sanity|detect-workspace|status|export-docs|print-doc-prompt|evidence-dir|show-files"
    exit 1
    ;;
esac
