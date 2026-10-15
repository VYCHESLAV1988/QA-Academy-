---
name: systematic-debugging
description: Investigate QA Academy failures by reproducing the problem, collecting evidence, testing one hypothesis and verifying the smallest fix. Use before proposing fixes for bugs, test failures or unexpected behavior.
license: MIT; see LICENSE.txt
metadata:
  upstream: obra/superpowers
  edition: qa-academy-instruction-only-2026-10-15
---
# Systematic debugging — QA Academy edition

Adapted on 2026-10-15 from Jesse Vincent's MIT-licensed systematic-debugging skill: https://github.com/obra/superpowers/tree/main/skills/systematic-debugging . This self-contained project edition does not bundle upstream helper/reference files.

## Principle
Find the cause before patching the symptom. Neither the user's urgency nor previous investment makes an untested guess reliable.

## 1. Establish what fails
- Read the full error, stack trace, exit code and relevant logs.
- Reproduce with the smallest input and document expected versus actual behavior.
- Compare the affected revision, data and environment with a known working case.
- Trace data through boundaries: content loader → question selection → answer evaluator → attempt storage → displayed score.
- Log only nonsecret identifiers and whether configuration is present. Never print tokens, passwords or raw private learner responses into public logs.
- If a tool call fails before the program starts, report an environment failure, not a failed application test.

## 2. Compare and isolate
- Find a working example in this repository.
- Read the relevant implementation and contract completely.
- List meaningful differences in state, inputs, dependencies and configuration.
- Do not assume a GitHub write succeeded; read the resulting file/ref.

## 3. Test one hypothesis
- State the suspected cause and the evidence supporting it.
- Change one variable in the smallest reproducer.
- Run the verification and inspect output.
- If it fails, return to evidence rather than stacking unrelated edits.

## 4. Fix and regress
- Add a test reproducing the defect where execution is available.
- Apply the smallest coherent correction.
- Re-run the failing scenario and relevant regression tests.
- Check wrong answers, boundaries, duplicate submissions and persistence where affected.
- Use verification-before-completion before claiming the fix works.

After repeated failed hypotheses, reconsider the design instead of making increasingly broad changes. Explain the blocker and preserve working user data. Do not rewrite unrelated parts of the platform to hide a defect.

## Output
Report reproduction, root cause or remaining uncertainty, files changed, commands run and actual results. A workaround must be labelled as a workaround; skipped tests remain skipped.
