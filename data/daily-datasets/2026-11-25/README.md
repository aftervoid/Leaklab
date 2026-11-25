# Daily synthetic dataset

**Date:** 2026-11-25  
**Seed:** 20261125  
**Profile records:** 10000 per format  
**Synthetic password samples:** 5000 per format  
**Chunk size:** 500 rows per file

> Large exports are split into numbered chunks so each file stays manageable in GitHub.
> All records and samples are synthetic; no real credentials or breach data are included.

## Preview: first 5 profile records

| Record ID | Username | Email | Source | Type |
|---|---|---|---|---|
| ll-00000001 | demo_user_00000001 | user00000001@example.invalid | sample-forum | contact |
| ll-00000002 | demo_user_00000002 | user00000002@example.invalid | demo-directory | account-metadata |
| ll-00000003 | demo_user_00000003 | user00000003@example.invalid | sample-forum | profile |
| ll-00000004 | demo_user_00000004 | user00000004@example.invalid | training-fixture | contact |
| ll-00000005 | demo_user_00000005 | user00000005@example.invalid | sample-forum | account-metadata |

## Password-sample aggregate

- Samples analyzed: **5000**
- Average length: **15.54** characters

| Pattern | Count |
|---|---:|
| lowercase_digits | 1667 |
| three_word_phrase | 1667 |
| mixed_random | 1666 |

## Profile records

**JSONL chunks**
- [records.jsonl](records/records.jsonl)

**CSV chunks**
- [records.csv](records/records.csv)

## Synthetic password samples

**JSONL chunks**
- [password_samples.jsonl](passwords/password_samples.jsonl)

**CSV chunks**
- [password_samples.csv](passwords/password_samples.csv)

- [Machine-readable manifest](manifest.json)
