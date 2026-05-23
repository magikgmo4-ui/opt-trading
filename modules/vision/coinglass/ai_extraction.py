from __future__ import annotations

import base64
import json
import logging
import os
from pathlib import Path
from typing import Any, Callable, List, Optional

from modules.vision.coinglass.vision_context_v1 import Detection

logger = logging.getLogger(__name__)

# Env gate for real AI calls — never active in tests
_AI_PROVIDER_ENV = "VISION_AI_PROVIDER"

_CONFIDENCE_THRESHOLD = 0.60

_SYSTEM_PROMPT = """You are an OCR assistant analyzing Coinglass trading dashboard screenshots.
Extract trading metrics visible in the image. Return ONLY valid JSON, no prose.

Output format:
{
  "detections": [
    {
      "detected_metric_type": "<type>",
      "extracted_value": <number or null>,
      "unit": "<USD|%|ratio>",
      "confidence": <0.0-1.0>,
      "notes": "<why null or uncertainty>"
    }
  ]
}

Valid metric types: liquidations_long, liquidations_short, long_short_ratio,
open_interest, liquidation_heatmap_level.

Rules:
- extracted_value MUST be null if the value is not clearly readable.
- confidence reflects OCR readability, not market judgment.
- Never invent or interpolate values.
- confidence < 0.6 → set extracted_value to null.
"""

# Type alias matching ExtractionFn from parser.py
ExtractionFn = Callable[[Path], List[Detection]]


def _image_to_b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("utf-8")


def _parse_ai_response(response_text: str, evidence_ref: str) -> List[Detection]:
    """Parse AI JSON response into Detection list. Returns [] on any parse error."""
    try:
        data = json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON block if wrapped in prose
        import re
        match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if not match:
            logger.warning("AI response contained no JSON: %r", response_text[:200])
            return []
        try:
            data = json.loads(match.group())
        except json.JSONDecodeError:
            logger.warning("AI response JSON could not be parsed")
            return []

    detections: List[Detection] = []
    for det in data.get("detections", []):
        try:
            confidence = float(det.get("confidence", 0))
            extracted_value = det.get("extracted_value")
            if extracted_value is not None:
                extracted_value = float(extracted_value)
            # Enforce: low confidence → null
            if confidence < _CONFIDENCE_THRESHOLD and extracted_value is not None:
                logger.info(
                    "confidence %.2f < %.2f — setting extracted_value to null for %s",
                    confidence, _CONFIDENCE_THRESHOLD, det.get("detected_metric_type"),
                )
                extracted_value = None
            detections.append(Detection(
                detected_metric_type=str(det.get("detected_metric_type", "")),
                extracted_value=extracted_value,
                unit=str(det.get("unit", "")),
                confidence=confidence,
                evidence_ref=evidence_ref,
                notes=str(det.get("notes", "")),
            ))
        except (TypeError, ValueError) as exc:
            logger.warning("skipping malformed detection: %s — %s", det, exc)

    return detections


def _call_openai(image_path: Path, api_key: str, model: str) -> str:
    """Call OpenAI vision API and return raw response text."""
    try:
        from openai import OpenAI
    except ImportError as exc:
        raise RuntimeError(
            "openai not installed — run: pip install openai"
        ) from exc

    client = OpenAI(api_key=api_key)
    b64 = _image_to_b64(image_path)
    resp = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}"}},
                {"type": "text", "text": "Extract all visible Coinglass metrics."},
            ]},
        ],
        max_tokens=512,
        temperature=0,
        response_format={"type": "json_object"},
    )
    return resp.choices[0].message.content or ""


def make_ai_extraction_fn(
    provider: Optional[str] = None,
    model: str = "gpt-4o-mini",
    _call_fn: Optional[Callable[[Path, str, str], str]] = None,
) -> ExtractionFn:
    """Return an ExtractionFn that uses an AI vision provider.

    provider: "openai" (reads OPENAI_API_KEY) or None → reads VISION_AI_PROVIDER env.
    _call_fn: injectable for tests (overrides real API call).

    Never raises — returns [] with a warning on any failure.
    """
    resolved_provider = provider or os.environ.get(_AI_PROVIDER_ENV, "")

    def _extract(image_path: Path) -> List[Detection]:
        if not resolved_provider:
            logger.warning(
                "VISION_AI_PROVIDER not set — AI extraction inactive, returning []"
            )
            return []

        if resolved_provider == "openai":
            api_key = os.environ.get("OPENAI_API_KEY", "")
            if not api_key:
                logger.warning("OPENAI_API_KEY not set — returning []")
                return []
            call = _call_fn or _call_openai
            try:
                response_text = call(image_path, api_key, model)
            except Exception:
                logger.exception("AI API call failed for %s", image_path)
                return []
        else:
            logger.warning("unknown VISION_AI_PROVIDER=%r — returning []", resolved_provider)
            return []

        dets = _parse_ai_response(response_text, str(image_path))
        logger.info("AI extraction: %d detections from %s", len(dets), image_path)
        return dets

    return _extract
