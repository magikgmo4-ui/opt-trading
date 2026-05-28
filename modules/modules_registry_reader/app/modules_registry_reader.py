#!/usr/bin/env python3
"""
Modules Registry Reader
Reads registry/modules_registry.yaml and provides CLI access.
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

# Paths
MODULE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_ROOT.parent.parent
CENTRAL_REGISTRY_FILE = PROJECT_ROOT / "registry" / "modules_registry.yaml"
OUTPUT_DIR = MODULE_ROOT / "output"
EXPORT_JSON = OUTPUT_DIR / "modules_registry.json"

class ModulesRegistry:
    def __init__(self):
        self.modules = []
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
                    
                    # Handle lists (e.g. wrappers_expected: ["menu", "cmd"])
                    val_str = parts[1].split('#', 1)[0].strip()
                    if val_str.startswith('[') and val_str.endswith(']'):
                        # Very simple list parsing
                        content = val_str[1:-1]
                        if not content:
                            val = []
                        else:
                            val = [x.strip().strip('"').strip("'") for x in content.split(',')]
                    else:
                        val = val_str.strip('"').strip("'")
                        # Handle boolean
                        if val.lower() == 'true': val = True
                        elif val.lower() == 'false': val = False
                        
                    current_item[key] = val
                    
        if current_item:
            items.append(current_item)
        return items

    def load_registry(self):
        if CENTRAL_REGISTRY_FILE.exists():
            try:
                if yaml:
                    with open(CENTRAL_REGISTRY_FILE, 'r', encoding='utf-8') as f:
                        self.modules = yaml.safe_load(f)
                else:
                    self.modules = self._parse_yaml_simple(CENTRAL_REGISTRY_FILE)
                
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
        print(f"Module: modules_registry_reader")
        print(f"Source: {self.source_file}")
        print(f"Source kind: {self.source_kind}")
        print(f"Canonical source: {self.is_canonical_source}")
        print(f"Modules: {len(self.modules)}")
        print(f"Ready: {len(self.modules) > 0}")

    def list_modules(self):
        print(f"{'MODULE':<25} {'DOMAIN':<20} {'TARGET':<15} {'PLACEMENT':<20} {'PRIORITY':<10}")
        print("-" * 100)
        for m in self.modules:
            print(
                f"{m.get('module_name', 'N/A'):<25} "
                f"{m.get('domain', 'N/A'):<20} "
                f"{m.get('machine_target', 'N/A'):<15} "
                f"{m.get('placement_mode', 'N/A'):<20} "
                f"{m.get('priority', 'N/A'):<10}"
            )

    def show_domains(self):
        domains = {}
        for m in self.modules:
            d = m.get('domain', 'unknown')
            if d not in domains:
                domains[d] = []
            domains[d].append(m)
            
        for d, items in domains.items():
            print(f"\n=== {d} ===")
            for item in items:
                print(f"  - {item.get('module_name')} ({item.get('description')})")

    def show_module(self, module_name):
        found = False
        for m in self.modules:
            if m.get('module_name') == module_name:
                print(json.dumps(m, indent=2))
                found = True
                break
        if not found:
            print(f"Error: Module '{module_name}' not found.")
            sys.exit(1)

    def export_json(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.modules, f, indent=2)
        print(f"Exported to {EXPORT_JSON}")

def main():
    parser = argparse.ArgumentParser(description="Modules Registry Reader")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List all modules")
    subparsers.add_parser("show-domains", help="Group by domain")
    
    show_parser = subparsers.add_parser("show", help="Show specific module details")
    show_parser.add_argument("module_name", help="Module name to show")
    
    subparsers.add_parser("export-json", help="Export to JSON")

    args = parser.parse_args()
    registry = ModulesRegistry()

    if args.command == "status":
        registry.status()
    elif args.command == "list":
        registry.list_modules()
    elif args.command == "show-domains":
        registry.show_domains()
    elif args.command == "show":
        registry.show_module(args.module_name)
    elif args.command == "export-json":
        registry.export_json()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
