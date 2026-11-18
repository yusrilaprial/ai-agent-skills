---
name: bug-analysis
description: Investigate bugs in software applications using a disciplined, evidence-driven engineering workflow. Use when a user reports unexpected behavior, an error, a regression, a crash, or asks to find the root cause of a software defect.
---

# Bug Analysis

Diagnose software defects methodically. Build conclusions from observable evidence, identify the most likely root cause, and propose the smallest reliable correction. Do not guess from symptoms or claim certainty beyond the evidence.

## Workflow

1. **Define the failure**
   - Restate the observed behavior, expected behavior, and affected area in concrete terms.
   - Identify the environment, inputs, and steps that trigger the issue when available.
   - If key information is missing, inspect the code and available logs first. Ask focused questions only when the missing details prevent meaningful investigation.

2. **Reproduce or trace it**
   - Follow the execution path from the triggering input to the incorrect result.
   - Inspect relevant call sites, state changes, data transformations, error handling, and external boundaries.
   - Use existing logs, stack traces, diffs, configuration, and runtime output as evidence.
   - Do not run destructive commands or modify user data while investigating.

3. **Form and test hypotheses**
   - List plausible causes that fit the observed evidence.
   - Prefer checks that distinguish between hypotheses instead of broad speculative changes.
   - Trace edge cases such as missing values, invalid input, timing, retries, concurrency, permissions, and environment differences when relevant.
   - Check recent changes when the issue appears to be a regression.

4. **Identify the root cause**
   - Separate the underlying cause from downstream symptoms.
   - Point to the specific behavior, condition, or interaction responsible, and explain how it produces the failure.
   - If evidence is incomplete, state what is confirmed, what remains uncertain, and what observation would resolve it.

5. **Recommend or implement a correction**
   - Propose the smallest change that addresses the cause without hiding the symptom.
   - Consider compatibility, error handling, security, and neighboring behavior affected by the change.
   - Do not silently broaden the task into an unrelated refactor.

6. **Verify the correction**
   - When asked to make a fix, use the most relevant existing checks or a focused reproduction if verification is requested or needed to support the result.
   - Add or update regression coverage when the project has a suitable test pattern and the user asks for implementation.
   - Report exactly what was checked and what was not. Never claim a bug is fixed based only on a plausible code change.

## Response Format

For an investigation, report:

- **Observed behavior**: what fails and under what conditions.
- **Root cause**: the cause supported by the evidence, or the leading hypothesis if not confirmed.
- **Evidence**: relevant code paths, logs, or reproduction results.
- **Correction**: the smallest reliable fix or the next diagnostic step.

For an implemented fix, summarize the change and its verification. Keep the explanation direct and distinguish confirmed findings from hypotheses.

## Guardrails

- Do not invent logs, reproduction steps, user impact, or test results.
- Do not treat correlation as proof of causation.
- Do not suppress exceptions, disable validation, or add retries as a default workaround without establishing why that is safe.
- Preserve existing behavior outside the defect unless the user approves a broader change.
