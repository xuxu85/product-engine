"""Execution boundary for BUILD mechanisms.

The pipeline router remains pure; this layer selects and executes a registered
mechanism, validates its contract, and returns a structured result for routing.
"""
from __future__ import annotations

from typing import Any, Callable

from .registry import BuildMechanismRegistry


class BuildExecutionError(RuntimeError):
    """Raised when a BUILD mechanism cannot execute safely."""


def run_build(
    registry: BuildMechanismRegistry,
    mechanism_id: str,
    inputs: dict[str, Any],
    executor: Callable[[dict[str, Any]], dict[str, Any]],
) -> dict[str, Any]:
    """Validate inputs, execute one registered mechanism, and return its result.

    This function deliberately does not advance the business pipeline. The
    canonical router owns PASS/FAIL/PIVOT routing; BUILD only produces a
    validated execution artifact.
    """
    mechanism = registry.get(mechanism_id)
    validation = registry.validate_inputs(mechanism_id, inputs)
    if not validation.ok:
        return {
            "status": "BLOCKED",
            "mechanism_id": mechanism_id,
            "missing_inputs": validation.missing,
        }

    output = executor(inputs)
    if not isinstance(output, dict):
        raise BuildExecutionError("BUILD mechanism must return a dictionary")

    return {
        "status": "COMPLETED",
        "mechanism_id": mechanism.id,
        "mechanism_version": mechanism.version,
        "output": output,
    }
