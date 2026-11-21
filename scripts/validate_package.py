#!/usr/bin/env python3
"""Static package QA; not a substitute for medical/legal expert evaluation."""
from pathlib import Path
import json
import re
import sys

root = Path(__file__).resolve().parent.parent
skill_path = root / "SKILL.md"
skill = skill_path.read_text(encoding="utf-8")
errors = []
match = re.match(r"\A---\n(.*?)\n---\n", skill, re.S)
if not match:
    errors.append("SKILL.md lacks YAML frontmatter")
else:
    fm = match.group(1)
    name = re.search(r"^name:\s*(.*)$", fm, re.M)
    desc = re.search(r"^description:\s*(.*)$", fm, re.M)
    if not name or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name.group(1)) or name.group(1) != root.name or len(name.group(1)) > 64:
        errors.append("Invalid or mismatched skill name")
    if not desc or not 1 <= len(desc.group(1)) <= 1024:
        errors.append("Invalid description")
for filename in ["README.md", "LICENSE", "SECURITY.md", "DISCLAIMER.md", ".gitignore", "references/SOURCE_POLICY.md", "references/REGULATORY_MAP.md", "references/OUTPUT_TEMPLATE.md", "references/PRIVACY_AND_THREATS.md", "scripts/combined_rating.py", "scripts/audit_structured_case.py", "tests/scenarios.json", "tests/test_audit_structured_case.py", "tests/public_synthetic_case.json", "tests/AGENT_BEHAVIOR_TEST_GUIDE.md", "references/VERIFIED_PUBLIC_SOURCES_2026-11-21.md", "PUBLIC_VALIDATION_REPORT.md"]:
    if not (root / filename).is_file():
        errors.append("Missing " + filename)
for required in ["Never fabricate", "CURRENT RULE NOT VERIFIED", "§ 4.26", "prompt", "source", "contrary", "redact", "proposed"]:
    if required.lower() not in skill.lower() and required.lower() not in (root / "references/PRIVACY_AND_THREATS.md").read_text().lower():
        errors.append("Missing guardrail term: " + required)
scenarios = json.loads((root / "tests/scenarios.json").read_text(encoding="utf-8"))
if len(scenarios) < 10 or len({s["id"] for s in scenarios}) != len(scenarios):
    errors.append("Too few/duplicate scenarios")
for item in scenarios:
    if not all(k in item and item[k] for k in ("id", "input", "expected")):
        errors.append("Bad scenario: " + str(item))
for path in root.rglob("*"):
    if path.is_file() and path.suffix.lower() in {".pdf", ".docx", ".doc", ".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic", ".zip"}:
        errors.append(f"Unexpected potential private attachment in public release: {path.relative_to(root)}")
for path in root.rglob("*"):
    if path.is_file() and ".git" not in path.parts and path.suffix in {".md", ".py", ".json", ".txt", ""}:
        contents = path.read_text(encoding="utf-8", errors="replace")
        for expr, description in [(r"\b\d{3}[- ]\d{2}[- ]\d{4}\b", "potential social security number"), (r"sk-[A-Za-z0-9_-]{16,}", "potential OpenAI API key"), (r"ghp_[A-Za-z0-9]{30,}", "potential GitHub token"), (r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", "private key")]:
            if re.search(expr, contents):
                errors.append(f"{path.name}: {description}")
if errors:
    print("FAILED:\n- " + "\n- ".join(errors))
    sys.exit(1)
print(f"PASS: Agent Skills metadata, {len(scenarios)} synthetic scenario definitions (NOT LLM executions), public files, basic privacy/secret-pattern scan")
