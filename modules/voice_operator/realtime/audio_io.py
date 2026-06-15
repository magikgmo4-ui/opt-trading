"""
Audio I/O — Microphone capture and speaker playback
GO_DESKPRO_VOICE_OPERATOR_01 — Lot D

Handles:
  - Push-to-talk recording (spacebar hold)
  - Audio playback (MP3/WAV)

Dependencies (optional): sounddevice, numpy, pydub
Without them, falls back to text-mode gracefully.
"""
from __future__ import annotations
import time
import io
import sys
from typing import Optional

AUDIO_AVAILABLE = False
AUDIO_ERROR = ""

try:
    import sounddevice as sd
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    AUDIO_ERROR = "sounddevice/numpy not installed. pip install sounddevice numpy"


def is_audio_available() -> bool:
    return AUDIO_AVAILABLE


def get_audio_error() -> str:
    return AUDIO_ERROR


def list_devices() -> list[dict]:
    """List available audio devices."""
    if not AUDIO_AVAILABLE:
        return []
    devices = []
    try:
        for i, d in enumerate(sd.query_devices()):
            devices.append({
                "index": i,
                "name": d["name"],
                "inputs": d["max_input_channels"],
                "outputs": d["max_output_channels"],
                "default_samplerate": d["default_samplerate"],
            })
    except Exception:
        pass
    return devices


def record_audio(
    duration: float | None = None,
    samplerate: int = 24000,
    channels: int = 1,
    push_to_talk: bool = True,
) -> Optional[bytes]:
    """Record audio from microphone.

    Args:
        duration: Max recording duration in seconds (None = push-to-talk)
        samplerate: Sample rate (24000 for Whisper)
        channels: Mono (1)
        push_to_talk: If True, records until Enter is pressed

    Returns:
        WAV audio bytes or None on failure.
    """
    if not AUDIO_AVAILABLE:
        return None

    try:
        if push_to_talk:
            return _record_push_to_talk(samplerate, channels, duration)
        else:
            return _record_fixed(duration or 5.0, samplerate, channels)
    except Exception:
        return None


def _record_push_to_talk(
    samplerate: int, channels: int, max_duration: float | None = None
) -> Optional[bytes]:
    """Push-to-talk recording — records until Enter is pressed."""
    import threading

    max_seconds = max_duration or 30.0
    frames = []
    recording = [True]

    def _callback(indata, frame_count, time_info, status):
        if recording[0]:
            frames.append(indata.copy())

    stream = sd.InputStream(
        samplerate=samplerate,
        channels=channels,
        dtype="float32",
        callback=_callback,
    )

    print("🎤 Enregistrement... Appuyez sur Entree pour arreter.", flush=True)
    stream.start()

    # Wait for Enter key in a thread
    def _wait_enter():
        try:
            input()
        except EOFError:
            pass
        recording[0] = False

    t = threading.Thread(target=_wait_enter, daemon=True)
    t.start()

    start = time.time()
    while recording[0] and (time.time() - start) < max_seconds:
        time.sleep(0.1)

    stream.stop()
    stream.close()

    if not frames:
        print("Aucun audio capture.")
        return None

    audio = np.concatenate(frames, axis=0)

    # Convert to 16-bit PCM WAV
    audio_int16 = (audio * 32767).astype(np.int16)

    wav_buffer = io.BytesIO()
    import wave
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(samplerate)
        wf.writeframes(audio_int16.tobytes())

    duration = len(audio) / samplerate
    print(f"✓ Capture: {duration:.1f}s audio.", flush=True)
    return wav_buffer.getvalue()


def _record_fixed(duration: float, samplerate: int, channels: int) -> Optional[bytes]:
    """Fixed-duration recording."""
    print(f"🎤 Enregistrement {duration}s...", flush=True)
    audio = sd.rec(
        int(duration * samplerate),
        samplerate=samplerate,
        channels=channels,
        dtype="float32",
    )
    sd.wait()

    audio_int16 = (audio * 32767).astype(np.int16)

    wav_buffer = io.BytesIO()
    import wave
    with wave.open(wav_buffer, "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_int16.tobytes())

    print(f"✓ Capture: {duration}s audio.", flush=True)
    return wav_buffer.getvalue()


def play_audio(audio_bytes: bytes) -> bool:
    """Play audio bytes (MP3 or WAV) through speakers.

    Args:
        audio_bytes: Audio file bytes

    Returns:
        True on success.
    """
    if not AUDIO_AVAILABLE:
        return False

    try:
        # Try pydub for MP3 decoding
        try:
            from pydub import AudioSegment
            from pydub.playback import play

            seg = AudioSegment.from_file(io.BytesIO(audio_bytes))
            play(seg)
            return True
        except ImportError:
            pass

        # Fallback: write temp WAV and play with sounddevice
        import tempfile
        import wave

        # Try to read as WAV directly
        try:
            with wave.open(io.BytesIO(audio_bytes), "rb") as wf:
                data = wf.readframes(wf.getnframes())
                dtype = np.int16
                channels = wf.getnchannels()
                samplerate = wf.getframerate()
                audio = np.frombuffer(data, dtype=dtype).reshape(-1, channels).astype(np.float32) / 32767.0
                sd.play(audio, samplerate=samplerate)
                sd.wait()
                return True
        except Exception:
            pass

        # Try to convert MP3 to WAV via ffmpeg (if available)
        try:
            import subprocess
            import tempfile
            with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp_in:
                tmp_in.write(audio_bytes)
                tmp_in_path = tmp_in.name
            tmp_out_path = tmp_in_path.replace(".mp3", ".wav")
            subprocess.run(
                ["ffmpeg", "-y", "-i", tmp_in_path, "-f", "wav", tmp_out_path],
                capture_output=True, timeout=10,
            )
            with wave.open(tmp_out_path, "rb") as wf:
                data = wf.readframes(wf.getnframes())
                audio = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32767.0
                sd.play(audio, samplerate=wf.getframerate())
                sd.wait()
            import os
            os.unlink(tmp_in_path)
            os.unlink(tmp_out_path)
            return True
        except Exception:
            pass

        return False
    except Exception:
        return False
