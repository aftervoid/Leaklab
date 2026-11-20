# Local API reference

All endpoints are served by the local FastAPI application. Interactive OpenAPI documentation is available at `/docs`.

## Health and configuration

### `GET /api/health`

Returns service status, runtime environment, and the active data policy.

### `GET /api/config`

Returns public defaults and the LeakLab version.

## Synthetic password research

### `GET /api/password-lab/summary?count=1000&seed=42`

Generates fictional samples deterministically and returns aggregate length, pattern, and shape-rating statistics. The `count` parameter is limited to 0–100,000. Sample strings are never included in the response.

### `GET /api/password-lab/hibp-summary?count=5&seed=42`

Optionally checks 1–10 generated fixtures through the HIBP Pwned Passwords k-anonymity range protocol. Only aggregate counts are returned. This endpoint requires network access to HIBP and may return HTTP 503 when the upstream service is unavailable.

## Daily dataset metadata

### `GET /api/datasets`

Returns a date-descending index of daily manifests. Each dataset card contains its UTC date, reproducibility seed, split status, profile-record count, synthetic password-sample count, average sample length, pattern aggregates, and chunk counts.

### `GET /api/datasets/{YYYY-MM-DD}`

Returns the manifest for one canonical ISO-8601 date. Invalid dates and dates without a readable manifest return HTTP 404.

The dataset endpoints read manifest files only. They do not read or return the underlying JSONL/CSV sample contents.

## Data safety

- Do not send real account passwords to any LeakLab endpoint.
- Do not add endpoints that accept, store, or transmit real credentials.
- Do not use this API to test logins or query breach dumps.
- Treat the shape score as an educational heuristic, not a security guarantee.
