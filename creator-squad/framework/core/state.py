from __future__ import annotations
import json
from datetime import datetime
from pathlib import Path
from typing import Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    agent: str
    content: str
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())


class BlackboardState(BaseModel):
    """Shared state visible to all agents in the squad."""

    task: str
    phase: str = "init"
    artifacts: dict[str, str] = Field(default_factory=dict)
    messages: list[Message] = Field(default_factory=list)
    current_agent: str = "orchestrator"
    completed_agents: list[str] = Field(default_factory=list)
    final_output_path: str = ""
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def set_artifact(self, name: str, content: str) -> None:
        self.artifacts[name] = content

    def get_artifact(self, name: str) -> str:
        return self.artifacts.get(name, "")

    def add_message(self, agent: str, content: str) -> None:
        self.messages.append(Message(agent=agent, content=content))

    def add_tokens(self, input_tokens: int, output_tokens: int) -> None:
        self.total_input_tokens += input_tokens
        self.total_output_tokens += output_tokens

    def estimated_cost_usd(self) -> float:
        # Sonnet-4-6 pricing as baseline
        input_cost = self.total_input_tokens * 3.0 / 1_000_000
        output_cost = self.total_output_tokens * 15.0 / 1_000_000
        return round(input_cost + output_cost, 4)

    def save(self, path: Path) -> None:
        path.write_text(self.model_dump_json(indent=2))

    @classmethod
    def load(cls, path: Path) -> BlackboardState:
        return cls.model_validate_json(path.read_text())

    def summary(self) -> str:
        return (
            f"Phase: {self.phase} | "
            f"Agent: {self.current_agent} | "
            f"Artifacts: {list(self.artifacts.keys())} | "
            f"Cost: ${self.estimated_cost_usd()}"
        )
