---
name: pstack-opencode
description: Translate PStack's Claude-specific tools, agents, model references, and runtime assumptions to OpenCode V2
---

# PStack on OpenCode

PStack's shared skills use Claude Code tool names. OpenCode loads the same skill tree, but the agent must translate the calls and respect OpenCode's configuration model.

The global `AGENTS.md` routing instruction is best-effort. For guaranteed activation, select or request `poteto-mode` with `/poteto-mode` before the task.

## Tool mapping

| PStack reference | OpenCode V2 behavior |
| --- | --- |
| `Skill` or `/skill-name` | Call the `skill` tool with the exact path-derived skill ID. |
| `AskUserQuestion` | Call `question` when the current client supports the interactive form. Otherwise ask the question in plain text and wait. |
| `Agent` or `Task` | Call `subagent` with an installed agent ID, a description, and a prompt. Use `pstack-agent` for a worker, `pstack-reviewer` for a read-only review, or `pstack-comment-sicko` for comment review. |
| `subagent_type` | No equivalent field. Select an agent by its OpenCode ID. |
| `model` on an agent call | No per-call model field. A configured agent may name a `provider/model` and `#variant`; otherwise it inherits the parent session model. |
| `TaskCreate`, `TaskUpdate`, or `TodoWrite` | Use an uncommitted `todo.md` checklist when no task-tracking tool is available. |
| Claude Code `run` | No equivalent built-in skill. Use a project verification skill and OpenCode's available shell or browser tools. |
| Claude Code `loop` | No equivalent built-in skill. Re-check manually. |
| `subagent_type: "pstack:poteto-agent"` and the namespaced effort agents `pstack:poteto-agent-<level>` and `pstack:effort-<level>` | OpenCode has no namespaced or effort agent types. Use the installed `pstack-agent` ID for any PStack worker. There is no per-call effort agent, so a variant belongs in the agent profile's `model` line. |
| `run_in_background: true` | Use the `subagent` tool's `background: true` field. A background subagent returns at once and notifies when done. |
| `plugin-dev:skill-development` | No bundled OpenCode equivalent. Author the SKILL.md per the Agent Skills spec, keeping `name` and `description` frontmatter and progressive disclosure. |
| `.claude/skills/verify/` | Write the project verification skill to `.opencode/skills/`, OpenCode's project skill directory. `.claude/skills/` and `.agents/skills/` also resolve. |
| `~/.claude/orchestrate/<slug>/` | Use a persistent directory outside the repo that is not `~/.claude`. |
| `CLAUDE.md` | `AGENTS.md`. |
| `pstack-models.mdc` or the `pstack-models.md` override sheet | Not loaded by OpenCode. See the `setup-pstack-opencode` skill. |

Do not translate PStack's Claude model aliases such as `opus`, `fable`, or `sonnet` into OpenCode model IDs. Select real provider/model IDs from `/models`. Use the current session model unless a named OpenCode agent profile sets a model.

## Codex, Pi, and Copilot platform maps

`poteto-mode` tells a reader on Codex to open `references/codex-tools.md`, a reader on Pi to open `references/pi-tools.md`, and a reader on GitHub Copilot, CLI or app, to open `references/copilot-tools.md`. None of these mappings applies on OpenCode. Read this skill instead for the OpenCode equivalent of a Claude tool, model, or skill. Do not claim the Codex, Pi, or Copilot mappings work here.

## Model configuration

OpenCode V2 accepts an `instructions` array in `opencode.json(c)` but does not load its entries. Do not use `~/.config/opencode/pstack-models.md` through that setting. The upstream `setup-pstack` sheet does not control OpenCode subagent models. The upstream `setup-pstack` runtime table has an `opencode` row that names `~/.config/opencode/pstack-models.md` and tells the user to add it to the `instructions` array. That row is superseded. The table's GitHub Copilot row, the `setup-pstack/copilot.md` setup path, and the `setup-pstack/scripts/` sheet validators (`check-sheet.sh`, `read-sheet.sh`, `sheet.awk`, `check-sheet.awk`) are Copilot-specific and do not apply here. Use the `setup-pstack-opencode` skill, which sets a model on the agent profile instead.

For the current setup, PStack subagents inherit the active session model. To add a role-specific model, create or edit a named agent profile under `~/.config/opencode/agents/` or the project's `.opencode/agents/`. Put the confirmed `provider/model` and optional `#variant` in the profile. Keep the agent ID mapping in `AGENTS.md`. Do not claim role-specific routing until a real child session reports the selected model.

## Skill-specific notes

| Upstream skill or reference | OpenCode behavior |
| --- | --- |
| `architect` runner models | The skill takes runner models from the `architect runners` line of the `pstack-models.md` override sheet, falling back to the aliases in its `## Models` section, such as `opus`, `fable`, and `sonnet`. Do not pass those names. Choose a real `provider/model` available in the session, or inherit the session model. |
| `correct` rule table | The skill keeps its rule table in the agent instruction file. On OpenCode that is `AGENTS.md`. |
| `benchmark-checklist` tooling | The checklist names Unix tools such as `uptime`, `nproc`, `pidstat`, `strace`, `py-spy`, and `perf`. Some are absent on Windows. Use the platform equivalent and keep the checklist's seven questions. `node --cpu-prof` is the cross-platform baseline. |
| `create-verification-skill` and `maintain-verification-skill` output | Both target `.claude/skills/verify/`. On OpenCode, write the skill to `.opencode/skills/`, with `.claude/skills/` and `.agents/skills/` also resolving. |

### poteto-help

The `poteto-help` skill answers setup, `/poteto-mode`, and skill-choice questions. Its Claude Code specifics map as follows.

- The install step, `/plugin marketplace add michael-denyer/pstack-claude` and `/plugin install pstack@pstack-claude`, does not apply. On OpenCode the workspace installer installs the plugin.
- The model sheet that `/setup-pstack` writes and `CLAUDE.md` imports does not apply. Use the `setup-pstack-opencode` skill and set the model on the agent profile.
- The SessionStart hook is the plugin's session context hook in `index.ts`.
- The `subagent_type: "pstack:poteto-agent"` value maps to the installed `pstack-agent` ID.
- The body's external links are not OpenCode documentation. That covers the pstack-claude README, the pstack-claude `docs/reference.md` pages, and the pstack-claude public-copy base. Read the OpenCode guide the plugin ships under `docs/guide/` instead.
- The note that the `principle-*` leaves are hidden from the slash menu does not hold. OpenCode registers every skill through the transform, so every ID is loadable with the `skill` tool.

## Runtime-only paths

Do not read Claude Code transcript paths such as `~/.claude/projects/` from OpenCode. Use `opencode session export`, described below, or mark a transcript-dependent PStack workflow unsupported. Do not inspect OpenCode databases directly. Keep app credentials and session state in their local stores.

## Reading sessions

Mine an OpenCode session with `opencode session export <session>`, not a Claude or Codex transcript path. It prints one JSON object with `info` and `messages`, and `messages` holds the session's messages with no limit flag. Find the session ID with `opencode session list --format json`, which lists the top-level sessions in the current project, newest first. Add `--sanitize` to redact transcript and file data. A history scan such as `reflect` reads this export in place of a transcript path.

## Picking up changes

Nothing needs restarting. A changed plugin, agent profile, or skill is picked up when the next session starts, so start a new session and re-check tool availability there. From a repository directory, `opencode debug agents` lists the agents, `opencode debug config` lists the configuration sources, and `opencode api --header "x-opencode-directory:<dir>" skill.list` and `plugin.list` list the skills and plugins, where `<dir>` is that repository directory.

## Worktrees without a base

A repository with no commit has no worktree base. A playbook that delegates into a worktree, such as the Feature playbook's subagent-in-worktree step, falls back to owning the change directly.

## Nested repository config

For a session rooted in a nested repository, the ancestor `opencode.jsonc` merges and the workspace `.opencode` agents, skills, and plugin load only when the workspace root is the OpenCode project. Confirm the effective layers with `opencode debug agents`, `opencode plugin list`, and `opencode debug config`.

## Glob paths

A `glob` pattern that contains an absolute Windows path returns no matches, for example `D:\dev\...\*`, and a recursive glob can return an incomplete tree. For an absolute directory listing use the `read` tool on the directory or a shell command, and never treat an empty glob as proof a file is absent.
