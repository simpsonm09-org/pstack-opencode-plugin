# CHANGES: substitutions applied by the OpenCode port

This repository adapts the pinned `michael-denyer/pstack-claude` tree to OpenCode. The Cursor original `cursor/plugins/pstack` is the authority for fidelity. `PORTING.md` states the policy.

This tree is pinned to `michael-denyer/pstack-claude` `8d3aa571` (version 0.9.73), absorbing `cursor/plugins` `2cbf585` (PStack v0.15.13).

## Fidelity rule

Every vendored file under `skills/` is byte-identical to its source after LF normalization. `scripts/verify-pin.py` fails on any byte difference, a missing file, or an extra file. The port edits no upstream skill body. All adaptations live in port-authored files.

## Vendored ahead of the pin

`vendor/skills/` holds upstream content sourced from a pstack-claude commit newer than the pin, for a change pstack-claude has not merged. It is upstream-sourced, not port-authored. `scripts/build.ps1` mirrors each `vendor/skills/<id>/` into `skills/<id>/`, and `scripts/verify-pin.py` byte-checks the copy against the vendor source the same way it checks the pin and the adapter.

An entry moves into the pinned set when the pin advances to a commit that carries it. Reconcile every one of these in the same change. Remove the `vendor/skills/<id>/` copy, because the pinned clone then supplies the skill. Remove the entry under `## Vendored ahead of the pin`. Bump `portOf.absorbedCommit` in `pstack.lock.json` to the newly absorbed `cursor/plugins` commit. Update the `pstack.lock.json` notes to drop the carried-ahead wording for that skill. Update the pin sentences in `README.md` and this file. Then rebuild and run the pin check. `scripts/verify-pin.py` now fails when a `vendor/skills/<id>/` entry is also present in the pinned upstream, so the removal cannot be forgotten.

The vendor copy's fidelity to its source pstack-claude commit is checked by hand at port time, because `scripts/verify-pin.py` compares `skills/` against the local `vendor/skills/` copy and not against the source commit, which is not in the pinned clone.

There are no current entries. `poteto-help` moved into the pinned set when the pin advanced to `8d3aa571`, so `vendor/skills/` is empty and the mechanism remains available for a future carry.

## Declared substitutions

The port replaces Claude Code primitives with OpenCode equivalents. The mapping lives in the adapter skill `pstack-opencode`, and `setup-pstack-opencode` covers model selection.

| Upstream primitive | OpenCode |
| --- | --- |
| `Skill` tool, `/skill-name` | `skill` tool with the skill ID derived from the directory path |
| `Agent`, `Task`, `subagent_type` | `subagent` tool with an installed agent ID |
| `AskUserQuestion` | `question` tool |
| Per-call `model` on a subagent | A `model` line in the agent profile, or session inheritance |
| SessionStart hook | The `session.hook("context")` hook in `index.ts` |
| `TaskCreate`, `TaskUpdate`, `TodoWrite` | An uncommitted `todo.md` checklist |
| Claude model aliases (`opus`, `fable`) | Real provider or model IDs chosen in the workspace |
| `subagent_type: "pstack:poteto-agent"` and the namespaced effort agents `pstack:poteto-agent-<level>` and `pstack:effort-<level>` | The installed `pstack-agent` ID. There is no per-call effort agent. Put a supported variant on the profile's `model` line instead. |
| `run_in_background: true` | The `background: true` field on the `subagent` tool. A background subagent returns at once and notifies when done. |
| Claude Code `run` | No OpenCode built-in. Use a project verification skill and OpenCode's shell or browser tools. |
| Claude Code `loop` | No OpenCode built-in. Re-check manually, or use an explicit OpenChamber scheduled task when the task fits. |
| Claude Code transcript paths such as `~/.claude/projects/` | The `openchamber` tool's `session.messages` action, or mark the workflow unsupported. The `last` and `limit` fields cannot be combined. |
| `plugin-dev:skill-development` | No bundled OpenCode equivalent. Author the SKILL.md per the Agent Skills spec, with `name` and `description` frontmatter and progressive disclosure. |
| `.claude/skills/verify/` | `.opencode/skills/`, OpenCode's project skill directory, with `.claude/skills/` and `.agents/skills/` also resolving. |
| `~/.claude/orchestrate/<slug>/` | A persistent directory outside the repo that is not `~/.claude`. |
| `CLAUDE.md` | `AGENTS.md`. |
| `pstack-models.mdc` or the `pstack-models.md` override sheet | Not loaded by OpenCode. The workspace model policy owns the injected `model:` line, and the installer overwrites a hand-edited one. Point at the workspace model policy, or a genuine project or global agent override that the installer does not manage. See the `setup-pstack-opencode` skill. |
| Codex `references/codex-tools.md` and Pi `references/pi-tools.md` platform maps | Not applicable on OpenCode. Read the `pstack-opencode` skill for the OpenCode equivalent. |
| Claude and Cursor runner model IDs in `architect` | The `architect` skill takes runner models from the `architect runners` line of the `pstack-models.md` override sheet, falling back to Claude aliases such as `opus`, `fable`, and `sonnet`. Do not pass those names. Choose a real `provider/model` available in the session, or use the session model. |
| Unix perf tooling in `benchmark-checklist` (`uptime`, `nproc`, `pidstat`, `strace`, `py-spy`, `perf`) | The platform equivalent, with `node --cpu-prof` as the cross-platform baseline. Keep the checklist's seven questions. |
| The upstream `setup-pstack` `opencode` runtime row | Superseded by the `setup-pstack-opencode` skill, which sets a model on the agent profile instead of the `instructions` array. |
| The `correct` rule table | Kept in the agent instruction file, which on OpenCode is `AGENTS.md`. |
| `poteto-help` Claude Code specifics (the `/plugin marketplace` install, the `pstack-models.md` sheet import, the SessionStart hook, and `subagent_type: "pstack:poteto-agent"`) | The workspace installer installs the plugin, the `setup-pstack-opencode` skill sets the model on the agent profile, the plugin's session context hook in `index.ts` is the SessionStart hook, and the installed `pstack-agent` ID replaces the `subagent_type`. See the `### poteto-help` note in the adapter skill `pstack-opencode`. |

These substitutions are additive. They change how an OpenCode agent reaches a skill, not the skill body.

The adapter also carries accuracy edits that are not substitutions, for example the `port-pstack` step 9 verify wording, and those are tracked in the diff rather than the table.

## Port-authored files

These files are authored for this port and are not vendored:

- `adapter/skills/pstack-opencode/SKILL.md`
- `adapter/skills/setup-pstack-opencode/SKILL.md`
- `adapter/skills/port-pstack/SKILL.md`
- `adapter/AGENTS.md`
- `agents/pstack-agent.md`, `agents/pstack-reviewer.md`, `agents/pstack-comment-sicko.md`
- `index.ts`, `package.json`
- `CHANGES.md`, `PORTING.md`, `README.md`
- `scripts/build.ps1`, `scripts/verify-pin.py`, `scripts/upstream-status.py`
- `docs/README.md`, `docs/guide/README.md`, `docs/guide/principles.md`, `docs/guide/verification.md`, `docs/guide/workflows.md`, `docs/guide/prompts.md`

The guide is port-authored and OpenCode-adapted from the upstream pstack guide and the pstack article series.

## Add a substitution

1. Change an adapter skill or an agent profile. Do not edit a vendored file.
2. Add a row to the table above with the Claude primitive and its OpenCode equivalent.
3. Keep the rebuild and parity steps in `PORTING.md` and `scripts/build.ps1` in step with the change.
