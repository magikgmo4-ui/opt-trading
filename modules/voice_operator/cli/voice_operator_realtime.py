#!/usr/bin/env python3
"""
Voice Operator Realtime CLI — Push-to-Talk Interface
GO_DESKPRO_VOICE_OPERATOR_01 — Lot D

Usage:
    # Interactive push-to-talk
    python -m modules.voice_operator.cli.voice_operator_realtime

    # Single text command
    python -m modules.voice_operator.cli.voice_operator_realtime "Etat systeme"

    # List audio devices
    python -m modules.voice_operator.cli.voice_operator_realtime --devices

    # Text-only mode (no mic)
    python -m modules.voice_operator.cli.voice_operator_realtime --text

    # Cost summary
    python -m modules.voice_operator.cli.voice_operator_realtime --cost

Requirements:
    export OPENAI_API_KEY=sk-...
    pip install sounddevice numpy  # for microphone
    pip install pydub              # for MP3 playback (optional)
"""
from __future__ import annotations
import sys
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.voice_operator.realtime.voice_session import run_voice_session, run_interactive_voice
from modules.voice_operator.realtime.audio_io import list_devices, is_audio_available, get_audio_error
from modules.voice_operator.realtime.openai_realtime_client import is_available, get_cost_summary


def main():
    import argparse

    parser = argparse.ArgumentParser(
        description="Voice Operator Realtime — Push-to-Talk Monitor-Only"
    )
    parser.add_argument(
        "phrase", nargs="*", default=[],
        help="Commande texte (ex: 'Etat systeme', 'Setup BTC')"
    )
    parser.add_argument(
        "--text", "-t", action="store_true",
        help="Mode texte uniquement (pas de micro)"
    )
    parser.add_argument(
        "--devices", "-d", action="store_true",
        help="Lister les peripheriques audio"
    )
    parser.add_argument(
        "--cost", "-c", action="store_true",
        help="Afficher le cout estime des appels API"
    )
    parser.add_argument(
        "--voice", "-v", type=str, default="alloy",
        choices=["alloy", "echo", "fable", "nova", "onyx", "shimmer"],
        help="Voix TTS (defaut: alloy)"
    )
    args = parser.parse_args()

    if args.devices:
        devices = list_devices()
        if devices:
            print("Peripheriques audio:")
            for d in devices:
                print(f"  [{d['index']}] {d['name']} (in:{d['inputs']} out:{d['outputs']} @{d['default_samplerate']}Hz)")
        else:
            print("Aucun peripherique audio detecte.")
            print(get_audio_error())
        return

    if args.cost:
        cost = get_cost_summary()
        print(f"Appels STT: {cost['stt_calls']}")
        print(f"Appels TTS: {cost['tts_calls']}")
        print(f"Cout estime: ${cost['estimated_cost_usd']:.6f} USD")
        return

    phrase = " ".join(args.phrase).strip()

    if phrase:
        result = run_voice_session(text_input=phrase, voice=args.voice)
        if result.get("one_line"):
            print(f"\n{result['one_line']}")
    else:
        run_interactive_voice(voice=args.voice)


if __name__ == "__main__":
    main()
