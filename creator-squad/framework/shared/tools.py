from __future__ import annotations
import json
from pathlib import Path


OUTPUT_DIR = Path("output")


def _ensure_output() -> None:
    OUTPUT_DIR.mkdir(exist_ok=True)


TOOL_DEFINITIONS = [
    {
        "name": "read_file",
        "description": "Read the contents of a file from the output directory.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "File name inside output/"},
            },
            "required": ["filename"],
        },
    },
    {
        "name": "write_file",
        "description": "Write content to a file in the output directory. Creates the file if it doesn't exist.",
        "input_schema": {
            "type": "object",
            "properties": {
                "filename": {"type": "string", "description": "File name inside output/"},
                "content": {"type": "string", "description": "Full content to write"},
            },
            "required": ["filename", "content"],
        },
    },
    {
        "name": "list_artifacts",
        "description": "List all files currently produced in the output directory.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "read_state",
        "description": "Read a specific artifact from the shared blackboard by name.",
        "input_schema": {
            "type": "object",
            "properties": {
                "artifact_name": {"type": "string"},
            },
            "required": ["artifact_name"],
        },
    },
    {
        "name": "mark_complete",
        "description": "Signal that this agent has finished its work and list what was produced.",
        "input_schema": {
            "type": "object",
            "properties": {
                "summary": {"type": "string", "description": "What was produced and key decisions made"},
                "artifacts": {"type": "array", "items": {"type": "string"}, "description": "File names produced"},
            },
            "required": ["summary", "artifacts"],
        },
    },
]


def execute_tool(name: str, inputs: dict, state) -> str:
    _ensure_output()

    if name == "read_file":
        path = OUTPUT_DIR / inputs["filename"]
        if not path.exists():
            return f"ERROR: {inputs['filename']} not found in output/"
        return path.read_text()

    if name == "write_file":
        path = OUTPUT_DIR / inputs["filename"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(inputs["content"])
        state.set_artifact(inputs["filename"], inputs["content"])
        return f"OK: wrote {len(inputs['content'])} chars to output/{inputs['filename']}"

    if name == "list_artifacts":
        files = list(OUTPUT_DIR.glob("**/*"))
        if not files:
            return "No artifacts yet."
        return "\n".join(str(f.relative_to(OUTPUT_DIR)) for f in files if f.is_file())

    if name == "read_state":
        artifact = state.get_artifact(inputs["artifact_name"])
        return artifact if artifact else f"No artifact named '{inputs['artifact_name']}'"

    if name == "mark_complete":
        return json.dumps({"status": "complete", "summary": inputs["summary"], "artifacts": inputs["artifacts"]})

    return f"ERROR: unknown tool '{name}'"
