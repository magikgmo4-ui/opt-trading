#!/usr/bin/env python3
"""
Registry Router
Landing menu for navigating between registry readers.
"""

import sys
import argparse
from pathlib import Path

# Paths
MODULE_ROOT = Path(__file__).resolve().parent.parent
PROJECT_ROOT = MODULE_ROOT.parent.parent
MODULES_DIR = PROJECT_ROOT / "modules"

class RegistryRouter:
    def __init__(self):
        self.entries = [
            {"name": "meta", "module": "registry_meta_reader", "desc": "Meta Index"},
            {"name": "machines", "module": "machines_registry_reader", "desc": "Machines Registry"},
            {"name": "modules", "module": "modules_registry_reader", "desc": "Modules Registry"},
            {"name": "ui", "module": "ui_registry_msi", "desc": "UI Surfaces"},
            {"name": "wrappers", "module": "wrappers_registry_reader", "desc": "Wrappers Registry"}
        ]

    def status(self):
        print(f"Module: registry_router")
        print(f"Role: Central Navigation")
        print(f"Entries: {len(self.entries)}")
        print(f"Ready: True")

    def show_entries(self):
        print(f"{'ENTRY':<15} {'MODULE':<30} {'DESCRIPTION':<30}")
        print("-" * 75)
        for e in self.entries:
            print(f"{e['name']:<15} {e['module']:<30} {e['desc']:<30}")

    def get_command_path(self, module_name):
        return MODULES_DIR / module_name / "scripts" / "cmd.sh"

    def open_entry(self, entry_name):
        found = next((e for e in self.entries if e["name"] == entry_name), None)
        if not found:
            print(f"Error: Entry '{entry_name}' not found.")
            sys.exit(1)
        
        module = found["module"]
        cmd_path = self.get_command_path(module)
        
        print(f"Opening {found['desc']} ({module})...")
        print(f"Path: {cmd_path}")
        print(f"Command to run: bash {cmd_path} list")
        # In a real shell execution, we would exec this, but here we just print the guidance
        # The shell wrapper (cmd.sh) can handle the actual delegation if needed, 
        # or we can just serve as a directory.

def main():
    parser = argparse.ArgumentParser(description="Registry Router")
    subparsers = parser.add_subparsers(dest="command", help="Command")

    subparsers.add_parser("status", help="Show status")
    subparsers.add_parser("show-entries", help="List available registry readers")
    
    subparsers.add_parser("open-meta", help="Open Meta Reader")
    subparsers.add_parser("open-machines", help="Open Machines Reader")
    subparsers.add_parser("open-modules", help="Open Modules Reader")
    subparsers.add_parser("open-ui", help="Open UI Reader")
    subparsers.add_parser("open-wrappers", help="Open Wrappers Reader")

    args = parser.parse_args()
    router = RegistryRouter()

    if args.command == "status":
        router.status()
    elif args.command == "show-entries":
        router.show_entries()
    elif args.command and args.command.startswith("open-"):
        entry = args.command.replace("open-", "")
        router.open_entry(entry)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
