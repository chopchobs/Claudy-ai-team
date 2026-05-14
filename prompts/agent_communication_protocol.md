# 📡 Agent Communication Protocol (ACP)
## โปรโตคอลสื่อสารระหว่าง AI Agents ในทีม

> **Version:** 1.0
> **Last Updated:** 2026-05-12
> **Scope:** ทุก Agent ในระบบ Claudy Orchestration

---

## 📖 TABLE OF CONTENTS

1. [Overview](#overview)
2. [Message Format Standard](#message-format)
3. [Task Lifecycle](#task-lifecycle)
4. [Communication Patterns](#communication-patterns)
5. [Handoff Protocol](#handoff-protocol)
6. [Status Reporting](#status-reporting)
7. [Error Handling](#error-handling)
8. [Iteration & Feedback Loop](#iteration)
9. [Data Schema](#data-schema)
10. [Priority & SLA](#priority-sla)
11. [Conflict Resolution](#conflict-resolution)
12. [Audit & Logging](#audit-logging)

---

## 🎯 OVERVIEW

### หลักการพื้นฐาน

```
┌─────────────────────────────────────────────────┐
│  1. STRUCTURED — ทุก message มี schema ชัดเจน    │
│  2. STATEFUL  — ทุก task ติดตาม state ได้         │
│  3. TRACEABLE — ทุก action ย้อนรอยได้             │
│  4. ASYNC     — Default เป็น non-blocking         │
│  5. IDEMPOTENT — Retry ได้โดยไม่เกิด side effect  │
│  6. CONTEXTUAL — ส่ง context พอ ไม่มาก ไม่น้อย     │
└─────────────────────────────────────────────────┘
```

### Communication Topology

```
                   ┌──────────┐
                   │   DEV    │
                   └─────┬────┘
                         │
                         ▼
                   ┌──────────┐
            ┌──────│  CLAUDY  │──────┐
            │      └────┬─────┘      │
            │           │            │
       ┌────▼───┐  ┌────▼───┐  ┌────▼───┐
       │ Agent  │  │ Agent  │  │ Agent  │
       │   A    │◄─┤   B    │─►│   C    │
       └────────┘  └────────┘  └────────┘
       
       Solid line: Direct command (Claudy → Agent)
       Dashed line: Agent-to-Agent (ต้องผ่าน Claudy)
```

**กฎสำคัญ:**
- 🚫 Agent ห้ามคุยกันตรงๆ
- ✅ ทุกการสื่อสารผ่าน Claudy
- ✅ Claudy เป็น single source of truth สำหรับสถานะ

---

## 📨 MESSAGE FORMAT STANDARD

### Message Envelope (โครงสร้างกลาง)

```yaml
message:
  # ─── Header ───
  id: msg_2N4kJxLm9pQ              # Unique message ID
  type: TASK_ASSIGN                # Message type (ดูตาราง)
  version: "1.0"                   # Protocol version
  timestamp: 2026-05-12T10:30:00Z  # ISO 8601 UTC
  
  # ─── Routing ───
  from: claudy                     # Sender
  to: backend_agent                # Receiver
  conversation_id: conv_abc123     # เชื่อมโยง messages ที่เกี่ยวข้อง
  parent_message_id: msg_prev_xyz  # อ้างถึง message ที่ตอบ
  
  # ─── Priority ───
  priority: P1                     # P0 / P1 / P2 / P3
  deadline: 2026-05-12T12:00:00Z   # Optional
  
  # ─── Payload ───
  payload:
    # Content ขึ้นกับ message type
    
  # ─── Metadata ───
  metadata:
    task_id: task_chk_001          # Reference ไปยัง task
    project: ecommerce-v2
    correlation_id: req_456        # สำหรับ tracing
    tags: [feature, urgent]
```

### Message Types

| Type | จาก → ถึง | วัตถุประสงค์ |
|------|----------|--------------|
| `TASK_ASSIGN` | Claudy → Agent | มอบหมายงานใหม่ |
| `TASK_ACCEPT` | Agent → Claudy | ตอบรับงาน |
| `TASK_REJECT` | Agent → Claudy | ปฏิเสธงาน (พร้อมเหตุผล) |
| `STATUS_UPDATE` | Agent → Claudy | รายงานความคืบหน้า |
| `INFO_REQUEST` | Agent → Claudy | ขอข้อมูลเพิ่ม |
| `INFO_PROVIDE` | Claudy → Agent | ส่งข้อมูลให้ |
| `HANDOFF_REQUEST` | Agent → Claudy | ขอส่งต่อให้ Agent อื่น |
| `DEPENDENCY_REQUEST` | Agent → Claudy | ขอ output จาก Agent อื่น |
| `RESULT_SUBMIT` | Agent → Claudy | ส่งผลงาน |
| `RESULT_ACCEPT` | Claudy → Agent | รับงาน (ผ่าน) |
| `RESULT_REJECT` | Claudy → Agent | ขอแก้ไข |
| `ERROR_REPORT` | Agent → Claudy | แจ้งข้อผิดพลาด |
| `BLOCKER_ALERT` | Agent → Claudy | แจ้ง blocker |
| `CONSULT_REQUEST` | Agent → Claudy | ขอปรึกษา |
| `ABORT_REQUEST` | Claudy → Agent | ยกเลิกงาน |

---

## 🔄 TASK LIFECYCLE

### State Machine

```
                    ┌─────────────┐
                    │   CREATED   │
                    └──────┬──────┘
                           │ TASK_ASSIGN
                           ▼
                    ┌─────────────┐
                    │  ASSIGNED   │
                    └──────┬──────┘
                           │ TASK_ACCEPT
                           ▼
                    ┌─────────────┐
              ┌────►│ IN_PROGRESS │◄────┐
              │     └──────┬──────┘     │
              │            │            │
              │  INFO_     │  STATUS_   │ DEPENDENCY_
              │  REQUEST   │  UPDATE    │ REQUEST
              │            │            │
              │            ▼            │
              │     ┌─────────────┐     │
              └─────┤  WAITING    ├─────┘
                    └──────┬──────┘
                           │ RESULT_SUBMIT
                           ▼
                    ┌─────────────┐
                    │  IN_REVIEW  │
                    └──────┬──────┘
                           │
              ┌────────────┴────────────┐
              │ RESULT_ACCEPT           │ RESULT_REJECT
              ▼                         ▼
       ┌─────────────┐           ┌─────────────┐
       │  COMPLETED  │           │   REVISION  │
       └─────────────┘           └──────┬──────┘
                                        │
                                        └──► IN_PROGRESS
                                        
       ┌─────────────┐
       │   FAILED    │ ◄── ERROR_REPORT / ABORT
       └─────────────┘
```

### State Definitions

| State | คำอธิบาย | Next Possible |
|-------|---------|---------------|
| `CREATED` | Task ถูกสร้างแต่ยังไม่ assign | ASSIGNED |
| `ASSIGNED` | Assign แล้วรอ accept | IN_PROGRESS / FAILED |
| `IN_PROGRESS` | Agent กำลังทำงาน | WAITING / IN_REVIEW / FAILED |
| `WAITING` | รอ input / dependency | IN_PROGRESS / FAILED |
| `IN_REVIEW` | ส่งงานแล้วรอ review | COMPLETED / REVISION |
| `REVISION` | ต้องแก้ไข | IN_PROGRESS |
| `COMPLETED` | เสร็จสมบูรณ์ | (terminal) |
| `FAILED` | ล้มเหลว | (terminal) |

---

## 📋 MESSAGE PAYLOADS

### 1. TASK_ASSIGN (Claudy → Agent)

```yaml
type: TASK_ASSIGN
from: claudy
to: backend_agent
priority: P1
payload:
  task_id: task_chk_001
  title: "สร้าง Order Checkout API"
  
  description: |
    สร้าง POST /api/v1/orders ที่รองรับ:
    - Multiple items
    - Inventory check
    - Payment integration
    - Idempotency
  
  context:
    project: ecommerce-v2
    related_tickets: [JIRA-1234]
    existing_code:
      - path: src/modules/orders/
      - description: "module ที่มีอยู่ — ต่อยอด ไม่สร้างใหม่"
    architecture_decisions:
      - "ใช้ Saga pattern สำหรับ distributed transaction"
      - "Event-driven via Kafka"
  
  inputs:
    - type: schema
      content: { ... }
    - type: file
      path: docs/api-spec.yaml
    - type: reference
      url: https://stripe.com/docs/idempotency
  
  expected_output:
    format: code + tests + api_doc
    deliverables:
      - "Working API endpoint"
      - "Unit tests (coverage > 80%)"
      - "OpenAPI spec update"
      - "PR description"
    location: feature/order-checkout branch
  
  success_criteria:
    - "API ทำงานตาม spec"
    - "Test coverage > 80%"
    - "ผ่าน lint และ type check"
    - "มี idempotency key support"
    - "Error handling ครบทุก case"
  
  constraints:
    - "ห้ามใช้ deprecated lib X"
    - "Response time < 300ms (P95)"
    - "Backward compatible กับ v1"
  
  dependencies:
    waiting_for: 
      - { agent: database_agent, task: task_db_001, output: schema }
    provides_to:
      - { agent: frontend_agent, output: api_contract }
      - { agent: qa_agent, output: endpoint_for_testing }
  
  deadline: 2026-05-12T16:00:00Z
  estimated_effort: 3h
```

### 2. TASK_ACCEPT (Agent → Claudy)

```yaml
type: TASK_ACCEPT
from: backend_agent
to: claudy
parent_message_id: msg_assign_001
payload:
  task_id: task_chk_001
  status: ACCEPTED
  
  acknowledgment: |
    รับทราบ task สร้าง Order Checkout API
    เข้าใจ requirement และ constraint ทั้งหมด
  
  plan:
    approach: |
      1. ออกแบบ controller + service layer
      2. Implement business logic ตาม Saga pattern
      3. เพิ่ม idempotency middleware
      4. Integration test กับ payment service
      5. เขียน unit test
  
  estimated_completion: 2026-05-12T15:30:00Z
  
  questions: []  # ถ้ามีข้อสงสัย ใส่ใน INFO_REQUEST แยก
  
  assumptions:
    - "ใช้ Stripe เป็น payment provider (ตามที่ระบุ)"
    - "Idempotency key มาจาก client (header X-Idempotency-Key)"
```

### 3. STATUS_UPDATE (Agent → Claudy)

```yaml
type: STATUS_UPDATE
from: backend_agent
to: claudy
payload:
  task_id: task_chk_001
  state: IN_PROGRESS
  progress_percent: 65
  
  completed:
    - "Controller scaffolding"
    - "Order creation logic"
    - "Idempotency middleware"
  
  current:
    - "Integration test"
  
  pending:
    - "Payment integration"
    - "Error scenarios"
  
  blockers: []
  
  notes: |
    Payment integration ต้องการ API key จาก Stripe
    จะใช้ test mode ไปก่อน
  
  eta: 2026-05-12T15:30:00Z
```

### 4. INFO_REQUEST (Agent → Claudy)

```yaml
type: INFO_REQUEST
from: backend_agent
to: claudy
priority: P1  # blocking task
payload:
  task_id: task_chk_001
  request_type: clarification
  
  questions:
    - id: q1
      question: "Idempotency key timeout ต้องการกี่ชั่วโมง?"
      options:
        - "24 ชั่วโมง (default ของ Stripe)"
        - "48 ชั่วโมง"
        - "Custom (โปรดระบุ)"
      default_assumption: "24 ชั่วโมง"
    
    - id: q2
      question: "ถ้า payment fail ต้อง rollback order หรือเก็บเป็น failed state?"
      blocking: true
  
  impact_if_no_answer: |
    จะใช้ default และ flag เป็น assumption
    Dev อาจต้องตรวจสอบและแก้ภายหลัง
  
  required_by: 2026-05-12T14:00:00Z
```

### 5. RESULT_SUBMIT (Agent → Claudy)

```yaml
type: RESULT_SUBMIT
from: backend_agent
to: claudy
payload:
  task_id: task_chk_001
  state: IN_REVIEW
  
  summary: |
    สร้าง Order Checkout API เสร็จเรียบร้อย
    รองรับ idempotency, payment integration, error handling
  
  deliverables:
    - type: code
      path: src/modules/orders/
      files_changed: 12
      lines_added: 847
      lines_removed: 132
    
    - type: test
      path: src/modules/orders/__tests__/
      coverage: 87.3
      test_count: 24
      passing: 24
    
    - type: documentation
      path: docs/api/orders.md
      format: openapi
    
    - type: pr
      url: https://github.com/example/repo/pull/234
      title: "feat: add order checkout API"
  
  success_criteria_met:
    - { criterion: "API ทำงานตาม spec", met: true }
    - { criterion: "Coverage > 80%", met: true, actual: "87.3%" }
    - { criterion: "Pass lint & type", met: true }
    - { criterion: "Idempotency support", met: true }
    - { criterion: "Error handling ครบ", met: true }
  
  decisions_made:
    - decision: "ใช้ Saga pattern with compensation"
      rationale: "ตาม architecture decision และเหมาะกับ distributed nature"
    - decision: "Idempotency timeout = 24h"
      rationale: "Default ของ Stripe และเหมาะกับ business case"
  
  assumptions:
    - "User authentication อยู่ใน middleware แล้ว (ใช้ req.user)"
  
  known_limitations:
    - "ยังไม่ support partial refund (ต้องเพิ่มใน next iteration)"
  
  recommended_next:
    - agent: code_review_agent
      action: "Review โค้ดเชิง quality"
    - agent: qa_agent
      action: "Test API ด้วย scenarios"
    - agent: security_agent
      action: "Audit security (เพราะเกี่ยว payment)"
  
  metrics:
    actual_effort: 2h 45m
    estimated_effort: 3h
    variance: -8.3%
```

### 6. RESULT_REJECT (Claudy → Agent)

```yaml
type: RESULT_REJECT
from: claudy
to: backend_agent
parent_message_id: msg_result_001
payload:
  task_id: task_chk_001
  state: REVISION
  
  feedback_from:
    - code_review_agent
    - security_agent
  
  required_changes:
    - severity: BLOCKER
      source: security_agent
      issue: "Card number ถูก log ใน application log"
      file: src/modules/orders/payment.service.ts:142
      fix: "ใช้ card.last4 แทน card.number"
    
    - severity: HIGH
      source: code_review_agent
      issue: "Race condition ใน handleSubmit"
      file: src/modules/orders/checkout.controller.ts:67
      fix: "เพิ่ม mutex หรือ optimistic locking"
  
  optional_improvements:
    - severity: SUGGESTION
      issue: "Extract magic number"
      file: src/modules/orders/checkout.controller.ts:23
  
  re_submit_by: 2026-05-12T17:00:00Z
```

### 7. BLOCKER_ALERT (Agent → Claudy)

```yaml
type: BLOCKER_ALERT
from: backend_agent
to: claudy
priority: P0  # ต้องการความสนใจทันที
payload:
  task_id: task_chk_001
  state: WAITING
  
  blocker_type: external_dependency
  
  description: |
    Stripe API ตอบกลับ 503 อย่างต่อเนื่อง
    ทำให้ test integration ไม่ผ่าน
  
  impact:
    - "ทำงานต่อไม่ได้ใน 30 นาทีที่ผ่านมา"
    - "ETA จะ delay 1-2 ชั่วโมง"
  
  attempts:
    - "Retry 5 ครั้ง — ยัง 503"
    - "เช็ค Stripe status page — มี incident กำลังแก้"
  
  options:
    a: "รอ Stripe กลับมาทำงาน (~ETA ไม่ชัด)"
    b: "Mock Stripe response สำหรับ test"
    c: "ทำส่วนอื่นต่อ ค่อย integrate ทีหลัง"
  
  recommendation: "b — Mock เพื่อ unblock"
  
  needs_decision_by: 2026-05-12T14:30:00Z
```

### 8. ERROR_REPORT (Agent → Claudy)

```yaml
type: ERROR_REPORT
from: backend_agent
to: claudy
priority: P0
payload:
  task_id: task_chk_001
  state: FAILED  # หรือ IN_PROGRESS ถ้ายังกู้ได้
  
  error_type: requirement_conflict
  
  description: |
    Requirement บอกให้ใช้ Saga pattern
    แต่ schema จาก Database Agent ไม่รองรับ compensation table
  
  details:
    - "Order table ไม่มี state column สำหรับ track saga step"
    - "ไม่มี outbox table สำหรับ event publishing"
  
  evidence:
    - file: db/schema.prisma
      issue: "Missing compensation tracking"
  
  attempted_solutions:
    - "ลองใช้ JSON column เก็บ saga state — ไม่ scalable"
  
  request: |
    ขอประสานงานกับ Database Agent เพื่อ:
    1. เพิ่ม `saga_state` column ใน orders
    2. สร้าง `event_outbox` table
  
  blocking_until_resolved: true
```

---

## 🤝 HANDOFF PROTOCOL

### Pattern 1: Sequential Handoff (ส่งต่อตาม flow)

```
Claudy:
  ├─ Step 1: Database Agent → ออกแบบ schema
  │   ├─ Output: schema.prisma + ERD
  │   └─ Status: COMPLETED
  │
  ├─ Step 2: Backend Agent → implement API
  │   ├─ Input from Step 1: schema
  │   ├─ Output: API code + tests
  │   └─ Status: COMPLETED
  │
  └─ Step 3: Frontend Agent → consume API
      ├─ Input from Step 2: API contract
      └─ Status: IN_PROGRESS
```

**Handoff Message Format:**

```yaml
type: TASK_ASSIGN
from: claudy
to: backend_agent
payload:
  task_id: task_chk_002
  
  prerequisite_outputs:
    - source_task: task_db_001
      source_agent: database_agent
      output_type: schema
      content:
        location: db/schema.prisma
        summary: "Order schema with saga support"
        key_decisions:
          - "ใช้ UUID เป็น PK"
          - "Soft delete via deleted_at"
  
  # ... rest of task assignment
```

### Pattern 2: Parallel Execution (ทำขนาน)

```
Claudy:
  │
  ├─ Branch A: Backend Agent (independent)
  │   └─ Status: IN_PROGRESS
  │
  ├─ Branch B: Database Agent (independent)
  │   └─ Status: IN_PROGRESS
  │
  └─ Branch C: Frontend Agent (waits for A & B)
      └─ Status: WAITING
```

**Coordination Message:**

```yaml
type: TASK_ASSIGN
from: claudy
to: frontend_agent
payload:
  task_id: task_fe_001
  state: ASSIGNED_PENDING_DEPENDENCIES
  
  dependencies:
    - task_id: task_be_001
      agent: backend_agent
      required_output: api_contract
      status: IN_PROGRESS
      eta: 2026-05-12T15:00:00Z
    
    - task_id: task_db_001
      agent: database_agent
      required_output: schema
      status: COMPLETED  # ✅
  
  start_when: "all_dependencies_completed"
```

### Pattern 3: Cross-Review (ขอ Agent อื่นช่วย review)

```
Backend Agent (เสร็จงาน)
   ↓ RESULT_SUBMIT
Claudy
   ↓ TASK_ASSIGN (review request)
   ├─→ Code Review Agent
   ├─→ Security Agent  
   └─→ QA Agent
   
ทั้ง 3 Agents ส่ง RESULT_SUBMIT กลับ
   ↓
Claudy รวม feedback
   ↓
ส่ง RESULT_ACCEPT หรือ RESULT_REJECT กลับ Backend Agent
```

### Pattern 4: Consultation (ขอคำปรึกษาแต่ไม่ส่งต่อ)

```yaml
type: CONSULT_REQUEST
from: backend_agent
to: claudy
payload:
  task_id: task_chk_001
  consult_with: research_agent
  
  question: |
    ระหว่าง Saga และ Two-phase commit
    อันไหนเหมาะกับ use case นี้?
  
  context:
    - "Microservices architecture"
    - "Eventual consistency acceptable"
    - "Need to rollback on failure"
  
  expect_back: recommendation_with_rationale
  blocking: false  # ทำงานต่อได้ระหว่างรอ
```

Claudy จะส่งต่อให้ Research Agent แล้วคืนคำตอบให้ Backend Agent

---

## 📊 STATUS REPORTING

### Reporting Frequency

| Task Duration | Update Frequency |
|--------------|------------------|
| < 30 minutes | เมื่อเสร็จ |
| 30 min - 2 hours | ทุก 30-60 นาที |
| 2-8 hours | ทุก 1-2 ชั่วโมง |
| > 8 hours | ทุก 2-4 ชั่วโมง + milestone |

### Status Indicators

```yaml
state_indicators:
  🟢 ON_TRACK:
    description: "ตามแผน"
    progress_vs_eta: "within ±10%"
  
  🟡 AT_RISK:
    description: "อาจ delay"
    progress_vs_eta: "10-25% behind"
    action: "แจ้ง Claudy + mitigation plan"
  
  🔴 DELAYED:
    description: "delay แน่นอน"
    progress_vs_eta: "> 25% behind"
    action: "BLOCKER_ALERT + re-estimate"
  
  ⚪ BLOCKED:
    description: "ติดปัญหา"
    action: "BLOCKER_ALERT ทันที"
  
  ✅ COMPLETED:
    description: "เสร็จ พร้อม review"
    action: "RESULT_SUBMIT"
```

### Dashboard View (สำหรับ Claudy track)

```
┌─────────────────────────────────────────────────────┐
│ TASK BOARD                              2026-05-12   │
├─────────────────────────────────────────────────────┤
│                                                       │
│ 🟢 task_db_001 │ Database Agent   │ ████████░░ 80%  │
│ 🟢 task_be_001 │ Backend Agent    │ ██████░░░░ 60%  │
│ 🟡 task_fe_001 │ Frontend Agent   │ ████░░░░░░ 40%  │
│ ⚪ task_qa_001 │ QA Agent         │ ░░░░░░░░░░  0%  │
│ ✅ task_rs_001 │ Research Agent   │ ██████████ ✓    │
│                                                       │
│ ⚠️  Alerts:                                          │
│ • task_fe_001 อาจ delay 1 ชั่วโมง                    │
│                                                       │
└─────────────────────────────────────────────────────┘
```

---

## 🚨 ERROR HANDLING

### Error Categories

| Type | ความหมาย | Recovery |
|------|---------|----------|
| `REQUIREMENT_AMBIGUOUS` | Requirement ไม่ชัด | INFO_REQUEST |
| `REQUIREMENT_CONFLICT` | Requirement ขัดกัน | ESCALATE |
| `DEPENDENCY_MISSING` | ขาด input จาก Agent อื่น | DEPENDENCY_REQUEST |
| `DEPENDENCY_FAILED` | Agent อื่นทำไม่ได้ | RE-PLAN |
| `EXTERNAL_FAILURE` | Third-party ล่ม | RETRY / BLOCKER_ALERT |
| `RESOURCE_EXHAUSTED` | Token / time หมด | SPLIT_TASK |
| `OUT_OF_SCOPE` | งานเกินขอบเขต Agent | HANDOFF_REQUEST |
| `TECHNICAL_FAILURE` | Tool / library พัง | ERROR_REPORT |

### Retry Strategy

```yaml
retry_policy:
  transient_errors:
    max_attempts: 3
    backoff: exponential
    initial_delay: 5s
    examples:
      - "Network timeout"
      - "Rate limit (with backoff)"
      - "Temporary service unavailable"
  
  permanent_errors:
    max_attempts: 1
    action: ERROR_REPORT
    examples:
      - "Invalid credentials"
      - "Resource not found"
      - "Permission denied"
  
  ambiguous_errors:
    max_attempts: 2
    then: ESCALATE
    examples:
      - "Validation failed (unclear)"
      - "Logic conflict"
```

### Error Escalation Path

```
Level 1: Agent retry automatically (transient)
   ↓ ถ้าไม่ได้
Level 2: Agent → Claudy (ERROR_REPORT)
   ↓ Claudy พยายามแก้ (เช่น ส่งให้ Agent อื่น)
Level 3: Claudy → Dev (ESCALATION)
   ↓ Dev ตัดสินใจ
```

---

## 🔄 ITERATION & FEEDBACK LOOP

### Revision Cycle

```
┌──────────────────────────────────────────┐
│ Agent submits result (Round 1)          │
│   ↓                                      │
│ Reviewers feedback                       │
│   ↓                                      │
│ Claudy aggregates feedback               │
│   ↓                                      │
│ ┌─ Approved ─→ COMPLETED                 │
│ └─ Changes Needed                        │
│     ↓                                    │
│     Agent revises (Round 2)              │
│     ↓                                    │
│     [Loop until approved หรือ max round] │
└──────────────────────────────────────────┘
```

### Iteration Limits

```yaml
iteration_policy:
  max_revisions: 3
  
  when_max_reached:
    action: ESCALATE_TO_DEV
    reason: "Agent ไม่สามารถ deliver ตาม requirement ได้"
    
    options_for_dev:
      - "Relax requirement"
      - "เปลี่ยน Agent ที่ทำ task นี้"
      - "Break task เป็นชิ้นเล็กลง"
      - "Manual override"
```

### Revision Message

```yaml
type: RESULT_REJECT
from: claudy
to: backend_agent
payload:
  task_id: task_chk_001
  revision_round: 2
  max_rounds: 3
  
  consolidated_feedback:
    must_fix:
      - { source: security_agent, ... }
    should_fix:
      - { source: code_review_agent, ... }
    nice_to_have:
      - { source: code_review_agent, ... }
  
  re_submit_by: 2026-05-12T18:00:00Z
  
  note: |
    Round 2/3 — ถ้ายังไม่ผ่านจะต้อง escalate ให้ Dev
```

---

## 📦 DATA SCHEMA

### Core Entities

```typescript
// ─── Task ───
interface Task {
  id: string;                    // task_xxx
  title: string;
  description: string;
  state: TaskState;
  priority: Priority;
  
  assigned_to: AgentId;
  created_by: 'claudy';
  
  created_at: ISO8601;
  assigned_at?: ISO8601;
  started_at?: ISO8601;
  completed_at?: ISO8601;
  deadline?: ISO8601;
  
  estimated_effort: Duration;
  actual_effort?: Duration;
  
  inputs: TaskInput[];
  expected_output: OutputSpec;
  success_criteria: string[];
  constraints: string[];
  
  dependencies: {
    waiting_for: TaskDependency[];
    provides_to: TaskDependency[];
  };
  
  revision_round: number;
  max_revisions: number;
  
  parent_task?: string;           // สำหรับ sub-task
  conversation_id: string;
  
  tags: string[];
}

type TaskState = 
  | 'CREATED' 
  | 'ASSIGNED' 
  | 'IN_PROGRESS' 
  | 'WAITING' 
  | 'IN_REVIEW' 
  | 'REVISION' 
  | 'COMPLETED' 
  | 'FAILED';

type Priority = 'P0' | 'P1' | 'P2' | 'P3';

type AgentId = 
  | 'claudy'
  | 'frontend_agent'
  | 'backend_agent'
  | 'database_agent'
  | 'devops_agent'
  | 'qa_agent'
  | 'security_agent'
  | 'code_review_agent'
  | 'docs_writer_agent'
  | 'research_agent';

// ─── Message ───
interface Message {
  id: string;                    // msg_xxx
  type: MessageType;
  version: string;
  timestamp: ISO8601;
  
  from: AgentId;
  to: AgentId;
  conversation_id: string;
  parent_message_id?: string;
  
  priority: Priority;
  deadline?: ISO8601;
  
  payload: unknown;              // depends on type
  
  metadata: {
    task_id?: string;
    project: string;
    correlation_id?: string;
    tags?: string[];
  };
}

// ─── Deliverable ───
interface Deliverable {
  type: 'code' | 'test' | 'documentation' | 'config' | 'pr' | 'analysis';
  path?: string;
  url?: string;
  content?: string;
  metrics?: Record<string, number>;
  files_changed?: number;
  lines_added?: number;
  lines_removed?: number;
}

// ─── Feedback ───
interface Feedback {
  source: AgentId;
  severity: 'BLOCKER' | 'HIGH' | 'MEDIUM' | 'LOW' | 'SUGGESTION';
  category: 'security' | 'performance' | 'quality' | 'logic' | 'style';
  issue: string;
  location?: { file: string; line?: number };
  suggested_fix?: string;
  rationale?: string;
}
```

---

## ⚡ PRIORITY & SLA

### Priority Levels

| Priority | ใช้เมื่อ | SLA Response | SLA Resolution |
|---------|---------|--------------|----------------|
| **P0 — Critical** | Production down, data loss risk | < 5 นาที | < 1 ชั่วโมง |
| **P1 — High** | Blocking feature delivery | < 30 นาที | < 4 ชั่วโมง |
| **P2 — Medium** | Standard work | < 2 ชั่วโมง | < 1 วัน |
| **P3 — Low** | Nice-to-have, backlog | < 1 วัน | best effort |

### Priority Inheritance

```
ถ้า Task A (P1) depends on Task B (P2)
   ↓
Task B จะถูก upgrade เป็น P1 อัตโนมัติ
(blocker ของงาน priority สูงต้องเร่ง)
```

### Priority Conflict Resolution

```yaml
when: agent_has_multiple_tasks
rule: |
  1. P0 ก่อนเสมอ
  2. ถ้า priority เท่ากัน → FIFO (มาก่อนทำก่อน)
  3. ถ้า deadline ใกล้กว่า → ทำก่อน
  4. Claudy สามารถ override เพื่อ re-prioritize
```

---

## ⚖️ CONFLICT RESOLUTION

### เมื่อ Agent ให้คำตอบขัดแย้งกัน

**Example Scenario:**
```
Backend Agent: "ใช้ Redis สำหรับ cache"
Research Agent: "Memcached ดีกว่าสำหรับ use case นี้"
```

**Resolution Process:**

```
Step 1: Claudy ระบุความขัดแย้ง
   ↓
Step 2: ขอ rationale จากทั้งคู่
   ↓
Step 3: เปรียบเทียบเชิง objective:
   - Performance benchmark
   - Cost
   - Maintenance burden
   - Existing infrastructure fit
   ↓
Step 4a: ถ้าตัดสินใจได้ → Claudy decide + แจ้งทั้งคู่
Step 4b: ถ้าตัดสินใจไม่ได้ → ESCALATE ให้ Dev
```

**Conflict Resolution Message:**

```yaml
type: CONFLICT_RESOLUTION
from: claudy
to: [backend_agent, research_agent]
payload:
  conflict_id: conflict_001
  
  positions:
    - agent: backend_agent
      claim: "ใช้ Redis"
      rationale: "ทีมคุ้นเคย, มี cluster อยู่แล้ว"
    
    - agent: research_agent
      claim: "ใช้ Memcached"
      rationale: "Benchmark ดีกว่า 15% สำหรับ simple key-value"
  
  decision: redis
  
  reasoning: |
    เลือก Redis เพราะ:
    1. มี infrastructure อยู่แล้ว — ไม่เพิ่ม complexity
    2. Performance gap 15% ไม่ critical สำหรับ use case นี้
    3. Redis flexible กว่า — ถ้าอนาคตต้องการ pub/sub ก็ได้
  
  trade_offs_accepted:
    - "Performance ต่ำกว่า Memcached เล็กน้อย"
  
  action_items:
    - { agent: backend_agent, action: "ใช้ Redis ตามแผนเดิม" }
    - { agent: research_agent, action: "บันทึก rationale ใน ADR" }
```

---

## 📝 AUDIT & LOGGING

### Logging Requirements

ทุก message ต้องถูก log ในรูปแบบที่ trace ได้

```yaml
log_entry:
  timestamp: 2026-05-12T10:30:00Z
  level: INFO
  
  message_id: msg_xxx
  message_type: TASK_ASSIGN
  
  from: claudy
  to: backend_agent
  task_id: task_chk_001
  conversation_id: conv_abc123
  
  duration_ms: 142          # processing time
  
  payload_summary: |
    Task: Create Order Checkout API
    Priority: P1
    Deadline: 2026-05-12T16:00:00Z
```

### Audit Trail

ทุก task ต้องสามารถ replay ได้จาก log

```
Query: task_id = "task_chk_001"
   ↓
Returns timeline:
   10:00:00 | CREATED          | claudy
   10:00:15 | TASK_ASSIGN      | claudy → backend_agent
   10:00:18 | TASK_ACCEPT      | backend_agent → claudy
   10:30:00 | STATUS_UPDATE    | backend_agent (30%)
   11:00:00 | INFO_REQUEST     | backend_agent → claudy
   11:05:00 | INFO_PROVIDE     | claudy → backend_agent
   12:30:00 | STATUS_UPDATE    | backend_agent (75%)
   13:00:00 | RESULT_SUBMIT    | backend_agent → claudy
   13:05:00 | TASK_ASSIGN      | claudy → code_review_agent
   13:30:00 | RESULT_SUBMIT    | code_review_agent → claudy
   13:35:00 | RESULT_REJECT    | claudy → backend_agent
   14:30:00 | RESULT_SUBMIT    | backend_agent → claudy (round 2)
   14:45:00 | RESULT_ACCEPT    | claudy → backend_agent
   14:45:01 | COMPLETED
```

---

## 🎯 PROTOCOL EXAMPLES (End-to-End)

### Example 1: Simple Feature

```
Dev: "เพิ่ม API endpoint สำหรับ user profile"
   ↓
Claudy: [วิเคราะห์ + plan]
   ↓
Claudy → Backend Agent: TASK_ASSIGN (task_001)
   ↓
Backend Agent → Claudy: TASK_ACCEPT
   ↓ [Backend Agent ทำงาน]
   ↓
Backend Agent → Claudy: STATUS_UPDATE (50%)
   ↓
Backend Agent → Claudy: RESULT_SUBMIT
   ↓
Claudy → Code Review Agent: TASK_ASSIGN (review)
   ↓
Code Review Agent → Claudy: RESULT_SUBMIT (1 minor issue)
   ↓
Claudy → Backend Agent: RESULT_REJECT (with feedback)
   ↓
Backend Agent → Claudy: RESULT_SUBMIT (revised)
   ↓
Claudy → Backend Agent: RESULT_ACCEPT
   ↓
Claudy → Dev: 📋 Final Report
```

### Example 2: Complex Feature with Dependencies

```
Dev: "ทำ Checkout flow ทั้งระบบ"
   ↓
Claudy: [วิเคราะห์ → 5 sub-tasks]
   ↓
Phase 1 (Parallel):
   ├─ Claudy → Database Agent: TASK_ASSIGN (schema)
   ├─ Claudy → Research Agent: TASK_ASSIGN (payment best practice)
   └─ Claudy → Frontend Agent: TASK_ASSIGN (UI design — independent)
   
Phase 2 (After DB schema ready):
   └─ Claudy → Backend Agent: TASK_ASSIGN (API + payment integration)
   
Phase 3 (After Backend ready):
   ├─ Claudy → Frontend Agent: TASK_ASSIGN (API integration)
   ├─ Claudy → QA Agent: TASK_ASSIGN (test scenarios)
   └─ Claudy → Security Agent: TASK_ASSIGN (audit)
   
Phase 4 (Final):
   └─ Claudy → Docs Writer: TASK_ASSIGN (API documentation)
   
   ↓
Claudy → Dev: 📋 Complete deliverables report
```

---

## ✅ PROTOCOL COMPLIANCE CHECKLIST

ทุก Agent ต้องปฏิบัติตาม:

- [ ] ใช้ message format ตาม schema เสมอ
- [ ] ตอบ TASK_ASSIGN ภายใน SLA (P0: 5min, P1: 30min, P2: 2h)
- [ ] ส่ง STATUS_UPDATE ตาม frequency ที่กำหนด
- [ ] แจ้ง BLOCKER ทันทีเมื่อพบ
- [ ] ไม่คุยกับ Agent อื่นโดยตรง (ผ่าน Claudy)
- [ ] Log ทุก message ที่ส่ง/รับ
- [ ] ใช้ conversation_id ที่สม่ำเสมอใน thread เดียวกัน
- [ ] ระบุ assumption เมื่อ decide เอง
- [ ] รับ feedback อย่างสร้างสรรค์
- [ ] ปฏิเสธงานพร้อมเหตุผลถ้าเกิน scope

---

## 🚀 VERSION HISTORY

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-05-12 | Initial protocol release |

---

## 📚 REFERENCES

- Inspired by **MAPE-K loop** (Monitor, Analyze, Plan, Execute, Knowledge)
- Message patterns from **Saga Pattern** and **Choreography vs Orchestration**
- State machine design from **TLA+** specifications
- Inspired by **Multi-Agent Communication Languages** (KQML, FIPA-ACL)

---

*End of Protocol Specification*
