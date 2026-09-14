# Agent Contract v0.2

## Purpose

Agents are replaceable workers inside the PRODUCT ENGINE pipeline.

An agent performs a defined task and returns a structured result.

The pipeline core is authoritative.

Agents do NOT control:

- pipeline routing;
- decision gates;
- stage transitions;
- capital allocation;
- project-level strategy.

---

## Architecture

```text
INPUT
  ↓
AGENT
  ↓
AGENT RESULT
  ↓
VALIDATION
  ↓
ROUTER
  ↓
DECISION GATE
  ↓
NEXT STAGE

The agent produces work.

The pipeline decides what happens next.

Agent Request

Agents receive:

{
  "task_id": "string",
  "agent_id": "string",
  "agent_version": "string",
  "stage": "PAIN",
  "input": {},
  "constraints": {},
  "evidence": []
}
Required fields
task_id

Unique identifier for the execution task.

Used to correlate the agent result with a pipeline run.

agent_id

Stable identifier of the agent.

Examples:

pain.amazon
pain.reddit
opportunity.h10
sourcing.1688
economics.basic
agent_version

Version of the agent implementation.

stage

Current pipeline stage.

The agent must operate within the supplied stage.

input

Task-specific input.

constraints

Rules and limits that the agent must respect.

Examples:

target market;
target price;
minimum evidence;
validation budget;
maximum capital exposure.
evidence

Evidence already available to the agent.

Agent Result

Every successful agent execution returns:

{
  "task_id": "string",
  "agent_id": "string",
  "agent_version": "string",
  "status": "SUCCESS",
  "decision": "PASS",
  "output": {},
  "evidence": [],
  "confidence": 0.0,
  "invalidation_conditions": [],
  "next_stage": null
}
Status

Valid values:

SUCCESS
ERROR

If execution fails:

{
  "task_id": "string",
  "agent_id": "string",
  "agent_version": "string",
  "status": "ERROR",
  "decision": "FAIL",
  "output": {},
  "evidence": [],
  "confidence": 0.0,
  "invalidation_conditions": [
    "Agent execution failed and result could not be independently verified."
  ],
  "next_stage": null
}

An agent must not fabricate evidence when execution fails.

Decision

The only valid decisions are:

PASS
FAIL
PIVOT
PASS

The evidence is sufficient to pass the current gate.

FAIL

The current hypothesis does not meet the gate requirements.

PIVOT

The evidence suggests that the current direction should change.

The agent must not invent additional decision states.

Evidence

Evidence belongs to the agent result.

Evidence should be:

traceable;
specific;
relevant to the current decision;
independently verifiable where possible.

For consumer research, the preferred structure is:

{
  "source": "Amazon",
  "source_url": "https://...",
  "consumer_context": "...",
  "pain_statement": "...",
  "intensity": 8,
  "frequency_signal": "recurring",
  "verbatim": "..."
}

Supported sources may include:

Amazon
Reddit
Google
Interview
Other

Unsupported assumptions must not be presented as evidence.

Confidence

confidence is a supporting signal only.

Valid range:

0.0 – 1.0

Confidence MUST NOT replace evidence.

Confidence MUST NOT override gate policy.

Example:

{
  "confidence": 0.82
}

means the agent has relatively high confidence in its interpretation.

It does NOT mean the pipeline must PASS.

Invalidation Conditions

Every agent result MUST contain at least one measurable or testable invalidation condition.

Example:

{
  "invalidation_conditions": [
    "Fewer than 5 independent consumer evidence sources confirm the same recurring pain."
  ]
}

Good invalidation condition:

FAIL if fewer than 5 independent evidence sources confirm
the same recurring consumer problem.

Bad invalidation condition:

The idea may not work.

The purpose of an invalidation condition is to define what future evidence would invalidate the current conclusion.

Next Stage

next_stage is optional.

Example:

{
  "next_stage": "OPPORTUNITY"
}

The agent may recommend a next stage.

The agent does NOT control the transition.

The Router MUST validate the proposed transition against the deterministic gate policy.

If the proposed stage contradicts the gate policy, the Router rejects it.

Therefore:

Agent recommendation
        ↓
      Router
        ↓
   Gate Policy
        ↓
Authoritative transition
Capital Control

Agents NEVER authorize capital deployment.

Agents may estimate:

validation cost;
supplier cost;
landed cost;
pilot cost;
required resources.

Agents cannot independently authorize:

inventory purchases;
production orders;
supplier payments;
advertising spend;
large validation budgets;
pilot production;
other material capital deployment.

Capital decisions belong to the pipeline decision layer.

Agent Responsibilities

An agent SHOULD:

execute the assigned task;
collect relevant evidence;
structure the evidence;
analyze the evidence;
return a decision;
define invalidation conditions;
return machine-readable output;
expose uncertainty where relevant.

An agent MUST NOT:

redefine the project goal;
bypass a decision gate;
independently change pipeline stage;
authorize capital;
fabricate evidence;
hide execution errors;
replace evidence with unsupported assumptions.
Replaceability

Agents are modular and replaceable.

Different implementations may perform the same function:

Amazon Pain Agent
Reddit Pain Agent
H10 Review Agent
LLM Pain Agent
Manual Research Agent

All should be able to return the same contract.

The pipeline core must not depend on a specific agent implementation.

Future Agents

The same contract can support:

H10 research;
Amazon research;
review analysis;
Reddit research;
opportunity discovery;
product thesis;
demand validation;
supplier research;
RFQ;
economics;
sourcing;
prototype;
listing;
launch.

New agents should integrate through the contract rather than modify the core state machine unless a proven architectural requirement exists.

Agent / Pipeline Boundary
Agent
Research
Analyze
Extract
Score
Recommend
Return evidence
Return result
Pipeline
Validate result
Apply gate policy
Control stage transition
Control capital
Persist state
Record history

This boundary is mandatory.

Design Rule

Before building a new agent or intelligence layer:

Existing Tool
      ↓
Existing Agent / Workflow
      ↓
Integration
      ↓
Minimal Adapter
      ↓
Custom Development

Custom development should occur only when an existing solution does not adequately close the current bottleneck.

Primary Project Metric

The system exists to accelerate:

EVIDENCE
→ DECISION
→ PRODUCT
→ PROTOTYPE
→ PILOT
→ FIRST REAL SALE
→ REPEAT PURCHASE
→ SCALE

Primary metric:

TIME → FIRST REAL SALE

Any agent, workflow, or infrastructure component that does not materially improve the speed, cost, or quality of reaching the next decision gate should be deferred.
