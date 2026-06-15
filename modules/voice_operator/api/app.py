"""
Voice Operator API — Standalone runner
GO_VOICE_OPERATOR_API_SERVICE_RUNTIME_01

Usage:
    python -m uvicorn modules.voice_operator.api.routes:app --host 127.0.0.1 --port 8020
"""
from modules.voice_operator.api.routes import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8020, log_level="info")
