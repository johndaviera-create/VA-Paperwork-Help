# VA Disability Evidence Review — free and open-source AI skill

A portable, independent **Agent Skills** package for reviewing U.S. veterans' supplied medical and service evidence against verified official VA disability rating rules. This is **not** an official VA service, not a medical examiner, not legal representation, and not a VA disability rating adjudicator.

**Mission:** Show what the *actual supplied documents* establish, compare to operative VA regulatory criteria, identify gaps and possible discrepancies, and preserve the contrary evidence. No invented diagnoses, symptoms, DBQs, nexus letters, deployments, regulatory rules, or guaranteed percentages.

## Important disclaimer — please read before using

> **Unofficial educational tool; not a substitute for a VSO.** The author privately tested earlier versions of this skill against their **own VA medical and claims records**, and this version has passed the reproducible, **synthetic-data** tests described in [`PUBLIC_VALIDATION_REPORT.md`](PUBLIC_VALIDATION_REPORT.md). **Testing on one person's records is not independent validation**, does not prove accuracy for other veterans, and is not an endorsement by VA. Independent review by a VA-accredited representative and qualified medical/legal reviewers **is still needed** before this project can be considered reliable for public claims guidance.
>
> The skill is intended to **help veterans understand their documents, locate relevant official rules, organize evidence, and prepare questions for an accredited Veterans Service Organization (VSO)** — **not replace a VSO**, an accredited claims agent or attorney, a treating clinician, a C&P examiner, or VA adjudicators. It does not make claim decisions, establish service connection, provide personalized legal or medical advice, submit claims on your behalf, or guarantee any disability rating or compensation. Always verify facts and current law with primary sources and seek review from a VA-accredited representative before acting.

**Privacy:** Personal medical records used for private testing are **not** part of this repository or its test fixtures. Please **do not post private medical records, VA claim numbers, or personally identifying information in public GitHub issues, discussions, or pull requests**. Review your chosen AI provider's data handling before uploading records. See [`DISCLAIMER.md`](DISCLAIMER.md) and [`SECURITY.md`](SECURITY.md).

Find free accredited VSO assistance through [VA's official representative search](https://www.va.gov/get-help-from-accredited-representative/).

## What it does

- Inventory the supplied VA decisions, DBQs, clinical notes, testing and service records.
- Extract evidence into a structured ledger with document date and page/section references.
- Verify the applicable 38 CFR diagnostic codes and their controlling versions *live* via eCFR, Federal Register and VA sources before drawing rating comparisons.
- Separate diagnosis, severity, service connection, nexus, and adjudication rather than conflating them.
- Show favorable, contradictory, and missing evidence and label insufficient cases candidly.
- Produce a neutral, actionable report for the veteran or an accredited VSO.
- Optionally show **non-bilateral, illustrative** combined-rating arithmetic using a local script (the bilateral factor requires separate review).

## How to use

1. Download this folder/ZIP and extract it.
2. Install or copy the `va-evidence-review` directory into a compatible AI agent's skills location, following that host's documentation; or attach `SKILL.md` and its `references/` to a conversation, if your host cannot natively load skills.
3. Enable **read access** to the veteran-provided documents and **web access limited to public official legal sources** if you want up-to-date legal/rating comparisons. Do not grant document-upload permissions to public websites.
4. Ask: `Use the va-evidence-review skill to analyze the records I provided. Show documented findings, exact source pages, the applicable verified diagnostic code, supporting and contrary evidence, and evidence gaps. Do not guess ratings.`
5. Double-check each reported fact against the original documents and current official law. Seek review from an accredited VSO or qualified professional where appropriate.

This skill contains **no remote service, telemetry, bundled model, secrets, or API keys**. Its package is free under MIT; the AI product you choose may charge for model usage or uploads. Uploaded records are governed by that product's privacy/retention practices, not this folder.

## Required source access

Before issuing a purportedly **current** rating comparison, a host must be able to open the official operative 38 CFR text and verify the relevant effective-date context. A model without live web access must return `CURRENT RULE NOT VERIFIED` and can still do a document-only evidence inventory. An offline model with vetted local historical copies is not automatically current.

Start with: https://www.ecfr.gov/current/title-38/chapter-I/part-4 and https://www.va.gov/disability/about-disability-ratings/ . The specific official-source map is in `references/SOURCE_POLICY.md`.

## Quality assurance

Run offline static and arithmetic checks (Python 3.9+; optional pytest for the full suite):

```bash
python3 scripts/validate_package.py
python3 tests/test_combined_rating.py
python3 scripts/combined_rating.py 60 40 20
python3 -m pytest -q
python3 scripts/audit_structured_case.py tests/public_synthetic_case.json
```

`tests/scenarios.json` contains 28 **synthetic, non-personal** evaluation prompts for manual or automated agent QA. They are test specifications, **not proof of AI output accuracy**. Before real-world rollout, evaluate fresh official sources, quoted page accuracy, false positive/false negative extraction, privacy policies, claim-type edge cases, and expert review of a blinded, permissioned test set.

## Limitations

A correct diagnosis in a medical note does not by itself prove service connection; symptoms do not automatically prove a diagnostic code's rating tier; not finding a fact in an uploaded file is not evidence that the condition is absent. The VA alone decides disability ratings. DBQs are medical instruments and must be completed/authenticated by clinicians when required.

The report is educational information, not medical or legal advice or an attorney/client relationship. Free accredited VSO assistance: https://www.va.gov/get-help-from-accredited-representative/

## Project files

- `SKILL.md` — portable skill instructions
- `references/` — rule source policy, lookup map, output template, security guidance
- `scripts/combined_rating.py` — limited, non-bilateral illustrative table-step arithmetic
- `scripts/validate_package.py` — static metadata/secret-pattern check
- `tests/` — synthetic QA cases and arithmetic test
- `PUBLIC_VALIDATION_REPORT.md` — public-only executed test results and clearly labeled limitations
- `tests/AGENT_BEHAVIOR_TEST_GUIDE.md` — separate, unrun AI behavior evaluation protocol
- `SECURITY.md` — disclosure and record-handling expectations
- `DISCLAIMER.md` — prominent disclosure of test limits, independence, and VSO role

## Status

**v0.2.0 — research-backed prompt/skill prototype (real-case-informed hardening, public tests remain synthetic).** Static validation and deterministic arithmetic tests can be run locally; this package has **not** undergone independent accredited VA reviewer validation, medical review, host-by-host integration tests, or any production privacy certification. File feedback and improvements without uploading real veteran medical data.

## v0.1.1 updates

Private testing informed safeguards for evidence attribution, decision chronology, and conservative interpretation. The public test cases use fictional data.

## v0.2.0 — reproducible public-data QA

- **Offline validator:** `python scripts/audit_structured_case.py tests/public_synthetic_case.json`. Checks the structure of an evidence ledger before narrative generation and prints summary counts and decisions only. The included JSON fixture is completely fictitious and deliberately contains a different-claimant document to verify exclusion.
- **Unit tests:** `python -m pytest -q` from the skill folder (requires the optional `pytest` package). These are executable tests for the combined-rating helper and structural audit.
- **Static package and privacy-pattern check:** `python scripts/validate_package.py`. This checks public test files and common token patterns, not unseen users' files, and does not constitute a complete privacy certification.
- **Behavior specifications:** `tests/scenarios.json` contains fully synthetic agent-behavior prompts. Merely having a scenario definition **does not count as a passed LLM test**. Run these against each intended AI host and have reviewers score actual outputs.
- **Verified public source snapshot:** `references/VERIFIED_PUBLIC_SOURCES_2026-11-21.md`. The links and dated notes are navigation aids only; live rule verification is required for every subsequent rating comparison.

### Information separation

The distributed ZIP intentionally contains no actual veteran documents, no real-case excerpts, and no private regression fixtures. With consent, a reviewer may evaluate private cases separately, but none of the case data or derived identifying combinations may be committed. The audit CLI may handle patient-provided JSON **only** in a trusted, private environment. Never upload a case file to public CI or open GitHub issues. If using a hosted AI system, its own data processing rules still apply.

### What has *not* been validated

The unit tests cannot establish that an AI model interprets 1,000-page health records correctly, checks every relevant legal nuance, or always resists malicious prompts. Independent physician and accredited VA representative review, including blind real-case audits and repeated prompt evaluations, are still needed before general-public reliability claims.
