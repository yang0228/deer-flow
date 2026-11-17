---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. This skill should be used when the user is looking for functionality that might exist as an installable skill.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## Choose the Installation Environment First

In a **DeerFlow agent sandbox**, discover skills but do not run the bundled
`scripts/install-skill.sh` helper. It requires a host repository checkout with
`deer-flow.code-workspace` in the current directory or an ancestor. A normal
sandbox workspace such as `/mnt/user-data/workspace` is not that checkout.
The projected `/mnt/skills/public`, `/mnt/skills/custom` and `/mnt/skills/legacy`
directories are read-only; do not write or symlink into them. A sandbox-global
`npx skills add -g` installation or files in a thread workspace/output directory
do not persist a skill in DeerFlow's per-user catalog for future chats.

Use the DeerFlow options in Step 4. The host helper is only for an operator
managing a repository checkout, not a substitute for user-scoped installation.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Search for Skills

Run the find command with a relevant query:

```bash
npx skills find [query]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

Results identify skills and their catalog links, for example:

```
vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

Any install command printed by an external catalog still needs the environment
check above; it is not a DeerFlow persistence mechanism.

### Step 3: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The installation option appropriate to their environment (Step 4)
3. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

In DeerFlow, a complete .skill archive can be imported through
Capability Center > Skills > Community with administrator permissions.

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 4: Install the Skill

#### Inside DeerFlow: text-only custom skills

The `skill_manage` tool is available **only when the operator enables
`skill_evolution.enabled` (default: `false`)**. Check the actual available tools;
do not assume it is present merely because this is DeerFlow.

When it is available and the user authorizes creating a text-only custom skill,
use `skill_manage(action="create", name=..., content=...)` for valid `SKILL.md`
content, `action="edit"` to replace it, and `action="write_file", path=...,
content=...` for text supporting files. These calls use the caller's per-user
skill storage and normal validation/security scans. Check each result before
reporting success.

This is not an archive installer or an atomic multi-file import. It cannot
preserve arbitrary binary assets (images, fonts, compiled files, etc.) through
text `content` arguments. Do not silently omit those resources or claim a
complete third-party package was installed by copying only its instructions.

#### Inside DeerFlow: complete skill packages

For a complete `.skill` archive, direct the user to **Capability Center > Skills >
Community** and select **Install .skill**. It installs into **My skills** through the existing
archive validation and security checks. The install/upload routes require
administrator authorization; being able to chat does not grant permission to
import. If the user lacks permission, ask them to contact their administrator.

If `skill_manage` is unavailable or a required operation is not permitted,
explain that limitation and offer the authorized archive-import/operator route.
You may help prepare a package for review, but a sandbox file is only an artifact,
not an installed skill. Do not bypass authorization or change mounts to install.

#### On the host: operator-managed repository checkout

Only for an operator intentionally managing the host checkout, run the bundled
helper **from the DeerFlow repository root or a nested directory**:

```bash
bash /path/to/skill/scripts/install-skill.sh <owner/repo@skill-name>
```

It uses `npx skills add ... -g -y` to install under the host's
`$HOME/.agents/skills/<skill-name>` and links that directory into the checkout's
`skills/custom/`. This is operator-managed repository configuration, not a
per-user DeerFlow installation. Without the checkout marker it exits nonzero
with a diagnostic before invoking the installer.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Offer to create a text-only skill with `skill_manage` if available in DeerFlow,
   or help prepare a `.skill` archive for authorized import. Outside DeerFlow,
   the user can use `npx skills init` in their own development environment.

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, I can help prepare a custom skill using
the creation or import options available in your environment.
```
