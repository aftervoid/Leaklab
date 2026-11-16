# Password research scope

LeakLab studies password construction patterns using deterministic, fictional fixtures.
The included analyzer reports length and character-class diversity as transparent
shape heuristics. Its score is educational and is not a guarantee of security,
an estimate of cracking time, or a check against known compromised passwords.

## Permitted inputs

- Generated samples from `leaklab.password_lab`.
- Public, aggregate research statistics with clear provenance and compatible terms.
- Hand-authored fictional examples in tests and documentation.

## Out of scope

- Breach dumps, credential lists, password hashes, account login testing,
  credential stuffing, password recovery, and collection of real credentials.
- Uploading or retaining passwords entered by users.

The dashboard preview uses generated samples and returns aggregate counts only.
