#!/usr/bin/env python3
"""
Wrappers Registry Reader
Reads registry/wrappers_registry.yaml and provides CLI access.
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
CENTRAL_REGISTRY_FILE = PROJECT_ROOT / "registry" / "wrappers_registry.yaml"
OUTPUT_DIR = MODULE_ROOT / "output"
EXPORT_JSON = OUTPUT_DIR / "wrappers_registry.json"

class WrappersRegistry:
    def __init__(self):
        self.wrappers = []
        self.source_file = None
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
                        self.wrappers = yaml.safe_load(f)
                else:
                    self.wrappers = self._parse_yaml_simple(CENTRAL_REGISTRY_FILE)
                
                self.source_file = CENTRAL_REGISTRY_FILE
                return
            except Exception as e:
                print(f"Error: Failed to load registry: {e}")
                sys.exit(1)
        
        print(f"Error: Registry file not found at {CENTRAL_REGISTRY_FILE}")
        sys.exit(1)

    def status(self):
        families = []
        for w in self.wrappers:
            family = w.get('wrapper_family', 'unknown')
            if family not in families:
                families.append(family)
        print(f"Module: wrappers_registry_reader")
        print(f"Source: {self.source_file}")
        print(f"Wrappers: {len(self.wrappers)}")
        print(f"Families: {', '.join(families)}")
        print(f"Ready: {len(self.wrappers) > 0}")

    def list_wrappers(self):
        print(f"{'WRAPPER':<30} {'FAMILY':<10} {'TARGET':<25} {'STATUS':<10}")
        print("-" * 80)
        for w in self.wrappers:
            print(f"{w.get('wrapper_name', 'N/A'):<30} {w.get('wrapper_family', 'N/A'):<10} {w.get('target_module', 'N/A'):<25} {w.get('status', 'N/A'):<10}")

    def show_families(self):
        families = {}
        for w in self.wrappers:
            f = w.get('wrapper_family', 'unknown')
            if f not in families:
                families[f] = []
            families[f].append(w)
            
        for f, items in families.items():
            print(f"\n=== {f} ===")
            for item in items:
                print(f"  - {item.get('wrapper_name')} ({item.get('target_module')})")

    def show_wrapper(self, wrapper_name):
        found = False
        for w in self.wrappers:
            if w.get('wrapper_name') == wrapper_name:
                print(json.dumps(w, indent=2))
                found = True
                break
        if not found:
            print(f"Error: Wrapper '{wrapper_name}' not found.")
            sys.exit(1)

    def export_json(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.wrappers, f, indent=2)
        print(f"Exported to {EXPORT_JSON}")

def main():
    parser = argparse.ArgumentParser(description="Wrappers Registry Reader")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List all wrappers")
    subparsers.add_parser("show-families", help="Group by family")
    
    show_parser = subparsers.add_parser("show", help="Show specific wrapper details")
    show_parser.add_argument("wrapper_name", help="Wrapper name to show")
    
    subparsers.add_parser("export-json", help="Export to JSON")

    args = parser.parse_args()
    registry = WrappersRegistry()

    if args.command == "status":
        registry.status()
    elif args.command == "list":
        registry.list_wrappers()
    elif args.command == "show-families":
        registry.show_families()
    elif args.command == "show":
        registry.show_wrapper(args.wrapper_name)
    elif args.command == "export-json":
        registry.export_json()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
