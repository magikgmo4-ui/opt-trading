from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen

from .errors import HttpRequestError


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    headers: dict[str, str]
    data: Any


class JsonHttpClient:
    def __init__(self, *, base_url: str, default_headers: dict[str, str] | None = None, timeout_seconds: int = 20) -> None:
        self.base_url = base_url.rstrip("/") + "/"
        self.default_headers = default_headers or {}
        self.timeout_seconds = timeout_seconds

    def get_json(self, path: str, params: dict[str, Any] | None = None) -> HttpResponse:
        query = urlencode(params or {}, doseq=True)
        url = urljoin(self.base_url, path.lstrip("/"))
        if query:
            url = f"{url}?{query}"

        request = Request(url, headers=self.default_headers, method="GET")
        try:
            with urlopen(request, timeout=self.timeout_seconds) as response:
                body = response.read().decode("utf-8")
                data = json.loads(body)
                return HttpResponse(
                    status_code=response.getcode(),
                    headers={key: value for key, value in response.headers.items()},
                    data=data,
                )
        except HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise HttpRequestError(
                message="HTTP request failed",
                status_code=exc.code,
                body=body,
                headers={key: value for key, value in exc.headers.items()},
                url=url,
            ) from exc
        except URLError as exc:
            raise HttpRequestError(message=f"Network request failed: {exc.reason}", url=url) from exc
        except json.JSONDecodeError as exc:
            raise HttpRequestError(message=f"Response body was not valid JSON: {exc}", url=url) from exc
