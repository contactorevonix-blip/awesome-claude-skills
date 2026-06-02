# Creator Squad

Multi-agent framework that builds AI agents from a task description.

## What this project does

Five specialized agents (Orchestrator, Architect, Prompt Engineer, Tool Builder, Eval Engineer)
collaborate via a shared blackboard to produce a complete agent package from a plain-language task:
`system_prompt.md`, `tools.py`, `evals.json`, and `eval_runner.py`.

## How to run

```bash
pip install -e ".[dev]"
export ANTHROPIC_API_KEY=your_key
./scripts/spawn-squad.sh "Build an agent that X"
```

## How to run tests

```bash
pytest tests/ -v --cov=framework
```

## How to run linter

```bash
ruff check framework/ && ruff format --check framework/
```

## Key architecture decisions

- **Blackboard pattern**: all agents read/write `BlackboardState` — no direct agent-to-agent calls
- **Linear flow by default**: architect → prompt_engineer → tool_builder → eval_engineer
- **Tool-use loop**: each agent runs until it calls `mark_complete` or hits 20 iterations
- **Output directory**: all agent-produced files land in `output/` (gitignored)

## Do not touch without asking

- `framework/agents/*/system_prompt.md` — these are carefully tuned; test before changing
- `framework/core/runner.py` — changing the tool loop breaks all agents
- `framework/shared/tools.py` — all agents depend on these tool definitions

## Conventions

- All new modules go under `framework/`
- Agent system prompts live in `framework/agents/{name}/system_prompt.md`
- Pydantic schemas in `framework/schemas/`
- Tests mirror source: `tests/unit/test_state.py` tests `framework/core/state.py`
