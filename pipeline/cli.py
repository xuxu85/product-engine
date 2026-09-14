from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import AgentResult
from .runner import PipelineRunner
from .state import Decision, Stage


def main() -> None:
    parser = argparse.ArgumentParser(description="PRODUCT ENGINE pipeline runner")
    parser.add_argument("command", choices=["status", "apply-result"])
    parser.add_argument("--file", default="runs/current/result.json")
    args = parser.parse_args()

    runner = PipelineRunner()

    if args.command == "status":
        state = runner.load_state()
        print(json.dumps({"stage": state.stage.value, "decision": state.decision.value if state.decision else None, "history": state.history}, indent=2))
        return

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    data["decision"] = Decision(data["decision"])
    if data.get("next_stage") is not None:
        data["next_stage"] = Stage(data["next_stage"])
    result = AgentResult(**data)
    state = runner.apply(result)
    print(json.dumps({"stage": state.stage.value, "decision": state.decision.value if state.decision else None}, indent=2))


if __name__ == "__main__":
    main()
