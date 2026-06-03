#!/usr/bin/env python3
"""
credentials_form.py — Interactive CLI for updating credentials.

Groups credentials by provider, uses masked input, writes to the correct
storage location. Values are never logged, echoed, or printed.

Usage:
  python3 scripts/credentials_form.py            # full interactive menu
  python3 scripts/credentials_form.py --status   # status only, no prompts
  python3 scripts/credentials_form.py --provider Telegram  # update one provider
"""
import sys
import os
import re
import json
import getpass
import subprocess
import argparse
from pathlib import Path
from datetime import datetime, timezone

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DOTENV_FILE = PROJECT_ROOT / ".env"
ROLES_DIR = Path("/etc/opt-trading/env.d/roles")
OPENCLAW_JSON = Path.home() / ".openclaw" / "openclaw.json"
SSHFS_ENV = Path("/etc/opt-trading/shared_sshfs_permanent.env")

CREDS = [
    # Telegram
    {"id": "telegram_api_id",          "provider": "Telegram",    "env_var": "TELEGRAM_API_ID",                  "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_api_hash",        "provider": "Telegram",    "env_var": "TELEGRAM_API_HASH",                "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_bot_token_main",  "provider": "Telegram",    "env_var": "TELEGRAM_BOT_TOKEN",               "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_session_path",    "provider": "Telegram",    "env_var": "TELEGRAM_SESSION_PATH",            "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_alert_chat_id",   "provider": "Telegram",    "env_var": "TELEGRAM_ALERT_CHAT_ID",           "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_channels_config", "provider": "Telegram",    "env_var": "TELEGRAM_CHANNELS_CONFIG",         "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "telegram_chat_id_alerts",  "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_ALERTS",          "storage": "role",     "file": str(ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_pipeline","provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_PIPELINE",        "storage": "role",     "file": str(ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_push",    "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_PUSH",            "storage": "role",     "file": str(ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    {"id": "telegram_chat_id_ops",     "provider": "Telegram",    "env_var": "TELEGRAM_CHAT_ID_OPS",             "storage": "role",     "file": str(ROLES_DIR / "telegram_collector.env"),  "role": "telegram_collector"},
    # TradingView / Internal
    {"id": "tv_webhook_key",           "provider": "TradingView", "env_var": "TV_WEBHOOK_KEY",                   "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "tv_webhook_secret",        "provider": "TradingView", "env_var": "TV_WEBHOOK_SECRET",                "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "ops_admin_key",            "provider": "Internal",    "env_var": "OPS_ADMIN_KEY",                    "storage": "env",      "file": str(DOTENV_FILE)},
    # Google — auth via ADC (gcloud auth application-default login), no service account JSON
    {"id": "google_sheets_sync_id",    "provider": "Google",      "env_var": "GOOGLE_SHEETS_SYNC_SHEET_ID",      "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "gemini_api_key",           "provider": "Google",      "env_var": "GEMINI_API_KEY",                   "storage": "env",      "file": str(DOTENV_FILE)},
    # GitHub
    {"id": "gh_token",                 "provider": "GitHub",      "env_var": "GH_TOKEN",                         "storage": "env",      "file": str(DOTENV_FILE)},
    # Binance
    {"id": "binance_api_key",          "provider": "Binance",     "env_var": "BINANCE_API_KEY",                  "storage": "env",      "file": str(DOTENV_FILE)},
    # Coinglass
    {"id": "coinglass_api_key",        "provider": "Coinglass",   "env_var": "COINGLASS_API_KEY",                "storage": "env",      "file": str(DOTENV_FILE)},
    # Ollama
    {"id": "ollama_base_url",          "provider": "Ollama",      "env_var": "OLLAMA_BASE_URL",                  "storage": "env",      "file": str(DOTENV_FILE)},
    # LLM cloud (via openclaw)
    {"id": "openai_api_key",           "provider": "OpenAI",      "env_var": "OPENAI_API_KEY",                   "storage": "openclaw", "file": str(OPENCLAW_JSON)},
    {"id": "anthropic_api_key",        "provider": "Anthropic",   "env_var": "ANTHROPIC_API_KEY",                "storage": "openclaw", "file": str(OPENCLAW_JSON)},
    # Database
    {"id": "db_host",                  "provider": "Database",    "env_var": "DB_HOST",                          "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "db_user",                  "provider": "Database",    "env_var": "DB_USER",                          "storage": "env",      "file": str(DOTENV_FILE)},
    {"id": "db_password",              "provider": "Database",    "env_var": "DB_PASSWORD",                      "storage": "env",      "file": str(DOTENV_FILE)},
    # Airtable
    {"id": "airtable_api_key",         "provider": "Airtable",    "env_var": "AIRTABLE_API_KEY",                 "storage": "role",     "file": str(ROLES_DIR / "airtable_user.env"),        "role": "airtable_user"},
    {"id": "airtable_base_id",         "provider": "Airtable",    "env_var": "AIRTABLE_BASE_ID",                 "storage": "role",     "file": str(ROLES_DIR / "airtable_user.env"),        "role": "airtable_user"},
    # DeskPro
    {"id": "deskpro_api_key",          "provider": "DeskPro",     "env_var": "DESKPRO_API_KEY",                  "storage": "role",     "file": str(ROLES_DIR / "deskpro_user.env"),         "role": "deskpro_user"},
    {"id": "deskpro_api_url",          "provider": "DeskPro",     "env_var": "DESKPRO_API_URL",                  "storage": "role",     "file": str(ROLES_DIR / "deskpro_user.env"),         "role": "deskpro_user"},
    # ClickUp
    {"id": "clickup_token",            "provider": "ClickUp",     "env_var": "CLICKUP_TOKEN",                    "storage": "role",     "file": str(ROLES_DIR / "clickup_user.env"),         "role": "clickup_user"},
    # Figma (future)
    {"id": "figma_token",              "provider": "Figma",       "env_var": "FIGMA_TOKEN",                      "storage": "role",     "file": str(ROLES_DIR / "figma_designer.env"),      "role": "figma_designer", "cred_status": "future"},
    {"id": "figma_file_key",           "provider": "Figma",       "env_var": "FIGMA_FILE_KEY",                   "storage": "role",     "file": str(ROLES_DIR / "figma_designer.env"),      "role": "figma_designer", "cred_status": "future"},
    # Infrastructure
    {"id": "sshfs_identity_file",      "provider": "Internal",    "env_var": "IDENTITY_FILE",                    "storage": "env",      "file": str(SSHFS_ENV)},
    {"id": "wireguard_private_key",    "provider": "Internal",    "env_var": None,                               "storage": "system",   "file": "/etc/wireguard/wg0.conf"},
    {"id": "termux_ssh_key",           "provider": "Internal",    "env_var": None,                               "storage": "system",   "file": str(Path.home() / ".ssh" / "id_ed25519_termux")},
]

ANSI_GREEN  = "\033[92m"
ANSI_RED    = "\033[91m"
ANSI_YELLOW = "\033[93m"
ANSI_BLUE   = "\033[94m"
ANSI_GRAY   = "\033[90m"
ANSI_BOLD   = "\033[1m"
ANSI_RESET  = "\033[0m"

# ── Status checks ────────────────────────────────────────────────────

def check_status(cred: dict) -> str:
    if cred.get("cred_status") == "future":
        return "FUTURE"
    storage = cred.get("storage")
    env_var = cred.get("env_var")
    file_path = cred.get("file", "")

    if storage == "system":
        try:
            p = Path(file_path)
            if p.exists():
                return "SET"
        except (OSError, PermissionError):
            pass
        try:
            r = subprocess.run(["sudo", "-n", "test", "-f", file_path], capture_output=True, timeout=3)
            return "SET" if r.returncode == 0 else "ABSENT"
        except Exception:
            return "UNKNOWN"

    if storage == "openclaw":
        return "SET" if OPENCLAW_JSON.exists() else "ABSENT"

    if not env_var:
        return "UNKNOWN"

    if storage == "env":
        try:
            p = Path(file_path)
            if not p.exists():
                return "ABSENT"
            for line in p.read_text().splitlines():
                if re.match(rf"^{re.escape(env_var)}=.+", line.strip()):
                    return "SET"
            return "ABSENT"
        except (OSError, PermissionError):
            return "UNKNOWN"

    if storage == "role":
        try:
            r = subprocess.run(
                ["sudo", "-n", "grep", "-c", f"^{env_var}=.", file_path],
                capture_output=True, text=True, timeout=3,
            )
            if r.returncode == 0 and r.stdout.strip() not in ("", "0"):
                return "SET"
            return "ABSENT"
        except Exception:
            return "UNKNOWN"

    return "UNKNOWN"


def status_label(s: str) -> str:
    if s == "SET":
        return f"{ANSI_GREEN}SET{ANSI_RESET}"
    if s == "ABSENT":
        return f"{ANSI_RED}ABSENT{ANSI_RESET}"
    if s == "FUTURE":
        return f"{ANSI_BLUE}FUTURE{ANSI_RESET}"
    return f"{ANSI_GRAY}UNKNOWN{ANSI_RESET}"


# ── Write helpers ────────────────────────────────────────────────────

def _write_env_key(file_path: str, env_var: str, value: str) -> bool:
    p = Path(file_path)
    p.parent.mkdir(parents=True, exist_ok=True)
    existing = p.read_text().splitlines() if p.exists() else []
    updated = False
    new_lines = []
    for line in existing:
        if re.match(rf"^{re.escape(env_var)}=", line.strip()):
            new_lines.append(f"{env_var}={value}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"{env_var}={value}")
    p.write_text("\n".join(new_lines).rstrip("\n") + "\n")
    return True


def _write_role_key(file_path: str, env_var: str, value: str) -> bool:
    r = subprocess.run(["sudo", "-n", "cat", file_path], capture_output=True, text=True)
    existing = r.stdout.splitlines() if r.returncode == 0 else []
    updated = False
    new_lines = []
    for line in existing:
        if re.match(rf"^{re.escape(env_var)}=", line.strip()):
            new_lines.append(f"{env_var}={value}")
            updated = True
        else:
            new_lines.append(line)
    if not updated:
        new_lines.append(f"{env_var}={value}")
    content = "\n".join(new_lines).rstrip("\n") + "\n"

    Path(file_path).parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["sudo", "mkdir", "-p", str(Path(file_path).parent)], check=False)
    result = subprocess.run(["sudo", "tee", file_path], input=content, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"  {ANSI_RED}ERROR{ANSI_RESET} writing {file_path}: {result.stderr.strip()}", file=sys.stderr)
        return False
    subprocess.run(["sudo", "chmod", "600", file_path], check=False)
    return True


def write_credential(cred: dict, value: str) -> bool:
    storage = cred.get("storage")
    env_var = cred.get("env_var")
    file_path = cred.get("file", "")

    if storage == "openclaw":
        print(f"  {ANSI_YELLOW}OpenAI/Anthropic keys are managed via openclaw.{ANSI_RESET}")
        print(f"  Run: {ANSI_BOLD}openclaw configure{ANSI_RESET}")
        return False

    if storage == "system":
        print(f"  {ANSI_YELLOW}System credential — managed outside env files.{ANSI_RESET}")
        print(f"  See: ROTATION_RUNBOOK.md")
        return False

    if not env_var:
        print(f"  {ANSI_YELLOW}No env_var defined for this credential.{ANSI_RESET}", file=sys.stderr)
        return False

    if storage == "env":
        return _write_env_key(file_path, env_var, value)

    if storage == "role":
        return _write_role_key(file_path, env_var, value)

    return False


# ── Display helpers ──────────────────────────────────────────────────

def print_status_table(filter_provider: str | None = None) -> None:
    from collections import OrderedDict
    providers: dict[str, list[dict]] = OrderedDict()
    for c in CREDS:
        providers.setdefault(c["provider"], []).append(c)

    for prov, pcreds in providers.items():
        if filter_provider and prov.lower() != filter_provider.lower():
            continue
        statuses = [check_status(c) for c in pcreds]
        set_n = sum(1 for s in statuses if s == "SET")
        tot = len([s for s in statuses if s != "FUTURE"])
        print(f"\n{ANSI_BOLD}{prov}{ANSI_RESET}  {ANSI_GRAY}({set_n}/{tot} set){ANSI_RESET}")
        for c, s in zip(pcreds, statuses):
            var = c.get("env_var") or "(system file)"
            pad = max(0, 40 - len(var))
            print(f"  {var}{' ' * pad}  {status_label(s)}")


def list_providers() -> list[str]:
    seen: list[str] = []
    for c in CREDS:
        if c["provider"] not in seen:
            seen.append(c["provider"])
    return seen


# ── Interactive update ───────────────────────────────────────────────

def prompt_provider_update(provider: str) -> list[str]:
    pcreds = [c for c in CREDS if c["provider"].lower() == provider.lower()]
    if not pcreds:
        print(f"  {ANSI_RED}Provider not found: {provider}{ANSI_RESET}")
        return []

    updated: list[str] = []
    print(f"\n{ANSI_BOLD}Updating: {provider}{ANSI_RESET}")
    print(f"{ANSI_GRAY}  Leave blank to skip a credential.{ANSI_RESET}\n")

    for cred in pcreds:
        if cred.get("cred_status") == "future":
            print(f"  {cred['id']}: {ANSI_BLUE}FUTURE — skip{ANSI_RESET}")
            continue

        storage = cred.get("storage")
        env_var = cred.get("env_var") or "(system file)"
        current = check_status(cred)

        if storage == "openclaw":
            print(f"  {env_var}: managed via `openclaw configure` — skipping")
            continue
        if storage == "system":
            print(f"  {env_var}: system file — see ROTATION_RUNBOOK.md — skipping")
            continue

        prompt = f"  {ANSI_BOLD}{env_var}{ANSI_RESET} [{status_label(current)}]: "
        try:
            value = getpass.getpass(prompt)
        except (KeyboardInterrupt, EOFError):
            print(f"\n  {ANSI_YELLOW}Aborted.{ANSI_RESET}")
            break

        if not value.strip():
            print(f"    {ANSI_GRAY}skipped{ANSI_RESET}")
            continue

        ok = write_credential(cred, value.strip())
        if ok:
            print(f"    {ANSI_GREEN}written{ANSI_RESET}  → {cred['file']}")
            updated.append(cred["id"])
        # value is discarded here — never stored in a variable beyond this scope

    return updated


def run_interactive(filter_provider: str | None = None) -> None:
    print(f"\n{ANSI_BOLD}=== Credentials Form — opt-trading ==={ANSI_RESET}")
    print(f"{ANSI_GRAY}Values are masked and never logged.{ANSI_RESET}\n")

    providers = list_providers()

    if filter_provider:
        selected = [filter_provider]
    else:
        print_status_table()
        print(f"\n{ANSI_BOLD}Providers:{ANSI_RESET}")
        for i, p in enumerate(providers, 1):
            print(f"  {i:2}. {p}")
        print(f"   0. All providers")
        print(f"   q. Quit\n")

        choice = input("Select provider (number or name): ").strip()
        if choice.lower() in ("q", "quit", ""):
            print("Aborted.")
            return

        if choice == "0":
            selected = providers
        elif choice.isdigit() and 1 <= int(choice) <= len(providers):
            selected = [providers[int(choice) - 1]]
        else:
            matching = [p for p in providers if p.lower() == choice.lower()]
            if not matching:
                print(f"{ANSI_RED}Unknown provider: {choice}{ANSI_RESET}")
                return
            selected = matching

    all_updated: list[str] = []
    for prov in selected:
        updated = prompt_provider_update(prov)
        all_updated.extend(updated)

    if all_updated:
        ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        print(f"\n{ANSI_GREEN}Done.{ANSI_RESET} {len(all_updated)} credential(s) updated at {ts}.")
        print(f"{ANSI_GRAY}IDs: {', '.join(all_updated)}{ANSI_RESET}")
        print(f"\n{ANSI_YELLOW}Next steps:{ANSI_RESET}")
        print("  1. Restart affected services (webhook_server, openclaw gateway, etc.)")
        print("  2. Run: scripts/verify_all.sh")
        print("  3. If role file changed: scripts/env_role_sync.sh push <machine> <role>")
    else:
        print(f"\n{ANSI_GRAY}No credentials updated.{ANSI_RESET}")


# ── Entry point ──────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Interactive credential update form")
    parser.add_argument("--status", action="store_true", help="Show status only, no prompts")
    parser.add_argument("--provider", metavar="NAME", help="Update a single provider directly")
    args = parser.parse_args()

    if args.status:
        print(f"\n{ANSI_BOLD}=== Credentials Status ==={ANSI_RESET}")
        print_status_table(filter_provider=args.provider)
        print()
        return

    run_interactive(filter_provider=args.provider)


if __name__ == "__main__":
    main()
