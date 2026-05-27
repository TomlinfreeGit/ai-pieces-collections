---
name: curl-api-testing
description: 'Test and debug DataService REST APIs with curl. Use when you need API smoke tests, request reproduction, payload validation, status-code checks, or quick endpoint verification from chat or the terminal.'
argument-hint: 'Endpoint or API scenario to test with curl'
user-invocable: true
disable-model-invocation: false
---

# Curl API Testing

Use this skill to exercise the DataService REST API with `curl` instead of Postman or ad hoc browser requests.

## When to Use

- Smoke-test a DataService endpoint after a code change.
- Reproduce a bug report with an exact HTTP request.
- Convert a request from the Postman collection into a terminal command.
- Validate request bodies, query parameters, headers, and returned status codes.
- Check whether a failure is caused by missing input, invalid input, a missing resource, or a server-side error.

## Inputs to Collect

Gather these before sending a request:

- Base URL, usually `http://localhost:4203` unless the user gives another host.
- HTTP method and endpoint path.
- Required query parameters, path parameters, and JSON body.
- Expected status code and any key fields expected in the response.

If the endpoint is not provided, look it up in [docs/data-service.postman_collection.json](../../../docs/data-service.postman_collection.json) first and use that as the request source of truth.

## Procedure

1. Confirm the target route.
   - Prefer the matching request in [docs/data-service.postman_collection.json](../../../docs/data-service.postman_collection.json).
   - If route behavior is unclear, check [README.md](../../../README.md) for how the REST layer handles routes, parameters, and errors.

2. Build the request explicitly.
   - Start with a base variable such as `BASE_URL=http://localhost:4203`.
   - Keep the path literal and only substitute path parameters once they are known.
   - For JSON bodies, prefer a heredoc or a temporary file over deeply escaped inline JSON.

3. Send the smallest useful request first.
   - For a read-only check, start with a `GET`.
   - For create or update flows, test one representative payload before batching or looping.
   - Use `--fail-with-body` so non-2xx responses still show the response body.

4. Capture status and body together.
   - Use a command shape like this:

```bash
BASE_URL=http://localhost:4203
curl --silent --show-error --fail-with-body \
  --write-out '\nHTTP %{http_code}\n' \
  --request GET \
  "$BASE_URL/DataService/Adapters"
```

5. Add request bodies safely when needed.
   - Example:

```bash
BASE_URL=http://localhost:4203
cat <<'EOF' >/tmp/request.json
{
  "name": "Profinet IO Connector",
  "type": "simaticadapter",
  "locked": false,
  "active": false,
  "isDefault": false,
  "config": {
    "brokerURL": "tcp://ie-databus:1883",
    "username": "",
    "password": "",
    "browseURL": "ie/m/j/simatic/v1/pnhs1/dp"
  }
}
EOF

curl --silent --show-error --fail-with-body \
  --write-out '\nHTTP %{http_code}\n' \
  --request POST \
  --header 'Content-Type: application/json' \
  --data @/tmp/request.json \
  "$BASE_URL/DataService/Adapters"
```

6. Interpret failures using the service conventions.
   - `400` usually means missing or invalid input.
   - `404` usually means the resource or route does not exist.
   - `500` usually means the endpoint threw a server-side exception.
   - These mappings are documented in [README.md](../../../README.md).

7. If the request fails unexpectedly, tighten the check instead of widening scope.
   - Compare the `curl` command against the matching Postman example.
   - Re-check path parameters, query parameters, and JSON field names.
   - If needed, inspect the owning feature implementation for the route registration and parameter handling.

8. Present the final result as a compact test report.
   - Always summarize executed cases in a Markdown table.
   - Keep one row per test case.
   - Include both the expected and actual status when expectations are known.
   - Reduce large response bodies to the smallest useful detail, usually `errorCode`, `title`, and `detail`.
   - If a case could not be executed, mark it clearly instead of leaving the row blank.

## Decision Points

- If the user only wants a health or smoke test, prefer one `GET` request with explicit status output.
- If the user wants to reproduce a create or update bug, use a saved JSON body file so the payload is reviewable.
- If the expected response is unknown, identify the closest request in the Postman collection before improvising.
- If the API surface appears to be gRPC-only for that scenario, stop and use a gRPC-specific workflow instead of forcing `curl`.

## Completion Criteria

Consider the task complete only when:

- The exact `curl` command is shown or executed.
- The target path, method, and payload match repo documentation or the user-provided scenario.
- The HTTP status code is captured explicitly.
- The response body is checked against the expected outcome or the mismatch is stated clearly.
- The final response includes a readable Markdown results table.
- Any next debugging hop is narrowed to one concrete route, parameter set, or owning feature.

## Final Output Format

The final answer must end with a Markdown table that is easy to scan in chat.

Use this column set by default:

| Case | Endpoint | Method | Input Summary | Expected | Actual | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |

Fill the columns with these rules:

- `Case`: Short human-readable label such as `missing file` or `invalid json body`.
- `Endpoint`: Route only, not the full host, unless multiple hosts were tested.
- `Method`: `GET`, `POST`, `PUT`, or `DELETE`.
- `Input Summary`: Short payload or parameter summary such as `body=not-json` or `form key=wrong`.
- `Expected`: Expected status and key behavior, such as `400 InvalidParameter`.
- `Actual`: Actual status and the most important returned error detail or success marker.
- `Result`: Use `PASS`, `FAIL`, or `BLOCKED` only.
- `Notes`: Keep this brief; mention mismatches, ambiguity, or follow-up hints.

When there are many cases:

- Order rows with successful baseline first, then client errors, then server errors.
- Keep wording aligned across rows so the table reads cleanly.
- Do not dump raw full JSON into the table; summarize and quote only the decisive fields.

If useful, precede the table with a one-line summary such as `Tested 6 cases: 5 PASS, 1 FAIL.`

## Reporting Template

Use this template when reporting results:

```md
Tested <N> cases: <PASS_COUNT> PASS, <FAIL_COUNT> FAIL, <BLOCKED_COUNT> BLOCKED.

| Case | Endpoint | Method | Input Summary | Expected | Actual | Result | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- |
| success baseline | /DataService/anchor-ex/v1/export/types | POST | empty body | 200 with export payload | 200 | PASS | Full export path works |
| invalid json body | /DataService/anchor-ex/v1/export/types | POST | body=not-json | 400 InvalidParameter | 400 `Valid JSON expected.` | PASS | ErrorCode 3 |
| missing file | /DataService/anchor-ex/v1/import/types | POST | no multipart file | 400 ImportFailed | 400 `Missing file with key: data` | PASS | ErrorCode 69 |
```

## Repo References

- [docs/data-service.postman_collection.json](../../../docs/data-service.postman_collection.json)
- [README.md](../../../README.md)