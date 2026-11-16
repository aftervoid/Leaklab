# Security and data-handling policy

## Synthetic-only password research

LeakLab is an educational password-pattern research project. It may generate and analyze fictional password samples and use appropriately licensed public aggregate statistics with clear attribution.

Never add functionality to:
- ingest, index, search, or redistribute real breach dumps or stolen credential lists;
- test passwords against real services, accounts, or leaked-password corpora;
- collect, store, transmit, or validate real passwords, hashes, authentication tokens, session cookies, or API keys;
- automate login attempts, credential stuffing, or account access;
- identify real people from exposed records.

Never enter a password used for a real account into LeakLab. The current analyzer operates on generated fixtures and reports aggregate shape statistics only. Its score is a limited heuristic, not a guarantee of safety.

## Reporting

Do not submit credentials, personal information, or breach samples in issues or pull requests. Reproduce problems with generated fixtures only.
