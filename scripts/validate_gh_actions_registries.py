import os
import sys
import yaml
from typing import List, Optional, Any, Dict

# --- Validation Logic without Pydantic ---

def check_required_keys(data: Dict[str, Any], required_keys: List[str], context: str):
    missing = [k for k in required_keys if k not in data]
    if missing:
        return [f"Missing keys {missing} in {context}"]
    return []

def validate_registries(inventory_path: str, registry_path: str):
    errors = []

    # 1. Load files
    try:
        with open(inventory_path, 'r') as f:
            inventory_data = yaml.safe_load(f)
        with open(registry_path, 'r') as f:
            registry_data = yaml.safe_load(f)
    except Exception as e:
        print(f"[FAIL] Error loading YAML files: {e}")
        sys.exit(1)

    # 2. Basic Schema Validation (Manual)
    
    # Inventory validation
    inv_required = ["registry_id", "target", "version", "status", "source_ref", "updated_at", "workflows"]
    errors.extend(check_required_keys(inventory_data, inv_required, "inventory root"))
    
    if "workflows" in inventory_data:
        wf_required = ["workflow_id", "path", "name", "triggers", "permissions", "jobs", "role", "orchestrable_by_openclaw", "risk_level", "requires_secret", "dedup_status"]
        for i, wf in enumerate(inventory_data["workflows"]):
            errors.extend(check_required_keys(wf, wf_required, f"workflow index {i} ({wf.get('workflow_id', 'unknown')})"))

    # Registry validation
    reg_required = ["registry_id", "target", "version", "status", "updated_at", "jobs"]
    errors.extend(check_required_keys(registry_data, reg_required, "registry root"))
    
    if "jobs" in registry_data:
        job_required = ["job_id", "role", "trigger", "owner_surface", "orchestrable_by_openclaw", "input_schema", "output_schema", "risk_level", "requires_secret", "duplicates", "status"]
        for i, job in enumerate(registry_data["jobs"]):
            errors.extend(check_required_keys(job, job_required, f"job index {i} ({job.get('job_id', 'unknown')})"))

    if errors:
        for err in errors:
            print(f"[FAIL] {err}")
        sys.exit(1)

    print("[PASS] Basic schema validation")

    # 3. Integrity Checks
    
    # Check 3.1: Unicity of Job IDs
    job_ids = [job["job_id"] for job in registry_data["jobs"]]
    if len(job_ids) != len(set(job_ids)):
        duplicates = [jd for jd in job_ids if job_ids.count(jd) > 1]
        err = f"Duplicate job_ids found in registry: {list(set(duplicates))}"
        print(f"[FAIL] {err}")
        errors.append(err)
    else:
        print("[PASS] Integrity: Unique job_ids")

    # Check 3.2: Referenced Workflows Existence (Physical)
    for wf in inventory_data["workflows"]:
        if not os.path.exists(wf["path"]):
            err = f"Workflow file not found: {wf['path']} (referenced by {wf['workflow_id']})"
            print(f"[FAIL] {err}")
            errors.append(err)
    
    # Check 3.3: Cross-reference Jobs vs Workflows
    workflow_paths = [wf["path"] for wf in inventory_data["workflows"]]
    for job in registry_data["jobs"]:
        if job.get("workflow") and job["workflow"] not in workflow_paths:
            err = f"Job {job['job_id']} references workflow path {job['workflow']} not found in inventory"
            print(f"[FAIL] {err}")
            errors.append(err)

    # Check 3.4: Mapping consistency
    all_job_ids = set(job_ids)
    for wf in inventory_data["workflows"]:
        if wf.get("maps_to_non_trading_jobs"):
            for mapped_job in wf["maps_to_non_trading_jobs"]:
                if mapped_job not in all_job_ids:
                    err = f"Workflow {wf['workflow_id']} maps to job {mapped_job} which is NOT in registry"
                    print(f"[FAIL] {err}")
                    errors.append(err)

    if errors:
        print(f"\n[SUMMARY] {len(errors)} errors found.")
        sys.exit(1)
    else:
        print("\n[SUMMARY] All checks passed successfully.")

if __name__ == "__main__":
    INV_PATH = "docs/registries/GITHUB_ACTIONS_WORKFLOWS_INVENTORY_01.yml"
    REG_PATH = "docs/registries/GITHUB_ACTIONS_JOBS_REGISTRY_01.yml"
    validate_registries(INV_PATH, REG_PATH)
