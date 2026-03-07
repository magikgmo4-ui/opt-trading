#!/usr/bin/env python3
"""
UI Registry MSI
Source of truth for UI surfaces, machines, and categories.
"""

import sys
import json
import argparse
import os
from datetime import datetime
from pathlib import Path

# Paths
MODULE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = MODULE_ROOT / "config"
OUTPUT_DIR = MODULE_ROOT / "output"
SEED_FILE = CONFIG_DIR / "ui_registry_seed.json"
EXPORT_JSON = OUTPUT_DIR / "ui_registry_msi.json"
EXPORT_MD = OUTPUT_DIR / "ui_registry_msi.md"

class UIRegistry:
    def __init__(self):
        self.surfaces = []
        self.load_seed()

    def load_seed(self):
        if not SEED_FILE.exists():
            print(f"Error: Seed file not found at {SEED_FILE}")
            sys.exit(1)
        try:
            with open(SEED_FILE, 'r', encoding='utf-8') as f:
                self.surfaces = json.load(f)
        except Exception as e:
            print(f"Error loading seed: {e}")
            sys.exit(1)

    def status(self):
        print(f"Module: ui_registry_msi")
        print(f"Seed: {SEED_FILE}")
        print(f"Surfaces: {len(self.surfaces)}")
        print(f"Ready: {len(self.surfaces) > 0}")

    def list_surfaces(self):
        print(f"{'SURFACE':<25} {'TARGET':<15} {'CATEGORY':<30} {'STATUS':<10}")
        print("-" * 80)
        for s in self.surfaces:
            print(f"{s['surface_name']:<25} {s['machine_target']:<15} {s['category']:<30} {s['status']:<10}")

    def show_machines(self):
        machines = {}
        for s in self.surfaces:
            m = s['machine_target']
            if m not in machines:
                machines[m] = []
            machines[m].append(s)
        
        for m, items in machines.items():
            print(f"\n=== {m} ===")
            for item in items:
                print(f"  - {item['surface_name']} ({item['category']})")

    def show_categories(self):
        cats = {}
        for s in self.surfaces:
            c = s['category']
            if c not in cats:
                cats[c] = []
            cats[c].append(s)
            
        for c, items in cats.items():
            print(f"\n=== {c} ===")
            for item in items:
                print(f"  - {item['surface_name']} ({item['machine_target']})")

    def show_msi(self):
        print("\n=== MSI / DB-LAYER SURFACES ===")
        for s in self.surfaces:
            if s['machine_target'] == 'msi_db_layer':
                print(f"  [{s['category']}] {s['surface_name']} -> {s['actions']}")

    def export_json(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.surfaces, f, indent=2)
        print(f"Exported to {EXPORT_JSON}")

    def export_md(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_MD, 'w', encoding='utf-8') as f:
            f.write("# UI Registry MSI Export\n\n")
            f.write(f"Generated: {datetime.now().isoformat()}\n\n")
            f.write("| Surface | Target | Category | Action | Status |\n")
            f.write("|---|---|---|---|---|\n")
            for s in self.surfaces:
                f.write(f"| {s['surface_name']} | {s['machine_target']} | {s['category']} | `{s['actions']}` | {s['status']} |\n")
        print(f"Exported to {EXPORT_MD}")

def main():
    parser = argparse.ArgumentParser(description="UI Registry MSI")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List all surfaces")
    subparsers.add_parser("show-machines", help="Group by machine")
    subparsers.add_parser("show-categories", help="Group by category")
    subparsers.add_parser("show-msi", help="Filter for MSI target")
    subparsers.add_parser("export-json", help="Export to JSON")
    subparsers.add_parser("export-md", help="Export to Markdown")

    args = parser.parse_args()
    registry = UIRegistry()

    if args.command == "status":
        registry.status()
    elif args.command == "list":
        registry.list_surfaces()
    elif args.command == "show-machines":
        registry.show_machines()
    elif args.command == "show-categories":
        registry.show_categories()
    elif args.command == "show-msi":
        registry.show_msi()
    elif args.command == "export-json":
        registry.export_json()
    elif args.command == "export-md":
        registry.export_md()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
