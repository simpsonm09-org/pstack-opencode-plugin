# Porting upstream PStack

This repository adapts the Cursor PStack skill tree to OpenCode. It is the source of truth for the `pstack-opencode` plugin package.

## Chain of custody

1. `cursor/plugins/pstack` is the Cursor original and the authority for fidelity.
2. `michael-denyer/pstack-claude` ports it to Claude Code and pins a Cursor commit.
3. This repository pins that port in `pstack.lock.json` and adapts it to OpenCode.
4. When pstack-claude has not merged a Cursor sync, this repository carries the newer skill under `vendor/skills/` until the pin advances.

The port stays faithful to the Cursor original. Where the Claude port and the original disagree, the original wins.

## Fidelity policy

- Every vendored file under `skills/` is byte-identical to its source after LF normalization. The tree has three source roots, the pinned `pstack-claude` clone, the port-authored `adapter/skills/`, and the upstream content in `vendor/skills/` carried ahead of the pin. `scripts/verify-pin.py` enforces all three. `vendor/skills/` is currently empty, and it remains available for a future carry.
- The OpenCode adaptation lives in port-authored files: `adapter/skills/`, `agents/`, `index.ts`, and `package.json`.
- A change that needs OpenCode-specific behavior goes in an adapter skill. It never edits a vendored body.
- Every substitution is declared in `CHANGES.md`.

## Update workflow

1. Run `python scripts/upstream-status.py`, or `mise run upstream-status`. A non-zero exit means upstream moved.
2. Read the reported commits and changed files for `pstack-claude` and `cursor/plugins`.
3. Read the pinned-port change and the Cursor original side by side. Follow the original where they disagree.
4. Apply the change:
   - Vendored content changes by pin, not by hand. Bump the pin and rebuild.
   - An OpenCode adaptation edits or adds an adapter skill under `adapter/skills/`.
5. Carry a skill ahead of the pin only when pstack-claude has not merged the sync. Copy it byte-for-byte from the newer pstack-claude commit into `vendor/skills/<id>/`, declare it under `## Vendored ahead of the pin` in `CHANGES.md`, and add the adapter note for its Claude Code specifics. When a later pin carries the skill, delete the `vendor/skills/<id>/` copy and its entry, and rebuild.
6. Declare every new substitution in `CHANGES.md`.
7. Bump `pstack.lock.json`. Set `commit` to the new `pstack-claude` commit, and set `portOf.absorbedCommit` to the newest absorbed `cursor/plugins` commit.
8. Rebuild and mirror. `pwsh -File scripts/build.ps1` regenerates `skills/` from the pin, the adapter sources, and `vendor/skills/`. When the pinned clone is unavailable, copy each adapter skill into `skills/<id>/` with identical LF bytes.
9. Verify. `python scripts/verify-pin.py --clone <pinned clone>` prints PASS and the file count.
10. Commit, push a branch to both remotes, and open a pull request against upstream `main`.

## The status script

`scripts/upstream-status.py` reads `pstack.lock.json` and `NOTICE-port.md`, fetches both upstreams into `maxstack/upstream-status/` under the user data directory, and prints commits and changed files past the pin. It keeps its own cache, so it never disturbs the clone `build.ps1` and `verify-pin.py` expect at `<data>/maxstack/pstack-claude`. It uses only the Python standard library and git, and it resolves every path from the environment, so it runs on Windows and macOS with no hardcoded drive. Run `python scripts/upstream-status.py --help` for the override flags.

## Line endings

`.gitattributes` sets `* text=auto eol=lf`. Keep newlines LF in the working tree and in git, so the parity check passes.

## The skill

`adapter/skills/port-pstack/SKILL.md` gives an agent the same workflow. The build mirrors it into `skills/port-pstack/` so the plugin registers it.
