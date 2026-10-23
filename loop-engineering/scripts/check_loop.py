#!/usr/bin/env python3
"""Deterministic verification runner for the `loop-engineering` skill.

Automates the mechanical, CI-grade checks for a build unit or subsystem and emits
structured JSON evidence to stdout. The LLM verifier layer consumes this JSON to
perform judgment checks (test fidelity, behavioral drive, and semantic acceptance).

Features:
- Discovers unit specs in history/units/, specs/, or units/
- Parses enumerated test IDs (T1..Tn, T1.1..Tn.m) and acceptance criteria
- Validates test collection mapping against test files in tests/
- Executes configured test suite and linters (supporting CONFIG.md overrides)
- Emits structured JSON summary

Usage:
    python check_loop.py NN            # e.g. python check_loop.py 01
    python check_loop.py <path-to-spec> # e.g. python check_loop.py history/units/01-scaffold.md
"""

from __future__ import annotations

import glob
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
from pathlib import Path


def find_repo_root() -> Path:
    cur = Path.cwd().resolve()
    for parent in [cur, *cur.parents]:
        if (parent / ".git").exists() or (parent / "pyproject.toml").exists() or (parent / "package.json").exists() or (parent / "CLAUDE.md").exists():
            return parent
    return cur


REPO = find_repo_root()


def _repo(*parts: str) -> Path:
    return REPO.joinpath(*parts)


def load_config() -> dict[str, str]:
    """Load configuration from CONFIG.md in skill paths or repo root."""
    candidate_paths = [
        _repo(".agent", "skills", "loop-engineering", "CONFIG.md"),
        _repo(".claude", "skills", "loop-engineering", "CONFIG.md"),
        _repo("CONFIG.md"),
    ]
    cfg = {}
    for p in candidate_paths:
        if p.is_file():
            try:
                for line in p.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if line and not line.startswith("#") and ":" in line:
                        k, v = line.split(":", 1)
                        cfg[k.strip()] = v.strip()
                break
            except Exception:
                pass
    return cfg


CONFIG = load_config()


def tool_cmd(tool: str, *args: str) -> list[str]:
    """Prefer uv/npm when available; fallback to executable in PATH or python -m."""
    if shutil.which("uv") and ((REPO / "uv.lock").exists() or (REPO / "pyproject.toml").exists()):
        return ["uv", "run", tool, *args]
    if shutil.which(tool):
        return [tool, *args]
    return [sys.executable, "-m", tool, *args]


def run_cmd(cmd: list[str] | str) -> tuple[int, str]:
    """Run command from REPO root and return (exit_code, output)."""
    try:
        proc = subprocess.run(
            cmd if isinstance(cmd, list) else shlex.split(cmd),
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=600,
        )
        return proc.returncode, (proc.stdout + proc.stderr)
    except Exception as e:
        return 1, f"Failed to execute {cmd}: {e}"


def last_summary_line(output: str) -> str:
    lines = [ln.strip() for ln in output.splitlines() if ln.strip()]
    return lines[-1] if lines else ""


def find_spec_path(target: str) -> Path | None:
    p = Path(target)
    if p.is_file():
        return p.resolve()
    if (_repo(target)).is_file():
        return _repo(target)

    search_patterns = [
        f"history/units/{target}-*.md",
        f"history/units/*{target}*.md",
        f"specs/{target}-*.md",
        f"specs/{target}.md",
        f"units/{target}-*.md",
        f"specs/*{target}*.md",
    ]
    for pattern in search_patterns:
        matches = sorted(glob.glob(str(_repo(pattern))))
        if matches:
            return Path(matches[0])
    return None


def parse_spec(spec_path: Path) -> dict:
    text = spec_path.read_text(encoding="utf-8")

    seen: list[str] = []
    # Capture both T1, T01, and sub-tokens like T2.1, T2.2
    for m in re.finditer(r"\*\*(T\d+(?:\.\d+)?)\b", text):
        tid = m.group(1)
        if tid not in seen:
            seen.append(tid)

    criteria: list[str] = []
    in_section = False
    for line in text.splitlines():
        if re.match(r"^##\s+Acceptance criteria\b", line, re.IGNORECASE):
            in_section = True
            continue
        if not in_section:
            continue
        if line.startswith("## "):
            break
        stripped = line.lstrip()
        if stripped.startswith("- ") or stripped.startswith("- [ ]") or stripped.startswith("- [x]"):
            clean = re.sub(r"^-(\s*\[[\sxX]\])?\s*", "", stripped)
            if clean:
                criteria.append(clean)
        elif stripped and criteria and line[:1] in " \t":
            criteria[-1] += " " + stripped

    rel_path = str(spec_path.relative_to(REPO)) if spec_path.is_relative_to(REPO) else str(spec_path)
    return {
        "test_ids": seen,
        "criteria": criteria,
        "spec_file": rel_path,
        "title": spec_path.stem,
    }


def find_test_files(target: str, spec_title: str = "") -> list[str]:
    keywords = [target]
    if spec_title:
        parts = re.split(r"[-_\s]+", spec_title.lower())
        keywords.extend([p for p in parts if len(p) > 2])

    test_dir_name = CONFIG.get("TESTS_DIR", "tests")
    test_dir = _repo(test_dir_name)
    if not test_dir.is_dir():
        return []

    valid_exts = (".py", ".ts", ".js", ".mjs", ".tsx", ".jsx")
    found: set[str] = set()
    for root, _, files in os.walk(str(test_dir)):
        for f in files:
            f_lower = f.lower()
            if not f_lower.endswith(valid_exts):
                continue
            if not (f_lower.startswith("test_") or ".test." in f_lower or ".spec." in f_lower):
                continue
            full_rel = str(Path(root, f).relative_to(REPO))
            if any(k in f_lower for k in keywords):
                found.add(full_rel)
    return sorted(list(found))


def test_mapping(target: str, test_ids: list[str], test_files: list[str]) -> dict:
    result: dict = {
        "files_found": test_files,
        "file_exists": bool(test_files),
        "mapped": [],
        "missing": [],
        "collect_exit": None,
    }
    if not test_ids:
        return result
    if not test_files:
        result["missing"] = list(test_ids)
        return result

    # Check for pytest or fallback to file content text inspection
    has_pytest = shutil.which("pytest") or (shutil.which("uv") and ((REPO / "uv.lock").exists() or (REPO / "pyproject.toml").exists()))
    lowered = ""
    if has_pytest and any(f.endswith(".py") for f in test_files):
        py_files = [f for f in test_files if f.endswith(".py")]
        code, out = run_cmd(tool_cmd("pytest", *py_files, "--collect-only", "-q"))
        result["collect_exit"] = code
        lowered = out.lower()
    else:
        # Static file inspection fallback across test files
        collected_text = []
        for tf in test_files:
            try:
                collected_text.append(_repo(tf).read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                pass
        lowered = " ".join(collected_text).lower()
        result["collect_exit"] = 0

    for tid in test_ids:
        # e.g. T1 -> t1, T2.1 -> t2[._]?1
        num = tid[1:].replace(".", r"[._]?")
        pattern = rf"(?<![a-z0-9])t{num}(?![0-9])"
        if re.search(pattern, lowered):
            result["mapped"].append(tid)
        else:
            result["missing"].append(tid)
    return result


def gate_tests(test_files: list[str]) -> dict:
    custom_cmd = CONFIG.get("TEST_COMMAND")
    if custom_cmd:
        code, out = run_cmd(custom_cmd)
        return {
            "exit": code,
            "summary": last_summary_line(out),
            "passed": code == 0,
            "command": custom_cmd,
        }

    targets = test_files if test_files else ["tests"]
    code, out = run_cmd(tool_cmd("pytest", *targets, "-q"))
    empty = code == 5  # No tests collected
    return {
        "exit": code,
        "summary": last_summary_line(out),
        "empty_ok": empty,
        "passed": code == 0 or empty,
        "command": "pytest",
    }


def gate_linter() -> dict:
    lint_cmd = CONFIG.get("LINT_COMMAND")
    fmt_cmd = CONFIG.get("FORMAT_COMMAND")

    if lint_cmd:
        check_code, check_out = run_cmd(lint_cmd)
        fmt_code, fmt_out = (0, "skipped") if not fmt_cmd else run_cmd(fmt_cmd)
        return {
            "check": {
                "exit": check_code,
                "summary": last_summary_line(check_out),
                "passed": check_code == 0,
            },
            "format": {
                "exit": fmt_code,
                "summary": last_summary_line(fmt_out),
                "passed": fmt_code == 0,
            },
        }

    # Default to ruff if present
    check_code, check_out = run_cmd(tool_cmd("ruff", "check", "."))
    fmt_code, fmt_out = run_cmd(tool_cmd("ruff", "format", "--check", "."))
    return {
        "check": {
            "exit": check_code,
            "summary": last_summary_line(check_out),
            "passed": check_code == 0,
        },
        "format": {
            "exit": fmt_code,
            "summary": last_summary_line(fmt_out),
            "passed": fmt_code == 0,
        },
    }


def main(argv: list[str]) -> int:
    target = argv[1] if len(argv) > 1 else "all"
    spec_path = find_spec_path(target) if target != "all" else None

    spec_data = parse_spec(spec_path) if spec_path else {"test_ids": [], "criteria": [], "spec_file": None}
    test_files = find_test_files(target, spec_data.get("title", "")) if target != "all" else []
    mapping = test_mapping(target, spec_data["test_ids"], test_files)
    test_res = gate_tests(test_files)
    linter_res = gate_linter()

    mechanical_ok = (
        test_res["passed"]
        and linter_res["check"]["passed"]
        and linter_res["format"]["passed"]
        and (not mapping["missing"] if spec_data["test_ids"] else True)
    )

    report = {
        "target": target,
        "spec": spec_data,
        "test_mapping": mapping,
        "gates": {
            "tests": test_res,
            "linter_check": linter_res["check"],
            "linter_format": linter_res["format"],
        },
        "mechanical_ok": mechanical_ok,
    }

    print(json.dumps(report, indent=2))
    return 0 if mechanical_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
