from __future__ import annotations
import json
import sys
from pathlib import Path
from .state import BlackboardState
from .handoff import AGENT_ORDER
from .runner import AgentRunner
from ..schemas.agent_spec import AgentSpecification

AGENTS_DIR = Path(__file__).parent.parent / "agents"

AGENT_MODELS = {
    "orchestrator": "claude-opus-4-8",
    "architect": "claude-sonnet-4-6",
    "prompt_engineer": "claude-sonnet-4-6",
    "tool_builder": "claude-sonnet-4-6",
    "eval_engineer": "claude-sonnet-4-6",
}

AGENT_TASKS = {
    "architect": (
        "Analyse the task and produce 'agent_spec.json' — a complete specification of the agent "
        "to be built: name, purpose, tools needed, capabilities, constraints, and eval case outlines."
    ),
    "prompt_engineer": (
        "Read 'agent_spec.json' and write 'system_prompt.md' — the full system prompt for the agent. "
        "It must be clear, complete, and cover all edge cases defined in the spec."
    ),
    "tool_builder": (
        "Read 'agent_spec.json' and write 'tools.py' — Anthropic tool definitions and Python "
        "implementations for every tool the agent needs. Include type hints and docstrings."
    ),
    "eval_engineer": (
        "Read 'agent_spec.json', 'system_prompt.md', and 'tools.py'. "
        "Write 'evals.json' — a complete evaluation suite: diverse input cases, "
        "expected behaviors, and edge cases that validate the agent works correctly."
    ),
}


class CreatorSquadOrchestrator:
    """
    Orchestrates the Creator Squad to build a new agent from a task description.

    Flow: architect → prompt_engineer → tool_builder → eval_engineer → done
    """

    def __init__(self, verbose: bool = True) -> None:
        self.verbose = verbose
        self.state: BlackboardState | None = None

    def run(self, task: str) -> BlackboardState:
        self.state = BlackboardState(task=task)
        self._log(f"Creator Squad starting\nTask: {task}\n")

        for agent_name in AGENT_ORDER[1:]:
            self.state.phase = agent_name
            self.state.current_agent = agent_name
            self._log(f"→ {agent_name.upper()}")

            runner = AgentRunner(
                agent_name=agent_name,
                system_prompt_path=AGENTS_DIR / agent_name / "system_prompt.md",
                model=AGENT_MODELS[agent_name],
            )

            agent_task = f"Original request: {task}\n\n{AGENT_TASKS[agent_name]}"
            summary, self.state = runner.run(agent_task, self.state, verbose=self.verbose)
            self._log(f"  ✓ {agent_name} done: {summary[:120]}")

        self.state.phase = "complete"
        self.state.current_agent = "done"
        self._validate_spec()
        self._print_summary()
        return self.state

    def _validate_spec(self) -> None:
        raw = self.state.get_artifact("agent_spec.json")
        if not raw:
            return
        try:
            AgentSpecification.model_validate_json(raw)
            self._log("  ✓ agent_spec.json validated against AgentSpecification schema")
        except Exception as e:
            self._log(f"  ⚠ agent_spec.json schema warning: {e}")

    def _log(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    def _print_summary(self) -> None:
        print("\n" + "=" * 60)
        print("Creator Squad Complete")
        print("=" * 60)
        print(f"Artifacts produced: {list(self.state.artifacts.keys())}")
        print(f"Total cost: ${self.state.estimated_cost_usd()}")
        print(f"Tokens: {self.state.total_input_tokens} in / {self.state.total_output_tokens} out")
        print("\nOutput files in: output/")
        print("=" * 60)


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python -m framework.core.orchestrator '<task>'")
        sys.exit(1)

    task = " ".join(sys.argv[1:])
    squad = CreatorSquadOrchestrator(verbose=True)
    state = squad.run(task)
    state.save(Path("output/session_state.json"))


if __name__ == "__main__":
    main()
