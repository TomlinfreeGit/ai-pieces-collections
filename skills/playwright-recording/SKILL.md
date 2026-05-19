---
name: playwright-recording
description: >-
  Playwright skill for recording and generating Typescript scripts When user says "record a new test case", "record playwright test", "playwright codegen new test case" or similar commands.
---

# Playwright Recording Playbook

Use this skill to produce Playwright scripts with enterprise-ready patterns.

## Apply this project structure by default

```text
playwright/tests
playwright/playwright.config.ts
```

- Place codegen output test scripts in `playwright/tests/`.
- Playwright configuration files in `playwright/playwright.config.ts`.

## Usage

1. Use playwright codegen functionality to generate original E2E test code, including test steps, asserts, locators. Always use `--ignore-https-errors` flag to avoid the failure caused by https errors, and use `--viewport-size "1920,1080"` flag to set the viewport size to avoid the failure caused by element not visible.
```bash
npx playwright codegen https://<ied-ip>/device/edge/a.service/api/v3/login --ignore-https-errors --viewport-size "1920,1080" -o tests/test-<random-6-numbers>.spec.ts
```

2. Test recording scripts
```bash
npx playwright test tests/test-<random-6-numbers>.spec.ts
```
