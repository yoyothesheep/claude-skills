#!/usr/bin/env python3
"""Deterministic verification runner for the `product-loop-engineering` skill.

Automates the mechanical, CI-grade checks for a build unit or subsystem and emits
structured JSON evidence to stdout. The LLM verifier layer consumes this JSON to
perform judgment checks (test fidelity, behavioral drive, and semantic acceptance).

Features:
- Discovers unit contracts in active/*/units/ or history/milestones/*/units/
- Parses enumerated test IDs (T1..Tn, T1.1..Tn.m) and acceptance criteria
- Validates test collection mapping against test files in tests/
- Validates contract structure (Type/Serves/Tier, testable outcome, M scenarios, instrumentation)
- Executes configured test suite and linters (supporting CONFIG.md overrides)
- `plan` mode validates active/*/plan.md: every unit pre-documented, tiers ordered
  skeleton → P0 → P1 → P2 → reporting, every product-spec flow tier-tagged, ordered
  (F1 is P0, tiers non-decreasing), and served by a journey unit
- Reports `diff`: changed files, plus test files that lost assertions or gained skips/sleeps/timeouts, so the verifier can tie each to a contract line
- Reports `hygiene` on changed source files: likely hardcoded secrets (fail the gate) and route files that mention no auth (heuristic, for the verifier to review)
- Emits structured JSON summary

Usage:
    python check_loop.py NN            # e.g. python check_loop.py 01
    python check_loop.py <path-to-spec> # e.g. python check_loop.py active/01-rebuild/units/01-scaffold.md
    python check_loop.py plan [NN]     # validate milestone plan(s) in active/
    python check_loop.py NN --base REF # diff against REF instead of HEAD (default: uncommitted work)
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
        _repo(".agent", "skills", "product-loop-engineering", "CONFIG.md"),
        _repo(".claude", "skills", "product-loop-engineering", "CONFIG.md"),
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
    # A command may chain several runners (e.g. unit + browser); report each runner's pass/fail count
    counts = [ln for ln in lines if re.search(r"\b\d+ (passed|failed)\b", ln) and len(ln) < 120]
    if counts:
        return " | ".join(dict.fromkeys(counts))
    return lines[-1] if lines else ""


def find_spec_path(target: str) -> Path | None:
    p = Path(target)
    if p.is_file():
        return p.resolve()
    if (_repo(target)).is_file():
        return _repo(target)

    search_patterns = [
        f"active/*/units/{target}-*.md",
        f"active/*/units/*{target}*.md",
        f"history/milestones/*/units/{target}-*.md",
        f"history/milestones/*/units/*{target}*.md",
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


UNIT_TYPES = ("infra", "journey", "reporting")
TIER_RANK = {"P0": 0, "P1": 1, "P2": 2}


def contract_field(text: str, name: str) -> str:
    m = re.search(rf"\*\*{name}\*\*:\s*(.+)", text)
    return m.group(1).strip() if m else ""


def check_contract(text: str) -> dict:
    """Structural rules every unit contract must satisfy."""
    errors: list[str] = []
    unit_type = contract_field(text, "Type").lower()
    serves = contract_field(text, "Serves")
    tier = contract_field(text, "Tier")
    if unit_type not in UNIT_TYPES:
        errors.append(f"`**Type**:` must be one of {', '.join(UNIT_TYPES)}")
    if not serves:
        errors.append("Missing `**Serves**:` (flow ids or `all`)")
    if tier not in (*TIER_RANK, "—", "-"):
        errors.append("`**Tier**:` must be P0, P1, P2, or — (reporting)")
    testable = contract_field(text, "Testable after this unit")
    if not testable or testable.startswith("["):
        errors.append("Missing `**Testable after this unit**:` outcome")
    if not re.search(r"\*\*M\d+\b", text):
        errors.append("No manual E2E scenarios (M1..Mk)")
    if unit_type == "journey":
        section = re.search(r"^###?\s+(?:C\.\s+)?Instrumentation\b(.*?)(?=^##|\Z)", text, re.MULTILINE | re.DOTALL)
        events = re.findall(r"^\s*-\s+`[^`\[\]]+`", section.group(1), re.MULTILINE) if section else []
        if not events:
            errors.append("Journey unit lists no Instrumentation events")
    return {"type": unit_type, "serves": serves, "tier": tier, "errors": errors, "ok": not errors}


def parse_plan_rows(text: str) -> list[dict]:
    header: list[str] = []
    rows: list[dict] = []
    for line in text.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if not header and "Type" in cells and "Tier" in cells:
            header = [c.lower() for c in cells]
        elif header and re.fullmatch(r"\d+", cells[0]) and len(cells) == len(header):
            rows.append(dict(zip(header, cells)))
    return rows


def spec_flows(plan_text: str) -> dict[str, str | None] | None:
    """Tier per flow (None if untagged), in spec order, from the product spec the plan links to."""
    m = re.search(r"specs/product/[\w./-]+\.md", plan_text)
    if not m or not _repo(m.group(0)).is_file():
        return None
    text = _repo(m.group(0)).read_text(encoding="utf-8")
    flows: dict[str, str | None] = {}
    for n, rest in re.findall(r"^###\s+F(\d+)\b(.*)$", text, re.MULTILINE):
        tag = re.search(r"\[P([0-2])\]\s*$", rest)
        flows[f"F{n}"] = f"P{tag.group(1)}" if tag else None
    return flows


def check_plan(plan_path: Path) -> dict:
    text = plan_path.read_text(encoding="utf-8")
    rows = parse_plan_rows(text)
    errors: list[str] = []
    units: list[dict] = []
    if not rows:
        errors.append("No Build Sequence table rows (expected columns # | Unit | Type | Serves | Tier | Status)")

    for row in rows:
        num = row["#"]
        matches = sorted(plan_path.parent.glob(f"units/{num}-*.md"))
        unit = {"unit": num, "type": row["type"].lower(), "serves": row["serves"], "tier": row["tier"], "contract": None}
        if not matches:
            errors.append(f"Unit {num} has no pre-documented contract in units/")
        else:
            contract = check_contract(matches[0].read_text(encoding="utf-8"))
            unit["contract"] = str(matches[0].relative_to(REPO)) if matches[0].is_relative_to(REPO) else str(matches[0])
            errors.extend(f"Unit {num}: {e}" for e in contract["errors"])
            if contract["type"] != unit["type"] or contract["tier"] != unit["tier"]:
                errors.append(f"Unit {num}: plan row and contract disagree on Type/Tier")
        units.append(unit)

    reporting = [i for i, u in enumerate(units) if u["type"] == "reporting"]
    if not reporting:
        errors.append("No reporting unit (dashboard/reports over instrumented events) at the end")
    elif reporting != list(range(len(units) - len(reporting), len(units))):
        errors.append("Reporting unit(s) must come last")

    tiers = [u["tier"] for u in units if u["type"] != "reporting"]
    if any(t not in TIER_RANK for t in tiers):
        errors.append("Non-reporting units need a Tier of P0, P1, or P2")
    elif tiers != sorted(tiers, key=TIER_RANK.get):
        errors.append(f"Units must run P0 → P1 → P2; found {' → '.join(tiers)}")
    if not any(u["type"] == "journey" and u["tier"] == "P0" for u in units):
        errors.append("No P0 journey unit")

    flows = spec_flows(text)
    if not flows:
        errors.append("Plan links no readable specs/product/*.md with `### F<n>` flows")
    else:
        errors.extend(f"Spec flow {fid} has no [P0|P1|P2] tier tag" for fid, t in flows.items() if t is None)
        tagged = [t for t in flows.values() if t]
        if next(iter(flows.values())) != "P0":
            errors.append("Spec flow F1 must be P0")
        if tagged != sorted(tagged, key=TIER_RANK.get):
            errors.append(f"Spec flows must be ordered P0 → P1 → P2; found {' → '.join(tagged)}")
        flows = {f: t for f, t in flows.items() if t}
        served_by_journeys: set[str] = set()
        for u in units:
            ids = re.findall(r"F\d+", u["serves"])
            if u["type"] == "journey":
                served_by_journeys.update(ids)
            known = [flows[f] for f in ids if f in flows]
            if known and u["tier"] in TIER_RANK and u["tier"] != min(known, key=TIER_RANK.get):
                errors.append(f"Unit {u['unit']} tier {u['tier']} doesn't match its flows ({', '.join(ids)})")
        for fid in flows:
            if fid not in served_by_journeys:
                errors.append(f"{fid} [{flows[fid]}] is not served by any journey unit")

    rel = str(plan_path.relative_to(REPO)) if plan_path.is_relative_to(REPO) else str(plan_path)
    return {"plan": rel, "units": units, "errors": errors, "ok": not errors}


def main_plan(argv: list[str]) -> int:
    pattern = f"active/{argv[2]}-*/plan.md" if len(argv) > 2 else "active/*/plan.md"
    plans = sorted(glob.glob(str(_repo(pattern))))
    reports = [check_plan(Path(p)) for p in plans]
    ok = bool(reports) and all(r["ok"] for r in reports)
    print(json.dumps({"plans": reports, "ok": ok, **({} if reports else {"error": f"No plan matching {pattern}"})}, indent=2))
    return 0 if ok else 1


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
    by_number: set[str] = set()
    by_keyword: set[str] = set()
    for root, _, files in os.walk(str(test_dir)):
        for f in files:
            f_lower = f.lower()
            if not f_lower.endswith(valid_exts):
                continue
            if not (f_lower.startswith("test_") or ".test." in f_lower or ".spec." in f_lower):
                continue
            full_rel = str(Path(root, f).relative_to(REPO))
            # A file named for the unit number (test_03_*) is authoritative; title words are a fallback
            if re.match(rf"test[_-]{re.escape(target)}[_-]", f_lower):
                by_number.add(full_rel)
            elif any(k in f_lower for k in keywords):
                by_keyword.add(full_rel)
    return sorted(by_number or by_keyword)


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


ASSERT_RE = re.compile(r"\b(assert\w*|expect\w*|should)\b|\.to(Be|Equal|Have|Match|Contain)\w*\(")
LOOSEN_RE = re.compile(r"@\w*\.?(skip|xfail)|\.skip\(|\bxit\(|pytest\.(skip|xfail)|wait_for_timeout|\bretr(y|ies)\b|expect\(.*timeout\s*=")


def diff_facts(base: str) -> dict:
    """Changed files plus test-gate edits, for the verifier's gate-integrity and scope-drift checks."""
    code, out = run_cmd(["git", "diff", base, "--name-only"])
    changed = [f for f in out.splitlines() if f.strip()] if code == 0 else []
    _, untracked = run_cmd(["git", "ls-files", "--others", "--exclude-standard"])
    changed += [f for f in untracked.splitlines() if f.strip() and f not in changed]

    test_dir = CONFIG.get("TESTS_DIR", "tests").strip("/") + "/"
    is_test = lambda f: f.startswith(test_dir) or "/" + test_dir in f or re.search(r"(^|/)test_[^/]*$|\.(test|spec)\.", f)
    tests = [f for f in changed if is_test(f)]

    edits = []
    for f in tests:
        _, d = run_cmd(["git", "diff", base, "--unified=0", "--no-color", "--", f])
        removed = [ln[1:] for ln in d.splitlines() if ln.startswith("-") and not ln.startswith("---")]
        added = [ln[1:] for ln in d.splitlines() if ln.startswith("+") and not ln.startswith("+++")]
        edits.append({
            "file": f,
            "assertions_removed": sum(bool(ASSERT_RE.search(ln)) for ln in removed),
            "assertions_added": sum(bool(ASSERT_RE.search(ln)) for ln in added),
            "loosening_added": [ln.strip() for ln in added if not ln.lstrip().startswith(("#", "//")) and LOOSEN_RE.search(ln)][:10],
        })
    return {
        "base": base,
        "source_files": [f for f in changed if f not in tests],
        "test_files_changed": len(edits),
        "test_files_to_justify": [e for e in edits if e["assertions_removed"] or e["loosening_added"]],
        "needs_justification": any(e["assertions_removed"] > e["assertions_added"] or e["loosening_added"] for e in edits),
    }


TEMPLATE_ENV_RE = re.compile(r"\.(example|sample|template|dist)$")
CODE_EXTS = (".py", ".ts", ".tsx", ".js", ".jsx", ".mjs")
HYGIENE_EXTS = CODE_EXTS + (".json", ".yml", ".yaml", ".toml", ".env", ".sql", ".sh")


SECRET_RES = [re.compile(p) for p in (
    r"AKIA[0-9A-Z]{16}", r"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----", r"\bsk-[A-Za-z0-9_-]{20,}",
    r"\b(?:sk|rk)_live_[A-Za-z0-9]{16,}", r"\bgh[pousr]_[A-Za-z0-9]{36,}", r"\bxox[baprs]-[A-Za-z0-9-]{10,}",
    r"(?i)(?:api[_-]?key|secret|token|passwd|password|service[_-]?role)\w*\s*[:=]\s*['\"][A-Za-z0-9_\-./+=]{16,}['\"]",
)]
SECRET_IGNORE = re.compile(r"(?i)process\.env|os\.environ|getenv|import\.meta\.env|example|your[_-]|xxx|changeme|placeholder|<[^>]+>|\$\{")
ROUTE_RE = re.compile(r"\b(?:app|router|api)\.(?:get|post|put|patch|delete|all)\(|@(?:app|router|api)\.(?:get|post|put|patch|delete)\(|export\s+(?:async\s+)?function\s+(?:GET|POST|PUT|PATCH|DELETE)\b")
AUTH_RE = re.compile(r"(?i)auth|session|getUser|currentUser|clerk|jwt|verify_token|Depends\(|login_required|requireUser|bearer|middleware")


def hygiene_facts(source_files: list[str]) -> dict:
    """Secrets and unauthenticated routes in the unit's changed source files (full-repo scan: product-launch-audit)."""
    secrets, routes_without_auth = [], []
    for f in source_files:
        path = _repo(f)
        if not path.is_file() or TEMPLATE_ENV_RE.search(f) or not f.endswith(HYGIENE_EXTS):
            continue
        text = path.read_text(encoding="utf-8", errors="ignore")
        for n, line in enumerate(text.splitlines(), 1):
            if len(line) < 400 and not SECRET_IGNORE.search(line) and any(r.search(line) for r in SECRET_RES):
                secrets.append({"file": f, "line": n})
                break
        if f.endswith(CODE_EXTS) and ROUTE_RE.search(text) and not AUTH_RE.search(text):
            routes_without_auth.append(f)
    return {"secrets": secrets, "routes_without_auth": routes_without_auth, "ok": not secrets}


def main(argv: list[str]) -> int:
    base = "HEAD"
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1] if i + 1 < len(argv) else base
        argv = argv[:i] + argv[i + 2:]
    target = argv[1] if len(argv) > 1 else "all"
    if target == "plan":
        return main_plan(argv)
    spec_path = find_spec_path(target) if target != "all" else None

    spec_data = parse_spec(spec_path) if spec_path else {"test_ids": [], "criteria": [], "spec_file": None}
    contract = check_contract(spec_path.read_text(encoding="utf-8")) if spec_path else None
    test_files = find_test_files(target, spec_data.get("title", "")) if target != "all" else []
    mapping = test_mapping(target, spec_data["test_ids"], test_files)
    test_res = gate_tests(test_files)
    linter_res = gate_linter()

    diff = diff_facts(base)
    hygiene = hygiene_facts(diff["source_files"])

    mechanical_ok = (
        test_res["passed"]
        and hygiene["ok"]
        and linter_res["check"]["passed"]
        and linter_res["format"]["passed"]
        and (not mapping["missing"] if spec_data["test_ids"] else True)
        and (contract["ok"] if contract else True)
    )

    report = {
        "target": target,
        "spec": spec_data,
        "contract": contract,
        "test_mapping": mapping,
        "gates": {
            "tests": test_res,
            "linter_check": linter_res["check"],
            "linter_format": linter_res["format"],
        },
        "diff": diff,
        "hygiene": hygiene,
        "mechanical_ok": mechanical_ok,
    }

    print(json.dumps(report, indent=2))
    return 0 if mechanical_ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
