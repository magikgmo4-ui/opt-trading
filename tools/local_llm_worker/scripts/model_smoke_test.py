#!/usr/bin/env python3
"""Smoke test for a local Ollama model."""

from __future__ import annotations

import argparse
import subprocess
import sys


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", required=True)
    parser.add_argument(
        "--prompt",
        default='Réponds seulement avec ce JSON exact: {"status":"OK_LOCAL_MODEL"}',
    )
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    try:
        proc = subprocess.run(
            ["ollama", "run", args.model],
            input=args.prompt,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=args.timeout,
            check=False,
        )
    except FileNotFoundError:
        print("Ollama introuvable. Installer ou vérifier le PATH.", file=sys.stderr)
        return 127
    except subprocess.TimeoutExpired:
        print("Timeout: modèle trop lent ou non disponible.", file=sys.stderr)
        return 124

    if proc.returncode != 0:
        print(proc.stderr.strip(), file=sys.stderr)
        return proc.returncode

    print(proc.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
