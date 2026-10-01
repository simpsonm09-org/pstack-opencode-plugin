---
name: port-pstack
description: Track upstream pstack changes and port them into this OpenCode plugin faithfully, keeping vendored skills byte-identical and declaring every substitution
---

# Port upstream PStack changes

This repository is a faithful adaptation of the Cursor plugin `cursor/plugins/pstack` to OpenCode, through the pinned `michael-denyer/pstack-claude` port. The Cursor original is the authority. Do not add behavior it does not have.

Read `PORTING.md` for the policy and `CHANGES.md` for the substitutions already declared.

## Check for upstream drift

```bash
python scripts/upstream-status.py
mise run upstream-status
```

The script reads `pstack.lock.json` and `NOTICE-port.md`, fetches the pinned repository and `cursor/plugins`, and prints the commits and changed files each one moved. It exits non-zero when either has changes this port has not absorbed.

## Port a change

1. Run the status script and read the reported commits and files.
2. Read the pinned-port change and the Cursor original side by side. Where they disagree, follow the original.
3. Apply the change:
   - Vendored content changes by pin, not by hand. Bump the pin, rebuild, and keep `skills/` byte-identical.
   - An OpenCode-specific adaptation goes in an adapter skill under `adapter/skills/`. Never edit a vendored file.
4. Declare every new substitution in `CHANGES.md`.
5. Bump `pstack.lock.json`:
   - `commit` to the new `pstack-claude` commit.
   - `portOf.absorbedCommit` to the newest absorbed `cursor/plugins` commit.
6. Rebuild and mirror. `pwsh -File scripts/build.ps1` regenerates `skills/` from the pin and the adapter sources. When the pinned clone is unavailable, copy each adapter skill into `skills/<id>/` with identical LF bytes.
7. Verify. `python scripts/verify-pin.py --clone <pinned clone>` prints PASS and the file count.
8. Commit, push the branch to the personal fork and the org repository, and open a pull request against upstream `main`.

## Rules

- Keep vendored skill bodies byte-identical to the pin. Keep newlines LF.
- Put adaptations in `adapter/skills/` and agent profiles in `agents/`.
- Record every substitution in `CHANGES.md`. An undeclared substitution is a bug.
- Never edit an installed copy under `.opencode/plugins/`.
