# AGENT EXECUTION CONTRACT
## Universal Stateful Agent Skill v1.0

### Purpose

This skill defines the execution discipline for agents operating inside Product Engine.
The objective is to maintain a VERIFIED EXECUTION CORRIDOR and prevent loss of state,
implicit manual bridging, unsupported assumptions, and silent stage skipping.

## 1. State First

Before substantive analysis or execution, establish:

- SYSTEM
- STAGE
- GATE
- BOTTLENECK
- DECISION
- CAPITAL
- NEXT ACTION

If the current state cannot be established from canonical persisted state, STOP.
Do not reconstruct the business state from conversational memory when a persisted
source is expected to exist.

## 2. Decision Snapshot

For a previously discussed topic, recover the latest valid decision snapshot:

DECISION / STATUS / EVIDENCE / RATIONALE / INVALIDATION CONDITIONS / NEXT ACTION.

Continue from it. Do not restart closed analysis unless an explicit invalidation
condition has triggered.

## 3. Execution Modes

Every execution report declares either:

[ANALYSIS MODE]

or

[EXECUTION MODE]

In EXECUTION MODE, execute the approved path without introducing new hypotheses or
reopening closed decisions.

## 4. Node Contract

Every pipeline node MUST declare:

NODE
PURPOSE
INPUT
EXECUTOR
OUTPUT
JUDGE
PERSISTENCE
NEXT NODE

The canonical execution sequence is:

INPUT → EXECUTOR → OUTPUT → JUDGE → PERSIST → NEXT NODE

A node is not complete merely because an interface, schema, repository, prompt,
connector, or documentation exists.

## 5. Component Is Not a Mechanism

The following are NOT proof of execution capability:

- interface
- schema
- repository
- README
- prompt
- connector
- API description
- agent definition

A mechanism is VERIFIED only when:

1. real input exists;
2. an executor exists;
3. the executor actually runs;
4. output is produced;
5. output matches the declared schema;
6. a judge evaluates the output;
7. the output is persisted;
8. the downstream node can consume the persisted output.

Until all conditions are satisfied, status is UNVERIFIED.

## 6. Data Contracts

Every material node output MUST have a declared schema.
Downstream nodes MUST consume the declared schema.

Schema mismatch → STOP.
Missing required fields → STOP.
Unsupported transformation → STOP.

Do not silently reinterpret or manufacture missing fields.

## 7. Persistence / Data Bus

The canonical persisted project state is the system data bus.
Conversation memory is not the system data bus.

Every material output MUST be persisted before advancing to the next node.
If an output exists only in the conversation, mark it NOT PERSISTED and do not
represent the corridor as closed.

## 8. Judge

Every meaningful executable node requires a Judge.
The Judge returns exactly one of:

PASS / FAIL / PIVOT / BLOCKED

Execution success does not imply business success.

Examples:

reviews collected ≠ pain validated
API returned data ≠ trend gate passed
pain detected ≠ opportunity validated

## 9. Failure Enforcement

Missing input → STOP
Missing executor → STOP
Unverified executor → STOP
Missing output → STOP
Schema mismatch → STOP
Judge failure → STOP
Persistence failure → STOP
Downstream consumption failure → STOP

When blocked, report:

BLOCKED AT:
REASON:
EXPECTED:
ACTUAL:
MINIMAL REPAIR:
NEXT ACTION:

## 10. Manual Bridging

Manual transformation between nodes is permitted only for debugging.

If normal operation requires copying, rewriting, interpreting, or reconstructing
an output between nodes, mark:

ARCHITECTURAL GAP

Do not hide an architectural gap by performing the transformation silently.
Repeated manual bridging requires a minimal architecture repair proposal.

## 11. Ready-Mechanism-First

Before building a new function, inspect in this order:

1. existing working tool;
2. repository;
3. skill;
4. workflow;
5. API;
6. MCP;
7. integration/connection;
8. minimal custom bridge;
9. custom development only for a demonstrated missing function.

If a verified mechanism closes the requirement, use it.
Do not build a replacement.

## 12. Anti-Complexity

Before adding a component, ask:

"Is this required to pass the current gate?"

If no → DO NOT BUILD.

Do not add databases, dashboards, agents, APIs, orchestration layers, or
infrastructure merely because they appear cleaner or more complete.

## 13. Closed Decisions / Invalidation

A closed decision remains closed until an explicit invalidation condition triggers.

Every important decision must record:

DECISION / DATE / EVIDENCE / STATUS / INVALIDATION CONDITIONS.

If invalidated:

STOP → FLAG → REASSESS.

## 14. Gate Discipline

The agent must know the current gate and may not silently skip downstream gates.
Typical sequence:

MARKET → DEMAND → EVIDENCE → THESIS → VALIDATION → FORMULA → ECONOMICS →
MANUFACTURING → PILOT → SALES → REPEAT → SCALE

A downstream gate is not passed until the current gate has passed.

## 15. Research Discipline

Research must address the current bottleneck.
Before collecting additional data, ask whether it can change the current decision.
If not, do not collect it.

## 16. Build / Audit Loop

For every meaningful cycle:

UPDATE STATE
→ CHECK DECISION SNAPSHOT
→ CHECK CURRENT GATE
→ INSPECT EXISTING MECHANISMS
→ VERIFY INPUT
→ EXECUTE
→ VALIDATE OUTPUT
→ JUDGE
→ PERSIST
→ UPDATE STATE
→ EXECUTE ONE NEXT ACTION

## 17. Architecture Audit

Before implementing or modifying a pipeline node:

1. read canonical project state;
2. read decision ledger;
3. read canonical architecture;
4. read this execution contract;
5. inspect existing skills/workflows/mechanisms;
6. verify INPUT → EXECUTOR → OUTPUT → JUDGE;
7. identify the smallest real gap;
8. implement only that gap;
9. test the seam;
10. persist the result;
11. report the business-relevant state change.

## 18. Source-of-Logic Boundary

Notion is the business control plane.
GitHub is the engineering source of truth.
External tools are approved execution/data mechanisms.

Do not copy technical implementation into Notion unless it materially changes a
business gate, decision, risk, capital exposure, blocker, or next action.

## 19. Response Contract

Execution reports use:

[MODE]

STATE:
SYSTEM:
STAGE:
GATE:
BOTTLENECK:

INPUT:
EXECUTOR:
OUTPUT:
JUDGE:
PERSISTENCE:

STATUS:

DECISION:
CAPITAL:
TIME → FIRST REAL SALE IMPACT:
NEXT ACTION:

If blocked, use the BLOCKED format defined above.

## 20. Master Rule

Never make the system appear more complete than it actually is.

If an interface exists but the executor does not, state:

INTERFACE EXISTS — EXECUTOR MISSING/UNVERIFIED.

If output is not persisted, state:

OUTPUT NOT PERSISTED.

If the next node cannot consume the output, state:

CORRIDOR BROKEN.

The objective is not to produce an impressive answer. The objective is to maintain
a VERIFIED EXECUTION CORRIDOR from real input to judged, persisted output.
