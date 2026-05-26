#!/usr/bin/env python3
"""
Registry Meta Reader
Reads registry/meta_index.yaml and provides CLI access.
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
CENTRAL_REGISTRY_FILE = PROJECT_ROOT / "registry" / "meta_index.yaml"
OUTPUT_DIR = MODULE_ROOT / "output"
EXPORT_JSON = OUTPUT_DIR / "meta_index.json"

class MetaRegistry:
    def __init__(self):
        self.registries = []
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
                        self.registries = yaml.safe_load(f)
                else:
                    self.registries = self._parse_yaml_simple(CENTRAL_REGISTRY_FILE)
                
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
        print(f"Module: registry_meta_reader")
        print(f"Source: {self.source_file}")
        print(f"Source kind: {self.source_kind}")
        print(f"Canonical source: {self.is_canonical_source}")
        print(f"Registries: {len(self.registries)}")
        print(f"Ready: {len(self.registries) > 0}")

    def list_registries(self):
        print(f"{'REGISTRY':<25} {'SCOPE':<15} {'STATUS':<10} {'CONSUMER':<30}")
        print("-" * 80)
        for r in self.registries:
            print(f"{r.get('registry_name', 'N/A'):<25} {r.get('scope', 'N/A'):<15} {r.get('status', 'N/A'):<10} {r.get('primary_consumer', 'N/A'):<30}")

    def show_registry(self, registry_name):
        found = False
        for r in self.registries:
            if r.get('registry_name') == registry_name:
                print(json.dumps(r, indent=2))
                found = True
                break
        if not found:
            print(f"Error: Registry '{registry_name}' not found.")
            sys.exit(1)

    def export_json(self):
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        with open(EXPORT_JSON, 'w', encoding='utf-8') as f:
            json.dump(self.registries, f, indent=2)
        print(f"Exported to {EXPORT_JSON}")

def main():
    parser = argparse.ArgumentParser(description="Registry Meta Reader")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("list", help="List all registries")
    
    show_parser = subparsers.add_parser("show", help="Show specific registry details")
    show_parser.add_argument("registry_name", help="Registry name to show")
    
    subparsers.add_parser("export-json", help="Export to JSON")

    args = parser.parse_args()
    registry = MetaRegistry()

    if args.command == "status":
        registry.status()
    elif args.command == "list":
        registry.list_registries()
    elif args.command == "show":
        registry.show_registry(args.registry_name)
    elif args.command == "export-json":
        registry.export_json()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
