# pstack-opencode-plugin working agreements

An OpenCode plugin that ports PStack into OpenCode.

## Ground rules

- `skills/` is generated. Do not hand-edit it. Change a vendored file by bumping the pin in `pstack.lock.json` and running `scripts/build.ps1`, or add an adapter skill under `adapter/skills/`.
- The Cursor original is the authority for fidelity. Where the Claude port and the original disagree, the original wins.
- Every substitution is declared in `CHANGES.md`.
- The build regenerates `LICENSE`, `LICENSE-cursor-team-kit`, `NOTICE`, and `NOTICE-port.md`. Do not hand-edit them. Port-authored code is under `LICENSE-port`.
- Keep newlines LF. `.gitattributes` sets `text=auto eol=lf`, and the pin check fails on CRLF.
- No secret, credential, or machine path is committed.

## Commands

- `just install`, `just lint`, `just pin`, `just verify`.
- `pwsh -File scripts/build.ps1` regenerates `skills/`.
- `python scripts/verify-pin.py --clone <clone>` proves the tree matches the pin.
- `python scripts/upstream-status.py` reports upstream drift.

## Repo facts

- Language and toolchain: TypeScript and Node. The pinned upstream clone lives at `%LOCALAPPDATA%\maxstack\pstack-claude`.
- The port chain is `cursor/plugins/pstack` to `michael-denyer/pstack-claude` to this repository.
- The current pin is `pstack-claude` `dc8e617`, absorbing `cursor/plugins` `e43c7ee` and PStack v0.15.9.
- `pstack.lock.json` is the single source of the pinned repository and commit.
- Vendored skills are byte-identical to the pin after LF normalization. The substitutions are additive, live in the adapter skills, and are declared in `CHANGES.md`.
- Docs: `PORTING.md` states the policy, `CHANGES.md` the substitutions, and the README the layout and the license.

## Skills

No repo-local skills. The adapter skills under `adapter/skills/` are part of the package.
