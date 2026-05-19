# GO_PROMPT_02_STUDENT_MACHINE_FACTS

## Objectif

Collecter les faits machine réels sur `student` / lab.

## Commandes Linux

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

hostnamectl || true
uname -a
lsb_release -a 2>/dev/null || cat /etc/os-release
nproc
lscpu | sed -n '1,80p'
free -h
df -h / /opt /home 2>/dev/null || df -h
```

## GPU

```bash
set -Eeuo pipefail
trap 'echo "ERROR line=$LINENO cmd=$BASH_COMMAND" >&2' ERR

command -v nvidia-smi && nvidia-smi || true
command -v rocm-smi && rocm-smi || true
lspci | grep -Ei 'vga|3d|display|nvidia|amd|intel' || true
ls /dev/dri 2>/dev/null || true
```

## Sortie attendue

```text
OS=
CPU=
RAM_TOTAL=
RAM_FREE=
GPU=
VRAM=
DISK_FREE=
VERDICT_MACHINE=LAB_OK|LAB_LIMITED|LAB_FAIL
```
