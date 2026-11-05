"""Stdlib tests for the guardrail tooling. Run: python3 -m unittest discover -s tests"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent
GEN = SKILL / "scripts" / "gen_guardrails.py"
CHECK = SKILL / "scripts" / "check_loop.py"
GUARD = SKILL / "templates" / "guardrails" / "guard.py"


def run(args, cwd, stdin=None):
    return subprocess.run([sys.executable, *map(str, args)], cwd=cwd, input=stdin, capture_output=True, text=True)


def git(cwd, *args):
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


class RepoCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)
        git(self.root, "init", "-q")
        git(self.root, "config", "user.email", "t@t")
        git(self.root, "config", "user.name", "t")
        (self.root / "history/decisions").mkdir(parents=True)
        (self.root / "history/decisions/001-baseline.md").write_text("# ADR-001\n")
        (self.root / "README.md").write_text("x\n")
        run([GEN, "--init"], self.root)
        git(self.root, "add", "-A")
        git(self.root, "commit", "-qm", "init")

    def tearDown(self):
        self._tmp.cleanup()

    def hook(self, tool, **tool_input):
        return run([self.root / ".claude/hooks/guard.py"], self.root, stdin=json.dumps({"tool_name": tool, "tool_input": tool_input}))

    def guardrails(self):
        r = run([CHECK, "guardrails"], self.root)
        return r.returncode, json.loads(r.stdout)


class GenerateTests(RepoCase):
    def test_writes_adapters_and_is_idempotent(self):
        settings = json.loads((self.root / ".claude/settings.json").read_text())
        self.assertIn("Read(./.env)", settings["permissions"]["deny"])
        self.assertIn("Bash(git push --force:*)", settings["permissions"]["deny"])
        self.assertEqual(len(settings["hooks"]["PreToolUse"]), 1)
        self.assertIn(".env", (self.root / ".cursorignore").read_text())
        self.assertIn("guardrails:start", (self.root / "AGENTS.md").read_text())
        run([GEN], self.root)
        again = json.loads((self.root / ".claude/settings.json").read_text())
        self.assertEqual(again, settings)

    def test_keeps_existing_settings(self):
        path = self.root / ".claude/settings.json"
        data = json.loads(path.read_text())
        data["permissions"]["deny"].append("Bash(mine:*)")
        data["model"] = "x"
        path.write_text(json.dumps(data))
        run([GEN], self.root)
        merged = json.loads(path.read_text())
        self.assertIn("Bash(mine:*)", merged["permissions"]["deny"])
        self.assertEqual(merged["model"], "x")


class HookTests(RepoCase):
    def test_blocks(self):
        for tool, args in [
            ("Read", {"file_path": ".env"}),
            ("Read", {"file_path": "app/keys/server.pem"}),
            ("Bash", {"command": "cat .env"}),
            ("Bash", {"command": "git push --force origin main"}),
            ("Bash", {"command": "rm -rf build"}),
            ("Bash", {"command": "psql -c 'DROP TABLE users'"}),
            ("Edit", {"file_path": ".claude/settings.json"}),
            ("Bash", {"command": "git reset --hard HEAD~1"}),
            ("Bash", {"command": "git clean -fd"}),
        ]:
            with self.subTest(tool=tool, args=args):
                self.assertEqual(self.hook(tool, **args).returncode, 2)

    def test_allows(self):
        for tool, args in [
            ("Read", {"file_path": ".env.example"}),
            ("Write", {"file_path": "history/decisions/002-new.md"}),
            ("Edit", {"file_path": "src/app.py"}),
            ("Bash", {"command": "git commit -m x"}),
            ("Bash", {"command": "git push origin main"}),
            ("Bash", {"command": "cat history/decisions/001-baseline.md"}),
            ("Edit", {"file_path": "history/decisions/001-baseline.md"}),
            ("Bash", {"command": "git branch -D old-idea"}),
        ]:
            with self.subTest(tool=tool, args=args):
                self.assertEqual(self.hook(tool, **args).returncode, 0)



class RoleAgentTests(RepoCase):
    def regen(self, config):
        (self.root / "CONFIG.md").write_text(config)
        return run([GEN], self.root)

    def test_default_claude_agents_carry_tier_models(self):
        agents = self.root / ".claude/agents"
        expected = {"loop-maker": "sonnet", "loop-maker-high": "opus", "loop-verifier": "sonnet",
                    "loop-verifier-strict": "opus", "loop-scribe": "haiku"}
        for name, model in expected.items():
            with self.subTest(name=name):
                text = (agents / f"{name}.md").read_text()
                self.assertIn(f"name: {name}\n", text)
                self.assertIn(f"model: {model}\n", text)
        self.assertIn("disallowedTools: Write, Edit", (agents / "loop-verifier-strict.md").read_text())
        self.assertNotIn("disallowedTools", (agents / "loop-maker.md").read_text())
        self.assertFalse((self.root / ".codex").exists())

    def test_config_overrides_tiers_and_models(self):
        self.regen("MAKER_TIER: top\nCLAUDE_MODELS: top=claude-x, mid=claude-y, small=claude-z\n")
        self.assertIn("model: claude-x\n", (self.root / ".claude/agents/loop-maker.md").read_text())
        self.assertIn("model: claude-z\n", (self.root / ".claude/agents/loop-scribe.md").read_text())

    def test_unknown_tier_inherits_and_warns(self):
        r = self.regen("SCRIBE_TIER: tiny\n")
        self.assertNotIn("model:", (self.root / ".claude/agents/loop-scribe.md").read_text())
        self.assertIn("loop-scribe: tier 'tiny'", r.stderr)

    def test_codex_agents_written_when_models_set(self):
        import tomllib
        self.regen("CODEX_MODELS: top=gpt-top, mid=gpt-mid, small=gpt-small\n")
        for name, model, effort in [("loop_maker", "gpt-mid", "medium"), ("loop_verifier_strict", "gpt-top", "high"),
                                    ("loop_scribe", "gpt-small", "low")]:
            with self.subTest(name=name):
                data = tomllib.loads((self.root / f".codex/agents/{name}.toml").read_text())
                self.assertEqual((data["name"], data["model"], data["model_reasoning_effort"]), (name, model, effort))
                self.assertTrue(data["description"] and data["developer_instructions"].strip())

    def test_agents_md_lists_roles(self):
        self.regen("CODEX_MODELS: top=gpt-top, mid=gpt-mid, small=gpt-small\n")
        text = (self.root / "AGENTS.md").read_text()
        self.assertIn("roles:start", text)
        self.assertIn("| `loop-maker` | 3–4 | mid | sonnet | session model | gpt-mid |", text)
        self.assertIn("| planner (main session) | 0–2, orchestration | top | opus | session model | gpt-top |", text)

    def test_role_agents_are_protected_and_required(self):
        self.assertEqual(self.hook("Edit", file_path=".claude/agents/loop-maker.md").returncode, 2)
        (self.root / ".claude/agents/loop-scribe.md").unlink()
        code, out = self.guardrails()
        self.assertNotEqual(code, 0)
        self.assertTrue(any("loop-scribe.md missing" in e for e in out["errors"]), out)


class VerifierTests(RepoCase):
    def as_verifier(self, tool, **tool_input):
        event = {"tool_name": tool, "tool_input": tool_input, "agent_type": "loop-verifier"}
        return run([self.root / ".claude/hooks/guard.py"], self.root, stdin=json.dumps(event)).returncode

    def test_generator_writes_verifier_agent(self):
        text = (self.root / ".claude/agents/loop-verifier.md").read_text()
        self.assertIn("disallowedTools: Write, Edit", text)

    def test_blocks_writes_and_unlisted_commands(self):
        for tool, args in [
            ("Edit", {"file_path": "src/app.py"}),
            ("Write", {"file_path": "tests/test_x.py"}),
            ("Bash", {"command": "echo x > src/app.py"}),
            ("Bash", {"command": "python3 -c 'open(\"a\", \"w\")'"}),
            ("Bash", {"command": "git commit -am fix"}),
            ("Bash", {"command": "git diff && sed -i s/a/b/ src/app.py"}),
            ("Bash", {"command": "cat $(echo x)"}),
            ("Bash", {"command": "npm run test:all"}),
        ]:
            with self.subTest(tool=tool, args=args):
                self.assertEqual(self.as_verifier(tool, **args), 2)

    def test_allows_reads_checker_and_configured_commands(self):
        cfg = self.root / "CONFIG.md"
        cfg.write_text("TEST_COMMAND: npm run test:all\nFORMAT_COMMAND:\n")
        run([GEN], self.root)
        for tool, args in [
            ("Read", {"file_path": "src/app.py"}),
            ("Bash", {"command": "git diff HEAD --stat"}),
            ("Bash", {"command": "python3 .agent/skills/product-engineering/scripts/check_loop.py 01 2>&1 | tail -5"}),
            ("Bash", {"command": "npm run test:all 2>&1"}),
        ]:
            with self.subTest(tool=tool, args=args):
                self.assertEqual(self.as_verifier(tool, **args), 0)

    def test_strict_verifier_is_read_only_too(self):
        event = {"tool_name": "Edit", "tool_input": {"file_path": "src/app.py"}, "agent_type": "loop-verifier-strict"}
        self.assertEqual(run([self.root / ".claude/hooks/guard.py"], self.root, stdin=json.dumps(event)).returncode, 2)

    def test_maker_is_unaffected(self):
        self.assertEqual(self.hook("Edit", file_path="src/app.py").returncode, 0)

    def test_fingerprint_changes_when_files_change(self):
        fp = lambda: json.loads(run([CHECK, "fingerprint"], self.root).stdout)["fingerprint"]
        before = fp()
        self.assertEqual(fp(), before)
        (self.root / "README.md").write_text("changed\n")
        self.assertNotEqual(fp(), before)


class CursorTests(RepoCase):
    """Cursor runs the same guard.py through .cursor/hooks.json and reads role agents from .cursor/agents/."""

    def cursor(self, event_name, **fields):
        event = {"hook_event_name": event_name, "cursor_version": "2.5.0", "workspace_roots": [str(self.root)], **fields}
        return run([self.root / ".claude/hooks/guard.py"], self.root, stdin=json.dumps(event))

    def test_generator_registers_guard_for_tools_and_reads(self):
        data = json.loads((self.root / ".cursor/hooks.json").read_text())
        self.assertEqual(data["version"], 1)
        for event in ("preToolUse", "beforeReadFile"):
            with self.subTest(event=event):
                self.assertEqual(sum("hooks/guard.py" in h["command"] for h in data["hooks"][event]), 1)
        run([GEN], self.root)
        self.assertEqual(json.loads((self.root / ".cursor/hooks.json").read_text()), data)

    def test_keeps_existing_cursor_hooks(self):
        path = self.root / ".cursor/hooks.json"
        data = json.loads(path.read_text())
        data["hooks"]["afterFileEdit"] = [{"command": "./fmt.sh"}]
        path.write_text(json.dumps(data))
        run([GEN], self.root)
        self.assertEqual(json.loads(path.read_text())["hooks"]["afterFileEdit"], [{"command": "./fmt.sh"}])

    def test_blocks(self):
        for event, fields in [
            ("beforeReadFile", {"file_path": str(self.root / ".env"), "content": "X=1"}),
            ("preToolUse", {"tool_name": "Read", "tool_input": {"file_path": "app/keys/server.pem"}}),
            ("preToolUse", {"tool_name": "Shell", "tool_input": {"command": "git push --force origin main"}}),
            ("preToolUse", {"tool_name": "Shell", "tool_input": {"command": "cat .env"}}),
            ("preToolUse", {"tool_name": "Write", "tool_input": {"file_path": ".claude/settings.json"}}),
            ("preToolUse", {"tool_name": "Write", "tool_input": {"path": str(self.root / ".cursor/hooks.json")}}),
            ("preToolUse", {"tool_name": "Delete", "tool_input": {"target_file": ".agent/guardrails.json"}}),
        ]:
            with self.subTest(event=event, fields=fields):
                r = self.cursor(event, **fields)
                self.assertEqual(r.returncode, 2)
                self.assertEqual(json.loads(r.stdout)["permission"], "deny")

    def test_allows_with_explicit_permission(self):
        # Cursor blocks a permission hook whose output isn't valid JSON, so an allow must say so.
        for event, fields in [
            ("beforeReadFile", {"file_path": str(self.root / "README.md"), "content": "x"}),
            ("preToolUse", {"tool_name": "Shell", "tool_input": {"command": "git status"}}),
            ("preToolUse", {"tool_name": "Write", "tool_input": {"file_path": "src/app.py"}}),
            ("preToolUse", {"tool_name": "Grep", "tool_input": {"pattern": "x"}}),
        ]:
            with self.subTest(event=event, fields=fields):
                r = self.cursor(event, **fields)
                self.assertEqual(r.returncode, 0, r.stderr)
                self.assertEqual(json.loads(r.stdout), {"permission": "allow"})

    def test_role_agents_use_cursor_fields(self):
        agents = self.root / ".cursor/agents"
        for name in ("loop-verifier", "loop-verifier-strict"):
            with self.subTest(name=name):
                text = (agents / f"{name}.md").read_text()
                self.assertIn("readonly: true\n", text)
                self.assertIn("model: inherit\n", text)
                self.assertNotIn("disallowedTools", text)
        self.assertNotIn("readonly", (agents / "loop-maker.md").read_text())

    def test_cursor_models_from_config(self):
        (self.root / "CONFIG.md").write_text("CURSOR_MODELS: top=cur-top, mid=cur-mid, small=cur-small\n")
        run([GEN], self.root)
        self.assertIn("model: cur-top\n", (self.root / ".cursor/agents/loop-verifier-strict.md").read_text())
        self.assertIn("model: cur-small\n", (self.root / ".cursor/agents/loop-scribe.md").read_text())
        self.assertIn("| `loop-maker` | 3–4 | mid | sonnet | cur-mid | session model |", (self.root / "AGENTS.md").read_text())

    def test_claude_verifier_is_read_only_for_cursor_fallback(self):
        # Cursor also reads .claude/agents/; `readonly` keeps the verifier locked there too.
        self.assertIn("readonly: true\n", (self.root / ".claude/agents/loop-verifier.md").read_text())

    def test_cursor_adapter_is_protected(self):
        for path in (".cursor/hooks.json", ".cursor/agents/loop-verifier.md"):
            with self.subTest(path=path):
                self.assertEqual(self.hook("Edit", file_path=path).returncode, 2)

    def test_missing_cursor_hook_fails_check(self):
        path = self.root / ".cursor/hooks.json"
        data = json.loads(path.read_text())
        data["hooks"].pop("beforeReadFile")
        path.write_text(json.dumps(data))
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertTrue(any("beforeReadFile" in e for e in facts["errors"]), facts)

    def test_readonly_removed_fails_check(self):
        path = self.root / ".cursor/agents/loop-verifier-strict.md"
        path.write_text(path.read_text().replace("readonly: true\n", ""))
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertTrue(any("loop-verifier-strict.md" in e and "readonly" in e for e in facts["errors"]), facts)


class CodexTests(RepoCase):
    CONFIG = "CODEX_MODELS: top=gpt-top, mid=gpt-mid, small=gpt-small\n"

    def setUp(self):
        super().setUp()
        (self.root / "CONFIG.md").write_text(self.CONFIG)
        run([GEN], self.root)

    def codex(self, tool, agent_type=None, **tool_input):
        event = {"hook_event_name": "PreToolUse", "session_id": "s", "cwd": str(self.root), "model": "gpt-mid",
                 "tool_name": tool, "tool_input": tool_input}
        if agent_type:
            event["agent_type"] = agent_type
        return run([self.root / ".claude/hooks/guard.py"], self.root, stdin=json.dumps(event)).returncode

    def patch(self, *headers):
        body = "\n".join(f"*** {h}\n@@\n-a\n+b" for h in headers)
        return f"*** Begin Patch\n{body}\n*** End Patch\n"

    def test_generator_registers_guard(self):
        data = json.loads((self.root / ".codex/hooks.json").read_text())
        entries = data["hooks"]["PreToolUse"]
        self.assertEqual(len(entries), 1)
        self.assertIn("apply_patch", entries[0]["matcher"])
        self.assertIn("hooks/guard.py", entries[0]["hooks"][0]["command"])
        run([GEN], self.root)
        self.assertEqual(json.loads((self.root / ".codex/hooks.json").read_text()), data)

    def test_no_codex_hooks_without_codex_models(self):
        (self.root / "CONFIG.md").write_text("")
        other = Path(tempfile.mkdtemp(dir=self._tmp.name))
        git(other, "init", "-q")
        run([GEN, "--init", "--root", other], self.root)
        self.assertFalse((other / ".codex").exists())

    def test_blocks_patches_to_protected_and_secret_paths(self):
        for patch in [
            self.patch("Update File: .claude/settings.json"),
            self.patch("Update File: src/app.py", "Add File: .env"),
            self.patch("Delete File: .codex/hooks.json"),
            self.patch("Update File: src/app.py\n*** Move to: .claude/hooks/guard.py"),
        ]:
            with self.subTest(patch=patch):
                self.assertEqual(self.codex("apply_patch", command=patch), 2)

    def test_allows_ordinary_patches_and_commands(self):
        self.assertEqual(self.codex("apply_patch", command=self.patch("Update File: src/app.py", "Add File: tests/test_x.py")), 0)
        self.assertEqual(self.codex("Bash", command="git status"), 0)
        self.assertEqual(self.codex("Bash", command="rm -rf build"), 2)

    def test_verifier_agent_type_with_underscores_is_read_only(self):
        self.assertEqual(self.codex("apply_patch", agent_type="loop_verifier_strict", command=self.patch("Update File: src/app.py")), 2)
        self.assertEqual(self.codex("Bash", agent_type="loop_verifier", command="git diff"), 0)
        self.assertEqual(self.codex("apply_patch", agent_type="loop_maker", command=self.patch("Update File: src/app.py")), 0)

    def test_missing_codex_hook_fails_check(self):
        (self.root / ".codex/hooks.json").write_text(json.dumps({"hooks": {}}))
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertTrue(any(".codex/hooks.json" in e for e in facts["errors"]), facts)


class HookRootTests(RepoCase):
    def test_uses_its_own_repo_config_whatever_the_env(self):
        # Cursor sets CLAUDE_PROJECT_DIR too, and Codex sets none; the hook trusts its own location.
        import os
        env = {**os.environ, "CLAUDE_PROJECT_DIR": tempfile.gettempdir()}
        r = subprocess.run([sys.executable, self.root / ".claude/hooks/guard.py"], cwd=tempfile.gettempdir(), env=env,
                           input=json.dumps({"tool_name": "Read", "tool_input": {"file_path": str(self.root / ".env")}}),
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 2, r.stderr)


class CheckLoopTests(RepoCase):
    def test_clean_repo_ok(self):
        code, facts = self.guardrails()
        self.assertEqual(code, 0, facts)

    def test_missing_config_fails(self):
        (self.root / ".agent/guardrails.json").unlink()
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertFalse(facts["config_present"])

    def test_missing_hook_registration_fails(self):
        path = self.root / ".claude/settings.json"
        data = json.loads(path.read_text())
        data["hooks"] = {}
        path.write_text(json.dumps(data))
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertTrue(any("hook" in e for e in facts["errors"]))

    def test_editing_a_frozen_adr_fails_the_check_not_the_hook(self):
        (self.root / "history/decisions/001-baseline.md").write_text("changed\n")
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertEqual(facts["append_only_violations"], ["history/decisions/001-baseline.md"])

    def test_config_change_needs_new_adr(self):
        path = self.root / ".agent/guardrails.json"
        data = json.loads(path.read_text())
        data["secret_paths"].append("vault/**")
        path.write_text(json.dumps(data))
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertIn(".agent/guardrails.json", facts["protected_changed"])
        self.assertTrue(any("vault/**" in e for e in facts["errors"]), "adapters must be regenerated too")
        run([GEN], self.root)
        (self.root / "history/decisions/002-vault.md").write_text("# ADR-002\n")
        code, facts = self.guardrails()
        self.assertEqual(code, 0, facts)


class DesignSystemTests(RepoCase):
    def test_copy_change_needs_no_adr(self):
        (self.root / "src/pages").mkdir(parents=True)
        (self.root / "src/pages/home.tsx").write_text("<h1>New headline</h1>\n")
        self.assertEqual(self.guardrails()[0], 0)

    def test_design_system_change_needs_adr(self):
        (self.root / "src/styles").mkdir(parents=True)
        (self.root / "src/styles/globals.css").write_text(":root { --brand: #123; }\n")
        code, facts = self.guardrails()
        self.assertEqual(code, 1)
        self.assertEqual(facts["adr_required_changed"], ["src/styles/globals.css"])
        (self.root / "history/decisions/002-brand-color.md").write_text("# ADR-002\n")
        self.assertEqual(self.guardrails()[0], 0)

    def test_agent_may_edit_design_system(self):
        self.assertEqual(self.hook("Edit", file_path="src/components/ui/button.tsx").returncode, 0)


class PrivacyTests(RepoCase):
    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def errors(self):
        return self.guardrails()[1]["errors"]

    def test_generator_gitignores_secrets_and_data(self):
        ignore = (self.root / ".gitignore").read_text()
        for line in (".env", "**/*.csv", "!tests/fixtures/**/*.csv"):
            self.assertIn(line, ignore.splitlines())

    def test_secret_path_missing_from_gitignore_fails(self):
        (self.root / ".gitignore").write_text("")
        self.assertTrue(any(".env is not in .gitignore" in e for e in self.errors()))

    def test_tracked_env_fails(self):
        self.write(".env", "X=1\n")
        git(self.root, "add", "-f", ".env")
        self.assertTrue(any("Secret file tracked" in e for e in self.errors()))

    def test_csv_only_inside_fixtures(self):
        self.write("tests/fixtures/users.csv", "name,email\nAda,ada@example.com\n")
        self.assertEqual(self.errors(), [])
        self.write("data/users.csv", "name\nAda\n")
        git(self.root, "add", "-f", "data/users.csv")
        self.assertTrue(any("data/users.csv" in e for e in self.errors()))

    def test_card_and_ssn_fail_test_values_pass(self):
        self.write("src/fake.py", 'CARD = "4242 4242 4242 4242"\nSSN = "123-45-6789"\n')
        self.assertEqual(self.errors(), [])
        self.write("src/real.py", 'CARD = "4539 1488 0343 6467"\nSSN = "219-09-9999"\n')
        errors = self.errors()
        self.assertTrue(any("card number: src/real.py:1" in e for e in errors), errors)
        self.assertTrue(any("SSN: src/real.py:2" in e for e in errors), errors)

    def test_long_ids_are_not_cards(self):
        self.write("src/ids.py", 'ORDER = "1234567812345670"\nTS = 1730592000000\n')
        self.assertEqual(self.errors(), [])

    def test_real_email_warns_only(self):
        self.write("src/contact.py", 'TO = "jane.doe@gmail.com"\nOK = "ada@example.com"\n')
        code, facts = self.guardrails()
        self.assertEqual(code, 0, facts)
        self.assertEqual(facts["privacy_warnings"], ["Real-looking email: src/contact.py:1"])

    def test_hardcoded_key_fails(self):
        self.write("src/client.ts", 'const key = "sk-abcdefghijklmnopqrstuvwxyz123456";\n')
        self.assertTrue(any("Likely secret: src/client.ts:1" in e for e in self.errors()))


def contract(risk="low", adr="ADR-001", extra=""):
    return f"""# Build Unit 02 — Thing
- **Type**: journey
- **Serves**: F1
- **Tier**: P0
- **Risk**: {risk}
- **Guardrails ADR**: {adr}
**Testable after this unit**: a human can do the thing
- **T1 [Happy Path] (e2e)** — works
- **T2 [Instrumentation]** — events asserted
{extra}
- **M1 [Desktop Happy Path]** — Steps: 1. go Expected: ok
### C. Instrumentation
- `thing_viewed` — on view. Properties: `id`
"""


class ContractTests(RepoCase):
    def check(self, text):
        sys.path.insert(0, str(SKILL / "scripts"))
        import os
        cwd = os.getcwd()
        os.chdir(self.root)
        try:
            import importlib
            import check_loop
            importlib.reload(check_loop)
            return check_loop.check_contract(text)
        finally:
            os.chdir(cwd)

    def test_low_risk_with_baseline_adr_ok(self):
        self.assertEqual(self.check(contract())["errors"], [])

    def test_placeholders_fail(self):
        errors = self.check(contract(risk="[low | medium | high]", adr="[ADR-NNN]"))["errors"]
        self.assertTrue(any("Risk" in e for e in errors))
        self.assertTrue(any("Guardrails ADR" in e for e in errors))

    def test_unknown_adr_fails(self):
        self.assertTrue(any("ADR-009" in e for e in self.check(contract(adr="ADR-009"))["errors"]))

    def test_medium_needs_guardrail_test_and_high_needs_abuse(self):
        self.assertTrue(any("[Guardrail]" in e for e in self.check(contract("medium"))["errors"]))
        guardrail = "- **T3 [Guardrail]** — blocked stays blocked"
        self.assertEqual(self.check(contract("medium", extra=guardrail))["errors"], [])
        self.assertTrue(any("[Abuse]" in e for e in self.check(contract("high", extra=guardrail))["errors"]))
        both = guardrail + "\n- **T4 [Abuse]** — injection does nothing"
        self.assertEqual(self.check(contract("high", extra=both))["errors"], [])

    def test_journey_needs_instrumentation_scenario(self):
        text = contract().replace("- **T2 [Instrumentation]** — events asserted\n", "")
        self.assertTrue(any("[Instrumentation]" in e for e in self.check(text)["errors"]))

    def test_journey_needs_e2e_happy_path(self):
        text = contract().replace("- **T1 [Happy Path] (e2e)** — works", "- **T1 [Happy Path] (unit)** — works")
        self.assertTrue(any("(e2e)" in e for e in self.check(text)["errors"]))
        combined = contract().replace("(e2e)", "(integration + e2e)")
        self.assertEqual(self.check(combined)["errors"], [])

    def test_live_walkthrough_needs_cost(self):
        no_cost = "- **M2 [Live]** — **Steps**: 1. run the eval. **Expected**: scores"
        self.assertTrue(any("Cost" in e for e in self.check(contract(extra=no_cost))["errors"]))
        placeholder = "- **M2 [Live]** — **Cost**: [e.g. ~$0.30]. **Steps**: 1. run"
        self.assertTrue(any("Cost" in e for e in self.check(contract(extra=placeholder))["errors"]))
        priced = "- **M2 [Live]** — **Cost**: ~$0.30 per run (12 model calls). **Steps**: 1. run"
        self.assertEqual(self.check(contract(extra=priced))["errors"], [])


if __name__ == "__main__":
    unittest.main()
