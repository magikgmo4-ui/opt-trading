"""
SPCX Insider Forms Watcher (Form 4 / Form 144)
GO_SPACEX_DAY1_ORDERFLOW_AND_OWNERSHIP_LEDGER_01

Monitors SEC EDGAR for new Form 4 (insider transactions) and Form 144
(intent to sell restricted/control securities) filings for SPCX.

Form 4 filed within 2 business days of transaction.
Form 144 filed before selling restricted/control securities above thresholds.
"""
from __future__ import annotations
import json, urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[4]
SEC_CIK = "1181412"

# Known SPCX insiders (for matching filings against)
SPCX_INSIDERS = {
    "Elon Musk": "CEO/Founder",
    "Gwynne Shotwell": "President/COO",
    "Bret Johnsen": "CFO",
    "Mark Juncosa": "VP Vehicle Engineering",
    "Antonio Gracias": "Director",
    "Donald Harrison": "Director",
}


def collect_spcx_insider_forms() -> dict[str, Any]:
    """Watch for new SPCX Form 4 and Form 144 filings.

    Returns recent insider transaction data matching spcx_ownership_ledger schema.
    """
    result = {
        "source": "spcx_insider_forms",
        "collected_at": datetime.now(timezone.utc).isoformat(),
        "ok": False,
        "symbol": "SPCX",
        "cik": SEC_CIK,

        "form4_filings": [],
        "form144_filings": [],
        "summary": {
            "form4_count_last_5_days": 0,
            "form144_count_last_5_days": 0,
            "net_insider_shares_5d": 0,
            "net_insider_value_usd_5d": 0,
            "recent_sellers": [],
            "recent_buyers": [],
        },

        "error": None,
    }

    # Fetch SEC submissions index
    filings_data = _fetch_sec_recent()
    if not filings_data:
        result["error"] = "edgar_fetch_failed"
        return result

    result["ok"] = True
    cutoff = datetime.now(timezone.utc) - timedelta(days=5)

    for f in filings_data.get("filings", []):
        form = (f.get("form") or "").upper()
        filing_date = f.get("filing_date")

        if form.startswith("4") or "FORM 4" in form:
            entry = {
                "schema": "spcx_ownership_ledger_v1",
                "source": "Form4",
                "as_of_date": filing_date,
                "filing_date": filing_date,
                "accession_number": f.get("accession_number"),
                "holder": _match_insider(f.get("primary_document", "")),
                "holder_type": "insider",
                "shares": None,
                "class": "Class A",
                "filing_disposition": "unknown",
                "notes": f"Form 4 filing. Doc: {f.get('primary_document', '')}",
            }
            result["form4_filings"].append(entry)

    for f in filings_data.get("filings", []):
        form = (f.get("form") or "").upper()
        if "144" in form:
            entry = {
                "schema": "spcx_ownership_ledger_v1",
                "source": "Form144",
                "as_of_date": f.get("filing_date"),
                "filing_date": f.get("filing_date"),
                "accession_number": f.get("accession_number"),
                "holder": None,
                "holder_type": "unknown",
                "shares": None,
                "class": "Class A",
                "filing_disposition": "partial_sale",
                "notes": f"Form 144 intent to sell. Doc: {f.get('primary_document', '')}",
            }
            result["form144_filings"].append(entry)

    # Summary
    result["summary"]["form4_count_last_5_days"] = len(result["form4_filings"])
    result["summary"]["form144_count_last_5_days"] = len(result["form144_filings"])

    if result["form144_filings"]:
        result["summary"]["recent_sellers"].append("insider_form144_detected")

    return result


def _fetch_sec_recent() -> dict | None:
    """Fetch recent SEC filings for SPCX CIK."""
    try:
        url = f"https://data.sec.gov/submissions/CIK{SEC_CIK}.json"
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "opt-trading spacex_super_desk contact=local",
                "Accept": "application/json",
            }
        )
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read().decode())
    except Exception:
        return None

    recent = data.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    dates = recent.get("filingDate", [])
    accessions = recent.get("accessionNumber", [])
    docs = recent.get("primaryDocument", [])

    filings = []
    for i in range(min(len(forms), 80)):
        filings.append({
            "form": forms[i],
            "filing_date": dates[i],
            "accession_number": accessions[i],
            "primary_document": docs[i] if i < len(docs) else None,
        })

    return {
        "company": data.get("name", "SpaceX"),
        "cik": SEC_CIK,
        "filings": filings,
    }


def _match_insider(doc_name: str) -> str | None:
    """Try to match a filing document name against known insiders."""
    if not doc_name:
        return None
    doc_lower = doc_name.lower()
    for name in SPCX_INSIDERS:
        if name.lower().replace(" ", "") in doc_lower.replace(" ", "").replace("-", "").replace("_", ""):
            return name
    return None
