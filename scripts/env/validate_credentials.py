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

def validate_credentials(machine_id, job_id):
    print(f"Validating credentials for machine: {machine_id}, job: {job_id}")

    machines = load_registry("machines")
    jobs = load_registry("jobs")
    roles = load_registry("roles")
    creds_reg = load_registry("credentials")

    # 1. Find machine
    machine = next((m for m in machines['machines'] if m['id'] == machine_id), None)
    if not machine:
        print(f"Error: Machine '{machine_id}' not found in registry.")
        return False

    # 2. Find job
    job = next((j for j in jobs['jobs'] if j['id'] == job_id), None)
    if not job:
        print(f"Error: Job '{job_id}' not found in registry.")
        return False

    required_role_id = job.get('requires_role')
    if not required_role_id:
        print(f"Job '{job_id}' requires no specific role. OK.")
        return True

    # 3. Check machine roles (Active vs Eligible vs Forbidden)
    if required_role_id in machine.get('roles', []):
        pass # Active
    elif required_role_id in machine.get('eligible_roles', []):
        print(f"Status: ELIGIBLE_DISABLED (Role '{required_role_id}' is eligible but not active on '{machine_id}')")
        return False
    else:
        print(f"Status: DENIED (Machine '{machine_id}' is forbidden from role '{required_role_id}')")
        return False

    # 4. Check credentials for the role
    role = next((r for r in roles['roles'] if r['id'] == required_role_id), None)
    if not role:
        print(f"Error: Role '{required_role_id}' not found in registry.")
        return False

    all_ok = True
    for cred_id in role.get('credentials', []):
        cred = next((c for c in creds_reg['credentials'] if c['id'] == cred_id), None)
        if not cred:
            print(f"- {cred_id}: UNKNOWN (Not in credentials registry)")
            all_ok = False
            continue

        env_var = cred.get('env_var')
        # Check if env var is set
        if env_var in os.environ:
            print(f"- {env_var}: OK")
        else:
            local_env_dir = Path("/etc/opt-trading/env.d")
            role_env_file = local_env_dir / f"{required_role_id}.env"

            if role_env_file.exists():
                 print(f"- {env_var}: OK (via {role_env_file})")
            else:
                 print(f"- {env_var}: MISSING")
                 all_ok = False

    return all_ok

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate credentials for a machine and job.")
    parser.add_argument("--machine", required=True)
    parser.add_argument("--job", required=True)
    args = parser.parse_args()

    if not validate_credentials(args.machine, args.job):
        sys.exit(1)
