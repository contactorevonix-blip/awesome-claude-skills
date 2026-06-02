from __future__ import annotations
import json
import anthropic
from pathlib import Path
from .state import BlackboardState
from ..shared.tools import TOOL_DEFINITIONS, execute_tool

MAX_ITERATIONS = 20
DEFAULT_MODEL = "claude-sonnet-4-6"


class AgentRunner:
    """Runs a single agent in a tool-use loop until it calls mark_complete or hits max iterations."""

    def __init__(self, agent_name: str, system_prompt_path: Path, model: str = DEFAULT_MODEL) -> None:
        self.agent_name = agent_name
        self.system_prompt = system_prompt_path.read_text()
        self.model = model
        self.client = anthropic.Anthropic()

    def run(self, task: str, state: BlackboardState, verbose: bool = True) -> tuple[str, BlackboardState]:
        """
        Run the agent against the given task.
        Returns (summary, updated_state).
        """
        messages = [{"role": "user", "content": self._build_user_message(task, state)}]
        summary = ""

        for iteration in range(MAX_ITERATIONS):
            if verbose:
                print(f"  [{self.agent_name}] iteration {iteration + 1}")

            response = self.client.messages.create(
                model=self.model,
                max_tokens=8096,
                system=self.system_prompt,
                tools=TOOL_DEFINITIONS,
                messages=messages,
            )

            state.add_tokens(response.usage.input_tokens, response.usage.output_tokens)

            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        summary = block.text
                state.add_message(self.agent_name, summary)
                break

            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = execute_tool(block.name, block.input, state)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": result,
                    })
                    if block.name == "mark_complete":
                        parsed = json.loads(result)
                        summary = parsed.get("summary", "")
                        state.add_message(self.agent_name, summary)
                        state.completed_agents.append(self.agent_name)
                        return summary, state

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        state.completed_agents.append(self.agent_name)
        return summary, state

    def _build_user_message(self, task: str, state: BlackboardState) -> str:
        artifacts_summary = "\n".join(
            f"- {name}: {len(content)} chars" for name, content in state.artifacts.items()
        )
        prior_messages = "\n".join(
            f"[{m.agent}]: {m.content[:300]}..." if len(m.content) > 300 else f"[{m.agent}]: {m.content}"
            for m in state.messages[-5:]
        )
        return (
            f"## Your Task\n{task}\n\n"
            f"## Current Phase\n{state.phase}\n\n"
            f"## Available Artifacts\n{artifacts_summary or 'None yet'}\n\n"
            f"## Recent Squad Messages\n{prior_messages or 'None yet'}\n\n"
            "Use your tools to complete your task, then call mark_complete when done."
        )
