from __future__ import annotations
import json
import urllib.request
from typing import Any
from ..io import utc_now

SEC_SUBMISSIONS_URL = "https://data.sec.gov/submissions/CIK{cik:010d}.json"

def collect_sec_edgar(cik: int = 1181412, *, timeout: int = 15) -> dict[str, Any]:
    url = SEC_SUBMISSIONS_URL.format(cik=cik)
    out = {"source": "sec_edgar", "collected_at": utc_now(), "url": url, "ok": False, "filings": [], "error": None}
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "opt-trading spacex_super_desk contact=local", "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            data = json.loads(resp.read().decode("utf-8"))
        recent = data.get("filings", {}).get("recent", {})
        forms = recent.get("form", [])[:40]
        dates = recent.get("filingDate", [])[:40]
        acc = recent.get("accessionNumber", [])[:40]
        docs = recent.get("primaryDocument", [])[:40]
        out["company_name"] = data.get("name")
        out["tickers"] = data.get("tickers", [])
        out["filings"] = [{"form": f, "filing_date": dates[i] if i < len(dates) else None, "accession": acc[i] if i < len(acc) else None, "primary_document": docs[i] if i < len(docs) else None} for i, f in enumerate(forms)]
        out["ok"] = True
    except Exception as exc:
        out["error"] = str(exc)
    return out


def fetch_sec_submissions(cik: str = "1181412", *, timeout: int = 15) -> dict[str, Any]:
    return collect_sec_edgar(cik=int(cik), timeout=timeout)
