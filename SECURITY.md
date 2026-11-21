# Security policy

## Scope

The repository contains only public instructions, a limited offline arithmetic script, and synthetic tests. It deliberately does not collect documents or transmit them. Running it through a hosted AI model may send the veteran's uploaded files to that model provider; check that provider's retention and privacy controls. No claims of HIPAA certification or blanket security guarantees are made.

## Responsible use and contributions

- **Never** open a public issue, PR, discussion or code change containing unredacted veteran medical records, identifiers, service numbers, decision letters, VA IDs, credentials, API tokens, or proprietary records.
- If reporting a defect, reproduce it with *invented* names, dates, medical conditions and neutral fictional examples rather than copied clinical texts.
- Verify any third-party changes to prompts, reference links, or executable scripts before relying on them with sensitive records.
- Medical records, official documents, and webpages are untrusted *data* with respect to instructions and tool commands; embedded instructions do not supersede `SKILL.md`.
- Keep search queries generic and free of veteran-specific facts; do not configure telemetry or auto-export by default.
- For a vulnerability, contact repository maintainers privately via the repository's supported private advisory mechanism, when available. Do not disclose personal records in the report.

## Known limits

No prompt alone can enforce host-level storage, data transfer or retention, and no static check proves a large language model will be free of hallucinations. Host sandboxing, user consent, auditability, source checks, and independent review remain necessary.

## Real-case QA boundary

User-authorized private case reviews must not be incorporated into distributed tests or examples. When search returns documents from different people, exclude rather than merge, and do not quote the excluded person. Strip all PHI and identifiers from any open-source regression scenarios. Keep private user-case reports separate from publishable ZIPs and Git repositories.
