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

1. Run the status script.
2. Read the reported commits and changed files.
3. Read the pinned-port change and the Cursor original side by side. Where they disagree, follow the original.
4. Apply the change:
   - Vendored content changes by pin, not by hand. Bump the pin, rebuild, and keep `skills/` byte-identical.
   - An OpenCode-specific adaptation goes in an adapter skill under `adapter/skills/`. Never edit a vendored file.
5. Carry a skill ahead of the pin only when pstack-claude has not merged the sync. Copy it byte-for-byte from the newer pstack-claude commit into `vendor/skills/<id>/`, declare it under `## Vendored ahead of the pin` in `CHANGES.md`, and add the adapter note for its Claude Code specifics. When a later pin carries the skill, delete the `vendor/skills/<id>/` copy and its entry, and rebuild.
6. Declare every new substitution in `CHANGES.md`.
7. Bump `pstack.lock.json`:
   - `commit` to the new `pstack-claude` commit.
   - `portOf.absorbedCommit` to the newest absorbed `cursor/plugins` commit.
8. Rebuild and mirror. `pwsh -File scripts/build.ps1` regenerates `skills/` from the pin, the adapter sources, and `vendor/skills/`. When the pinned clone is unavailable, copy each adapter skill into `skills/<id>/` with identical LF bytes.
9. Verify. `python scripts/verify-pin.py --clone <pinned clone>` compares `skills/` against the pinned upstream skills, the adapter skills, and `vendor/skills/`. It prints PASS and the file count on success, and fails on any missing, extra, or differing file.
10. Commit, push the branch to the personal fork and the org repository, and open a pull request against upstream `main`.

## Rules

- Keep vendored skill bodies byte-identical to the pin. Keep newlines LF.
- Content carried ahead of the pin under `vendor/skills/` is upstream-sourced, declared under `## Vendored ahead of the pin` in `CHANGES.md`, and removed when the pin advances.
- Put adaptations in `adapter/skills/` and agent profiles in `agents/`.
- Record every substitution in `CHANGES.md`. An undeclared substitution is a bug.
- Never edit an installed copy under `.opencode/plugins/`.
