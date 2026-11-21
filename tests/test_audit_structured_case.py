"""Publicly distributable synthetic-only tests of offline evidence safeguards."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from audit_structured_case import audit, is_official_url

FIXTURE = Path(__file__).resolve().parent / "public_synthetic_case.json"


def sample():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


def test_clean_public_synthetic_case():
    result = audit(sample())
    assert result["valid"] and not result["errors"]
    assert result["documents_accepted"] == 3
    assert result["documents_excluded"] == 1
    assert result["latest_known_decisions"]["shoulder_strain"]["status"] == "granted"
    assert result["latest_known_decisions"]["shoulder_strain"]["effective_date"] == "2025-01-01"
    assert result["latest_known_decisions"]["skin_condition"]["status"] == "denied"
    assert result["latest_known_decisions"]["skin_condition"]["rating"] is None


def test_excluded_person_cannot_appear_as_fact():
    case = sample()
    case["facts"].append({"id": "F-other", "document_id": "D-other", "issue": "other", "page": 1,
                          "date": "2026-04-06", "provenance": "clinical_note", "direction": "supports", "text": "Synthetic"})
    result = audit(case)
    assert not result["valid"] and result["facts_rejected"] == 1
    assert "Synthetic" not in json.dumps(result)


def test_no_fake_or_out_of_range_page():
    case = sample()
    case["facts"][0]["page"] = 9
    assert not audit(case)["valid"]


def test_no_guessed_date_or_provenance():
    case = sample()
    case["facts"][0]["date"] = "sometime in 2026"
    case["facts"][0].pop("provenance")
    assert len(audit(case)["errors"]) >= 2


def test_no_unverified_rating_comparison():
    case = sample()
    case["rating_comparisons"] = [{"fact_ids": ["F-rash"], "code": "8100", "section": "4.124a",
                                    "url": "https://example.com/fake-law", "contrary_reviewed": True, "missing_reviewed": True}]
    result = audit(case)
    assert not result["valid"] and "CURRENT RULE NOT VERIFIED" in " ".join(result["errors"])


def test_spoofed_official_hosts_disallowed():
    assert not is_official_url("https://www.ecfr.gov.evil.test/section-4.124a")
    assert not is_official_url("http://www.ecfr.gov/current/title-38")
    assert is_official_url("https://www.ecfr.gov/current/title-38/chapter-I/part-4/section-4.124a")


def test_comparison_requires_contrary_and_missing_evidence_review():
    case = sample()
    case["rating_comparisons"].append({"fact_ids": ["F-rash"], "code": "8100", "section": "4.124a",
         "url": "https://www.ecfr.gov/current/title-38/chapter-I/part-4/section-4.124a", "source_checked": True,
         "checked_on": "2026-11-21", "law_as_of": "2026-11-19", "contrary_reviewed": False, "missing_reviewed": False})
    assert not audit(case)["valid"]


def test_valid_comparison_still_warns_not_live_verified_by_script():
    case = sample()
    case["rating_comparisons"].append({"fact_ids": ["F-rash"], "code": "8100", "section": "4.124a",
         "url": "https://www.ecfr.gov/current/title-38/chapter-I/part-4/section-4.124a", "source_checked": True,
         "checked_on": "2026-11-21", "law_as_of": "2026-11-19", "contrary_reviewed": True, "missing_reviewed": True})
    result = audit(case)
    assert result["valid"] and result["warnings"]


def test_invalid_rating_rejected():
    case = sample()
    case["decisions"][1]["rating"] = 15
    assert not audit(case)["valid"]


def test_conflicting_same_day_decisions_rejected():
    case = sample()
    case["decisions"].append({"document_id": "D-newer", "issue": "shoulder_strain", "page": 3,
                              "date": "2026-02-01", "status": "denied", "rating": None})
    assert not audit(case)["valid"]


def test_no_input_text_repeated_in_results():
    case = sample()
    case["facts"][0]["text"] = "SENSITIVE-SYNTHETIC-ONLY-NEVER-OUTPUT"
    assert "SENSITIVE-SYNTHETIC-ONLY-NEVER-OUTPUT" not in json.dumps(audit(case))


def test_cli_never_prints_issue_labels_or_clinical_text(tmp_path):
    import subprocess
    case = sample()
    case["facts"][0]["issue"] = "SENSITIVE_SYNTHETIC_ISSUE"
    case["facts"][0]["text"] = "SENSITIVE_SYNTHETIC_NOTE"
    case["decisions"][0]["issue"] = "SENSITIVE_SYNTHETIC_ISSUE"
    case["decisions"][1]["issue"] = "SENSITIVE_SYNTHETIC_ISSUE"
    path = tmp_path / "case.json"
    path.write_text(json.dumps(case), encoding="utf-8")
    code = Path(__file__).resolve().parents[1] / "scripts" / "audit_structured_case.py"
    r = subprocess.run([sys.executable, str(code), str(path)], capture_output=True, text=True)
    assert r.returncode == 0
    assert "SENSITIVE_SYNTHETIC_ISSUE" not in r.stdout
    assert "SENSITIVE_SYNTHETIC_NOTE" not in r.stdout
