#!/usr/bin/env python3
"""Repo checks: run from the repo root. Exits 1 on any failure."""
import hashlib
import pathlib
import py_compile
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[2]
MAX_DESC = 500
errors = []


def skills():
    return sorted(p for p in ROOT.iterdir() if p.is_dir() and not p.name.startswith(".") and (p / "SKILL.md").exists())


def frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    if not m:
        return None
    fm = {}
    for line in m.group(1).splitlines():
        k, _, v = line.partition(":")
        fm[k.strip()] = v.strip()
    return fm


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


found = skills()
if not found:
    errors.append("no skill folders found")

root_license = sha(ROOT / "LICENSE")
shared = {}
for s in found:
    fm = frontmatter((s / "SKILL.md").read_text(encoding="utf-8"))
    if fm is None:
        errors.append(f"{s.name}/SKILL.md: missing frontmatter")
        continue
    if fm.get("name") != s.name:
        errors.append(f"{s.name}/SKILL.md: frontmatter name {fm.get('name')!r} != folder name")
    desc = fm.get("description", "")
    if not desc:
        errors.append(f"{s.name}/SKILL.md: missing description")
    elif len(desc) > MAX_DESC:
        errors.append(f"{s.name}/SKILL.md: description is {len(desc)} chars, limit {MAX_DESC}")
    for req in ("README.md", "LICENSE"):
        if not (s / req).exists():
            errors.append(f"{s.name}: missing {req}")
    if (s / "LICENSE").exists() and sha(s / "LICENSE") != root_license:
        errors.append(f"{s.name}/LICENSE differs from root LICENSE")
    for py in sorted(s.glob("scripts/*.py")):
        try:
            py_compile.compile(str(py), doraise=True)
        except py_compile.PyCompileError as e:
            errors.append(f"{py.relative_to(ROOT)}: {e.msg}")
        shared.setdefault(py.name, {})[s.name] = sha(py)

for name, copies in shared.items():
    if len(copies) > 1 and len(set(copies.values())) > 1:
        errors.append(f"scripts/{name} differs between {', '.join(sorted(copies))}; keep the copies identical")

for e in errors:
    print("FAIL:", e)
if errors:
    sys.exit(1)
print(f"ok: {len(found)} skills checked ({', '.join(s.name for s in found)})")
