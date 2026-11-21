# Public development and validation report — v0.2.0

**Review date:** 2026-11-21. **Inputs in this distributable package:** Official public legal sources and entirely fictional cases. **Private patient files in release:** None.

## Author-testing disclosure and release boundary

Earlier prototypes were privately tested by the author against their own VA evidence. This was **not an independent review** and does not establish the safety, accuracy, or suitability of the tool for another veteran's claim. No author records or real-case test fixtures are included in this public release. The automated checks below use **fictional data**. A VSO, qualified medical reviewer, and independent agent-behavior evaluator should review the tool before general claims reliance. See `DISCLAIMER.md`.

## What was actually run

| Test/check | Result | Meaning |
|---|---|---|
| Python unit tests | **14 passed** | Tests of non-bilateral arithmetic and structured-ledger guardrails, using invented data. |
| Package static validator | **Passed** | Checks skill file format, required docs, 28 scenario definitions, generic secrets patterns and disallowed medical attachment formats. It cannot prove absence of all secrets or patient information. |
| Offline public synthetic fixture | **Passed** | Accepted 3 fictional same-case documents; excluded 1 different fictional claimant, and preserved the newer decision per issue. |
| Confidentiality of CLI output | **Passed** | Unit test confirmed fake clinical note text and fake condition labels are not echoed to stdout. |
| Prior permissioned private-review regression | **11 categories checked** | Read an existing private test report to verify that identified safety categories are represented in the public skill. No real-case contents are included in this package. This is not a fresh full-record or clinical validation. |
| Adversarial LLM scenarios | **28 definitions prepared; 0 independently run by an AI test harness** | Requires execution and scored outputs in the intended model host before claiming agent behavioral reliability. |
| Accredited/legal/medical reviewer sign-off | **Not obtained** | Professional independent evaluation remains necessary. |

## Current official legal-source check

On 2026-11-21, the following were consulted from authoritative public sources: **§4.25** (combined ratings), **§4.26** (bilateral factor, including paragraph (d)), **§4.71a** (spine/flatfoot), **§4.124a** (sciatic nerve and migraines), **§4.130** (mental disorders), **§3.310** (secondary conditions), public VA DBQs and review options, plus the Federal Register rescission on **2026-02-27** of the medication interim final rule. Title 38 eCFR pages reported up-to-date through **2026-11-19**. Exact URLs: `references/VERIFIED_PUBLIC_SOURCES_2026-11-21.md`.

**Important:** This is a dated source check, not a promise that all these sections remain unchanged after this release. The skill must re-check legal sources for each case and historical point-in-time question. No complete case-by-case legal interpretation, diagnosis or rating was established by the offline scripts.

## Safety architecture tested

- Each fact must link to a listed case document and a valid page, with provenance, date, issue and supports/contradicts/neutral status.
- Documents from a different `case_key` are excluded; facts/decisions sourced to excluded docs fail validation. The case key itself must be set only after private identity verification.
- Newer issue-specific decisions supersede older statuses in the latest-known report; retroactive effective dates are preserved as distinct fields.
- Proposed comparisons must reference verified official-source metadata, but the script cannot authenticate that a live external source check really occurred; it warns accordingly.
- The default script CLI does not echo clinical evidence, filenames, issue names or person identifiers.
- No client-side storage, network requests, API key, telemetry or upload function exists in the bundled Python tools.

## Remaining limitations

- It is a **skill/instructions package, not a standalone AI model**. It requires a compatible host with document access and live legal-source checking.
- No automated extraction or OCR of actual veteran files has been independently benchmarked.
- The private regression was a review of earlier test-report categories, **not** fresh execution against every page of the user's private medical records.
- The 28 behavioral scenarios still require model-host execution, scored rubrics, and expert review; unit tests alone are not a clinical/legal/accuracy validation.
- No open-source code can guarantee confidentiality if a hosted AI or external plugin sends the veteran's data elsewhere. Users must evaluate the host's storage and privacy controls.

**Conclusion:** v0.2.0 provides a more inspectable, structurally testable evidence-review workflow, but is not yet independently validated for unrestricted public claims guidance.
