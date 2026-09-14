"""Strict architecture-only workers for post-PAIN pipeline stages."""
from __future__ import annotations
from typing import Any, Callable
from pipeline.contracts import AgentRequest, AgentResult

_NEXT = {"OPPORTUNITY":"PRODUCT_THESIS","PRODUCT_THESIS":"DEMAND_VALIDATION","DEMAND_VALIDATION":"PRODUCT_SPEC","PRODUCT_SPEC":"FORMULA","FORMULA":"ECONOMICS","ECONOMICS":"MANUFACTURING","MANUFACTURING":"PILOT","PILOT":"SALES","SALES":"REPEAT","REPEAT":"SCALE"}
_REQUIRED = {"OPPORTUNITY":"opportunity","PRODUCT_THESIS":"product_thesis","DEMAND_VALIDATION":"demand_validation","PRODUCT_SPEC":"product_spec","FORMULA":"formula","ECONOMICS":"economics","MANUFACTURING":"manufacturing","PILOT":"pilot","SALES":"sales","REPEAT":"repeat"}

def _error(request: AgentRequest, condition: str) -> AgentResult:
    return AgentResult(task_id=request.task_id, agent_id=request.agent_id, agent_version=request.agent_version, status="ERROR", decision="FAIL", output={}, evidence=[], confidence=0.0, invalidation_conditions=[condition], next_stage=None)

def run_stage(request: AgentRequest) -> AgentResult:
    stage = request.stage.value
    key, next_stage = _REQUIRED.get(stage), _NEXT.get(stage)
    payload: dict[str, Any] = request.input if isinstance(request.input, dict) else {}
    if not key or not next_stage:
        return _error(request, "FAIL if the worker receives an unsupported stage.")
    if key not in payload:
        return _error(request, f"FAIL if required fixture field '{key}' is absent.")
    return AgentResult(task_id=request.task_id, agent_id=request.agent_id, agent_version=request.agent_version, status="SUCCESS", decision="PASS", output={key: payload[key]}, evidence=request.evidence, confidence=1.0, invalidation_conditions=[f"Architecture test only: FAIL if supplied {key} fixture is not replaced by real evidence or execution output before a business decision."], next_stage=next_stage)

def make_worker(stage: str) -> Callable[[AgentRequest], AgentResult]:
    def worker(request: AgentRequest) -> AgentResult:
        if request.stage.value != stage:
            return _error(request, f"FAIL if expected stage {stage} does not match request stage.")
        return run_stage(request)
    return worker

opportunity = make_worker("OPPORTUNITY")
product_thesis = make_worker("PRODUCT_THESIS")
demand_validation = make_worker("DEMAND_VALIDATION")
product_spec = make_worker("PRODUCT_SPEC")
formula = make_worker("FORMULA")
economics = make_worker("ECONOMICS")
manufacturing = make_worker("MANUFACTURING")
pilot = make_worker("PILOT")
sales = make_worker("SALES")
repeat = make_worker("REPEAT")
