# CHANGES: substitutions applied by the OpenCode port

This repository adapts the pinned `michael-denyer/pstack-claude` tree to OpenCode. The Cursor original `cursor/plugins/pstack` is the authority for fidelity. `PORTING.md` states the policy.

## Fidelity rule

Every vendored file under `skills/` is byte-identical to the pinned upstream commit after LF normalization. `scripts/verify-pin.py` fails on any byte difference, a missing file, or an extra file. The port edits no upstream skill body. All adaptations live in port-authored files.

## Declared substitutions

The port replaces Claude Code primitives with OpenCode equivalents. The mapping lives in the adapter skill `pstack-opencode`, and `setup-pstack-opencode` covers model selection.

| Claude Code | OpenCode |
| --- | --- |
| `Skill` tool, `/skill-name` | `skill` tool with the skill ID derived from the directory path |
| `Agent`, `Task`, `subagent_type` | `subagent` tool with an installed agent ID |
| `AskUserQuestion` | `question` tool |
| Per-call `model` on a subagent | A `model` line in the agent profile, or session inheritance |
| SessionStart hook | The `session.hook("context")` hook in `index.ts` |
| `TaskCreate`, `TaskUpdate`, `TodoWrite` | An uncommitted `todo.md` checklist |
| Claude model aliases (`opus`, `fable`) | Real provider or model IDs chosen in the workspace |

These substitutions are additive. They change how an OpenCode agent reaches a skill, not the skill body.

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

## Add a substitution

1. Change an adapter skill or an agent profile. Do not edit a vendored file.
2. Add a row to the table above with the Claude primitive and its OpenCode equivalent.
3. Keep the rebuild and parity steps in `PORTING.md` and `scripts/build.ps1` in step with the change.
