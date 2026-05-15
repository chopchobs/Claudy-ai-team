---
name: 🐛 Bugfix
about: Fix a bug
labels: ["bug", "fix"]
---

# 🐛 Bugfix: [Bug Title]

## 📝 Summary

<!-- บั๊กอะไร แก้ยังไง 1-2 ประโยค -->

## 🔗 Related

- Fixes #
- Bug Report: [link]
- Severity: P0 / P1 / P2 / P3

## 🐛 Bug Description

### Symptoms

<!-- User เห็นอะไร? -->

### Affected Users

- [ ] All users
- [ ] Specific user segment:
- [ ] Edge case only

**Estimated impact:** XX% of users / requests

### When It Happens

<!-- เกิดขึ้นเมื่อไหร่ ? บ่อยแค่ไหน? -->

## 🔍 Root Cause Analysis

### What Was Wrong

<!-- ปัญหาอยู่ตรงไหน? technical detail -->

### Why It Happened

<!-- ทำไมถึงเกิด? assumption ผิด? edge case ที่ไม่ได้คิด? -->

### When It Was Introduced

- **Commit:**
- **PR:** #
- **Date:**
- **Duration in production:**

## 🔧 The Fix

### What Changed

<!-- เปลี่ยนอะไรบ้าง? -->

### Why This Approach

<!-- ทำไมเลือกแก้แบบนี้? -->

### Alternatives Considered

<!-- มีวิธีอื่นไหม? ทำไมไม่เลือก? -->

1. **Alternative A:** ... (rejected because ...)
2. **Alternative B:** ... (rejected because ...)

## 🧪 Reproduction & Verification

### Reproduction Steps (Before Fix)

1.
2.
3.

**Expected:**
**Actual (before fix):**

### Verification Steps (After Fix)

1.
2.
3.

**Result:** ✅ Bug no longer reproducible

### Test Coverage Added

- [ ] Regression test added (prevents recurrence)
- [ ] Edge case tests added
- [ ] Integration test added
- [ ] E2E test added (if user-facing)

## 📊 Impact Assessment

### Severity Justification

<!-- ทำไมเป็น P0/P1/P2/P3? -->

### Customer Impact

<!-- กระทบลูกค้ายังไง? -->

- Reports received:
- Customer support tickets:
- Revenue impact (if applicable):

## 🚨 Was a Hotfix Needed?

- [ ] Yes — bypassed normal flow
- [ ] No — normal release cycle

If yes:

- **Cherry-pick to:** branches
- **Deploy ETA:**

## 🔄 Rollout Plan

- [ ] Deploy to dev → verify
- [ ] Deploy to staging → verify
- [ ] Deploy to production
- [ ] Monitor metrics for 24 hours

## 📈 Monitoring

### What to Watch After Deploy

- [ ] Error rate for affected endpoint
- [ ] User reports / complaints
- [ ] Related metrics:

### Success Criteria

- [ ] No related errors for 7 days
- [ ] No new bug reports of same type

## 🎓 Post-Mortem (if SEV1/SEV2)

### Timeline

- **Bug introduced:**
- **First detected:**
- **Fix deployed:**
- **Total duration:**

### What Went Well

-

### What Went Wrong

-

### Action Items

- [ ]
- [ ]

## ✅ Pre-Merge Checklist

- [ ] Bug verified fixed
- [ ] Regression test added
- [ ] No new bugs introduced
- [ ] Performance not degraded
- [ ] Security not weakened
- [ ] Documentation updated (if behavior changed)
- [ ] Reviewed by Code Review Agent
- [ ] Reviewed by QA Agent

## 🤖 Claudy Agent Notes

**QA Verdict:** PASS / FAIL
**Code Review:** APPROVED / CHANGES_REQUESTED
**Regression Test Coverage:** ✅ Added

---

**🌟 Squashed with Claudy AI Team**
