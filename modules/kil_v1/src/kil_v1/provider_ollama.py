from __future__ import annotations

import json
import os
from typing import Any
from urllib import error, request

from .errors import ValidationError
from .storage import now_z


def call_ollama_provider(question: dict[str, Any], response_input: dict[str, Any]) -> dict[str, Any]:
    provider = response_input.get("provider")
    if not isinstance(provider, dict):
        raise ValidationError("response.provider must be an object")

    model = str(provider.get("model") or "deepseek-r1:1.5b").strip()
    timeout_seconds = _require_timeout(provider.get("timeout_seconds", 45))
    base_url = str(provider.get("base_url") or os.environ.get("OLLAMA_BASE_URL") or "http://127.0.0.1:11434").rstrip("/")
    prompt = _build_prompt(question)
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    request_id = None
    try:
        http_request = request.Request(
            f"{base_url}/api/generate",
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(http_request, timeout=timeout_seconds) as response:
            request_id = response.headers.get("X-Request-Id")
            raw = response.read().decode("utf-8")
    except error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise ValidationError(f"ollama_http_error: {exc.code} {body.strip()}") from exc
    except error.URLError as exc:
        raise ValidationError(f"ollama_unavailable: {exc.reason}") from exc
    except TimeoutError as exc:
        raise ValidationError("ollama_timeout") from exc

    try:
        decoded = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValidationError("ollama_invalid_json_response") from exc
    if not isinstance(decoded, dict):
        raise ValidationError("ollama_invalid_response_object")

    text = decoded.get("response")
    if not isinstance(text, str) or not text.strip():
        raise ValidationError("ollama_empty_response")

    return {
        "response_text": text,
        "source_citations": [],
        "external_validation": False,
        "provider_label": "ollama",
        "provider_model": model,
        "provider_request_id": request_id,
        "provider_finish_reason": decoded.get("done_reason"),
        "provider_error": None,
        "provider_timeout_seconds": timeout_seconds,
        "captured_at": now_z(),
    }


def _build_prompt(question: dict[str, Any]) -> str:
    return (
        "You are answering a KIL V1 interview question. "
        "Answer directly, avoid unsupported truth claims, and cite sources only if explicitly known.\n\n"
        f"Question template: {question['prompt_template_id']}\n"
        f"Expected mode: {question['expected_answer_mode']}\n"
        f"Question: {question['question_text']}\n"
    )


def _require_timeout(value: Any) -> int:
    if isinstance(value, int) and value > 0:
        return value
    if isinstance(value, str) and value.strip().isdigit() and int(value.strip()) > 0:
        return int(value.strip())
    raise ValidationError("provider.timeout_seconds must be a positive integer")
