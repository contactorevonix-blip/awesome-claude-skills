from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field
from datetime import datetime


AGENT_ORDER = ["orchestrator", "architect", "prompt_engineer", "tool_builder", "eval_engineer"]


class HandoffMessage(BaseModel):
    """Protocol for passing work between agents."""

    from_agent: str
    to_agent: str
    task: str
    context: str
    artifacts_produced: list[str] = Field(default_factory=list)
    status: Literal["pending", "in_progress", "complete", "failed"] = "pending"
    error: str = ""
    timestamp: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

    def is_terminal(self) -> bool:
        return self.status in ("complete", "failed")


class HandoffQueue:
    """FIFO queue of handoff messages managed by the orchestrator."""

    def __init__(self) -> None:
        self._queue: list[HandoffMessage] = []

    def enqueue(self, msg: HandoffMessage) -> None:
        self._queue.append(msg)

    def dequeue(self) -> HandoffMessage | None:
        return self._queue.pop(0) if self._queue else None

    def peek(self) -> HandoffMessage | None:
        return self._queue[0] if self._queue else None

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def __len__(self) -> int:
        return len(self._queue)
