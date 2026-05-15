---
name: ♻️ Refactor
about: Code improvement without behavior change
labels: ["refactor", "tech-debt"]
---

# ♻️ Refactor: [What's Being Refactored]

## 📝 Summary

<!-- Refactor อะไร? เพราะอะไร? 1-2 ประโยค -->

## 🎯 Motivation

### Why Now?

<!-- ทำไมถึงต้อง refactor ตอนนี้? -->

- [ ] Blocking new feature
- [ ] Performance issue
- [ ] Maintainability concern
- [ ] Code review feedback
- [ ] Tech debt cleanup
- [ ] Standardization
- [ ] Other:

### Pain Points Being Addressed

1.
2.
3.

## 🏗️ What's Changing

### Architecture Changes

#### Before

#### After

### Files Affected

- **Renamed:**
- **Moved:**
- **Deleted:**
- **Created:**
- **Heavily modified:**

### API/Interface Changes

#### Internal APIs

<!-- Changes to internal modules/classes/functions -->

#### Public APIs (if any)

<!-- ⚠️ Breaking changes? -->

- [ ] No public API changes
- [ ] Breaking changes (see Migration Path below)
- [ ] Backward-compatible additions

## ✅ Behavior Preservation

### Functional Equivalence

<!-- พิสูจน์ว่าพฤติกรรมเหมือนเดิม -->

- [ ] All existing tests still pass
- [ ] Manual testing confirms same behavior
- [ ] Performance benchmarks comparable
- [ ] No user-visible changes

### Test Strategy

- [ ] Existing tests cover the refactor
- [ ] Added characterization tests (locked existing behavior)
- [ ] Added tests for previously untested paths
- [ ] Property-based tests (if applicable)

## 📊 Metrics

### Code Quality

| Metric                | Before | After | Change |
| --------------------- | ------ | ----- | ------ |
| Lines of code         |        |       |        |
| Cyclomatic complexity |        |       |        |
| Test coverage         |        |       |        |
| Type coverage         |        |       |        |
| Bundle size           |        |       |        |

### Performance (if applicable)

| Metric              | Before | After | Change |
| ------------------- | ------ | ----- | ------ |
| Response time (P95) |        |       |        |
| Memory usage        |        |       |        |
| CPU usage           |        |       |        |

## 🎓 Lessons / Patterns Introduced

### New Patterns

<!-- มีแบบไหนใหม่ที่ทีมจะใช้ต่อ? -->

1.
2.

### Anti-patterns Removed

<!-- ลบ anti-pattern อะไรไป? -->

1.
2.

## 🚨 Risks

### What Could Go Wrong?

1. **Risk:**
   - **Mitigation:**
2. **Risk:**
   - **Mitigation:**

### Rollback Plan

<!-- ถ้าพังจะทำยังไง? -->

## 🛣️ Migration Path (if breaking)

### For Internal Code

```typescript
// Before
oldFunction(arg1, arg2);

// After
newFunction({ arg1, arg2 });
```

### For External Consumers (if applicable)

#### Deprecation Timeline

- **v1.5:** New API added, old marked deprecated
- **v2.0:** Old API removed
- **Migration guide:** [link]

## 📚 Documentation Updates

- [ ] Architecture docs updated
- [ ] Code comments updated
- [ ] README updated
- [ ] ADR created (if significant decision)
- [ ] Migration guide written (if breaking)

## ✅ Pre-Merge Checklist

### Verification

- [ ] All existing tests pass
- [ ] No behavior changes (or breaking changes documented)
- [ ] Performance not degraded
- [ ] No new dependencies introduced unnecessarily

### Quality

- [ ] Code review passed
- [ ] Patterns consistent with codebase
- [ ] No "improvement opportunities" left for future

### Documentation

- [ ] Reasoning documented in PR
- [ ] ADR created if architectural decision

## 🤖 Claudy Agent Notes

**Code Review Verdict:** APPROVED / CHANGES_REQUESTED
**Patterns Suggested:**
**Tech Debt Reduced:**

---

**🌟 Cleaned up with Claudy AI Team**
