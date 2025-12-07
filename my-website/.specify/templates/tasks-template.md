# Tasks: [FEATURE_NAME]

**Spec:** `specs/[feature-name]/spec.md`
**Plan:** `specs/[feature-name]/plan.md`
**Generated:** [YYYY-MM-DD]
**Status:** [NOT_STARTED | IN_PROGRESS | COMPLETED]

## Task Execution Order

Tasks are dependency-ordered. Complete in sequence unless explicitly marked parallel.

---

## Phase 1: [Phase Name]

### Task 1.1: [Task Title]

**ID:** T-001
**Type:** [Setup | Implementation | Testing | Documentation]
**Dependencies:** None
**Estimated Complexity:** [Low | Medium | High]

**Description:**
[Clear, actionable description of what needs to be done]

**Acceptance Criteria:**
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Files to Modify:**
- `[path/to/file1.ts]` - [What changes]
- `[path/to/file2.md]` - [What changes]

**Test Cases:**
```typescript
// Test case 1
describe('[Feature]', () => {
  it('should [expected behavior]', () => {
    // Arrange
    // Act
    // Assert
  });
});
```

**Constitution Check:**
- [ ] Meets Educational Excellence (clear, accurate, pedagogical)
- [ ] Accessibility compliant (keyboard nav, ARIA labels)
- [ ] Performance impact assessed (bundle size, load time)

**Notes:**
[Any additional context, gotchas, or references]

---

### Task 1.2: [Task Title]

**ID:** T-002
**Type:** [Setup | Implementation | Testing | Documentation]
**Dependencies:** T-001
**Estimated Complexity:** [Low | Medium | High]

**Description:**
[Clear, actionable description]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Files to Modify:**
- `[path/to/file.ts]` - [What changes]

**Test Cases:**
```typescript
// Test specifications
```

**Constitution Check:**
- [ ] [Principle 1 check]
- [ ] [Principle 2 check]

---

## Phase 2: [Phase Name]

### Task 2.1: [Task Title]

**ID:** T-003
**Type:** [Setup | Implementation | Testing | Documentation]
**Dependencies:** T-002
**Estimated Complexity:** [Low | Medium | High]

[Follow same structure as above]

---

## Cross-Cutting Tasks

### Task X.1: Documentation Update

**ID:** T-XXX
**Type:** Documentation
**Dependencies:** All implementation tasks complete
**Estimated Complexity:** Low

**Description:**
Update all documentation to reflect new feature, including README, tutorials, and
API references.

**Acceptance Criteria:**
- [ ] README.md updated with new feature description
- [ ] Tutorial created/updated in `docs/`
- [ ] Code examples tested and verified
- [ ] Changelog updated
- [ ] Migration guide created (if breaking changes)

**Files to Modify:**
- `README.md`
- `docs/[module]/[feature].md`
- `CHANGELOG.md`

---

### Task X.2: Accessibility Audit

**ID:** T-XXX
**Type:** Testing
**Dependencies:** All UI implementation tasks complete
**Estimated Complexity:** Medium

**Description:**
Comprehensive accessibility testing across browsers and assistive technologies.

**Acceptance Criteria:**
- [ ] WCAG 2.1 Level AA compliance verified
- [ ] Keyboard navigation tested (Tab, Enter, Escape, Arrow keys)
- [ ] Screen reader tested (NVDA on Windows, VoiceOver on macOS)
- [ ] Color contrast verified (4.5:1 for normal text, 3:1 for large text)
- [ ] Focus indicators visible and logical order
- [ ] ARIA labels present and accurate
- [ ] Automated axe-core scan passes
- [ ] Manual testing checklist completed

**Tools:**
- axe DevTools
- WAVE browser extension
- Lighthouse accessibility audit
- Manual keyboard testing
- Screen reader testing

---

### Task X.3: Performance Validation

**ID:** T-XXX
**Type:** Testing
**Dependencies:** All implementation tasks complete
**Estimated Complexity:** Medium

**Description:**
Validate performance metrics meet constitution requirements.

**Acceptance Criteria:**
- [ ] Lighthouse Performance score > 90
- [ ] Page load < 3s on 3G connection
- [ ] Bundle size increase < [X]KB
- [ ] No console errors in production build
- [ ] Images optimized (WebP/AVIF)
- [ ] Code splitting implemented where appropriate
- [ ] Critical CSS inlined

**Metrics to Capture:**
- First Contentful Paint (FCP)
- Largest Contentful Paint (LCP)
- Cumulative Layout Shift (CLS)
- Time to Interactive (TTI)
- Total Blocking Time (TBT)

---

### Task X.4: Security & Privacy Review

**ID:** T-XXX
**Type:** Testing
**Dependencies:** All implementation tasks complete
**Estimated Complexity:** Low

**Description:**
Ensure security and privacy requirements met.

**Acceptance Criteria:**
- [ ] No PII collected without explicit consent
- [ ] External links validated and marked
- [ ] Dependencies scanned for vulnerabilities (`npm audit`)
- [ ] No hardcoded secrets or API keys
- [ ] Content Security Policy configured
- [ ] HTTPS enforced
- [ ] Privacy policy updated (if data collection added)

---

## Rollback Plan

**Trigger Conditions:**
- [Condition that would require rollback]
- [Critical failure scenario]

**Rollback Steps:**
1. [Step 1: Immediate action]
2. [Step 2: Revert procedure]
3. [Step 3: Validation]
4. [Step 4: Communication]

**Recovery Time Objective:** [X minutes/hours]

---

## Task Summary

| Phase | Task Count | Completed | Status |
|-------|------------|-----------|--------|
| Phase 1 | [X] | 0 | Not Started |
| Phase 2 | [X] | 0 | Not Started |
| Cross-Cutting | [X] | 0 | Not Started |
| **Total** | **[X]** | **0** | **0%** |

---

## Progress Tracking

**Last Updated:** [YYYY-MM-DD]

**Current Phase:** [Phase X]

**Blocked Tasks:** None

**Next Up:**
1. T-001: [Task title]
2. T-002: [Task title]

**Notes:**
[Any blockers, risks, or updates]

---

**Constitution Check:** ✅ All tasks aligned with v1.0.0
**Review Status:** [DRAFT | APPROVED]
