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
            ("Bash", {"command": "python3 .agent/skills/product-loop-engineering/scripts/check_loop.py 01 2>&1 | tail -5"}),
            ("Bash", {"command": "npm run test:all 2>&1"}),
        ]:
            with self.subTest(tool=tool, args=args):
                self.assertEqual(self.as_verifier(tool, **args), 0)

    def test_maker_is_unaffected(self):
        self.assertEqual(self.hook("Edit", file_path="src/app.py").returncode, 0)

    def test_fingerprint_changes_when_files_change(self):
        fp = lambda: json.loads(run([CHECK, "fingerprint"], self.root).stdout)["fingerprint"]
        before = fp()
        self.assertEqual(fp(), before)
        (self.root / "README.md").write_text("changed\n")
        self.assertNotEqual(fp(), before)


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
- **T1 [Happy Path]** — works
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
        guardrail = "- **T2 [Guardrail]** — blocked stays blocked"
        self.assertEqual(self.check(contract("medium", extra=guardrail))["errors"], [])
        self.assertTrue(any("[Abuse]" in e for e in self.check(contract("high", extra=guardrail))["errors"]))
        both = guardrail + "\n- **T3 [Abuse]** — injection does nothing"
        self.assertEqual(self.check(contract("high", extra=both))["errors"], [])


if __name__ == "__main__":
    unittest.main()
