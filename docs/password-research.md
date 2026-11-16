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


## Have I Been Pwned integration

LeakLab does not download or import the raw RockYou corpus or other breached-password
lists. Instead, the optional integration checks only records emitted by the synthetic
sample generator against the Have I Been Pwned Pwned Passwords range API.

For each generated fixture, the client computes SHA-1 locally, sends only the first
five hexadecimal characters to the range endpoint, and compares the returned suffixes
locally. The request enables response padding. No raw password, complete hash, matched
suffix list, or individual sample result is persisted or returned. The API endpoint
exposes aggregate counts only and limits each request to ten generated samples.

This is a privacy-preserving research integration, not a password checker for real
users or accounts. Never adapt it to accept real credentials. See
https://haveibeenpwned.com/api/v3#PwnedPasswords for the protocol.
