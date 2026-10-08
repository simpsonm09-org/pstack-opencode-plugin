---
name: setup-pstack-opencode
description: Configure PStack subagent profiles for OpenCode without using Claude model sheets or unsupported instructions settings
---

# Set up PStack agent profiles for OpenCode

OpenCode selects subagents by agent ID. A profile can set its own model, or inherit the current session model. OpenCode does not load PStack's model sheet from the `instructions` array and does not accept Claude's per-call `model` or `subagent_type` fields.

## This supersedes the upstream opencode row

The upstream `setup-pstack` runtime table has an `opencode` row that names `~/.config/opencode/pstack-models.md` and tells the user to add that path to the `instructions` array in `opencode.json`. That row is wrong for OpenCode and this skill supersedes it.

- The upstream sheet does not control OpenCode subagent models.
- OpenCode V2 accepts an `instructions` array but does not load its entries, so adding the sheet there changes nothing.
- The supported path is a real `provider/model`, and an optional `#variant`, set on an OpenCode agent profile under `~/.config/opencode/agents/` or the project `.opencode/agents/`.

The upstream `/setup-pstack` prose about reasoning effort is Claude-specific. Its `@<level>` suffix and its effort agents do not apply here, so do not write an effort suffix onto an OpenCode profile. Express a supported model variant through the profile's `#variant` instead. Do not import the Claude model sheet.

## Current profiles

- `pstack-agent` is the default PStack worker and inherits the current session model.
- `pstack-reviewer` is read-only and inherits the current session model.
- `pstack-comment-sicko` is the read-only comment reviewer and inherits the current session model.

The profile sources are the plugin layer's `agents/` directory in the `pstack-opencode-plugin` repository. The workspace installer copies them into the workspace's `.opencode/agents` directory and strips any `model:` line from their frontmatter, so each profile runs on the session's model. Do not edit an installed copy. Edit the source profile in the plugin repository, then rerun the workspace installer.

## Add a model override

The workspace sets no model. The three pstack profiles carry no `model:` line, and the workspace installer strips one if it finds it, so a hand-edited `model:` line in an installed profile does not survive the next install. The user picks the model in the harness, and each pstack subagent runs on the session's model.

To run a pstack role on a different model, use an OpenCode agent profile outside the installer's managed set, whether project `.opencode/agents/` or a global `~/.config/opencode/agents/` entry that the installer does not overwrite. Such a profile can set its own `model:`. Use `/models` in the target project to confirm the exact `provider/model` ID and any supported variant, then run a fresh subagent session and inspect its reported model before relying on it.

This setup does not generate per-role profiles or promise multi-model diversity. Separate sessions can compare models, but the parent must still perform PStack's judging and synthesis steps.
