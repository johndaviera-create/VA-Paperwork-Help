#!/usr/bin/env python3
"""Offline, privacy-minimizing structural audit of a SOURCE-GROUNDED case ledger.

Does NOT extract data from medical records, practice medicine, verify laws online,
calculate entitlements, or make a VA decision. Designed for an LLM to propose a
structured ledger first, then get deterministic validation before sharing claims.

Input may contain PHI: run locally; do not commit input files or console logs.
The default CLI output includes only counts and generic errors (no clinical facts or issue names).
"""
from __future__ import annotations

import argparse
from collections import defaultdict, Counter
from datetime import date
import json
from pathlib import Path
from urllib.parse import urlparse

ALLOWED_PROVENANCE = {"clinical_note", "objective_result", "service_record", "va_decision", "lay_statement", "veteran_report"}
ALLOWED_DIRECTIONS = {"supports", "contradicts", "neutral"}
ALLOWED_DECISIONS = {"granted", "denied", "continued", "increased", "decreased", "deferred", "remanded", "unknown"}
OFFICIAL_HOSTS = {"ecfr.gov", "www.ecfr.gov", "govinfo.gov", "www.govinfo.gov", "federalregister.gov", "www.federalregister.gov", "va.gov", "www.va.gov", "benefits.va.gov", "www.benefits.va.gov", "uscode.house.gov"}


def is_official_url(value: object) -> bool:
    if not isinstance(value, str):
        return False
    parsed = urlparse(value)
    return parsed.scheme == "https" and parsed.hostname in OFFICIAL_HOSTS and not parsed.username and not parsed.password


def valid_date(value: object) -> bool:
    if not isinstance(value, str):
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def audit(case: dict) -> dict:
    """Return only a structural QA summary, not input text, names or clinical data."""
    errs: list[str] = []
    warns: list[str] = []
    key = case.get("case_key")
    if not isinstance(key, str) or not key.strip():
        errs.append("case_key missing: cannot verify record ownership")
    documents = {}
    excluded = 0
    for index, doc in enumerate(case.get("documents", [])):
        doc_id = doc.get("id")
        if not isinstance(doc_id, str) or not doc_id or doc_id in documents:
            errs.append(f"document[{index}]: invalid or duplicate document id")
            continue
        if doc.get("case_key") != key or not key:
            excluded += 1
            continue
        if not isinstance(doc.get("pages"), int) or isinstance(doc.get("pages"), bool) or doc["pages"] < 1:
            errs.append(f"document[{index}]: positive page count required")
        documents[doc_id] = doc

    seen_facts: set[str] = set()
    kept_facts: set[str] = set()
    excluded_facts = 0
    for index, fact in enumerate(case.get("facts", [])):
        fact_id = fact.get("id")
        if not isinstance(fact_id, str) or not fact_id or fact_id in seen_facts:
            errs.append(f"fact[{index}]: invalid or repeated fact id")
            continue
        seen_facts.add(fact_id)
        doc_id = fact.get("document_id")
        if doc_id not in documents:
            excluded_facts += 1
            # A fact from another person, or an unknown document, is NEVER usable.
            errs.append(f"fact[{index}]: source excluded or unavailable")
            continue
        doc = documents[doc_id]
        page = fact.get("page")
        if isinstance(page, bool) or not isinstance(page, int) or not (1 <= page <= doc.get("pages", 0)):
            errs.append(f"fact[{index}]: missing/out-of-bounds source page")
        if fact.get("provenance") not in ALLOWED_PROVENANCE:
            errs.append(f"fact[{index}]: source provenance missing or invalid")
        if fact.get("direction") not in ALLOWED_DIRECTIONS:
            errs.append(f"fact[{index}]: missing supports/contradicts/neutral label")
        if not valid_date(fact.get("date")):
            errs.append(f"fact[{index}]: documented date required (YYYY-MM-DD)")
        if not isinstance(fact.get("issue"), str) or not fact["issue"].strip():
            errs.append(f"fact[{index}]: issue missing")
        if not isinstance(fact.get("text"), str) or not fact["text"].strip():
            errs.append(f"fact[{index}]: cited observation missing")
        kept_facts.add(fact_id)

    decisions = defaultdict(list)
    for index, item in enumerate(case.get("decisions", [])):
        doc_id = item.get("document_id")
        if doc_id not in documents:
            errs.append(f"decision[{index}]: source excluded or unavailable")
            continue
        if item.get("status") not in ALLOWED_DECISIONS:
            errs.append(f"decision[{index}]: invalid decision status")
        if not valid_date(item.get("date")):
            errs.append(f"decision[{index}]: decision date required")
            continue
        page = item.get("page")
        if isinstance(page, bool) or not isinstance(page, int) or not (1 <= page <= documents[doc_id].get("pages", 0)):
            errs.append(f"decision[{index}]: page missing or out of bounds")
        if not isinstance(item.get("issue"), str) or not item["issue"].strip():
            errs.append(f"decision[{index}]: issue missing")
            continue
        rating = item.get("rating")
        if rating is not None and (isinstance(rating, bool) or not isinstance(rating, int) or rating < 0 or rating > 100 or rating % 10):
            errs.append(f"decision[{index}]: invalid individual rating")
        if item.get("effective_date") is not None and not valid_date(item.get("effective_date")):
            errs.append(f"decision[{index}]: invalid effective date")
        decisions[item["issue"]].append(item)

    # Report only the latest known issue statuses, never the patient's notes.
    latest = {}
    for issue, entries in decisions.items():
        entries.sort(key=lambda d: d["date"])
        if len(entries) > 1 and entries[-1]["date"] == entries[-2]["date"] and entries[-1]["status"] != entries[-2]["status"]:
            errs.append("conflicting same-day decisions: human review required")
        chosen = entries[-1]
        latest[issue] = {"date": chosen["date"], "status": chosen["status"], "rating": chosen.get("rating"), "effective_date": chosen.get("effective_date")}

    for index, match in enumerate(case.get("rating_comparisons", [])):
        linked = match.get("fact_ids")
        if not isinstance(linked, list) or not linked or any(f not in kept_facts for f in linked):
            errs.append(f"comparison[{index}]: no complete supporting fact citations")
        if not match.get("code") or not match.get("section"):
            errs.append(f"comparison[{index}]: diagnostic code/section missing")
        if match.get("source_checked") is not True or not valid_date(match.get("checked_on")) or not valid_date(match.get("law_as_of")) or not is_official_url(match.get("url")):
            errs.append(f"comparison[{index}]: CURRENT RULE NOT VERIFIED; no current rating claim permitted")
        if not match.get("contrary_reviewed") or not match.get("missing_reviewed"):
            errs.append(f"comparison[{index}]: contrary or missing evidence not considered")
        warns.append(f"comparison[{index}]: source fields are attestations, not proof that a live legal check occurred")

    return {
        "valid": not errs,
        "documents_accepted": len(documents),
        "documents_excluded": excluded,
        "facts_accepted_for_review": len(kept_facts),
        "facts_rejected": excluded_facts,
        "latest_known_decisions": latest,
        "errors": errs,
        "warnings": warns,
        "limitations": ["Structural validation only; cannot verify medical truth or live rule text", "No official VA determination, rating prediction, or complete privacy assurance"],
    }


def main() -> int:
    p = argparse.ArgumentParser(description="Offline audit of structured case evidence; input should be kept PRIVATE")
    p.add_argument("path", type=Path, help="JSON case ledger input (never commit real case JSON)")
    args = p.parse_args()
    result = audit(json.loads(args.path.read_text(encoding="utf-8")))
    # Never print case-specific condition/issue names by default; a condition
    # label may itself reveal sensitive medical information. The Python return
    # value remains available to an authorized private review workflow.
    output = {k: v for k, v in result.items() if k != "latest_known_decisions"}
    output["latest_decision_status_counts"] = dict(sorted(Counter(
        row["status"] for row in result["latest_known_decisions"].values()
    ).items()))
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
