"""Preflight and postflight contracts for ready mechanisms.

This module is provider-neutral. It prevents a mechanism from reaching paid or
side-effecting execution unless its declared input contract is satisfied, and
it prevents unvalidated provider output from entering the business pipeline.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class FieldSpec:
    name: str
    required: bool = True
    value_type: type | tuple[type, ...] = str


@dataclass(frozen=True)
class MechanismContract:
    mechanism: str
    input_fields: tuple[FieldSpec, ...] = ()
    output_required_keys: tuple[str, ...] = ()
    output_item_required_keys: tuple[str, ...] = ()


@dataclass(frozen=True)
class ContractCheck:
    ok: bool
    phase: str
    errors: tuple[str, ...] = field(default_factory=tuple)


def validate_inputs(contract: MechanismContract, values: Mapping[str, Any]) -> ContractCheck:
    errors: list[str] = []
    for field in contract.input_fields:
        if field.name not in values:
            if field.required:
                errors.append(f"missing required input: {field.name}")
            continue
        value = values[field.name]
        if not isinstance(value, field.value_type):
            errors.append(
                f"invalid input type: {field.name}; expected={field.value_type}, got={type(value)}"
            )
    return ContractCheck(not errors, "INPUT", tuple(errors))


def validate_output(contract: MechanismContract, output: Any) -> ContractCheck:
    errors: list[str] = []
    if not isinstance(output, Mapping):
        errors.append(f"output must be a mapping, got={type(output)}")
        return ContractCheck(False, "OUTPUT", tuple(errors))

    for key in contract.output_required_keys:
        if key not in output:
            errors.append(f"missing required output key: {key}")

    if contract.output_item_required_keys:
        items = output.get("results")
        if not isinstance(items, list):
            errors.append("output.results must be a list")
        else:
            for index, item in enumerate(items):
                if not isinstance(item, Mapping):
                    errors.append(f"output.results[{index}] must be a mapping")
                    continue
                for key in contract.output_item_required_keys:
                    if key not in item:
                        errors.append(f"missing output.results[{index}] key: {key}")

    return ContractCheck(not errors, "OUTPUT", tuple(errors))


def require_valid(check: ContractCheck) -> None:
    """Raise before execution/downstream handoff when a contract check fails."""
    if not check.ok:
        raise ValueError(f"{check.phase} contract failed: {'; '.join(check.errors)}")
