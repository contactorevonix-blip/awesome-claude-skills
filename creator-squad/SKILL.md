---
name: creator-squad
description: Multi-agent framework that builds AI agents from a task description. Five specialized agents collaborate — Architect, Prompt Engineer, Tool Builder, Eval Engineer, and Orchestrator — each doing one job well.
---

# Creator Squad

A squad of specialized AI agents that work together to build other AI agents. You describe what you need, the squad designs it, writes it, and tests it.

## When to Use This Skill

- You need a Claude agent for a specific, repeatable task
- You want a fully specified agent: system prompt, tools, and eval suite
- You are building an AI product and need a reliable agent foundation
- You want a second opinion on agent architecture before writing code

## What This Skill Does

1. **Architect** — Analyses your request and produces a complete agent specification (tools, capabilities, constraints, eval cases)
2. **Prompt Engineer** — Writes the system prompt from the spec using proven prompt engineering patterns
3. **Tool Builder** — Implements every tool the agent needs as runnable Python with Anthropic tool definitions
4. **Eval Engineer** — Creates a test suite (12+ cases) that validates the agent works correctly
5. **Orchestrator** — Coordinates all agents, enforces quality gates, and delivers the final package

## How to Use

### Quick Start

```
Build an agent that reviews Python pull requests for security vulnerabilities
```

### With More Context

```
Build an agent that helps customer support teams classify incoming tickets.
It should: read the ticket text, assign a category (billing/technical/general),
assign a priority (low/medium/high/critical), and suggest a reply template.
We handle about 500 tickets/day. Team uses Zendesk.
```

### Via Script

```bash
./scripts/spawn-squad.sh "Build an agent that monitors GitHub Actions and summarises failures"
```

### Via GitHub Actions

Trigger the `orchestrate.yml` workflow with your task description. The built agent is uploaded as a workflow artifact.

## What Gets Produced

```
output/
├── agent_spec.json     Complete specification (tools, capabilities, constraints)
├── system_prompt.md    Ready to use — copy into your project
├── tools.py            Anthropic tool definitions + implementations
├── evals.json          12+ test cases across 5 categories
├── eval_runner.py      Run this to validate the agent works
└── session_state.json  Full session log with token usage and cost
```

## Framework Structure

```
creator-squad/
├── SKILL.md
├── framework/
│   ├── core/
│   │   ├── orchestrator.py    Main loop — coordinates all agents
│   │   ├── runner.py          Single agent runner with tool-use loop
│   │   ├── state.py           Shared blackboard — all agents read/write here
│   │   └── handoff.py         Handoff protocol between agents
│   ├── agents/
│   │   ├── orchestrator/      Coordinates, enforces quality gates
│   │   ├── architect/         Designs the agent specification
│   │   ├── prompt_engineer/   Writes the system prompt
│   │   ├── tool_builder/      Implements tools in Python
│   │   └── eval_engineer/     Creates the test suite
│   ├── shared/
│   │   └── tools.py           Tools available to all squad agents
│   └── schemas/
│       └── agent_spec.py      Pydantic schema for agent specifications
├── scripts/
│   ├── spawn-squad.sh         Run the squad locally
│   └── monitor-squad.sh       Check session state and cost
└── workflows/
    └── orchestrate.yml        GitHub Actions trigger
```

## How the Squad Works

```
Your request
      ↓
Orchestrator reads the task
      ↓
Architect → agent_spec.json
      ↓ (quality gate: valid JSON, 5+ eval cases)
Prompt Engineer → system_prompt.md
      ↓ (quality gate: >300 words, all sections present)
Tool Builder → tools.py
      ↓ (quality gate: TOOL_DEFINITIONS + execute_tool, no stubs)
Eval Engineer → evals.json + eval_runner.py
      ↓ (quality gate: 12+ cases, all 5 categories)
Orchestrator delivers final package
```

## Agent Models

| Agent | Model | Why |
|-------|-------|-----|
| Orchestrator | claude-opus-4-8 | Complex coordination and quality judgment |
| Architect | claude-sonnet-4-6 | Structured analysis and specification |
| Prompt Engineer | claude-sonnet-4-6 | Nuanced writing and pattern application |
| Tool Builder | claude-sonnet-4-6 | Code generation with reliability |
| Eval Engineer | claude-sonnet-4-6 | Test case design and coverage thinking |

## Shared State (Blackboard)

All agents read and write to a shared `BlackboardState`. This means:
- Every agent sees what previous agents produced
- No information is lost between handoffs
- The full session is serializable to disk
- Sessions can be resumed after failure

Key state fields:
- `task` — the original user request (never changes)
- `phase` — current agent working
- `artifacts` — dict of filename → content (all produced files)
- `messages` — log of what each agent said
- `total_input_tokens` / `total_output_tokens` — running cost tracker

## Instructions

When this skill is invoked:

1. Ask for the task if not provided: "What agent do you want to build?"
2. If running locally: check `ANTHROPIC_API_KEY` is set, then run `./scripts/spawn-squad.sh '<task>'`
3. If in Claude Code: run `python -m framework.core.orchestrator '<task>'` from the `creator-squad/` directory
4. Monitor progress with `./scripts/monitor-squad.sh`
5. When complete, read `output/session_state.json` for the cost summary
6. Deliver the contents of `output/` to the user

If a quality gate fails, the Orchestrator will automatically retry that agent with specific feedback. No manual intervention needed.

## Setup

```bash
# Install dependencies
pip install anthropic pydantic httpx

# Set API key
export ANTHROPIC_API_KEY=your_key_here

# Run the squad
./scripts/spawn-squad.sh "Build an agent that X"
```

## Examples

### Example 1: Code Review Agent

**Input**: "Build an agent that reviews Python pull requests for security vulnerabilities"

**Architect produces:**
```json
{
  "name": "python-security-reviewer",
  "model": "claude-sonnet-4-6",
  "tools_needed": [
    {"name": "read_file", "description": "Read a Python source file"},
    {"name": "search_pattern", "description": "Search for dangerous patterns in code"},
    {"name": "write_report", "description": "Write the security review report"}
  ],
  "capabilities": [
    "Detect SQL injection patterns",
    "Find hardcoded secrets",
    "Identify insecure deserialization",
    "Flag missing input validation"
  ],
  "constraints": [
    "Never suggest fixing code directly — only report findings",
    "Never hallucinate vulnerabilities — only flag patterns present in the code"
  ]
}
```

**Prompt Engineer produces**: A system prompt that instructs the agent to read each file, check each vulnerability class in sequence, and output findings as `[SEVERITY] file:line — description`.

**Tool Builder produces**: `tools.py` with `read_file`, `search_pattern`, and `write_report` fully implemented.

**Eval Engineer produces**: 12 cases including: a clean file (no findings expected), a file with SQL injection, a file with a hardcoded API key, an empty file, a file with a false positive pattern.

---

### Example 2: Support Ticket Classifier

**Input**: "Build an agent that classifies customer support tickets and suggests reply templates"

**Output**: An agent with tools to read ticket text, classify into billing/technical/general, assign priority, and select from a template library. Includes 14 eval cases covering ticket types, edge cases (no category fits), and multilingual inputs.

---

### Example 3: Data Pipeline Monitor

**Input**: "Build an agent that checks our daily ETL jobs, detects failures, and sends a Slack summary"

**Output**: An agent with tools to query job logs, detect anomalies, format a Slack message, and post it via webhook. Eval suite includes: all jobs green, one job failed, all jobs failed, job data missing.

## Tips

- The more context you give, the better the spec. Include: who uses the agent, what inputs it receives, what it should output, any constraints.
- The squad runs in 3-8 minutes depending on complexity.
- Typical cost: $0.05–$0.30 per agent built.
- The produced `system_prompt.md` and `tools.py` are ready to use — just copy them into your project.
- Run `eval_runner.py` before using the agent in production.

## Common Use Cases

- Building agents for internal tools (Slack bots, Notion integrations, CI assistants)
- Prototyping an AI feature before committing to a full implementation
- Getting a second architectural opinion on an agent you are already building
- Creating eval suites for existing agents that lack test coverage
