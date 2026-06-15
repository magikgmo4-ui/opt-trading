"""
Voice Session — Push-to-Talk Orchestrator
GO_DESKPRO_VOICE_OPERATOR_01 — Lot D

Orchestrates a single push-to-talk voice interaction:
  1. Record audio (push-to-talk)
  2. STT via OpenAI Whisper
  3. Route intent via intent_router
  4. Call /read/* endpoint
  5. TTS via OpenAI → voice response
  6. Play audio response

Fallback: if no mic/key, operates in text-mode (typing instead of speaking).
"""
from __future__ import annotations
import sys
import time
from pathlib import Path
from typing import Optional

REPO_ROOT = Path(__file__).resolve().parents[3]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from modules.voice_operator.realtime.openai_realtime_client import (
    speech_to_text, text_to_speech, is_available, get_cost_summary,
)
from modules.voice_operator.realtime import audio_io
from modules.voice_operator.engine.intent_router import route, list_intents
from modules.voice_operator.engine.read_api_client import call


def run_voice_session(
    text_input: str | None = None,
    voice: str = "alloy",
    speed: float = 1.1,
) -> dict:
    """Run a single push-to-talk voice interaction.

    Args:
        text_input: If provided, skip STT and use this text directly
        voice: OpenAI TTS voice (alloy, echo, fable, nova, onyx, shimmer)
        speed: Speech speed (0.25 to 4.0)

    Returns:
        Session result dict with intent, endpoint, response, mode
    """
    result = {
        "ok": False,
        "mode": "text-only",
        "intent": "unknown",
        "endpoint": "/read/system",
        "one_line": "",
        "stt_text": "",
        "cost": {},
    }

    # --- Step 1: Get user input (voice or text) ---
    stt_text = ""

    if text_input:
        stt_text = text_input
        print(f"📝 Texte: \"{stt_text}\"", flush=True)
    elif audio_io.is_audio_available() and is_available():
        result["mode"] = "voice"
        print("🎤 Push-to-talk — parlez maintenant...", flush=True)
        audio_bytes = audio_io.record_audio(duration=15.0, push_to_talk=True)
        if audio_bytes:
            print("🔄 Transcription Whisper...", flush=True)
            stt_text = speech_to_text(audio_bytes, language="fr") or ""
            if stt_text:
                print(f"📝 Transcrit: \"{stt_text}\"", flush=True)
            else:
                print("⚠️ Transcription vide.", flush=True)
                result["one_line"] = "Desole, je n'ai pas compris. Repetez s'il vous plait."
                return result
        else:
            print("⚠️ Aucun audio capture.", flush=True)
            result["one_line"] = "Aucun audio detecte. Veuillez reessayer."
            return result
    else:
        # Text-mode fallback
        if not text_input:
            try:
                stt_text = input("📝 Votre commande: ").strip()
            except (EOFError, KeyboardInterrupt):
                print()
                return result
        else:
            stt_text = text_input

    if not stt_text:
        result["one_line"] = "Aucune commande recue."
        return result

    result["stt_text"] = stt_text

    # --- Step 2: Route intent ---
    routed = route(stt_text)
    result["intent"] = routed.intent
    result["endpoint"] = routed.endpoint

    print(f"🎯 Intent: {routed.intent} → {routed.endpoint}", flush=True)

    # --- Step 3: Call /read/* ---
    if routed.endpoint.startswith("/read/"):
        api_result = call(routed.endpoint, routed.params if routed.params else None)
    else:
        api_result = {"one_line": f"Endpoint inconnu: {routed.endpoint}"}

    result["ok"] = True
    result["one_line"] = api_result.get("one_line", str(api_result))
    result["raw_response"] = api_result
    result["cost"] = get_cost_summary()

    print(f"📊 Reponse: {result['one_line'][:120]}", flush=True)

    # --- Step 4: TTS voice output ---
    if result["mode"] == "voice" and is_available() and result["one_line"]:
        print("🔊 Synthese vocale...", flush=True)
        mp3_bytes = text_to_speech(result["one_line"], voice=voice, speed=speed)
        if mp3_bytes:
            audio_io.play_audio(mp3_bytes)
            print("✓ Lecture terminee.", flush=True)
        else:
            print("⚠️ TTS echoue — reponse texte uniquement.", flush=True)

    return result


def run_interactive_voice(voice: str = "alloy"):
    """Interactive push-to-talk loop (CTRL+C to exit)."""
    print()
    print("╔══════════════════════════════════════════╗")
    print("║  VOICE OPERATOR — Push-to-Talk         ║")
    print("║  MONITOR-ONLY — Validation humaine     ║")
    print("║  CTRL+C pour quitter                   ║")
    print("╚══════════════════════════════════════════╝")
    print()

    if not audio_io.is_audio_available():
        print(f"⚠️ Audio non disponible: {audio_io.get_audio_error()}")
        print("   Mode texte: tapez vos commandes.")
        print()

    if not is_available():
        print("⚠️ OPENAI_API_KEY non definie — TTS/STT desactive.")
        print("   export OPENAI_API_KEY=sk-...")
        print()

    session_count = 0
    total_cost = 0.0

    try:
        while True:
            if audio_io.is_audio_available() and is_available():
                print(f"\n[Sessions: {session_count} | Cout estime: ${total_cost:.4f}]")
                print("Appuyez sur ENTRÉE pour parler, ou tapez une commande texte:")

                try:
                    user_input = input("> ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nAu revoir.")
                    break

                if user_input.lower() in ("quit", "exit", "q", "sortir"):
                    print("Au revoir.")
                    break
                if user_input.lower() in ("help", "aide", "?"):
                    _print_help()
                    continue
                if user_input.lower() in ("cost", "cout"):
                    print(f"Cout estime total: ${total_cost:.4f} USD")
                    continue
                if user_input == "":
                    # Empty = push-to-talk
                    text_input = None
                else:
                    text_input = user_input

                result = run_voice_session(text_input=text_input, voice=voice)
            else:
                # Text-only mode
                try:
                    user_input = input("📝 Commande: ").strip()
                except (EOFError, KeyboardInterrupt):
                    print("\nAu revoir.")
                    break

                if user_input.lower() in ("quit", "exit", "q", "sortir"):
                    print("Au revoir.")
                    break
                if user_input.lower() in ("help", "aide", "?"):
                    _print_help()
                    continue
                if not user_input:
                    continue

                result = run_voice_session(text_input=user_input, voice=voice)

            if result.get("ok"):
                print(f"     → {result['one_line'][:100]}")
                session_count += 1
                cost = result.get("cost", {})
                total_cost = cost.get("estimated_cost_usd", 0)

    except KeyboardInterrupt:
        print(f"\n\nSessions: {session_count} | Cout estime: ${total_cost:.4f} USD")
        print("Au revoir.")


def _print_help():
    print()
    print("Commandes vocales disponibles :")
    intents = list_intents()
    for i in intents:
        print(f"  \"{i['example']}\" → {i['endpoint']}")
    print()
    print("  ENTRÉE vide  → push-to-talk (parler)")
    print("  help / aide  → cette aide")
    print("  cost / cout  → afficher le cout API estime")
    print("  quit / exit  → quitter")
    print()
