"""Stdlib tests for audit_repo.py. Run: python3 -m unittest discover -s product-launch-audit/tests"""

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

AUDIT = Path(__file__).resolve().parent.parent / "scripts" / "audit_repo.py"


class AuditCase(unittest.TestCase):
    def setUp(self):
        self._tmp = tempfile.TemporaryDirectory()
        self.root = Path(self._tmp.name)

    def tearDown(self):
        self._tmp.cleanup()

    def write(self, rel, text):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)

    def checks(self):
        r = subprocess.run([sys.executable, AUDIT, self.root], capture_output=True, text=True)
        return {c["id"]: c for c in json.loads(r.stdout)["checks"]}


class PaidKeyTests(AuditCase):
    def test_one_spend_row_per_paid_service(self):
        self.write("requirements.txt", "openai==1.0\nfastapi\n")
        self.write(".env.example", "GEMINI_API_KEY=\nELEVENLABS_API_KEY=\n")
        checks = self.checks()
        for service in ("OpenAI", "Google Gemini", "ElevenLabs"):
            with self.subTest(service=service):
                row = checks[f"paid_key:{service}"]
                self.assertEqual(row["status"], "manual")
                self.assertEqual(row["pillar"], "observability")
                for word in ("cap", "alert", "restricted", "your own code"):
                    self.assertIn(word, row["detail"])
        self.assertNotIn("paid_key:Anthropic", checks)

    def test_no_paid_services_keeps_generic_cost_row(self):
        self.write("package.json", '{"dependencies": {"express": "4"}}')
        checks = self.checks()
        self.assertFalse([c for c in checks if c.startswith("paid_key:")])
        self.assertEqual(checks["monthly_cost"]["status"], "manual")


class InfraTokenTests(AuditCase):
    def test_one_scope_row_per_host(self):
        self.write("railway.json", "{}")
        self.write("render.yaml", "services: []\n")
        self.write("infra/main.tf", 'provider "aws" {}\n')
        checks = self.checks()
        for host in ("Railway", "Render", "Terraform"):
            with self.subTest(host=host):
                row = checks[f"infra_token:{host}"]
                self.assertEqual((row["status"], row["pillar"]), ("manual", "security"))
                self.assertIn("one environment", row["detail"])

    def test_host_found_from_env_var_name(self):
        self.write("scripts/deploy.sh", 'railway up --service "$SERVICE"  # needs RAILWAY_TOKEN\n')
        self.assertIn("infra_token:Railway", self.checks())

    def test_no_host_asks_generically(self):
        self.assertEqual(self.checks()["infra_tokens"]["status"], "manual")


class BackupTests(AuditCase):
    def test_backups_row_asks_off_volume_and_restore(self):
        row = self.checks()["backups"]
        self.assertEqual((row["status"], row["pillar"]), ("manual", "infra"))
        self.assertIn("outside", row["detail"])
        self.assertIn("restore", row["detail"])


class CiSecretScanTests(AuditCase):
    def test_no_ci_warns(self):
        self.assertEqual(self.checks()["ci_secret_scan"]["status"], "warn")

    def test_ci_without_scanner_warns(self):
        self.write(".github/workflows/test.yml", "jobs:\n  test:\n    steps:\n      - run: pytest\n")
        self.assertEqual(self.checks()["ci_secret_scan"]["status"], "warn")

    def test_ci_with_scanner_passes(self):
        for step in ("uses: gitleaks/gitleaks-action@v2", "run: python3 check_loop.py guardrails", "run: trufflehog git file://."):
            with self.subTest(step=step):
                self.write(".github/workflows/test.yml", f"jobs:\n  scan:\n    steps:\n      - {step}\n")
                self.assertEqual(self.checks()["ci_secret_scan"]["status"], "pass")


if __name__ == "__main__":
    unittest.main()
