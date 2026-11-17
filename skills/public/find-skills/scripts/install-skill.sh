#!/bin/bash

# Host-only helper: install globally and link into a DeerFlow repository checkout.
# Run from the checkout or a nested directory, not an isolated agent sandbox.
# Usage: bash /path/to/find-skills/scripts/install-skill.sh <owner/repo@skill-name>

set -e

if [[ -z "$1" ]]; then
  echo "Usage: $0 <owner/repo@skill-name>" >&2
  echo "Example: $0 vercel-labs/agent-skills@vercel-react-best-practices" >&2
  exit 1
fi

FULL_SKILL_NAME="$1"

# Extract skill name (the part after @)
SKILL_NAME="${FULL_SKILL_NAME##*@}"

if [[ ! "$FULL_SKILL_NAME" =~ ^[^/@[:space:]]+/[^/@[:space:]]+@[^/@[:space:]]+$ ]]; then
  echo "Error: Invalid skill format. Expected: owner/repo@skill-name" >&2
  exit 1
fi

# Find project root by looking for deer-flow.code-workspace
find_project_root() {
  local dir="$PWD"
  while [[ "$dir" != "/" ]]; do
    if [[ -f "$dir/deer-flow.code-workspace" ]]; then
      echo "$dir"
      return 0
    fi
    dir="$(dirname "$dir")"
  done
  echo ""
  return 1
}

if ! PROJECT_ROOT=$(find_project_root); then
  echo "Error: This host-only helper requires a DeerFlow repository checkout (deer-flow.code-workspace not found)." >&2
  echo "Run it on the host from the checkout or a nested directory. In DeerFlow, use Capability Center > Skills > Community to import a .skill archive with administrator permissions." >&2
  exit 1
fi

SKILL_SOURCE="$HOME/.agents/skills/$SKILL_NAME"
SKILL_TARGET="$PROJECT_ROOT/skills/custom"

# Step 1: Install the skill using npx
npx skills add "$FULL_SKILL_NAME" -g -y > /dev/null 2>&1

# Step 2: Verify installation
if [[ ! -d "$SKILL_SOURCE" ]]; then
  echo "Skill '$SKILL_NAME' installation failed" >&2
  exit 1
fi

# Step 3: Create symlink
mkdir -p "$SKILL_TARGET"
ln -sf "$SKILL_SOURCE" "$SKILL_TARGET/"

echo "Skill '$SKILL_NAME' installed successfully"
