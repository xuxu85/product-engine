# Agent Contract

## Purpose

Agents are replaceable workers inside the PRODUCT ENGINE pipeline.

An agent performs a defined task and returns structured evidence and results.

Agents do NOT control:

- pipeline routing;
- decision gates;
- capital allocation;
- stage transitions;
- project-level strategy.

These responsibilities belong to the pipeline core.

---

## Core Principle

The pipeline controls the system.

Agents provide work.

Architecture:

INPUT
→ AGENT
→ STRUCTURED RESULT
→ VALIDATION
→ ROUTER
→ DECISION GATE
→ NEXT STAGE

An agent may recommend a next stage, but the pipeline policy is authoritative.

---

## Agent Input

Agents receive an `AgentRequest`.

Conceptual structure:

```json
{
  "stage": "PAIN",
  "input": {},
  "constraints": {},
  "evidence": []
}
Fields
stage

Current pipeline stage.

Examples:

IDEA
MARKET
PAIN
OPPORTUNITY
PRODUCT_THESIS
DEMAND_VALIDATION
PRODUCT_SPEC
FORMULA
ECONOMICS
MANUFACTURING
PILOT
SALES
REPEAT
SCALE
input

Task-specific input required by the agent.

constraints

Rules or limits that the agent must respect.

Examples:

market;
target price;
validation budget;
minimum evidence;
maximum capital exposure.
evidence

Evidence already available to the agent.

Agent Output

Every agent returns an AgentResult.

Conceptual structure:

{
  "decision": "PASS",
  "output": {},
  "evidence": [],
  "invalidation_conditions": [],
  "next_stage": null
}
Decision

The only valid decisions are:

PASS
FAIL
PIVOT
PASS

The current gate has sufficient evidence to proceed.

FAIL

The current hypothesis or gate should not proceed.

PIVOT

The current direction should change and return to the appropriate earlier stage.

The agent must not invent additional decision states.

Evidence

Agents are responsible for producing evidence relevant to their task.

Evidence should be:

traceable;
specific;
relevant to the current decision;
preferably independently verifiable.

For consumer research, evidence may include:

Amazon reviews;
Reddit discussions;
interviews;
search behavior;
marketplace observations;
competitor evidence;
other directly relevant consumer signals.

Evidence should not be replaced by unsupported model assumptions.

Invalidation Conditions

Every AgentResult MUST contain at least one measurable invalidation condition.

Example:

{
  "invalidation_conditions": [
    "Fewer than 3 independent consumer evidence sources confirm the pain"
  ]
}

An invalidation condition defines what evidence would cause the current conclusion to become invalid.

Good:

At least 5 independent consumers report the same recurring problem.

Better:

FAIL if fewer than 5 independent consumer evidence sources confirm
the same problem at meaningful frequency.

Bad:

The idea may not work.
Next Stage

next_stage is optional.

Example:

{
  "next_stage": "OPPORTUNITY"
}

However:

The agent does NOT control the pipeline transition.

The Router validates the result against the deterministic gate policy.

If the agent proposes a stage that contradicts the gate policy, the Router must reject the override.

Therefore:

Agent recommendation
        ↓
Router
        ↓
Gate Policy
        ↓
Authoritative next stage
Capital Control

Agents NEVER authorize meaningful capital expenditure.

Agents may report:

estimated validation cost;
estimated supplier cost;
estimated landed cost;
estimated pilot cost;
required resources.

But the agent cannot independently authorize:

inventory purchases;
production orders;
advertising spend;
supplier payments;
large validation budgets;
pilot production.

Capital decisions belong to the pipeline policy and decision layer.

Agent Responsibilities

An agent SHOULD:

execute the assigned task;
collect relevant evidence;
structure the evidence;
produce a decision;
define invalidation conditions;
return machine-readable output.

An agent SHOULD NOT:

redefine the project goal;
bypass a decision gate;
change the pipeline stage independently;
authorize capital;
create a new strategic thesis without being asked;
hide uncertainty;
replace evidence with unsupported assumptions.
Example: PAIN Agent

Input:

{
  "stage": "PAIN",
  "input": {
    "category": "kitchen organization"
  },
  "constraints": {
    "minimum_evidence": 5
  },
  "evidence": []
}

Output:

{
  "decision": "PASS",
  "output": {
    "pain_verified": true,
    "pain_statement": "Consumers repeatedly struggle with ...",
    "frequency": "recurring",
    "severity": 7,
    "evidence_count": 8
  },
  "evidence": [
    {
      "source": "Amazon",
      "source_url": "...",
      "consumer_context": "...",
      "pain_statement": "...",
      "intensity": 8,
      "frequency_signal": "repeated",
      "verbatim": "..."
    }
  ],
  "invalidation_conditions": [
    "Fewer than 5 independent evidence sources confirm the same recurring pain"
  ],
  "next_stage": "OPPORTUNITY"
}
Replaceability

Agents are modular and replaceable.

The pipeline must not depend on a specific implementation.

For example:

Amazon Pain Agent
Reddit Pain Agent
LLM Pain Agent
Manual Research Agent
H10 Review Agent

can all produce the same AgentResult.

Therefore the core pipeline remains unchanged.

Future Agents

The same contract can support:

H10 research agent;
Amazon research agent;
review analysis agent;
Reddit research agent;
opportunity finder;
product thesis agent;
validation agent;
supplier research agent;
RFQ agent;
economics agent;
sourcing agent;
prototype agent;
listing agent;
launch agent.

Each agent remains a worker.

The pipeline remains the controller.

Boundary: Agent vs Pipeline
Agent
Research
Analyze
Extract
Score
Recommend
Return evidence
Return decision
Pipeline
Validate result
Apply gate policy
Control stage transition
Control capital
Persist state
Record history

This boundary must remain explicit.

Design Rule

Do not add intelligence to the pipeline core unless it is required for a decision gate.

Prefer:

Existing tool
→ Existing agent / workflow
→ Integration
→ Minimal adapter
→ Custom code only when proven necessary

The objective is not to build a sophisticated AI platform.

The objective is:

Evidence
→ Decision
→ Product
→ Prototype
→ Pilot
→ First Real Sale
→ Repeat Purchase
→ Scale
Primary Metric

The system should optimize for:

TIME → FIRST REAL SALE

Any component that does not materially improve the speed, cost, or quality of reaching the next decision gate should be deferred
