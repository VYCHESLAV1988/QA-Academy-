---
name: frontend-design
description: Design and refine QA Academy learning screens with readable Russian typography, deliberate visual hierarchy, responsive layout and complete interaction states. Use when implementing or reviewing UI rather than writing curriculum content.
license: Complete terms in LICENSE.txt
metadata:
  upstream: anthropics/skills
  edition: qa-academy-instruction-only-2026-10-15
---
# Frontend design — QA Academy edition

Modified for this project on 2026-10-15 from the Apache-2.0 frontend-design guidance by Anthropic. This is a self-contained project adaptation, not a byte-for-byte upstream installation. Original: https://github.com/anthropics/skills/tree/main/skills/frontend-design

## Brief
A Russian-speaking learner is restoring Junior QA knowledge after a break. The page's primary job is to teach one manageable concept, collect one answer, explain mistakes and preserve progress. The programming curriculum is Java, not JavaScript. Browser JavaScript is an implementation detail.

## Before building
1. Read AGENTS.md and inspect the existing screen. Preserve working controls and existing progress unless an explicit migration is included.
2. Write a compact design plan: purpose, audience, information hierarchy, 4–6 named palette tokens, type scale, spacing, layout and a subject-specific signature.
3. Critique the plan against the actual brief. Do not substitute a generic landing page, decorative statistics, unrelated stock images or a dashboard full of empty cards for the lesson.
4. Keep the current visual direction coherent. The signature interaction is a clear progression from explanation to one task to evidence-based feedback.

## Build
- Use real Russian examples and terminology from the lesson. Code is marked translate="no" and uses a monospace face.
- Body text should be comfortably readable; start around 17–18px and a 1.5–1.7 line-height. Avoid dense multi-column prose on small screens.
- Separate the learning explanation, task, learner's answer and feedback. Do not reveal an exam answer before submission.
- Choose purposeful typography and CSS tokens; do not add new fonts, colors or animation independently in each component.
- Use one clearly named primary action. Secondary actions include a hint, retry and returning to explanation.
- Implement loading, empty, validation-error, submitted, correct, incorrect and storage-failure states. No decorative fake buttons.
- Preserve visible focus, semantic forms, mobile layout and reduced-motion preferences.
- Do not use color as the only indicator of correctness. Show text and points.
- Do not inflate independent mastery with hints or self-assessment. Show these modes separately.

## Verify
Use web-design-guidelines on the changed files and webapp-testing for interaction checks. Inspect screenshots when a browser is available. Explain any environment limitation; a static code review is not a browser test. Verify long Russian text, code overflow, mobile width, keyboard navigation and actual error feedback.

## Delivery
Report concrete changed files, acceptance criteria, test results and remaining limitations. A beautiful lesson screen is not a completed user database or the full course.
