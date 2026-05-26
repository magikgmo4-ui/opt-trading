#!/usr/bin/env python3
"""
Machines Registry Reader
Reads registry/machines_registry.yaml and provides CLI access.
"""

import sys
import json
import argparse
import os
try:
    import yaml
except ImportError:
    yaml = None
from pathlib import Path
from datetime import datetime

# Paths
MODULE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_ROOT.parent.parent
CENTRAL_REGISTRY_FILE = PROJECT_ROOT / "registry" / "machines_registry.yaml"
OUTPUT_DIR = MODULE_ROOT / "output"
EXPORT_JSON = OUTPUT_DIR / "machines_registry.json"

class MachinesRegistry:
    def __init__(self):
        self.machines = []
        self.source_file = None
        self.source_kind = None
        self.is_canonical_source = False
        self.load_registry()

    def _parse_yaml_simple(self, file_path):
        """Minimal YAML parser for simple lists of dicts"""
        items = []
        current_item = {}
        
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                    
                # New item start
                if line.startswith('- ') or line == '-':
                    if current_item:
                        items.append(current_item)
                    current_item = {}
                    line = line[1:].strip() # Remove '-' prefix
                
                if ':' in line:
                    parts = line.split(':', 1)
                    key = parts[0].strip().strip('"').strip("'")
                    val = parts[1].split('#', 1)[0].strip().strip('"').strip("'")
                    current_item[key] = val
                    
        if current_item:
            items.append(current_item)
        return items

    def load_registry(self):
        if CENTRAL_REGISTRY_FILE.exists():
            try:
                if yaml:
                    with open(CENTRAL_REGISTRY_FILE, 'r', encoding='utf-8') as f:
                        self.machines = yaml.safe_load(f)
                else:
                    self.machines = self._parse_yaml_simple(CENTRAL_REGISTRY_FILE)
                
                self.source_file = CENTRAL_REGISTRY_FILE
                self.source_kind = "central"
                self.is_canonical_source = True
                return
            except Exception as e:
                print(f"Error: Failed to load registry: {e}")
                sys.exit(1)
        
        print(f"Error: Registry file not found at {CENTRAL_REGISTRY_FILE}")
        sys.exit(1)

    def status(self):
        print(f"Module: machines_registry_reader")
        print(f"Source: {self.source_file}")
        print(f"Source kind: {self.source_kind}")
        print(f"Canonical source: {self.is_canonical_source}")
        print(f"Machines: {len(self.machines)}")
        print(f"Ready: {len(self.machines) > 0}")

    def list_machines(self):
        print(f"{'ID':<20} {'HOSTNAME':<20} {'ROLE':<15} {'PRIORITY':<10}")
        print("-" * 70)
        for m in self.machines:
            print(f"{m.get('machine_id', 'N/A'):<20} {m.get('hostname', 'N/A'):<20} {m.get('role', 'N/A'):<15} {m.get('ui_priority', 'N/A'):<10}")

    def show_roles(self):
        roles = {}
        for m in self.machines:
            r = m.get('role', 'unknown')
            if r not in roles:
                roles[r] = []
            roles[r].append(m)
            
        for r, items in roles.items():
            print(f"\n=== {r} ===")
            for item in items:
                print(f"  - {item.get('machine_id')} ({item.get('hostname')})")

    def show_machine(self, machine_id):
        found = False
        for m in self.machines:
            if m.get('machine_id') == machine_id:
                print(json.dumps(m, indent=2))
                found = True
                break
        if not found:
            print(f"Error: Machine '{machine_id}' not found.")
            sys.exit(1)

    def export_json(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.machines, f, indent=2)
        print(f"Exported to {EXPORT_JSON}")

def main():
    parser = argparse.ArgumentParser(description="Machines Registry Reader")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List all machines")
    subparsers.add_parser("show-roles", help="Group by role")
    
    show_parser = subparsers.add_parser("show", help="Show specific machine details")
    show_parser.add_argument("machine_id", help="Machine ID to show")
    
    subparsers.add_parser("export-json", help="Export to JSON")

    args = parser.parse_args()
    registry = MachinesRegistry()

    if args.command == "status":
        registry.status()
    elif args.command == "list":
        registry.list_machines()
    elif args.command == "show-roles":
        registry.show_roles()
    elif args.command == "show":
        registry.show_machine(args.machine_id)
    elif args.command == "export-json":
        registry.export_json()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
