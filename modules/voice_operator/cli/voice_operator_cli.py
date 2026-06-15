#!/usr/bin/env python3
"""
Voice Operator CLI — Text-Mode Interface
GO_DESKPRO_VOICE_OPERATOR_01 — Lot C

Usage:
    python -m modules.voice_operator.cli.voice_operator_cli "Etat systeme"
    python -m modules.voice_operator.cli.voice_operator_cli "Setup BTC"
    python -m modules.voice_operator.cli.voice_operator_cli "Rapport marche"
    python -m modules.voice_operator.cli.voice_operator_cli --help
    python -m modules.voice_operator.cli.voice_operator_cli --interactive

No microphone, no TTS, no OpenAI — pure text-mode CLI.
Displays: intent → endpoint → response (one_line) → mode
"""
from __future__ import annotations
import sys
import json
from pathlib import Path

# Allow running from repo root
REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.voice_operator.engine.intent_router import route, list_intents
from modules.voice_operator.engine.read_api_client import call


def _display(result: dict, routed) -> None:
    """Format and print the voice operator response."""
    print()
    print("╔══════════════════════════════════════════╗")
    print("║        VOICE OPERATOR — Monitor Only     ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║ Intent:   {routed.intent:<32} ║")
    print(f"║ Endpoint: {routed.endpoint:<32} ║")
    if routed.params:
        params_str = " ".join(f"{k}={v}" for k, v in routed.params.items())
        print(f"║ Params:   {params_str:<32} ║")
    print("╠══════════════════════════════════════════╣")
    if result.get("one_line"):
        print(f"║ {result['one_line']:<42} ║")
    else:
        print(f"║ (pas de reponse)                        ║")
    print("╠══════════════════════════════════════════╣")
    print("║ Mode: MONITOR-ONLY — Validation humaine  ║")
    print("╚══════════════════════════════════════════╝")
    print()


def _display_json(result: dict, routed) -> None:
    """JSON output for programmatic consumption."""
    output = {
        "intent": routed.intent,
        "endpoint": routed.endpoint,
        "params": routed.params,
        "response": result,
        "mode": "monitor_only",
    }
    print(json.dumps(output, ensure_ascii=False, indent=2, default=str))


def _display_interactive_header():
    print()
    print("╔══════════════════════════════════════════╗")
    print("║  VOICE OPERATOR — Interactive (text)    ║")
    print("║  Tapez 'help' pour les commandes        ║")
    print("║  Tapez 'quit' pour quitter              ║")
    print("╚══════════════════════════════════════════╝")
    print()


def run_once(phrase: str, json_mode: bool = False):
    """Process a single voice command."""
    routed = route(phrase)
    result = call(routed.endpoint, routed.params if routed.params else None)
    if json_mode:
        _display_json(result, routed)
    else:
        _display(result, routed)


def run_interactive():
    """Interactive REPL mode."""
    _display_interactive_header()
    while True:
        try:
            phrase = input("VOIX> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nAu revoir.")
            break

        if not phrase:
            continue

        lower = phrase.lower()
        if lower in ("quit", "exit", "q", "sortir", "quitter"):
            print("Au revoir.")
            break
        if lower in ("help", "aide", "?", "h"):
            _show_help()
            continue

        routed = route(phrase)
        result = call(routed.endpoint, routed.params if routed.params else None)
        _display(result, routed)


def _show_help():
    print()
    print("Commandes disponibles :")
    intents = list_intents()
    for i in intents:
        print(f"  {i['example']:<30} → {i['endpoint']}")
    print()
    print("  help / aide                           → cette aide")
    print("  quit / exit / q                       → quitter")
    print()


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Voice Operator CLI — Monitor-Only Text Interface"
    )
    parser.add_argument(
        "phrase", nargs="*", default=[],
        help="Phrase a analyser (ex: 'Etat systeme', 'Setup BTC')"
    )
    parser.add_argument(
        "--json", action="store_true",
        help="Sortie JSON au lieu du format console"
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true",
        help="Mode interactif (REPL)"
    )
    parser.add_argument(
        "--help-intents", action="store_true",
        help="Afficher la liste des intents disponibles"
    )
    args = parser.parse_args()

    if args.help_intents:
        _show_help()
        return

    if args.interactive:
        run_interactive()
        return

    phrase = " ".join(args.phrase).strip()
    if not phrase:
        print("Usage: voice_operator_cli 'Etat systeme'")
        print("       voice_operator_cli --interactive")
        print("       voice_operator_cli --help-intents")
        sys.exit(1)

    run_once(phrase, json_mode=args.json)


if __name__ == "__main__":
    main()
