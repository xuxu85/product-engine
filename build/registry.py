from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class BuildMechanism:
    """Provider-neutral descriptor for a ready BUILD mechanism."""

    id: str
    version: str
    capabilities: tuple[str, ...]
    required_inputs: tuple[str, ...]
    runner: Callable[[dict[str, Any]], dict[str, Any]]

    def validate_input(self, payload: dict[str, Any]) -> list[str]:
        return [key for key in self.required_inputs if key not in payload]

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        missing = self.validate_input(payload)
        if missing:
            return {
                "gate": "BLOCKED",
                "unknowns": missing,
                "blockers": [f"Missing required input: {key}" for key in missing],
                "mechanism_id": self.id,
                "mechanism_version": self.version,
            }
        return self.runner(payload)


class BuildMechanismRegistry:
    """Selects mechanisms; it does not make business or gate decisions."""

    def __init__(self, mechanisms: list[BuildMechanism] | None = None) -> None:
        self._mechanisms = {m.id: m for m in (mechanisms or [])}

    def register(self, mechanism: BuildMechanism) -> None:
        if mechanism.id in self._mechanisms:
            raise ValueError(f"BUILD mechanism already registered: {mechanism.id}")
        self._mechanisms[mechanism.id] = mechanism

    def get(self, mechanism_id: str) -> BuildMechanism:
        try:
            return self._mechanisms[mechanism_id]
        except KeyError as exc:
            raise KeyError(f"Unknown BUILD mechanism: {mechanism_id}") from exc

    def list(self) -> list[BuildMechanism]:
        return list(self._mechanisms.values())
