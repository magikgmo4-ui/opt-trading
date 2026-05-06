#!/usr/bin/env python3
"""ClickUp V1 execution: workspace, spaces, statuses, fields, templates, dashboards."""

import json, os, sys, time
import requests

TOKEN_FILE = "/tmp/clickup_token"
BASE = "https://api.clickup.com/api/v2"

with open(TOKEN_FILE) as f:
    TOKEN = f.read().strip()
HEADERS = {"Authorization": TOKEN, "Content-Type": "application/json"}
TEAM_ID = "90141225112"

LOG = []

def log(msg):
    print(msg)
    LOG.append(msg)

def api(method, path, data=None):
    url = f"{BASE}{path}"
    if method == "GET":
        r = requests.get(url, headers=HEADERS)
    elif method == "POST":
        r = requests.post(url, headers=HEADERS, json=data)
    elif method == "PUT":
        r = requests.put(url, headers=HEADERS, json=data)
    elif method == "DELETE":
        r = requests.delete(url, headers=HEADERS)
    else:
        raise ValueError(f"Unknown method: {method}")
    return r

def safe_id(result, key="id"):
    if result is None:
        return None
    if isinstance(result, dict):
        return result.get(key)
    return None

# ─── STEP 1: Spaces ───
SPACES = {
    "CANON_GOVERNANCE": "GO parents, gouvernance, matrice, reprise, indexation",
    "MODULES": "risk_engine, derivatives_collector, derivatives_analyzer, probability_engine, bot_vision, desk_pro, localcms, reseau_ssh",
    "MACHINES": "admin-trading, student, db-layer, cursor-ai",
    "TRADING_OPS": "chantiers trading, strategie, tests, paper/live boundaries",
    "INCIDENTS_DEBUG": "bugs, diagnostics, blocages, corrections ciblees",
    "ARCHIVE_CLOSED": "GO clos, historiques, references non actives",
}

space_ids = {}  # name -> ClickUp space id
for name, desc in SPACES.items():
    r = api("POST", f"/team/{TEAM_ID}/space", {"name": name, "multiple_assignees": False})
    if r.status_code in (200, 201):
        sid = r.json().get("id")
        space_ids[name] = sid
        log(f"SPACE CREATED: {name} -> {sid}")
    else:
        log(f"SPACE FAIL {name}: {r.status_code} {r.text[:200]}")
    time.sleep(0.3)

# ─── STEP 2: List in CANON_GOVERNANCE ───
gov_space_id = space_ids.get("CANON_GOVERNANCE")
if gov_space_id:
    r = api("POST", f"/space/{gov_space_id}/list", {"name": "GO_ACTIVE", "content": "Taches GO actives du cockpit opt-trading"})
    if r.status_code in (200, 201):
        list_id = r.json().get("id")
        log(f"LIST CREATED: GO_ACTIVE -> {list_id}")
    else:
        log(f"LIST FAIL: {r.status_code} {r.text[:200]}")
        list_id = None
else:
    log("LIST SKIP: CANON_GOVERNANCE space missing")
    list_id = None

# ─── STEP 3: Custom Fields on GO_ACTIVE list ───
CUSTOM_FIELDS = [
    {"name": "GO_ID", "type": "short_text"},
    {"name": "GO_TYPE", "type": "drop_down", "type_config": {
        "options": [
            {"name": "PARENT", "orderindex": 0},
            {"name": "CHILD", "orderindex": 1},
            {"name": "SIMPLE", "orderindex": 2},
            {"name": "DOC_ONLY", "orderindex": 3},
            {"name": "PATCH", "orderindex": 4},
            {"name": "AUDIT", "orderindex": 5},
            {"name": "EXECUTION", "orderindex": 6},
        ]
    }},
    {"name": "PARENT_GO", "type": "short_text"},
    {"name": "MODULE", "type": "short_text"},
    {"name": "SURFACE", "type": "short_text"},
    {"name": "MACHINE_OWNER", "type": "short_text"},
    {"name": "BRANCH", "type": "short_text"},
    {"name": "BASE_BRANCH", "type": "short_text"},
    {"name": "DOC_PATH", "type": "short_text"},
    {"name": "PR_URL", "type": "short_text"},
    {"name": "COMMIT_SHA", "type": "short_text"},
    {"name": "VALIDATION_STATUS", "type": "drop_down", "type_config": {
        "options": [
            {"name": "NONE", "orderindex": 0},
            {"name": "PARTIAL", "orderindex": 1},
            {"name": "PASS", "orderindex": 2},
            {"name": "FAIL", "orderindex": 3},
        ]
    }},
    {"name": "NEXT_GO", "type": "short_text"},
    {"name": "RESUME_POINT", "type": "short_text"},
    {"name": "CANON_PROOF_STATUS", "type": "drop_down", "type_config": {
        "options": [
            {"name": "MISSING", "orderindex": 0},
            {"name": "DOC_PRESENT", "orderindex": 1},
            {"name": "BRANCH_PRESENT", "orderindex": 2},
            {"name": "COMMIT_PRESENT", "orderindex": 3},
            {"name": "PR_PRESENT", "orderindex": 4},
            {"name": "CLOSEOUT_PRESENT", "orderindex": 5},
        ]
    }},
]

field_ids = {}  # name -> field id
if list_id:
    for cf in CUSTOM_FIELDS:
        r = api("POST", f"/list/{list_id}/field", cf)
        if r.status_code in (200, 201):
            fid = r.json().get("field", {}).get("id")
            field_ids[cf["name"]] = fid
            log(f"FIELD CREATED: {cf['name']} -> {fid}")
        else:
            log(f"FIELD FAIL {cf['name']}: {r.status_code} {r.text[:200]}")
        time.sleep(0.2)
else:
    log("FIELDS SKIP: no list_id")

# ─── STEP 4: Create GO tasks ───
GO_TASKS = [
    {
        "name": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01",
        "description": "ClickUp cockpit de pilotage GO — parent continuity bundle V1",
        "custom_fields": [
            {"id": field_ids.get("GO_ID"), "value": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"},
            {"id": field_ids.get("GO_TYPE"), "value": "PARENT"},
            {"id": field_ids.get("MODULE"), "value": "governance"},
            {"id": field_ids.get("MACHINE_OWNER"), "value": "admin-trading"},
            {"id": field_ids.get("BRANCH"), "value": "go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"},
            {"id": field_ids.get("BASE_BRANCH"), "value": "sot/mainline"},
            {"id": field_ids.get("DOC_PATH"), "value": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"},
            {"id": field_ids.get("VALIDATION_STATUS"), "value": "PASS"},
            {"id": field_ids.get("CANON_PROOF_STATUS"), "value": "PR_PRESENT"},
            {"id": field_ids.get("NEXT_GO"), "value": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01"},
            {"id": field_ids.get("RESUME_POINT"), "value": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01/CLICKUP_IMPLEMENTATION_BUNDLE_V1/"},
        ],
    },
    {
        "name": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01",
        "description": "Execution du bundle ClickUp V1 — cockpit operateur initial",
        "custom_fields": [
            {"id": field_ids.get("GO_ID"), "value": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01"},
            {"id": field_ids.get("GO_TYPE"), "value": "EXECUTION"},
            {"id": field_ids.get("PARENT_GO"), "value": "GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_01"},
            {"id": field_ids.get("MODULE"), "value": "governance"},
            {"id": field_ids.get("MACHINE_OWNER"), "value": "fantome"},
            {"id": field_ids.get("BRANCH"), "value": "go/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01"},
            {"id": field_ids.get("BASE_BRANCH"), "value": "sot/mainline"},
            {"id": field_ids.get("DOC_PATH"), "value": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01"},
            {"id": field_ids.get("VALIDATION_STATUS"), "value": "NONE"},
            {"id": field_ids.get("CANON_PROOF_STATUS"), "value": "MISSING"},
            {"id": field_ids.get("NEXT_GO"), "value": "GO_OPT_TRADING_REPO_KG_PARENT_GRAPH_SYSTEM_01"},
            {"id": field_ids.get("RESUME_POINT"), "value": "docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/"},
        ],
    },
]

task_ids = []
if list_id:
    for gt in GO_TASKS:
        payload = {"name": gt["name"], "description": gt["description"]}
        cf = []
        for c in gt.get("custom_fields", []):
            cf_id = c.get("id")
            if cf_id:
                cf.append({"id": cf_id, "value": c["value"]})
        payload["custom_fields"] = cf
        r = api("POST", f"/list/{list_id}/task", payload)
        if r.status_code in (200, 201):
            tid = r.json().get("id")
            task_ids.append(tid)
            log(f"TASK CREATED: {gt['name']} -> {tid}")
        else:
            log(f"TASK FAIL {gt['name']}: {r.status_code} {r.text[:200]}")
        time.sleep(0.3)
else:
    log("TASKS SKIP: no list_id")

# ─── STEP 5: Create Dashboards ───
if gov_space_id:
    dashboards = {
        "GO actifs": "Toutes les taches GO actives et ouvertes",
        "GO bloques": "GO avec statut BLOCKED",
        "GO sans preuve": "GO avec CANON_PROOF_STATUS MISSING",
        "GO par machine": "Vue par MACHINE_OWNER",
        "NEXT_GO": "Prochains GO a ouvrir",
    }
    for dname, ddesc in dashboards.items():
        r = api("POST", f"/team/{TEAM_ID}/dashboard", {"name": dname, "description": ddesc})
        if r.status_code in (200, 201):
            log(f"DASHBOARD CREATED: {dname} -> {r.json().get('id')}")
        else:
            log(f"DASHBOARD FAIL {dname}: {r.status_code} {r.text[:200]}")
        time.sleep(0.3)

# ─── SUMMARY ───
log("\n=== CLICKUP EXECUTION SUMMARY ===")
log(f"Team: {TEAM_ID}")
log(f"Spaces created: {len(space_ids)}")
log(f"List: GO_ACTIVE -> {list_id}")
log(f"Custom fields: {len(field_ids)}")
log(f"Tasks: {len(task_ids)}")

results = {
    "team_id": TEAM_ID,
    "spaces": space_ids,
    "list_id": list_id,
    "fields": field_ids,
    "task_ids": task_ids,
    "log": LOG,
}

with open("docs/chantiers/GO_OPT_TRADING_CLICKUP_PARENT_CONTINUITY_EXECUTION_01/execution_results.json", "w") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("\nResults saved to execution_results.json")
print("\n".join(LOG))
