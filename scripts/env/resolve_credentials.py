#!/usr/bin/env python3
import sys
import argparse
import yaml
import os
from pathlib import Path

def load_registry(name):
    path = Path(__file__).parent.parent.parent / "configs" / "env" / "registry" / f"{name}.yaml"
    with open(path, 'r') as f:
        return yaml.safe_load(f)

def resolve_credentials(machine_id, job_id, print_status=False):
    if print_status:
        print(f"Resolving credentials for machine: {machine_id}, job: {job_id}")

    machines = load_registry("machines")
    jobs = load_registry("jobs")
    roles = load_registry("roles")
    creds_reg = load_registry("credentials")

    machine = next((m for m in machines['machines'] if m['id'] == machine_id), None)
    job = next((j for j in jobs['jobs'] if j['id'] == job_id), None)

    if not machine or not job:
        if print_status: print("Error: Machine or Job not found.")
        return {}

    required_role_id = job.get('requires_role')
    if not required_role_id:
        if print_status: print("Status: OK (No role required)")
        return {}

    if required_role_id not in machine.get('roles', []):
        if print_status: print(f"Status: DENIED (Role {required_role_id} missing)")
        return {}

    # Logic to "resolve" would normally involve loading values into a dict or exporting them
    # But we NEVER return real values to the console if print_status is on.

    if print_status:
        role = next((r for r in roles['roles'] if r['id'] == required_role_id), None)
        if role:
            print(f"Authorized Credentials for {required_role_id}:")
            for cred_id in role.get('credentials', []):
                cred = next((c for c in creds_reg['credentials'] if c['id'] == cred_id), None)
                if cred:
                    print(f"- {cred['env_var']} (Authorized)")
        print("Status: READY_TO_INJECT")

    return {"status": "authorized", "role": required_role_id}

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Resolve and inject credentials.")
    parser.add_argument("--machine", required=True)
    parser.add_argument("--job", required=True)
    parser.add_argument("--print-status", action="store_true")
    args = parser.parse_args()

    resolve_credentials(args.machine, args.job, args.print_status)
