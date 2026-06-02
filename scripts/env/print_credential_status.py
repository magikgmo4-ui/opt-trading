#!/usr/bin/env python3
import sys
import argparse
import yaml
from pathlib import Path

def load_registry(name):
    path = Path(__file__).parent.parent.parent / "configs" / "env" / "registry" / f"{name}.yaml"
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def print_credential_status(machine_id):
    print(f"Credential status for machine: {machine_id}")

    machines = load_registry("machines")
    roles_reg = load_registry("roles")
    creds_reg = load_registry("credentials")

    machine = next((m for m in machines['machines'] if m['id'] == machine_id), None)
    if not machine:
        print(f"Error: Machine '{machine_id}' not found.")
        return

    assigned_roles = machine.get('roles', [])
    print(f"Assigned Roles: {', '.join(assigned_roles) if assigned_roles else 'None'}")

    for role_id in assigned_roles:
        print(f"\nRole: {role_id}")
        role = next((r for r in roles_reg['roles'] if r['id'] == role_id), None)
        if not role:
            print("  Error: Role definition missing in registry.")
            continue

        for cred_id in role.get('credentials', []):
            cred = next((c for c in creds_reg['credentials'] if c['id'] == cred_id), None)
            if cred:
                # In a real impl, we'd check if the secret exists on disk/env
                # Here we just show it's tracked.
                print(f"  - {cred['env_var']}: TRACKED")
            else:
                print(f"  - {cred_id}: UNKNOWN")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print credential status for a machine.")
    parser.add_argument("--machine", required=True)
    args = parser.parse_args()

    print_credential_status(args.machine)
