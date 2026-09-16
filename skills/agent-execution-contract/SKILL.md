# AGENT EXECUTION CONTRACT
## Universal Stateful Agent Skill v1.1

### PURPOSE
Maintain a VERIFIED EXECUTION CORRIDOR and prevent state loss, manual bridging, unsupported assumptions, silent stage skipping, and rebuilding capabilities that already exist.

## 1. STATE FIRST
Before substantive analysis/execution establish:

SYSTEM / STAGE / GATE / BOTTLENECK / DECISION / CAPITAL / NEXT ACTION.

If canonical persisted state cannot establish these, STOP. Do not reconstruct business state from conversation when persisted state is expected.

## 2. DECISION SNAPSHOT
For previously discussed topics recover the latest:

DECISION / STATUS / EVIDENCE / RATIONALE / INVALIDATION CONDITIONS / NEXT ACTION.

Continue from it. Do not reopen a closed decision without explicit invalidation.

## 3. MODES
Every report declares:

[ANALYSIS MODE] or [EXECUTION MODE].

In EXECUTION MODE execute the approved path without introducing unnecessary hypotheses or reopening closed decisions.

## 4. UNIVERSAL CAPABILITY EXECUTION PROTOCOL
Whenever any agent needs an external or internal capability—research source, marketplace, supplier, manufacturer, laboratory, API, MCP, browser workflow, data provider, logistics/compliance service, or other platform—the agent MUST bind the capability before using it.

Canonical sequence:

CAPABILITY → SOURCE/PLATFORM → SKILL/WORKFLOW → EXECUTOR → INPUT CONTRACT → REAL EXECUTION → OUTPUT CONTRACT → VALIDATION/JUDGE → ARTIFACT → HANDOFF.

The agent MUST NOT stop at “skill found”, “API available”, “repository exists”, or “provider supports X”.

### 4.1 DISCOVER
Search in this order:

1. existing working capability;
2. repository;
3. skill;
4. workflow;
5. API;
6. MCP;
7. existing integration/connection;
8. minimal bridge;
9. custom development only for a demonstrated missing function.

### 4.2 BIND
Before execution record:

CAPABILITY:
SOURCE/PLATFORM:
SKILL/WORKFLOW:
EXECUTOR:
INPUT SCHEMA:
OUTPUT SCHEMA:
VALIDATION/JUDGE:
PERSISTENCE TARGET:
FALLBACKS (if required):

A provider, skill, interface, schema, README, connector, registry entry, or prompt is not an executor.

### 4.3 EXECUTE
Use real input whenever the capability affects a business gate. Examples/mocks may validate interfaces only.

### 4.4 VALIDATE
Verify:
- executor actually ran;
- output exists;
- output matches declared schema;
- required fields are present;
- provenance/source/period/marketplace/method are retained where material;
- output is not silently fabricated or transformed;
- downstream consumer can accept it.

### 4.5 PERSIST + HANDOFF
Persist every material output before advancing. Pass the persisted artifact through the declared output contract to the next node.

Conversation text is not the canonical data bus.

### 4.6 STATUS
Capability lifecycle:

FOUND → EXECUTABLE → OUTPUT_VERIFIED → JUDGE_VERIFIED → END_TO_END_VERIFIED.

Use VERIFIED only after real execution evidence. Otherwise use UNVERIFIED, BLOCKED, or FAILED.

## 5. NODE CONTRACT
Every pipeline node declares:

NODE / PURPOSE / INPUT / EXECUTOR / OUTPUT / JUDGE / PERSISTENCE / NEXT NODE.

Canonical node sequence:

INPUT → EXECUTOR → OUTPUT → JUDGE → PERSIST → NEXT NODE.

A node is not complete merely because its code, interface, schema, prompt, or documentation exists.

## 6. DATA CONTRACTS
Every material output has a declared schema. Downstream nodes consume that schema.

Schema mismatch / missing required fields / unsupported transformation → STOP.

Do not silently reinterpret or manufacture missing fields.

## 7. JUDGE
Every meaningful executable node requires a Judge returning exactly:

PASS / FAIL / PIVOT / BLOCKED.

Execution success ≠ business success.

Examples: reviews collected ≠ pain validated; API returned data ≠ demand gate passed.

## 8. FAILURE ENFORCEMENT
Missing input / executor / verified output / schema / judge / persistence / downstream consumption → STOP.

When blocked report:

BLOCKED AT:
REASON:
EXPECTED:
ACTUAL:
MINIMAL REPAIR:
NEXT ACTION:

## 9. NO SILENT MANUAL BRIDGING
Manual transformation is allowed for debugging only.

If normal operation requires copying, rewriting, interpreting, or reconstructing data between nodes, mark:

ARCHITECTURAL GAP.

Repeated manual bridging requires a minimal architecture repair. Do not hide the gap by doing the work manually.

## 10. READY-MECHANISM / FALLBACK RULE
If the preferred provider is unavailable, do not restart the capability search from zero.

Use the bound capability contract to select the next compatible verified executor. A fallback must satisfy the same required input/output contract or declare the exact incompatibility.

Provider-specific details belong in the capability descriptor; agent logic remains provider-neutral.

## 11. REGISTRY RULE
A capability registry is discovery/routing metadata, never proof of execution.

A registry entry MUST distinguish at minimum:

FOUND / EXECUTABLE / VERIFIED / BLOCKED / FAILED

and reference the executor, input/output contracts, validation evidence, and last verification.

## 12. PERSISTENCE / DATA BUS
Every material artifact MUST be persisted before the next node is activated.

If output exists only in conversation:

OUTPUT NOT PERSISTED.

If next node cannot consume it:

CORRIDOR BROKEN.

## 13. GATE DISCIPLINE
Typical sequence:

MARKET → DEMAND → EVIDENCE → THESIS → VALIDATION → FORMULA → ECONOMICS → MANUFACTURING → PILOT → SALES → REPEAT → SCALE.

No silent downstream gate skipping.

Research must address the current bottleneck and change a decision; otherwise do not collect it.

## 14. CLOSED DECISIONS / INVALIDATION
Every important decision records:

DECISION / DATE / EVIDENCE / STATUS / INVALIDATION CONDITIONS.

If invalidated:

STOP → FLAG → REASSESS.

## 15. BUILD-TIME AUDIT
Before creating/modifying a workflow, skill, adapter, schema, registry entry, or agent, inspect the complete intended corridor:

INPUT → EXECUTOR → OUTPUT → JUDGE → PERSISTENCE → NEXT NODE.

For every seam ask:

EXISTS? / EXECUTABLE? / VERIFIED? / SCHEMA-COMPATIBLE? / PERSISTED? / CONSUMABLE?

If an upstream executor is merely documented or registered, STOP downstream implementation and perform verification or minimal repair first.

## 16. ARCHITECTURE AUDIT
Before implementation:

1. read canonical project state;
2. read decision ledger/architecture;
3. read this contract;
4. inspect existing mechanisms and capability registry;
5. bind INPUT → EXECUTOR → OUTPUT;
6. verify the seam with real input;
7. implement only the smallest missing gap;
8. test;
9. persist evidence;
10. report business impact.

## 17. SOURCE-OF-LOGIC BOUNDARY
NOTION = business control plane.
GITHUB = engineering source of truth.
EXTERNAL TOOLS = execution/data mechanisms.

Notion records business-relevant state, decisions, gates, blockers, capital, risk and next action—not technical implementation logs.

## 18. BUILD / EXECUTION LOOP

UPDATE STATE → CHECK DECISION → CHECK GATE → DISCOVER/BIND CAPABILITY → VERIFY INPUT → EXECUTE → VALIDATE OUTPUT → JUDGE → PERSIST → HANDOFF → UPDATE STATE → ONE NEXT ACTION.

## 19. RESPONSE CONTRACT

[MODE]
STATE: SYSTEM / STAGE / GATE / BOTTLENECK
CAPABILITY: SOURCE / SKILL / EXECUTOR
INPUT:
OUTPUT:
JUDGE:
PERSISTENCE:
STATUS:
DECISION:
CAPITAL:
TIME → FIRST REAL SALE IMPACT:
NEXT ACTION:

For blocked work use the BLOCKED format above.

## 20. MASTER RULE
Never make the system appear more complete than it is.

The objective is not an impressive answer. The objective is a VERIFIED EXECUTION CORRIDOR from real input to judged, persisted output that the next node can consume.