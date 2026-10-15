---
name: webapp-testing
description: Verify QA Academy UI with Python Playwright using real browser interactions, assertions and diagnostic evidence. Use for lesson flows, filters, scoring, hints, review, persistence and mobile checks.
license: Complete terms in LICENSE.txt
metadata:
  upstream: anthropics/skills
  edition: qa-academy-instruction-only-2026-10-15
---
# Web application testing — QA Academy edition

Modified on 2026-10-15 from the Apache-2.0 webapp-testing guidance by Anthropic. This instruction-only adaptation uses the project's own tests. Upstream helper scripts and example files are not bundled and must not be assumed installed. Original: https://github.com/anthropics/skills/tree/main/skills/webapp-testing

## Scope
Playwright is a developer verification tool. It does not change the learner's requested Java automation curriculum.

## Inspect, then act
1. Read the changed HTML/components and identify how to start the application.
2. Start the server in the permitted environment. Do not bypass browser policies or change system security settings.
3. Open a page using Python Playwright. Wait for the application readiness condition; for a finite-load static page, networkidle can be useful. Do not rely on arbitrary long sleeps.
4. Inspect the rendered DOM and capture a screenshot if supported.
5. Choose semantic selectors such as get_by_role and get_by_label from the actual rendered page.
6. Execute the user's actions and assert visible outcomes and persisted state.
7. Record console errors, network failures and screenshots on failure. Remove secrets from evidence.
8. Close browser contexts and stop test servers even when a test fails.

## Required cases for a learning flow
- Initial explanation and one task are visible; no fabricated progress.
- Empty submission shows an accessible error and creates no attempt.
- Wrong answer gives the correct explanation and an honest score.
- Correct answer creates exactly one attempt; repeated clicks do not duplicate it.
- A hint is recorded as assisted; self-assessment is not presented as automatic AI grading.
- The next question, previous explanation, review queue and topic filters really work.
- Wrong or due items return for review; mastered items are not arbitrarily lost.
- Reload and server restart preserve progress when persistence is implemented.
- Two accounts cannot read or change each other's answers when accounts exist.
- Long Russian text and code fit a 390px viewport without page-level horizontal overflow.
- Radio options, text fields and submission work by keyboard with visible focus.
- Disabled storage or unavailable API produces a clear recoverable state.

## Minimal pattern
```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    try:
        page = browser.new_page()
        page.goto('http://127.0.0.1:8765/')
        page.get_by_role('main').wait_for()
        # Inspect actual DOM, then use the observed labels and roles.
        assert page.title()
    finally:
        browser.close()
```

## Evidence boundaries
A DOM-only set_content run does not prove HTTP routing, authentication or persistence. A source file containing tests is not a passing test report. Keep passed, failed, skipped and not-run counts distinct. Use verification-before-completion before reporting success.
