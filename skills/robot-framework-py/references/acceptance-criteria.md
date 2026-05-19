# Acceptance Criteria: robot-framework-py

These criteria are written as concrete, checkable rules for generated content, examples, and reviews.

## Process alignment

This repository keeps acceptance criteria in two locations for compatibility:
- Canonical reference: `references/acceptance-criteria.md`
- Skill package path: `.github/skills/robot-framework-py/references/acceptance-criteria.md`

Both files must remain identical.

## A) Correct Robot Framework syntax

### Required (pass rules)
- Output must use valid section headers for `.robot` suites:
  - `*** Settings ***`
  - `*** Variables ***` (when variables are used)
  - `*** Test Cases ***`
  - `*** Keywords ***` (when custom keywords are present)
- If output is a resource file, it must be in `.resource` format with valid sections for resource content.
- Assertions must use BuiltIn keywords, and generated examples must include:
  - `Should Be Equal`
  - `Should Contain`
- Keywords and section names must use canonical Robot Framework spelling.

### Forbidden (fail rules)
- Invalid section headers such as:
  - `*** Setting ***`
  - `*** TestCase ***`
- Raw Python assertion styles in `.robot` outputs (`assert x == y`).
- Invented assertion keywords that are not defined in the same output.

## B) Library correctness

### Required (pass rules)
- API testing scenarios must prefer RequestsLibrary and include installation guidance:
  - `pip install robotframework-requests`
- OS and file operations must use OperatingSystem library keywords.
- Library usage must favor official and widely used Robot Framework ecosystem libraries.
- Library imports must be explicit in `*** Settings ***`.

### Forbidden (fail rules)
- Python `requests` usage inside Robot suite output (`import requests`, `requests.get(...)`).
- Replacing OperatingSystem keyword usage with shell commands for file checks.
- Claiming third-party libraries are built-in.

## C) Scalability practices

### Required (pass rules)
- Reusable logic must be moved into resource files when shared by multiple tests.
- Credentials/secrets must not be hardcoded; use variable files and/or environment variables.
- Shared lifecycle operations must be implemented with `Suite Setup` / `Suite Teardown` when appropriate.
- Examples should separate test intent (test cases) from implementation details (keywords/resources).

### Forbidden (fail rules)
- Inline credentials or tokens in test bodies.
- Duplicated setup/auth boilerplate in every test case.
- Unbounded synchronization patterns (for example long static sleeps instead of deterministic checks).

## D) Do-not-hallucinate constraints

### Required (pass rules)
- If a library is not in Robot Framework standard libraries and not explicitly user-selected, label it as **OPTIONAL external**.
- Generated content must only use known keywords from imported libraries or explicitly defined custom keywords.

### Forbidden (fail rules)
- Presenting fabricated keywords as built-in.
- Stating a non-standard library is part of Robot Framework core.

## Correct/incorrect import patterns

### Correct
- `Library    RequestsLibrary`
- `Library    OperatingSystem`
- `Library    Browser`
- `Library    AppiumLibrary`
- `Library    DatabaseLibrary`
- `Resource    ../resources/common.resource`

### Incorrect
- `import requests` in `.robot` files
- `Library    requests`
- Omitting required library import while using its keywords

## Authentication patterns

### Required
- Build auth headers in reusable keywords.
- Read secrets from environment variables or variable files.
- Validate both status code and critical payload fields.

### Forbidden
- Hardcoded bearer tokens, passwords, or API keys.
- Duplicated auth setup in each test case.

## Async variants

### Required
- Use bounded waits/timeouts for async flows.
- Keep async handling logic in reusable keywords/resources.

### Forbidden
- Arbitrary static waits as the primary synchronization mechanism.
- Unbounded polling loops.
