import json
import logging
import os
import time
from typing import Any, Optional
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

logger = logging.getLogger(__name__)

AIRTABLE_API_BASE = "https://api.airtable.com/v0"
REQUEST_TIMEOUT = 10
MAX_RETRIES = 3
BATCH_LIMIT = 10


def _get_api_key() -> str:
    key = os.environ.get("AIRTABLE_API_KEY", "")
    if not key:
        logger.warning("AIRTABLE_API_KEY not set")
    return key


def _get_base_id() -> str:
    base_id = os.environ.get("AIRTABLE_BASE_ID", "")
    if not base_id:
        logger.warning("AIRTABLE_BASE_ID not set")
    return base_id


def _build_url(table: str) -> str:
    base_id = _get_base_id()
    return f"{AIRTABLE_API_BASE}/{base_id}/{table}"


def _build_headers() -> dict[str, str]:
    return {
        "Authorization": f"Bearer {_get_api_key()}",
        "Content-Type": "application/json",
    }


def send_records(
    table: str,
    records: list[dict[str, Any]],
    timeout: int = REQUEST_TIMEOUT,
) -> dict[str, Any]:
    if not records:
        return {"records": []}

    if len(records) > BATCH_LIMIT:
        logger.warning(f"batch truncated to {BATCH_LIMIT} records (got {len(records)})")
        records = records[:BATCH_LIMIT]

    payload = json.dumps({"records": records}).encode("utf-8")
    url = _build_url(table)
    headers = _build_headers()

    last_error: Optional[Exception] = None

    for attempt in range(1, MAX_RETRIES + 1):
        try:
            req = Request(url, data=payload, headers=headers, method="POST")
            with urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8")
                return json.loads(body)
        except HTTPError as e:
            if e.code == 429:
                wait = min(2 ** attempt, 30)
                logger.warning(f"rate limited (429), retry in {wait}s (attempt {attempt}/{MAX_RETRIES})")
                time.sleep(wait)
                last_error = e
                continue
            logger.error(f"HTTP {e.code}: {e.reason}")
            return {"error": f"HTTP {e.code}", "detail": str(e.reason)}
        except URLError as e:
            logger.error(f"URL error: {e.reason}")
            return {"error": "url_error", "detail": str(e.reason)}
        except Exception as e:
            logger.error(f"unexpected error: {e}")
            return {"error": "unexpected", "detail": str(e)}

    logger.error(f"all {MAX_RETRIES} retries exhausted")
    return {"error": "retries_exhausted", "detail": str(last_error)}


def send_trade(data: dict[str, Any]) -> dict[str, Any]:
    return send_records("Trades", [{"fields": data}])


def send_signal(data: dict[str, Any]) -> dict[str, Any]:
    return send_records("Signals", [{"fields": data}])


def send_backtest(data: dict[str, Any]) -> dict[str, Any]:
    return send_records("Backtests", [{"fields": data}])


def send_go_status(data: dict[str, Any]) -> dict[str, Any]:
    return send_records("GO_Status", [{"fields": data}])
