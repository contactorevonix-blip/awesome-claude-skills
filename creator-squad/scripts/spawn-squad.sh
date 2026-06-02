#!/usr/bin/env bash
# Spawn the Creator Squad for a task.
# Usage: ./scripts/spawn-squad.sh "Build an agent that reviews pull requests"

set -euo pipefail

TASK="${*}"
if [[ -z "$TASK" ]]; then
  echo "Usage: $0 '<task description>'"
  exit 1
fi

if [[ -z "${ANTHROPIC_API_KEY:-}" ]]; then
  echo "ERROR: ANTHROPIC_API_KEY is not set."
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(dirname "$SCRIPT_DIR")"

mkdir -p "$ROOT/output"

echo "Creator Squad starting..."
echo "Task: $TASK"
echo ""

cd "$ROOT"
python -m framework.core.orchestrator "$TASK"
