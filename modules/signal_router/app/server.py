"""Lightweight HTTP server — POST /webhook → NormalizedSignal JSON."""
from __future__ import annotations
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer

from .router import route
from .schema import SignalValidationError

log = logging.getLogger("signal_router.server")

PORT = int(os.getenv("SIGNAL_ROUTER_PORT", "18900"))
HOST = os.getenv("SIGNAL_ROUTER_HOST", "127.0.0.1")


class SignalHandler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:  # silence default access log
        log.debug(fmt, *args)

    def _send_json(self, code: int, body: dict) -> None:
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"ok": True, "status": "live", "module": "signal_router"})
        else:
            self._send_json(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/webhook":
            self._send_json(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            raw = json.loads(body)
        except json.JSONDecodeError as exc:
            self._send_json(400, {"error": f"invalid JSON: {exc}"})
            return

        try:
            normalized = route(raw)
        except SignalValidationError as exc:
            log.warning("signal validation error: %s", exc)
            self._send_json(422, {"error": str(exc)})
            return
        except Exception as exc:
            log.error("unexpected error routing signal: %s", exc)
            self._send_json(500, {"error": "internal error"})
            return

        self._send_json(200, {"ok": True, "signal": normalized.to_dict()})


def run(host: str = HOST, port: int = PORT) -> None:
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    server = HTTPServer((host, port), SignalHandler)
    log.info("signal_router listening on %s:%d", host, port)
    server.serve_forever()
