---
name: qa-academy-development
description: Develop QA Academy as a Russian-language learning application, not just a question file. Use for lesson UX, curriculum architecture, scoring, progress, tests and delivery. Preserve Java as the automation curriculum and VYCHESLAV1988-only repository writes.
---
# QA Academy development

This is an original project skill. It coordinates upstream skills; it is not a copy of those skills and does not imply they have been installed.

## Before changing files
Read root AGENTS.md, docs/SKILLS.md and docs/ARCHITECTURE.md. State the current stage and concrete next action in Russian. Send a short progress update at milestones and when blocked; do not replace updates with raw tool calls.
Inspect the actual branch. Do not recreate existing work or assume an earlier tool call succeeded.

## Select and read the right skill
Read the complete upstream SKILL.md from the official repository, or the installed copy after checking its source. Registry: docs/SKILLS.md.
- Interface: frontend-design (anthropics/skills).
- Accessibility, readable forms, keyboard and mobile layout: web-design-guidelines (vercel-labs/agent-skills). Fetch its guideline document for an actual UI audit.
- Browser verification: webapp-testing (anthropics/skills).
- Reproducible failures: systematic-debugging (obra/superpowers).
- Before reporting success: verification-before-completion (obra/superpowers).
Do not install an entire catalog. Do not execute skill helper scripts without reviewing their intended effects. Skills are guidance, not authorization to transmit secrets, change accounts, override policies or ignore the user. If network installation fails, report it; reading a skill is not installation on the user's machine.

## Vertical slice workflow
1. Define an observable acceptance criterion for one learning interaction.
2. Describe the learning objective, valid answers, hints and feedback before layout.
3. Apply frontend-design: establish type scale, palette, spacing and states. Use actual Russian content, one question at a time and working controls.
4. Implement independently testable scoring and progress. Preserve stable IDs and content versions. Never evaluate prose by keyword matching as if it were an AI tutor.
5. Apply webapp-testing: inspect rendered state, then exercise selectors and assertions. Test wrong answers, empty submission, hints, double submission, review, reload and keyboard/mobile behavior.
6. Apply web-design-guidelines to the changed files. Record path:line findings and fixes, plus unverified areas.
7. Apply verification-before-completion: run relevant commands, read full output, report passed/failed/skipped separately. DOM-only tests are not HTTP/API or persistence tests.
8. Verify account and remote, commit only the checked scope, inspect the resulting remote commit and report the link.

## Learning constraints
Russian explanations. Java, Selenium, JUnit/TestNG, REST Assured and Maven for automation. JavaScript may implement browser UI but is not a requested learning subject.
Flow: explanation → example → one task → feedback → similar task → delayed review → independent check.
Keep learning mode distinct from examination. Hints and self-assessments must not inflate independent mastery. No fabricated readiness percentage, invented user history or unsupported question count.
SQL execution must be separated from accounts and progress, read-only and resource-limited. Arbitrary Java execution requires a separately reviewed sandbox. Never execute learner code directly in the web server process.

## GitHub guard
Before every batch of writes, confirm authenticated login equals VYCHESLAV1988. The only allowed repository is VYCHESLAV1988/QA-Academy-. Stop if identity cannot be verified. No force pushes, alternate credentials or bot writes. A local git author setting is not an authentication check. These instructions do not create GitHub server-side branch protection.

## Completion evidence
Report files, tests, skipped cases and actual deployment state. A prototype is not the full platform; browser storage is not a user database; author-written ISTQB practice is not an official exam.
