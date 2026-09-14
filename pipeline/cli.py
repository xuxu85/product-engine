from __future__ import annotations

import argparse
import json
from pathlib import Path

from .contracts import AgentResult
from .runner import PipelineRunner


def main() -> None:
    parser = argparse.ArgumentParser(description="PRODUCT ENGINE pipeline runner")
    parser.add_argument("command", choices=["status", "apply-result"])
    parser.add_argument("--file", default="runs/current/result.json")
    args = parser.parse_args()

    runner = PipelineRunner()

    if args.command == "status":
        state = runner.load_state()
        print(json.dumps({"stage": state.stage.value, "decision": getattr(state.decision, "value", state.decision), "history": state.history}, indent=2))
        return

    data = json.loads(Path(args.file).read_text(encoding="utf-8"))
    result = AgentResult(**data)
    state = runner.apply(result)
    print(json.dumps({"stage": state.stage.value, "decision": getattr(state.decision, "value", state.decision)}, indent=2))


if __name__ == "__main__":
    main()
