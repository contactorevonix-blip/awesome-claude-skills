from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Literal


class ToolDefinition(BaseModel):
    name: str
    description: str
    parameters: dict
    implementation_notes: str = ""


class EvalCase(BaseModel):
    id: str
    description: str
    input: str
    expected_behavior: str
    should_use_tools: list[str] = Field(default_factory=list)
    should_not_do: list[str] = Field(default_factory=list)


class AgentSpecification(BaseModel):
    name: str
    description: str
    purpose: str
    model: Literal["claude-opus-4-8", "claude-sonnet-4-6", "claude-haiku-4-5-20251001"] = "claude-sonnet-4-6"
    tools_needed: list[ToolDefinition] = Field(default_factory=list)
    capabilities: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    eval_cases: list[EvalCase] = Field(default_factory=list)
    system_prompt_draft: str = ""
    output_format: str = ""
    requires_memory: bool = False
    requires_tools: bool = True
    estimated_tokens_per_run: int = 0
