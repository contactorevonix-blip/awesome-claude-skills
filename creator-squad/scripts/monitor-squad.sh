#!/usr/bin/env bash
# Monitor the Creator Squad session state.
# Usage: ./scripts/monitor-squad.sh

set -euo pipefail

STATE_FILE="output/session_state.json"

if [[ ! -f "$STATE_FILE" ]]; then
  echo "No active session. Run spawn-squad.sh first."
  exit 0
fi

python3 - <<'EOF'
import json
from pathlib import Path

state = json.loads(Path("output/session_state.json").read_text())

print("=" * 50)
print("Creator Squad — Session State")
print("=" * 50)
print(f"Task:          {state['task'][:80]}...")
print(f"Phase:         {state['phase']}")
print(f"Current agent: {state['current_agent']}")
print(f"Completed:     {', '.join(state['completed_agents']) or 'none'}")
print(f"Artifacts:     {', '.join(state['artifacts'].keys()) or 'none'}")
print(f"Tokens in:     {state['total_input_tokens']:,}")
print(f"Tokens out:    {state['total_output_tokens']:,}")

input_cost = state['total_input_tokens'] * 3.0 / 1_000_000
output_cost = state['total_output_tokens'] * 15.0 / 1_000_000
print(f"Est. cost:     ${round(input_cost + output_cost, 4)}")

if state['messages']:
    print("\nLast 3 messages:")
    for msg in state['messages'][-3:]:
        preview = msg['content'][:100].replace('\n', ' ')
        print(f"  [{msg['agent']}] {preview}...")
EOF
