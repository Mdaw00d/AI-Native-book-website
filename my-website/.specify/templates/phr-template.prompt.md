---
id: "{{ID}}"
title: "{{TITLE}}"
stage: "{{STAGE}}"
date: "{{DATE_ISO}}"
surface: "{{SURFACE}}"
model: "{{MODEL}}"
feature: "{{FEATURE}}"
branch: "{{BRANCH}}"
user: "{{USER}}"
command: "{{COMMAND}}"
labels: {{LABELS_YAML}}
links:
  spec: {{SPEC_LINK}}
  ticket: {{TICKET_LINK}}
  adr: {{ADR_LINK}}
  pr: {{PR_LINK}}
files: {{FILES_YAML}}
tests: {{TESTS_YAML}}
---

# Prompt History Record: {{TITLE}}

## Context

**Stage:** {{STAGE}}
**Feature:** {{FEATURE}}
**Command:** {{COMMAND}}
**Model:** {{MODEL}}
**Date:** {{DATE_ISO}}

## User Prompt

```text
{{PROMPT_TEXT}}
```

## Assistant Response

### Summary

{{RESPONSE_SUMMARY}}

### Key Actions Taken

{{RESPONSE_ACTIONS}}

### Files Modified

{{FILES_YAML}}

### Tests Run/Created

{{TESTS_YAML}}

## Outcome

**Status:** {{OUTCOME_STATUS}}

**Result:**
{{OUTCOME_RESULT}}

## Evaluation

**Effectiveness:** {{EVAL_EFFECTIVENESS}}

**Constitution Alignment:** {{EVAL_CONSTITUTION}}

**Lessons Learned:**
{{EVAL_LESSONS}}

## Follow-Up

**Next Steps:**
{{FOLLOWUP_STEPS}}

**Blockers:**
{{FOLLOWUP_BLOCKERS}}

**Related Records:**
{{FOLLOWUP_RELATED}}

---

**Record ID:** {{ID}}
**Created:** {{DATE_ISO}}
**Surface:** {{SURFACE}}
