---
name: verification-before-completion
description: Require fresh evidence before stating that a QA Academy feature, question count, test suite, build, GitHub update or skill installation is complete. Use immediately before every completion report.
license: MIT; see LICENSE.txt
metadata:
  upstream: obra/superpowers
  edition: qa-academy-instruction-only-2026-10-15
---
# Verification before completion — QA Academy edition

Adapted on 2026-10-15 from Jesse Vincent's MIT-licensed verification-before-completion skill: https://github.com/obra/superpowers/tree/main/skills/verification-before-completion . Instruction-only project edition.

## Gate
1. Identify the exact evidence needed for the claim.
2. Run or retrieve that evidence fresh in the current work session.
3. Read the complete relevant output and exit status.
4. Compare the evidence with the user's requirement, not with an easier substitute.
5. Report only what the evidence supports, with explicit limitations.

## Evidence required in this project
| Claim | Required evidence |
|---|---|
| Questions added | Loader/count output, stable unique IDs, nonempty answers and explanations, and an inspected repository revision |
| No duplicate questions | Defined duplicate rule and its check; textual uniqueness alone is not semantic uniqueness |
| 1,070 questions available in the UI | The loaded curriculum count and a test that all IDs are reachable through the actual UI/API |
| Correct SQL answer | Execution on the specified isolated fixtures, including edge cases; string equality alone is insufficient |
| Tests pass | Fresh test run with passed, failed and skipped counts; a test file is not a test result |
| Progress persists | Save, reload/restart and retrieve the same attempt; in-memory state is not persistence |
| Users are isolated | Tests with at least two accounts plus server-side access checks |
| GitHub changes published | Read back the branch head and files after the update; validate author and committer mapping |
| Skills installed in repository | Actual .agents/skills/<name>/SKILL.md files with valid metadata and required local resources present |
| Skills installed on user's computer | Evidence from that computer or environment, not merely a repository commit |
| Full upstream package installed | Actual upstream distribution/CLI output, not a locally adapted SKILL.md |

## No substitutions
A source review is not an execution test. A DOM-only run is not an HTTP integration test. A prototype is not the platform. An author-written practice set is not an official ISTQB exam. Automated schema tests do not independently validate every answer's technical correctness.

If execution is unavailable, state that fact and provide the written checks as not run. Do not fabricate logs, question counts, dashboards, scores, screenshots or installation success.
