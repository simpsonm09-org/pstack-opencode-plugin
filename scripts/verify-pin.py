#!/usr/bin/env python3
"""Verify the vendored skills match the pinned upstream and the adapter sources.

Compares skills/ against the pinned pstack-claude clone and adapter/skills,
ignoring CRLF versus LF. Exit 0 on a match, 1 on any drift.
"""

import argparse
import json
import os
import pathlib
import subprocess
import sys


def default_clone() -> str:
    if os.name == "nt":
        base = os.environ.get("LOCALAPPDATA", str(pathlib.Path.home() / "AppData/Local"))
    else:
        base = str(pathlib.Path.home() / ".local" / "share")
    return str(pathlib.Path(base) / "maxstack" / "pstack-claude")


def normalize(path: pathlib.Path) -> str:
    return path.read_bytes().decode("utf-8", "surrogateescape").replace("\r\n", "\n")


def relative_files(root: pathlib.Path) -> set[str]:
    if not root.is_dir():
        return set()
    return {str(p.relative_to(root)).replace("\\", "/") for p in root.rglob("*") if p.is_file()}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=str(pathlib.Path(__file__).resolve().parent.parent))
    parser.add_argument("--clone", default=default_clone())
    args = parser.parse_args()

    repo_root = pathlib.Path(args.repo_root)
    clone = pathlib.Path(args.clone)
    lock = json.loads((repo_root / "pstack.lock.json").read_text(encoding="utf-8"))
    vendored = repo_root / "skills"

    failures: list[str] = []

    if not (clone / ".git").is_dir():
        print(f"FAIL: pinned clone not found at {clone}", file=sys.stderr)
        return 1
    head = subprocess.run(
        ["git", "-C", str(clone), "rev-parse", "HEAD"], capture_output=True, text=True, check=True
    ).stdout.strip()
    if head != lock["commit"]:
        failures.append(f"clone HEAD {head} is not the pinned commit {lock['commit']}")

    upstream_root = clone / lock["skillsPath"]
    if not upstream_root.is_dir():
        print(f"FAIL: pinned skills not found at {upstream_root}", file=sys.stderr)
        return 1

    pairs: list[tuple[str, pathlib.Path, pathlib.Path]] = []
    for source_root, label in (
        (upstream_root, "upstream"),
        (repo_root / "adapter" / "skills", "adapter"),
    ):
        for name in sorted(p.name for p in source_root.iterdir() if p.is_dir()):
            pairs.append((f"{label} skill {name}", source_root / name, vendored / name))

    checked = 0
    for label, source, target in pairs:
        if not target.is_dir():
            failures.append(f"{label}: missing vendored copy at {target}")
            continue
        source_files = relative_files(source)
        target_files = relative_files(target)
        for missing in sorted(source_files - target_files):
            failures.append(f"{label}: missing {missing}")
        for extra in sorted(target_files - source_files):
            failures.append(f"{label}: unexpected {extra}")
        for rel in sorted(source_files & target_files):
            if normalize(source / rel) != normalize(target / rel):
                failures.append(f"{label}: differs {rel}")
            checked += 1

    if failures:
        for failure in failures:
            print(f"FAIL: {failure}", file=sys.stderr)
        return 1

    print(f"PASS: {checked} files match the pin {lock['commit'][:12]}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
