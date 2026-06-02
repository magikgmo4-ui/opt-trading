#!/usr/bin/env python3
import sys
import argparse
import os

def redact_env(env_file):
    if not os.path.exists(env_file):
        print(f"Error: File {env_file} not found.")
        return

    print(f"Redacting environment file: {env_file} (Simulation)")
    with open(env_file, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                print(line)
                continue
            if '=' in line:
                key, _ = line.split('=', 1)
                print(f"{key}=[REDACTED]")
            else:
                print(line)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Redact values in an environment file.")
    parser.add_argument("--env-file", required=True)
    args = parser.parse_args()

    redact_env(args.env_file)
